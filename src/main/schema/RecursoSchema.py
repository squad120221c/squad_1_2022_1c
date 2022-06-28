from pydantic import BaseModel
from pydantic import Field

class Recurso(BaseModel):
    legajo: int = Field(
        ...,
        example= "1"
    )
    nombre: str = Field(
        ...,
        example="Juan"
    )
    apellido: str = Field(
        ...,
        example="Perez"
    )