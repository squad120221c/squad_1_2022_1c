from fastapi import HTTPException, status
import requests

from src.main.schema import TareaSchema

def get_tareas():

    tareas = requests.get("clhttps://aninfo-projects.herokuapp.com/api/v1/tasks").json()

    if tareas == None:
        msg = "No hay tareas disponibles :("
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )

    listaTareas = []
    for tarea in tareas:
        listaTareas.append(
            TareaSchema.Tarea(
                id = tarea.get("id"),
                name = tarea.get("name")
            )
        )

    return listaTareas

def get_tarea_id(idTarea: int):

    tareas = requests.get("https://aninfo-projects.herokuapp.com/api/v1/tasks/").json()
    
    if tareas == None:
        msg = "No existe una tarea con el id ingresado"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )

    tarea_id = None
    for tarea in tareas:
        if tarea.get("id") == idTarea:
            tarea_id = TareaSchema.Tarea(
                    id = tarea.get("id"),
                    name = tarea.get("name"),
                    collaborators = tarea.get("collaborators")
            )
        
    if tarea_id == None:
        msg = "El id ingresado no corresponde a ningúna tarea existente"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )

    return tarea_id    

def tareaTieneAsignado(idTarea: int, idRecurso: int):
    tarea = get_tarea_id(idTarea)    
    tieneAsignado = False
    for recurso in tarea.collaborators:
        if recurso == idRecurso:
            tieneAsignado = True
    
    return tieneAsignado