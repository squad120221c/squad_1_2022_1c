from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import Path

from src.main.schema import RecursoSchema
from src.main.service import RecursosService

from src.main.utils.db import get_db

router = APIRouter(prefix="/recursos")

@router.get(
    "/",
    tags=["recursos"],
    status_code=status.HTTP_200_OK,
    response_model=list[RecursoSchema.Recurso],
    dependencies=[Depends(get_db)],
    summary="Obtener todos los recursos"
)
def get_recursos():

    """
    ## Obtener todos los recursos disponibles de PSA desde la API externa

    ### Argumentos
    - No recibe argumentos

    ### Retorna
    - Lista de recursos en formato JSON con el formato:
        - legajo
        - nombre
        - apellido
    """

    return RecursosService.get_recursos()

@router.get(
    "/{legajo}",
    tags=["recursos"],
    status_code=status.HTTP_200_OK,
    response_model=RecursoSchema.Recurso,
    dependencies=[Depends(get_db)],
    summary="Obtener recurso por legajo"
)
def get_recursos(
    legajo: int = Path(
        ...,
    ),
):

    """
    ## Obtener un recurso disponible determinado a partir de su legajo

    ### Argumentos
    - Legajo del recurso

    ### Retorna
    - En caso de existir el legajo ingresado, un recurso en formato JSON con el siguiente formato
        - legajo
        - nombre
        - apellido   
    """

    return RecursosService.get_recurso_legajo(legajo)