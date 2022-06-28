from fastapi import HTTPException, status

from src.main.exceptions.RegistroExistente import RegistroExistente
from src.main.exceptions.RecursoNoAsignado import RecursoNoAsignado
from src.main.exceptions.RegistroNoExiste import RegistroNoExiste
from src.main.model.RegistroDeHorasModel import RegistroDeHoras as RegistroDeHorasModel 

from src.main.schema import RegistroDeHorasSchema 
from src.main.service import TareaService

def cargarHoras(carga: RegistroDeHorasSchema.RegistroDeHoras):

    if TareaService.tareaTieneAsignado(carga.id_tarea, carga.id_recurso):
        msg = "El recurso no está asignado a la tarea"
        raise RecursoNoAsignado(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )
    
    getCarga = RegistroDeHorasModel.filter((RegistroDeHorasModel.id_recurso == carga.id_recurso) 
    and (RegistroDeHorasModel.id_tarea == carga.id_tarea) and (RegistroDeHorasModel.fecha_trabajada == carga.fecha_trabajada)).first()
    if getCarga:
        msg = "Ya se cargaron horas para la tarea, el recurso y la fecha seleccionada"
        raise RegistroExistente and HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )

    db_carga = RegistroDeHorasModel(
        nombre_proyecto = carga.nombre_proyecto,
        nombre_tarea = carga.nombre_tarea,
        nombre_recurso = carga.nombre_recurso,
        fecha_trabajada = carga.fecha_trabajada,
        cantidad = carga.cantidad,
        id_proyecto = carga.id_proyecto,
        id_tarea = carga.id_tarea,
        id_recurso = carga.id_recurso
    )

    db_carga.save()

    return RegistroDeHorasSchema.RegistroDeHorasCargar(
        nombre_proyecto = db_carga.nombre_proyecto,
        nombre_tarea = db_carga.nombre_tarea,
        nombre_recurso = db_carga.nombre_recurso,
        fecha_trabajada = db_carga.fecha_trabajada,
        cantidad = db_carga.cantidad,
        id_proyecto = db_carga.id_proyecto,
        id_tarea = db_carga.id_tarea,
        id_recurso = db_carga.id_recurso,
        id_registro_horas = db_carga.id_registro_horas
    )

def listar_cargas(cargas, msg):
    if not cargas:
        raise RegistroNoExiste() and HTTPException(
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
                id_registro_horas=carga.id_registro_horas,
                id_proyecto = carga.id_proyecto,
                id_tarea = carga.id_tarea,
                id_recurso = carga.id_recurso
            )
        )

    return list_cargas

def get_cargas():
    cargas = RegistroDeHorasModel.select()
    return listar_cargas(cargas, "No hay cargas de horas registradas")

def get_cargas_id(id: int):
    cargas = RegistroDeHorasModel.filter(RegistroDeHorasModel.id_registro_horas == id)
    return listar_cargas(cargas, "El registro ingresado no existe")

def get_cargas_proyecto(id: int):
    cargas = RegistroDeHorasModel.filter(RegistroDeHorasModel.id_proyecto == id)
    return listar_cargas(cargas, "El proyecto ingresado no tiene horas cargadas")

def get_cargas_tarea(id: int):
    cargas = RegistroDeHorasModel.filter(RegistroDeHorasModel.id_tarea == id)
    return listar_cargas(cargas, "La tarea ingresada no tiene horas cargadas")

def get_cargas_recurso(id: int):
    cargas = RegistroDeHorasModel.filter(RegistroDeHorasModel.id_recurso == id)
    return listar_cargas(cargas, "El recurso ingresado no tiene horas cargadas")

def modificar_horas_cargadas(aumentar: bool, id_registro_horas: int, cantidad: int):
    carga = RegistroDeHorasModel.filter(RegistroDeHorasModel.id_registro_horas == id_registro_horas).first()

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
        id_proyecto=carga.id_proyecto,
        id_recurso=carga.id_recurso,
        id_tarea=carga.id_tarea
    )

def modificar_carga(id_registro_horas: int, carga_nueva: RegistroDeHorasSchema.RegistroDeModificar):
    carga = RegistroDeHorasModel.filter(RegistroDeHorasModel.id_registro_horas == id_registro_horas).first()

    if not carga:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La carga de horas con el código ingresado no existe"
        )

    carga.nombre_proyecto=carga_nueva.nombre_proyecto
    carga.nombre_recurso=carga_nueva.nombre_recurso
    carga.nombre_tarea=carga_nueva.nombre_tarea
    carga.cantidad=carga_nueva.cantidad
    carga.id_proyecto=carga_nueva.id_proyecto
    carga.id_recurso=carga_nueva.id_recurso
    carga.id_tarea=carga_nueva.id_tarea

    carga.save()

    return RegistroDeHorasSchema.RegistroDeHorasCargar(
        nombre_proyecto=carga.nombre_proyecto,
        nombre_recurso=carga.nombre_recurso,
        nombre_tarea=carga.nombre_tarea,
        cantidad=carga.cantidad,
        fecha_trabajada=carga.fecha_trabajada,
        id_proyecto=carga.id_proyecto,
        id_recurso=carga.id_recurso,
        id_tarea=carga.id_tarea
    )

def delete_carga(id_registro_horas: int):
    carga = RegistroDeHorasModel.filter(RegistroDeHorasModel.id_registro_horas == id_registro_horas).first()

    if not carga:
         raise RegistroNoExiste()

    carga.delete_instance()

def horasConsumidasDeRecurso(idTarea: int, legajo: int):
    cargas = get_cargas()
    horasTotal = 0
    for carga in cargas:
        if carga.id_recurso == legajo & carga.id_tarea == idTarea:
            horasTotal = horasTotal + carga.cantidad

    return horasTotal