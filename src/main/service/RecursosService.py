from fastapi import HTTPException, status
import requests
import os

from src.main.schema import RecursoSchema

def get_recursos():

    recursos = requests.get('https://anypoint.mulesoft.com/mocking/api/v1/sources/exchange/assets/754f50e8-20d8-4223-bbdc-56d50131d0ae/recursos-psa/1.0.0/m/api/recursos').json()

    if recursos == None:
        msg = "No hay recursos disponibles :("
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )

    listaRecursos = []
    for recurso in recursos:
        listaRecursos.append(
            RecursoSchema.Recurso(
                legajo = recurso.get("legajo"),
                Nombre = recurso.get("Nombre"),
                Apellido = recurso.get("Apellido")
            )
        )

    return listaRecursos

def get_recurso_legajo(legajo: int):

    recursos = requests.get('https://anypoint.mulesoft.com/mocking/api/v1/sources/exchange/assets/754f50e8-20d8-4223-bbdc-56d50131d0ae/recursos-psa/1.0.0/m/api/recursos').json()
    
    if recursos == None:
        msg = "No hay recursos disponibles :("
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )

    recurso_legajo = None
    for recurso in recursos:
        if recurso.get("legajo") == legajo:
            recurso_legajo = RecursoSchema.Recurso(
                    legajo = recurso.get("legajo"),
                    Nombre = recurso.get("Nombre"),
                    Apellido = recurso.get("Apellido")
            )
        
    if recurso_legajo == None:
        msg = "El legajo ingresado no corresponde a ningún recurso existente"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )

    return recurso_legajo   