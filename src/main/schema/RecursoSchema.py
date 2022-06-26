from pydantic import BaseModel
from pydantic import Field

class Recurso(BaseModel):
    legajo: int = Field(
        ...,
        example= "1"
    )
    Nombre: str = Field(
        ...,
        example="Juan"
    )
    Apellido: str = Field(
        ...,
        example="Perez"
    )