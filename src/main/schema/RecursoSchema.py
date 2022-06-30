from pydantic import BaseModel
from pydantic import Field

class Recurso(BaseModel):
    id: int = Field(
        ...,
        example= "1"
    )
    name: str = Field(
        ...,
        example="Juan"
    )
    lastname: str = Field(
        ...,
        example="Perez"
    )