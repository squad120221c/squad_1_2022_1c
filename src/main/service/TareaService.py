from fastapi import HTTPException, status
import requests
from src.main.exceptions.TareaNoExiste import TareaNoExiste
from src.main.schema import TareaSchema

def get_tareas():

    try:
        tareas = requests.get("clhttps://aninfo-projects.herokuapp.com/api/v1/tasks").json()
    except:
        return None

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

    try: 
        tareas = requests.get("https://aninfo-projects.herokuapp.com/api/v1/tasks/").json()
    except: 
        return None
    
    if tareas == None:
        msg = "No existe una tarea con el id ingresado"
        raise TareaNoExiste and HTTPException(
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

    return tarea_id    

def tareaTieneAsignado(idTarea: int, idRecurso: int):
    try: 
        tarea = get_tarea_id(idTarea)    
    except TareaNoExiste:
        return False
    tieneAsignado = False
    for recurso in tarea.collaborators:
        if recurso == idRecurso:
            tieneAsignado = True
    
    return tieneAsignado