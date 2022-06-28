from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import Body
from fastapi import Query
from fastapi import Path

from src.main.schema import RegistroDeHorasSchema
from src.main.service import RegistroDeHorasService

from src.main.utils.db import get_db

router = APIRouter(prefix="/rrhh")

@router.post(
    "/",
    tags=["rrhh"],
    status_code=status.HTTP_201_CREATED,
    response_model=RegistroDeHorasSchema.RegistroDeHorasCargar,
    dependencies=[Depends(get_db)],
    summary="Cargar horas en una tarea" 
)
def create_trabajo(trabajoRealizado: RegistroDeHorasSchema.RegistroDeHoras= Body(...)):
    """
    ## Registrar carga de horas

    ### Argumentos:
    - Nombre del proyecto
    - Nombre de la tarea
    - Nombre del recurso
    - Identificador único del proyecto
    - Identificador único de la tarea
    - Identificador único del recurso
    - Fecha en la que se registran las horas
    - Cantidad de horas que se registran
  
    ### Retorna
    - El registro cargado y su identificador único en formato JSON
    """

    return RegistroDeHorasService.cargarHoras(trabajoRealizado)

@router.get(
    "/",
    tags=["rrhh"],
    status_code=status.HTTP_200_OK,
    response_model=list[RegistroDeHorasSchema.RegistroDeHorasCargar],
    dependencies=[Depends(get_db)],
    summary="Obtener todas las cargas de horas"
)
def get_cargas():

    """
    ## Obtener todos los registros de horas

    ### Argumentos
    - No recibe argumentos

    ### Retorna
    - Todas las cargas realizadas en formato JSON
    """

    return RegistroDeHorasService.get_cargas()

@router.get(
    "/proyecto/{id_proyecto}",
    tags=["rrhh"],
    status_code=status.HTTP_200_OK,
    response_model=list[RegistroDeHorasSchema.RegistroDeHoras],
    dependencies=[Depends(get_db)],
    summary="Obtener todas los registros de horas de un proyecto"
)
def get_cargas_recurso(
    id_proyecto: int = Path(
        ...,
    ),
):

    """
    ## Obtener todas los registros de un proyecto por proyecto a partir de su identificador único

    ### Argumentos
    - Identificador único del proyecto

    ### Retorna
    - Todas los registros realizados en el proyecto en formato JSON
    """

    return RegistroDeHorasService.get_cargas_proyecto(id_proyecto)

@router.get(
    "/tarea/{id_tarea}",
    tags=["rrhh"],
    status_code=status.HTTP_200_OK,
    response_model=list[RegistroDeHorasSchema.RegistroDeHoras],
    dependencies=[Depends(get_db)],
    summary="Obtener todas los registros de horas de una tarea"
)
def get_cargas_recurso(
    id_tarea: int = Path(
        ...,
    ),
):

    """
    ## Obtener todas loss registros de horas por tarea a partir de su identificador único

    ### Argumentos
    - Identificador único de la tarea

    ### Retorna
    - Todas los registros realizadas para la tarea en formato JSON
    """

    return RegistroDeHorasService.get_cargas_tarea(id_tarea)

@router.get(
    "/recurso/{id_recurso}",
    tags=["rrhh"],
    status_code=status.HTTP_200_OK,
    response_model=list[RegistroDeHorasSchema.RegistroDeHoras],
    dependencies=[Depends(get_db)],
    summary="Obtener todos los registros de horas de un recurso"
)
def get_cargas_recurso(
    id_recurso: int = Path(
        ...,
    ),
):

    """
    ## Obtener todos los registros para un recurso a partir de su identificador único

    ### Argumentos
    - Identificador único del recurso

    ### Retorna
    - Todas los registros realizados para el proyecto en formato JSON
    """

    return RegistroDeHorasService.get_cargas_recurso(id_recurso)

@router.put(
    "/{id_registro_horas}",
    tags=["rrhh"],
    status_code=status.HTTP_200_OK,
    response_model=RegistroDeHorasSchema.RegistroDeHorasCargar,
    dependencies=[Depends(get_db)],
    summary="Modificar registro de horas"
)
def update_carga(
    id_registro_horas: int = Path(
        ...,
    ), carga: RegistroDeHorasSchema.RegistroDeModificar = Body(...)
):

    """
    ## Modificar un registro de horas
    ### No se podrá modificar la fecha de la misma

    ### Argumentos
    - Nombre del proyecto
    - Nombre de la tarea
    - Nombre del recurso
    - Identificador único del proyecto
    - Identificador único de la tarea
    - Identificador único del recurso
    - Cantidad de horas que se registran
    ### Retorna
    - El registro modificado con los nuevos datos en formato JSON
    """
    return RegistroDeHorasService.modificar_carga(id_registro_horas, carga)

@router.put(
    "/{id_registro_horas}/aumentar",
    tags=["rrhh"],
    status_code=status.HTTP_200_OK,
    response_model=RegistroDeHorasSchema.RegistroDeHorasCargar,
    dependencies=[Depends(get_db)],
    summary="Aumentar horas de un registro"
)
def update_carga(
    id_registro_horas: int = Path(
        ...,
    ),
    cantidad: int = Path(
        ...,
    )
):

    """
    ## Modificar un registro de horas
    ### Solo se permiten cantidad de horas positivas

    ### Argumentos
    - Cantidad de horas que se quieran aumentar
    ### Retorna
    - El registro modificado con la cantidad de horas aumentada en formato JSON
    """

    return RegistroDeHorasService.modificar_horas_cargadas(True, id_registro_horas, cantidad)

@router.put(
    "/{id_registro_horas}/disminuir",
    tags=["rrhh"],
    status_code=status.HTTP_200_OK,
    response_model=RegistroDeHorasSchema.RegistroDeHorasCargar,
    dependencies=[Depends(get_db)],
    summary="Disminuir horas cargadas"
)
def update_carga(
    id_registro_horas: int = Path(
        ...,
    ),
    cantidad: int = Path(
        ...,
    )
):
    """
    ## Modificar un registro de horas
    ### Solo se permiten cantidad de horas positivas

    ### Argumentos
    - Cantidad de horas que se quieran disminuir
    ### Retorna
    - El registro modificado con la cantidad de horas disminuida en formato JSON
    """

    return RegistroDeHorasService.modificar_horas_cargadas(False, id_registro_horas, cantidad)

@router.delete(
    "/{id_registro_horas}",
    tags=["rrhh"],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_db)],
    summary="Eliminar un registro de horas"
)
def delete_task(
    id_registro_horas: int = Path(
        ...,
    ),
):
    """
    ## Eliminar un registro de horas
    """

    RegistroDeHorasService.delete_carga(id_registro_horas)

    return {
        'msg': 'La carga de horas se ha eliminado correctamente'
    }