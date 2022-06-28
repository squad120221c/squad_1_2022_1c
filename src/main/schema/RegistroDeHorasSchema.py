from datetime import date
from pydantic import BaseModel
from pydantic import Field

class RegistroDeModificar(BaseModel):    
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
    id_proyecto: int = Field(
        ...,
        example = "3"
    )
    id_tarea: int = Field(
        ...,
        example="67"
    )
    id_recurso: int = Field(
        ...,
        example="32"
    )
    cantidad: int = Field(
        ...,
        example="6"
    )

class RegistroDeHoras(RegistroDeModificar):
    fecha_trabajada: date = Field(
        ...,
        example="yyyy-mm-dd"
    )

class RegistroDeHorasCargar(RegistroDeHoras):
    id_registro_horas: int = Field(
        ...,
        example="5"
    )