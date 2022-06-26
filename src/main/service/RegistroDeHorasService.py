import json
from fastapi import HTTPException, status
from src.main.exceptions.RecursoNoAsignado import RecursoNoAsignado

# Importo el modelo de peewee para poder crear un trabajo
from src.main.model.RegistroDeHorasModel import RegistroDeHoras as RegistroDeHorasModel 
# Importo el modelo de Pydantic para retornar al trabajo la informaición del trabajo creado
from src.main.schema import RegistroDeHorasSchema 
# from src.main.schema import TareaSchema
from src.main.service import TareaService

# Función que se encargará de guardar el trabajoRealizado en la base de datos
# Recibe como parámetro un modelo de Pydantic de tipo TrabajoRealizado
def cargarHoras(carga: RegistroDeHorasSchema.RegistroDeHorasCargar):

    if TareaService.tareaTieneAsignado(carga.codigo_tarea, carga.codigo_recurso):
        msg = "El recurso no está asignado a la tarea"
        raise RecursoNoAsignado(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )
    
    # Primero compruebo que la carga de horas no exista ya en la base de datos
    # Si es asi lanzo una excepción HTTPException con el código de estado 400 con un mensaje
    getCarga = RegistroDeHorasModel.filter((RegistroDeHorasModel.codigo_recurso == carga.codigo_recurso) 
    & (RegistroDeHorasModel.codigo_tarea == carga.codigo_tarea) & (RegistroDeHorasModel.fecha_trabajada == carga.fecha_trabajada)).first()
    if getCarga:
        msg = "Ya se cargaron horas para la tarea, el recurso y la fecha seleccionada"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )

    # Usando el modelo de peewee creo la carga y lo guardo
    db_carga = RegistroDeHorasModel(
        nombre_proyecto = carga.nombre_proyecto,
        nombre_tarea = carga.nombre_tarea,
        nombre_recurso = carga.nombre_recurso,
        fecha_trabajada = carga.fecha_trabajada,
        cantidad = carga.cantidad,
        codigo_proyecto = carga.codigo_proyecto,
        codigo_tarea = carga.codigo_tarea,
        codigo_recurso = carga.codigo_recurso
    )

    #force_insert=True
    db_carga.save()

    #Retorno la información del trabajo recién creado empleando el modelo de Pydantic
    return RegistroDeHorasSchema.RegistroDeHorasCargar(
        nombre_proyecto = db_carga.nombre_proyecto,
        nombre_tarea = db_carga.nombre_tarea,
        nombre_recurso = db_carga.nombre_recurso,
        fecha_trabajada = db_carga.fecha_trabajada,
        cantidad = db_carga.cantidad,
        codigo_proyecto = db_carga.codigo_proyecto,
        codigo_tarea = db_carga.codigo_tarea,
        codigo_recurso = db_carga.codigo_recurso,
        codigo_carga = db_carga.codigo_carga
    )

def listar_cargas(cargas, msg):
    if not cargas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg
        )

    list_cargas = []
    for carga in cargas:
        list_cargas.append(
            RegistroDeHorasSchema.RegistroDeHorasCargar(
                nombre_proyecto=carga.nombre_proyecto,
                nombre_tarea=carga.nombre_tarea,
                nombre_recurso=carga.nombre_recurso,
                cantidad=carga.cantidad,
                fecha_trabajada=carga.fecha_trabajada,
                codigo_carga=carga.codigo_carga,
                codigo_proyecto = carga.codigo_proyecto,
                codigo_tarea = carga.codigo_tarea,
                codigo_recurso = carga.codigo_recurso
            )
        )

    return list_cargas

def get_cargas():
    cargas = RegistroDeHorasModel.select()
    return listar_cargas(cargas, "No hay cargas de horas registradas")

def get_cargas_id(id: int):
    cargas = RegistroDeHorasModel.filter(RegistroDeHorasModel.codigo_carga == id)
    return listar_cargas(cargas, "El registro ingresado no existe")

def get_cargas_proyecto(codigo: int):
    cargas = RegistroDeHorasModel.filter(RegistroDeHorasModel.codigo_proyecto == codigo)
    return listar_cargas(cargas, "El proyecto ingresado no tiene horas cargadas")

def get_cargas_tarea(codigo: int):
    cargas = RegistroDeHorasModel.filter(RegistroDeHorasModel.codigo_tarea == codigo)
    return listar_cargas(cargas, "La tarea ingresada no tiene horas cargadas")

def get_cargas_tarea(codigo: int):
    cargas = RegistroDeHorasModel.filter(RegistroDeHorasModel.codigo_recurso == codigo)
    return listar_cargas(cargas, "El recurso ingresado no tiene horas cargadas")

def modificar_horas_cargadas(aumentar: bool, codigo_carga: int, cantidad: int):
    carga = RegistroDeHorasModel.filter(RegistroDeHorasModel.codigo_carga == codigo_carga).first()

    if not carga:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La carga de horas con el código ingresado no existe"
        )

    if aumentar == True:
        carga.cantidad = carga.cantidad + cantidad
    else:
        carga.cantidad = carga.cantidad - cantidad

    carga.save()

    return RegistroDeHorasSchema.RegistroDeHorasCargar(
        nombre_proyecto=carga.nombre_proyecto,
        nombre_recurso=carga.nombre_recurso,
        nombre_tarea=carga.nombre_tarea,
        cantidad=carga.cantidad,
        fecha_trabajada=carga.fecha_trabajada,
        codigo_proyecto=carga.codigo_proyecto,
        codigo_recurso=carga.codigo_recurso,
        codigo_tarea=carga.codigo_tarea
    )

def modificar_carga(codigo_carga: int, carga_nueva: RegistroDeHorasSchema.RegistroDeHorasCargar):
    carga = RegistroDeHorasModel.filter(RegistroDeHorasModel.codigo_carga == codigo_carga).first()

    if not carga:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La carga de horas con el código ingresado no existe"
        )

    carga.nombre_proyecto=carga_nueva.nombre_proyecto
    carga.nombre_recurso=carga_nueva.nombre_recurso
    carga.nombre_tarea=carga_nueva.nombre_tarea
    carga.cantidad=carga_nueva.cantidad
    carga.fecha_trabajada=carga_nueva.fecha_trabajada
    carga.codigo_proyecto=carga_nueva.codigo_proyecto
    carga.codigo_recurso=carga_nueva.codigo_recurso
    carga.codigo_tarea=carga_nueva.codigo_tarea

    carga.save()

    return RegistroDeHorasSchema.RegistroDeHorasCargar(
        nombre_proyecto=carga.nombre_proyecto,
        nombre_recurso=carga.nombre_recurso,
        nombre_tarea=carga.nombre_tarea,
        cantidad=carga.cantidad,
        fecha_trabajada=carga.fecha_trabajada,
        codigo_proyecto=carga.codigo_proyecto,
        codigo_recurso=carga.codigo_recurso,
        codigo_tarea=carga.codigo_tarea
    )

def delete_carga(codigo_carga: int):
    carga = RegistroDeHorasModel.filter(RegistroDeHorasModel.codigo_carga == codigo_carga).first()

    if not carga:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La carga de horas con el código ingresado no existe"
        )

    carga.delete_instance()

def horasConsumidasDeRecurso(idTarea: int, legajo: int):
    cargas = get_cargas()
    horasTotal = 0
    for carga in cargas:
        if carga.codigo_recurso == legajo & carga.codigo_tarea == idTarea:
            horasTotal = horasTotal + carga.cantidad

    return horasTotal