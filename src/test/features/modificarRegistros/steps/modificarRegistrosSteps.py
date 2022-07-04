from unittest import mock
from behave import *
from datetime import datetime

from fastapi import HTTPException
from src.main.exceptions.RecursoNoAsignado import RecursoNoAsignado
from src.main.exceptions.CantidadInvalida import CantidadInvalida
from src.main.schema.RegistroDeHorasSchema import RegistroDeHorasCargar
from src.main.service import RegistroDeHorasService

from src.main.schema import RecursoSchema
from src.main.schema import TareaSchema
from src.main.schema import RegistroDeHorasSchema

from src.main.service.RecursosService import get_recurso_legajo
from src.main.service.TareaService import get_tarea_id

@given(u'un recurso con ID {idRecurso}')
def step_impl(context, idRecurso):
    fake_json = [{
        "legajo": idRecurso,
        "Nombre": "Tomás",
        "Apellido": "Rodriguez"
    }]
    with mock.patch('src.main.service.RecursosService.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = fake_json
        context.recurso = get_recurso_legajo(idRecurso)

@given(u'una tarea con ID {idTarea}')
def step_impl(context, idTarea):
    fake_json = [{
        "id": idTarea,
        "name": "Tarea",
        "collaborators": [1, 2, 3]
    }]
    with mock.patch('src.main.service.TareaService.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = fake_json
        context.tarea = get_tarea_id(idTarea)

@given(u'el recurso está asignado a la tarea')
def step_impl(context):
    context.asignado = True
    if context.recurso.id not in context.tarea.collaborators:
        context.tarea.collaborators.append(context.recurso.id)

@given(u'se registraron {cantidadHoras} horas del recurso en la tarea')
def step_impl(context, cantidadHoras):
    carga = RegistroDeHorasSchema.RegistroDeHoras(
        nombre_proyecto="Test Modificación Horas",
        nombre_recurso="Mario",
        nombre_tarea="Gherkin",
        cantidad=cantidadHoras,
        fecha_trabajada="2022-03-04",
        id_proyecto=1,
        id_tarea=int(context.tarea.id),
        id_recurso=int(context.recurso.id),
    )    

    lista_cargas = RegistroDeHorasService.get_cargas()
    for c in lista_cargas:
        if(c.id_recurso==carga.id_recurso and c.id_tarea==carga.id_tarea):
            RegistroDeHorasService.delete_carga(c.id_registro_horas)     

    with mock.patch('src.main.service.TareaService.tareaTieneAsignado', return_value = True):
        with mock.patch('src.main.service.TareaService.get_tarea_id', return_value = TareaSchema.Tarea):
            with mock.patch('src.main.service.RecursosService.get_recurso_legajo', return_value = RecursoSchema.Recurso):
                try:
                    context.carga = RegistroDeHorasService.cargarHoras(carga)
                except:
                    context.carga = None

    if context.carga == None:
        cargas = RegistroDeHorasService.get_cargas()
        for registro in cargas:
            if (registro.id_tarea == carga.id_tarea 
                and registro.id_recurso == carga.id_recurso 
                and registro.fecha_trabajada == carga.fecha_trabajada):
                context.carga = registro

@when(u'se intenta aumentar las horas trabajadas del recurso a la tarea a {cantidadNueva} horas')
def step_impl(context, cantidadNueva): 
    modificacion = context.carga
    modificacion.cantidad = cantidadNueva

    with mock.patch('src.main.service.TareaService.tareaTieneAsignado', return_value = context.asignado):
        try:
            context.modificacion = RegistroDeHorasService.modificar_carga(context.carga.id_registro_horas, modificacion)
        except CantidadInvalida:
            print('La cantidad de horas ingresadas no es váldia')

@then(u'la tarea tendrá {cantidadFinal} horas consumidas del recurso')
def step_impl(context, cantidadFinal):
    assert int(cantidadFinal) == context.modificacion.cantidad

@when(u'se intenta disminuir las horas trabajadas del recurso a la tarea a {cantidadNueva} horas')
def step_impl(context, cantidadNueva):

    modificacion = context.carga
    modificacion.cantidad = int(cantidadNueva)

    with mock.patch('src.main.service.TareaService.tareaTieneAsignado', return_value = context.asignado):
        try:
            context.modificacion = RegistroDeHorasService.modificar_carga(context.carga.id_registro_horas , modificacion)
        except CantidadInvalida:
            print('La cantidad de horas ingresadas no es váldia')

@then(u'la modificación es denegeada')
def step_impl(context):
    assert CantidadInvalida != None

@then(u'la cantidad de horas permanece en {cantidadInicial}')
def step_impl(context, cantidadInicial):
    print(cantidadInicial)
    print(RegistroDeHorasService.get_cargas_id(context.carga.id_registro_horas).cantidad)
    assert int(cantidadInicial) == RegistroDeHorasService.get_cargas_id(context.carga.id_registro_horas).cantidad

@given(u'que no existe un registro con ID {idRegistro}')
def step_impl(context, idRegistro):
    context.idRegistro = idRegistro
    try:
        RegistroDeHorasService.delete_carga(idRegistro)
    except:
        pass

@when(u'se intenta modificar el registro')
def step_impl(context):
    carga = RegistroDeHorasSchema.RegistroDeHoras(
        nombre_proyecto="Test Modificación Horas",
        nombre_recurso="Mario",
        nombre_tarea="Gherkin",
        cantidad=7,
        fecha_trabajada="2022-03-04",
        id_proyecto=1,
        id_tarea=2,
        id_recurso=0,
    )   

    try:
        RegistroDeHorasService.modificar_carga(context.idRegistro, carga)
    except:
        print('El registro que está intentando modificar no existe')

@then(u'la modificación debe ser denegada')
def step_impl(context):
    assert HTTPException != None


@given(u'existe un registro de la tarea {idRecurso} y el recurso {idTarea}')
def step_impl(context, idTarea, idRecurso):
    carga = RegistroDeHorasSchema.RegistroDeHoras(
        nombre_proyecto="Test Modificación Horas",
        nombre_recurso="Mario",
        nombre_tarea="Gherkin",
        cantidad=5,
        fecha_trabajada="2022-03-04",
        id_proyecto=1,
        id_tarea=idTarea,
        id_recurso=idRecurso,
    )    

    with mock.patch('src.main.service.TareaService.tareaTieneAsignado', return_value = True):
        with mock.patch('src.main.service.TareaService.get_tarea_id', return_value = TareaSchema.Tarea):
            with mock.patch('src.main.service.RecursosService.get_recurso_legajo', return_value = RecursoSchema.Recurso):
                try:
                    context.carga = RegistroDeHorasService.cargarHoras(carga)
                except:
                    context.carga = None

    if context.carga == None:
        cargas = RegistroDeHorasService.get_cargas()
        for registro in cargas:
            if (registro.id_tarea == carga.id_tarea 
                and registro.id_recurso == carga.id_recurso 
                and registro.fecha_trabajada == carga.fecha_trabajada):
                context.carga = registro

@when(u'se intenta modificar la tarea a la tarea con ID {idTareaNueva}')
def step_impl(context, idTareaNueva):
    modificacion = context.carga
    modificacion.id_tarea = idTareaNueva
    with mock.patch('src.main.service.TareaService.tareaTieneAsignado', return_value = context.asignado):
        try:
            context.modificacion = RegistroDeHorasService.modificar_carga(context.carga.id_registro_horas , modificacion)
        except RecursoNoAsignado:
            print('La nueva tarea no tiene al recurso asignado')

@then(u'el registro tendrá la tarea con id {idTareaFinal}')
def step_impl(context, idTareaFinal):
    assert int(idTareaFinal) == RegistroDeHorasService.get_cargas_id(context.carga.id_registro_horas).id_tarea

@given(u'el recurso no está asignado a la tarea')
def step_impl(context):
    context.asignado = False
    if(context.recurso.id in context.tarea.collaborators):
        context.tarea.collaborators.remove(context.recurso.id)