# Ruta para la creación de Trabajos, para cargar horas

#APIRouter nos permite crear rutas a nuestra API
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
# Para recuperar información que envíe el usuario en la petición para cargar las horas
from fastapi import Body
# Este lo usaremos cuando queramos capturar parámetros vía query en la url
# En una url serían los que se envían después del carácter `?`
from fastapi import Query
# Lo utilizaremos para capturar parámetros que estén dentro de la url del endpoint
from fastapi import Path
from typing import List, Optional

#Importo el modelo de Pydantic
from src.main.schema import RegistroDeHorasSchema
#Importo el servicio
from src.main.service import RegistroDeHorasService

# Importo la función para la conexión a la base de datos
#from src.main.utils.db import get_db

# Genero una instancia de la clase APIRouter y la añdo un prefijo
# para que todas las rutas creadas a partir de la instancia router 
# lo tengan
router = APIRouter(prefix="/CargasDeHoras")

# endpoint
@router.post(
    "/",
    tags=["Carga de Horas"], #Para agrupar los endpoints
    status_code=status.HTTP_201_CREATED,
    response_model=RegistroDeHorasSchema.RegistroDeHoras, # Indica que la respuesta que retornamos será un modelo de Pydantic
    #dependencies=[Depends(get_db)], # Pasamos la conexión a la base de datos
    summary="Cargar horas en una tarea" # Esto es informativo para la documentación de la API
)
def create_trabajo(trabajoRealizado: RegistroDeHorasSchema.RegistroDeHorasCargar= Body(...)):
    """
    ## Cargar horas de un recurso a una tarea

    ### Argumentos
    La app recibe los siguientes campos dentro de un JSON
    - cantidad: Horas del recurso a cargar en la tarea
    - fecha_trabajada: Una fecha valida del pasado
    - codigo_tarea: Código único de la tarea (Numérico)
    - codigo_recurso: Código único que identifica un recurso (Numérico)

    ### Retorna
    - trabajoRealizado: Información de la carga de horas 
    """

    # Llamo a la función create_trabajo que definí en el archivo TrabajoRealizadoService.py 
    # y envio por parámetro la variable trabajoRealizado. Esta retornará el modelo TrabajoRealizado 
    # de Pydantic que definimos en trabajoRealizadoSchema.py
    return RegistroDeHorasService.cargarHoras(trabajoRealizado)

@router.get(
    "/",
    tags=["Carga de Horas"],
    status_code=status.HTTP_200_OK,
    response_model=list[RegistroDeHorasSchema.RegistroDeHoras],
    #dependencies=[Depends(get_db)],
    summary="Obtener todas las cargas de horas"
)
def get_cargas():

    """
    ## Obtener todas las cargas de horas de un recurso a partir de su código

    ### Argumentos
    No recibe argumentos

    ### Retorna
    - Todas las cargas realizadas
    """

    return RegistroDeHorasService.get_cargas()

@router.get(
    "/proyecto/{codigo_proyecto}",
    tags=["Carga de Horas"],
    status_code=status.HTTP_200_OK,
    response_model=list[RegistroDeHorasSchema.RegistroDeHoras],
    #dependencies=[Depends(get_db)],
    summary="Obtener todas las cargas de horas de un proyecto"
)
def get_cargas_recurso(
    codigo_proyecto: int = Path(
        ...,
    ),
):

    """
    ## Obtener todas las cargas de horas por proyecto a partir de su código

    ### Argumentos
    La app recibe los siguientes campos a través del url
    - codigo_proyecto: Código único que identifica un proyecto

    ### Retorna
    - Todas las cargas realizadas
    """

    return RegistroDeHorasService.get_cargas_proyecto(codigo_proyecto)

@router.get(
    "/tarea/{codigo_tarea}",
    tags=["Carga de Horas"],
    status_code=status.HTTP_200_OK,
    response_model=list[RegistroDeHorasSchema.RegistroDeHoras],
    #dependencies=[Depends(get_db)],
    summary="Obtener todas las cargas de horas de una tarea"
)
def get_cargas_recurso(
    codigo_tarea: int = Path(
        ...,
    ),
):

    """
    ## Obtener todas las cargas de horas por tarea a partir de su código

    ### Argumentos
    La app recibe los siguientes campos a través del url
    - codigo_tarea: Código único que identifica un proyecto

    ### Retorna
    - Todas las cargas realizadas para la tarea ingresada
    """

    return RegistroDeHorasService.get_cargas_tarea(codigo_tarea)

@router.get(
    "/recurso/{codigo_recurso}",
    tags=["Carga de Horas"],
    status_code=status.HTTP_200_OK,
    response_model=list[RegistroDeHorasSchema.RegistroDeHoras],
    #dependencies=[Depends(get_db)],
    summary="Obtener todas las cargas de horas de un recurso"
)
def get_cargas_recurso(
    codigo_recurso: int = Path(
        ...,
    ),
):

    """
    ## Obtener todas las cargas de horas por recurso a partir de su código

    ### Argumentos
    La app recibe los siguientes campos a través del url
    - codigo_recurso: Código único que identifica un recurso

    ### Retorna
    - Todas las cargas realizadas para el recurso ingresado
    """

    return RegistroDeHorasService.get_cargas_tarea(codigo_recurso)

@router.put(
    "/{codigo_carga}",
    tags=["Carga de Horas"],
    status_code=status.HTTP_200_OK,
    response_model=RegistroDeHorasSchema.RegistroDeHorasCargar,
    #dependencies=[Depends(get_db)],
    summary="Modificar registro de horas"
)
def update_carga(
    codigo_carga: int = Path(
        ...,
    ), carga: RegistroDeHorasSchema.RegistroDeHorasCargar = Body(...)
):
    return RegistroDeHorasService.modificar_carga(codigo_carga, carga)

@router.put(
    "/{codigo_carga}/aumentar",
    tags=["Carga de Horas"],
    status_code=status.HTTP_200_OK,
    response_model=RegistroDeHorasSchema.RegistroDeHorasCargar,
    #dependencies=[Depends(get_db)],
    summary="Aumentar horas cargadas"
)
def update_carga(
    codigo_carga: int = Path(
        ...,
    ),
    cantidad: int = Query(None)
):
    return RegistroDeHorasService.modificar_horas_cargadas(True, codigo_carga, cantidad)

@router.put(
    "/{codigo_carga}/disminuir",
    tags=["Carga de Horas"],
    status_code=status.HTTP_200_OK,
    response_model=RegistroDeHorasSchema.RegistroDeHorasCargar,
    #dependencies=[Depends(get_db)],
    summary="Disminuir horas cargadas"
)
def update_carga(
    codigo_carga: int = Path(
        ...,
    ),
    cantidad: int = Query(None)
):
    return RegistroDeHorasService.modificar_horas_cargadas(False, codigo_carga, cantidad)

@router.delete(
    "/{codigo_carga}",
    tags=["Carga de Horas"],
    status_code=status.HTTP_200_OK,
    #dependencies=[Depends(get_db)]
)
def delete_task(
    codigo_carga: int = Path(
        ...,
    ),
):
    RegistroDeHorasService.delete_carga(codigo_carga)

    return {
        'msg': 'La carga de horas se ha eliminado correctamente'
    }