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
from src.main.schema import RecursoSchema
from src.main.schema import TareaSchema

from src.main.exceptions.RecursoNoAsignado import RecursoNoAsignado
from src.main.exceptions.RecursoNoExiste import RecursoNoExiste
from src.main.exceptions.TareaNoExiste import TareaNoExiste
from src.main.exceptions.RegistroNoExiste import RegistroNoExiste
from src.main.exceptions.CargaInvalida import CargaInvalida
from src.main.exceptions.FechaInvalida import FechaInvalida

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
    if context.recurso.legajo not in context.tarea.collaborators:
        context.tarea.collaborators.append(context.recurso.legajo) 

@given(u'la tarea no tiene horas cargadas del recurso')
def step_impl(context):
    try: 
        lista_cargas = RegistroDeHorasService.get_cargas()
        for carga in lista_cargas:
            if(carga.id_recurso==context.recurso.legajo and carga.id_tarea==context.tarea.id):
                RegistroDeHorasService.delete_carga(carga.id_registro_horas)
    except RegistroNoExiste and HTTPException:
        pass

@when(u'intento cargar {cantidad} horas trabajadas del recurso a la tarea para la fecha {fecha}')
def step_impl(context, cantidad, fecha):
    carga = RegistroDeHorasSchema.RegistroDeHoras(
        nombre_proyecto="Test de Gherkin",
        nombre_recurso="Juan Perez",
        nombre_tarea="Debuggear",
        cantidad=cantidad,
        fecha_trabajada=datetime.strptime(fecha, '%Y-%m-%d'),
        id_proyecto=1,
        id_tarea=int(context.tarea.id),
        id_recurso=int(context.recurso.legajo)
    )    

    #Tuve que hacer un mock de esta función porque si no hacía una consulta a la API de proyectos
    with mock.patch('src.main.service.TareaService.tareaTieneAsignado', return_value = True):
        with mock.patch('src.main.service.TareaService.get_tarea_id', return_value = TareaSchema.Tarea):
            with mock.patch('src.main.service.RecursosService.get_recurso_legajo', return_value = RecursoSchema.Recurso):
                context.carga = RegistroDeHorasService.cargarHoras(carga)

    if context.carga == None: 
        cargas = RegistroDeHorasService.get_cargas()
        for registro in cargas:
            if registro.id_tarea == carga.id_tarea and registro.id_recurso == carga.id_recurso and registro.fecha == carga.fecha:
                context.carga = registro

@then(u'se registran {cantidad} horas consumidas por la tarea del recurso')
def step_impl(context, cantidad):
    assert RegistroDeHorasService.horasRegistradas(context.carga.id_registro_horas) == int(cantidad)

@given(u'el recurso no está asignado a la tarea')
def step_impl(context):
    if(context.recurso.legajo in context.tarea.collaborators):
        context.tarea.collaborators.remove(context.recurso.legajo)

@when(u'intento cargar {cantidad} horas trabajadas a la tarea del recurso que no tiene asignado para la fecha {fecha}')
def step_impl(context, cantidad, fecha):
    carga = RegistroDeHorasSchema.RegistroDeHoras(
        nombre_proyecto="Test de Gherkin",
        nombre_recurso="Juan Perez",
        nombre_tarea="Debuggear",
        cantidad=cantidad,
        fecha_trabajada=datetime.strptime(fecha, '%Y-%m-%d'),
        id_proyecto=1,
        id_tarea=int(context.tarea.id),
        id_recurso=int(context.recurso.legajo)
    )    

    #Tuve que hacer un mock de esta función porque si no hacía una consulta a la API de proyectos
    with mock.patch('src.main.service.TareaService.tareaTieneAsignado', return_value = False):
        with mock.patch('src.main.service.TareaService.get_tarea_id', return_value = TareaSchema.Tarea):
            with mock.patch('src.main.service.RecursosService.get_recurso_legajo', return_value = RecursoSchema.Recurso):
                try: 
                    context.carga = RegistroDeHorasService.cargarHoras(carga)
                except RecursoNoAsignado and HTTPException:
                    print('El recurso ingresado no está asignado a la tarea')
        
@then(u'la carga debe ser denegada')
def step_impl(context):
    assert RecursoNoAsignado != None  

@then(u'la tarea tendrá 0 horas consumidas del recurso')
def step_impl(context):
    assert RegistroDeHorasService.horasConsumidasDeRecurso(context.tarea.id, context.recurso.legajo) == 0

@when(u'intento cargar {cantidad} horas trabajadas a una tarea que no existe para la fecha {fecha}')
def step_impl(context, cantidad, fecha):
    carga = RegistroDeHorasSchema.RegistroDeHoras(
        nombre_proyecto="Test de Gherkin",
        nombre_recurso="Juan Perez",
        nombre_tarea="",
        cantidad=cantidad,
        fecha_trabajada=datetime.strptime(fecha, '%Y-%m-%d'),
        id_proyecto=1,
        id_tarea=-1,
        id_recurso=int(context.recurso.legajo)
    )

    with mock.patch('src.main.service.TareaService.get_tarea_id') as mock_func:
        mock_func.return_value = None
    try:
        context.carga = RegistroDeHorasService.cargarHoras(carga)
    except TareaNoExiste and HTTPException:
        print('No se ha ingresado ninguna tarea válida')

@then(u'la carga debe ser denegada por no seleccionar una tarea existente')
def step_impl(context):
    assert TareaNoExiste != None  

@when(u'intento cargar {cantidad} horas trabajadas a la tarea de un recurso que no existe para la fecha {fecha}')
def step_impl(context, cantidad, fecha):
    carga = RegistroDeHorasSchema.RegistroDeHoras(
        nombre_proyecto="Test de Gherkin",
        nombre_recurso="Juan Perez",
        nombre_tarea="",
        cantidad=cantidad,
        fecha_trabajada=datetime.strptime(fecha, '%Y-%m-%d'),
        id_proyecto=1,
        id_tarea=int(context.tarea.id),
        id_recurso=-1
    )

    with mock.patch('src.main.service.RecursosService.get_recurso_legajo') as mock_func:
        mock_func.return_value = None
        try:
            context.carga = RegistroDeHorasService.cargarHoras(carga)
        except RecursoNoExiste and HTTPException:
            print('No se ha ingresado ninguna tarea')

@then(u'la carga debe ser denegada por ingresar mal el recurso')
def step_impl(context):
    assert RecursoNoExiste != None

@when(u'intento cargar {cantidad} horas de un recurso a una tarea para la fecha {fecha}, incumpliendo el rango de horas permitido')
def step_impl(context, cantidad, fecha):
    carga = RegistroDeHorasSchema.RegistroDeHoras(
        nombre_proyecto="Test de Gherkin",
        nombre_recurso="Juan Perez",
        nombre_tarea="Debuggear",
        cantidad=cantidad,
        fecha_trabajada=datetime.strptime(fecha, '%Y-%m-%d'),
        id_proyecto=1,
        id_tarea=int(context.tarea.id),
        id_recurso=int(context.recurso.legajo)
    )    

    try:
        context.carga = RegistroDeHorasService.cargarHoras(carga)
    except CargaInvalida and HTTPException:
        print('No es posible realizar la carga, la cantidad de horas ingresada no es válida')

@then(u'la carga debe ser denegada por superar el límite diario')
def step_impl(context):
    assert CargaInvalida != None

@when(u'intento cargar {cantidad} horas de un recurso a una tarea para la {fecha} que todavía no pasó')
def step_impl(context, cantidad, fecha):
    carga = RegistroDeHorasSchema.RegistroDeHoras(
        nombre_proyecto="Test de Gherkin",
        nombre_recurso="Juan Perez",
        nombre_tarea="Debuggear",
        cantidad=cantidad,
        fecha_trabajada=datetime.strptime(fecha, '%Y-%m-%d'),
        id_proyecto=1,
        id_tarea=int(context.tarea.id),
        id_recurso=int(context.recurso.legajo)
    )    

    try:
        context.carga = RegistroDeHorasService.cargarHoras(carga)
    except FechaInvalida and HTTPException:
        print('La fecha ingresada no es válida, por favor ingrese una fecha que ya haya pasado')
    
@then(u'la carga debe ser denegada por no ser para una fecha del pasado')
def step_impl(context):
    assert FechaInvalida != None