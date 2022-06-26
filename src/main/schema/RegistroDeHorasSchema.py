from datetime import date
from pydantic import BaseModel
from pydantic import Field

class RegistroDeHoras(BaseModel):
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

class RegistroDeHorasCargar(RegistroDeHoras):
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
    codigo_carga: int = Field(
        ...,
        example="5"
    )