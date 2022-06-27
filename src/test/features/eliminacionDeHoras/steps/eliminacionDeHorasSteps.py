from src.main.exceptions.RegistroNoExiste import RegistroNoExiste
from fastapi import HTTPException, status

from datetime import datetime
from behave import *

from src.main.service import TareaService
from src.main.service import RegistroDeHorasService
from src.main.schema import RegistroDeHorasSchema

from unittest import mock

@given(u'un registro de horas con tarea {idTarea}, recurso {idRecurso} y fecha {fecha}')
def step_impl(context,idTarea, idRecurso,fecha):
    
    context.registro = RegistroDeHorasSchema.RegistroDeHorasCargar(
            nombre_proyecto="Test de Gherkin",
            nombre_recurso="Juan Perez",
            nombre_tarea="Debuggear",
            cantidad= 5,
            fecha_trabajada=datetime.strptime(fecha, '%Y-%m-%d'),
            codigo_proyecto=1,
            codigo_tarea= idTarea,
            codigo_recurso=idRecurso,
            codigo_carga= 1
        )
    try:
        RegistroDeHorasService.cargarHoras(context.registro)
    except HTTPException:
        pass


@when(u'elimino el registro de horas')
def step_impl(context):
    try:
        RegistroDeHorasService.delete_carga(context.registro.codigo_carga)
    except RegistroNoExiste:
        print("No existe el registro de horas que se esta intentando eliminar.")


@then(u'no existe ningun registro con ese codigo de carga')
def step_impl(context):
    try:
        RegistroDeHorasService.get_cargas_id(context.registro.codigo_carga)
    except RegistroNoExiste:
        pass
        

@given(u'que no existe un registro de horas para la tarea {idTarea}, el recurso {idRecurso} y fecha {fecha}')
def step_impl(context,idTarea,idRecurso,fecha):
    lista = RegistroDeHorasService.get_cargas()

    context.id = None

    for carga in lista:
        if carga.codigo_recurso == idRecurso and carga.codigo_tarea == idTarea and carga.fecha_trabajada == fecha:
            context.id = carga.codigo_recurso
            RegistroDeHorasService.delete_carga(carga.codigo_carga)

@when(u'intento eliminar el registro de horas')
def step_impl(context):
    try:
        RegistroDeHorasService.delete_carga(context.id)
    except RegistroNoExiste:
        pass

@then(u'la eliminación debe ser denegada')
def step_impl(context):
    assert RegistroNoExiste != None