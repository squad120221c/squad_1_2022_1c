# Modelo de Pydantic

# Todas las variables que definamos dentro de la clase que extienda de BaseModel, 
# pasará por un proceso de validación y si hay algún error lanzará una excepción.

# Importamos la función Field. Esta función nos permite validar distintos tipos de datos, 
# marcar si es obligatorio o no, tamaños máximos y mínimos, etc.

from datetime import date
from pydantic import BaseModel
from pydantic import Field

class RegistroDeHorasBase(BaseModel):
    nombre_proyecto: str = Field(
        ...,
        example="Proyecto 1"
    )
    nombre_tarea: str = Field(
        ...,
        example="Tarea 1"
    )
    nombre_recurso: str = Field(
        ...,
        example="Recurso 1"
    )
    fecha_trabajada: date = Field(
        ...,
        example="yyyy-mm-dd"
    )
    cantidad: int = Field(
        ...,
        example="6"
    )

class RegistroDeHoras(RegistroDeHorasBase):
    codigo_carga: int = Field(
        ...,
        example="5"
    )

class RegistroDeHorasCargar(RegistroDeHorasBase):
    codigo_proyecto: int = Field(
        ...,
        example = "3"
    )
    codigo_tarea: int = Field(
        ...,
        example="67"
    )
    codigo_recurso: int = Field(
        ...,
        example="32"
    )