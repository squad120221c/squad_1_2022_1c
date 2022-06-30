from src.main.exceptions.RegistroNoExiste import RegistroNoExiste
from fastapi import HTTPException, status

from datetime import datetime
from behave import *

from src.main.service import TareaService
from src.main.service import RegistroDeHorasService
from src.main.schema import RegistroDeHorasSchema
from src.main.schema import TareaSchema
from src.main.schema import RecursoSchema

from unittest import mock

@given(u'un registro de horas con tarea {idTarea}, recurso {idRecurso} y fecha {fecha}')
def step_impl(context,idTarea, idRecurso,fecha):
    
    carga = RegistroDeHorasSchema.RegistroDeHoras(
            nombre_proyecto="Test de Gherkin",
            nombre_recurso="Juan Perez",
            nombre_tarea="Debuggear",
            cantidad= 5,
            fecha_trabajada=datetime.strptime(fecha, '%Y-%m-%d'),
            id_proyecto=1,
            id_tarea= idTarea,
            id_recurso=idRecurso,
        )
    with mock.patch('src.main.service.TareaService.tareaTieneAsignado', return_value = True):
        with mock.patch('src.main.service.TareaService.get_tarea_id', return_value = TareaSchema.Tarea):
            with mock.patch('src.main.service.RecursosService.get_recurso_legajo', return_value = RecursoSchema.Recurso):
                try:
                    context.registro = RegistroDeHorasService.cargarHoras(carga)
                except HTTPException:
                    print("lpm")
                    pass


@when(u'elimino el registro de horas')
def step_impl(context):
    try:
        print(context.registro.id_registro_horas)
        RegistroDeHorasService.delete_carga(context.registro.id_registro_horas)
    except RegistroNoExiste:
        print("No existe el registro de horas que se esta intentando eliminar.")


@then(u'no existe ningun registro con ese codigo de carga')
def step_impl(context):
    try:
        RegistroDeHorasService.get_cargas_id(context.registro.id_registro_horas)
    except RegistroNoExiste and HTTPException:
        pass
        

@given(u'que no existe un registro de horas para la tarea {idTarea}, el recurso {idRecurso} y fecha {fecha}')
def step_impl(context,idTarea,idRecurso,fecha):
    lista = RegistroDeHorasService.get_cargas()

    context.id = None

    for carga in lista:
        if carga.id_recurso == idRecurso and carga.id_tarea == idTarea and carga.fecha_trabajada == fecha:
            context.id = carga.id_recurso
            RegistroDeHorasService.delete_carga(context.id)

@when(u'intento eliminar el registro de horas')
def step_impl(context):
    try:
        RegistroDeHorasService.delete_carga(context.id)
    except RegistroNoExiste:
        pass

@then(u'la eliminación debe ser denegada')
def step_impl(context):
    assert RegistroNoExiste != None