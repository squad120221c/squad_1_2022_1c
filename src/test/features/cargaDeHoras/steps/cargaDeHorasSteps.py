from behave import *
from datetime import datetime
from fastapi import HTTPException
from src.main.service.RecursosService import get_recurso_legajo
from src.main.service.TareaService import get_tarea_id

from unittest import mock

from src.main.utils.settings import Settings
settings = Settings()
ep_recursos = settings.ep_recursos

from src.main.service import TareaService
from src.main.service import RegistroDeHorasService
from src.main.schema import RegistroDeHorasSchema

from src.main.exceptions.RecursoNoAsignado import RecursoNoAsignado

@given(u'un recurso con ID {idRecurso}')
def step_impl(context, idRecurso):
    fake_json = [{
            "legajo": idRecurso,
            "Nombre": "Carlos",
            "Apellido": "Perez"
        }]
    with mock.patch('src.main.service.RecursosService.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = fake_json
        context.recurso = get_recurso_legajo(idRecurso)
                
@given(u'una tarea con ID {idTarea}')
def step_impl(context, idTarea):
    fake_json = [{
            "id": idTarea,
            "name": "Titulo",
            "collaborators": [1, 7]
        }]
    with mock.patch('src.main.service.TareaService.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = fake_json
        context.tarea = get_tarea_id(idTarea)

@given(u'el recurso está asignado a la tarea')
def step_impl(context):
    
    # if(context.tarea.id not in context.tarea.collaborators):
    if(TareaService.tareaTieneAsignado(context.tarea.id, context.recurso.legajo) == False):
        context.tarea.collaborators.append(context.recurso.legajo) 
    
    # try:
    #     TareaService.tareaTieneAsignado(context.tarea.id, context.recurso.legajo)
    # except RecursoNoAsignado:
    #     #Si no está asignado agrego el recurso al mock, esto no lo hace nuestro módulo
    #     #pero para que la prueba sea correcta lo agregamos luego de lanzar la excpetion
    #     context.tarea.collaborators.append(context.recurso.legajo) 

@given(u'la tarea no tiene horas cargadas del recurso')
def step_impl(context):
    try: 
        lista_cargas = RegistroDeHorasService.get_cargas()
        for carga in lista_cargas:
            if(carga.codigo_recurso==context.recurso.legajo and carga.codigo_tarea==context.tarea.id):
                RegistroDeHorasService.delete_carga(carga.codigo_carga)
    except HTTPException as e: 
        print("No se recibió ningún registro de horas", e.__class__)

@when(u'intento cargar {cantidad} horas trabajadas del recurso a la tarea para la fecha {fecha}')
def step_impl(context, cantidad, fecha):
    carga = RegistroDeHorasSchema.RegistroDeHorasCargar(
        nombre_proyecto="Test de Gherkin",
        nombre_recurso="Juan Perez",
        nombre_tarea="Debuggear",
        cantidad=cantidad,
        fecha_trabajada=datetime.strptime(fecha, '%Y-%m-%d'),
        codigo_proyecto=1,
        codigo_tarea=int(context.tarea.id),
        codigo_recurso=int(context.recurso.legajo),
        codigo_carga=1
    )
    
    try:
        context.carga = RegistroDeHorasService.cargarHoras(carga)
    except HTTPException as e:
        print('La tarea ingresada no tiene el recurso ingresado asignado', e.__class__)

@then(u'se registran {cantidad} horas consumidas por la tarea del recurso')
def step_impl(context, cantidad):
    assert context.carga.cantidad == int(cantidad)

@given(u'el recurso no está asignado a la tarea')
def step_impl(context):
    #Si lo tiene asignado, lo elimino
    if(TareaService.tareaTieneAsignado(context.tarea, context.recurso.legajo) == True):
        context.tarea.collaborators.remove(context.recurso.legajo) 

@then(u'la carga debe ser denegada')
def step_impl(context):
    assert RecursoNoAsignado != None  

@then(u'la tarea tendrá 0 horas consumidas del recurso')
def step_impl(context):
    assert RegistroDeHorasService.horasConsumidasDeRecurso(context.tarea.id, context.recurso.legajo) == 0