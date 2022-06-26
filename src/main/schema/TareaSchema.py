from datetime import date
from pydantic import BaseModel
from pydantic import Field
from src.main.schema import ProjectSchema 

class Tarea(BaseModel):
    name: str = Field(
        ...,
    )
    # description: str = Field(
    #     ...,
    # )
    # recursos: list[int] = Field(
    #     ...,
    # )
    # initial_date: date = Field(
    #     ...,
    # )
    # final_date: date = Field(
    #     ...,
    # )
    # estimated_hours: int = Field(
    #     ...,
    # )
    id: int = Field(
        ...,
        example= "1"
    )
    # project: ProjectSchema.ProjectInfo = Field(
    #     ...,
    # ) 
    # assigned_employee: int = Field(
    #     ...,
    # )
    collaborators: list = Field(
        ...,
    )
