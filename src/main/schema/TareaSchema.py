from pydantic import BaseModel
from pydantic import Field

class Tarea(BaseModel):
    name: str = Field(
        ...,
    )
    id: int = Field(
        ...,
        example= "1"
    )
    collaborators: list = Field(
        ...,
    )
