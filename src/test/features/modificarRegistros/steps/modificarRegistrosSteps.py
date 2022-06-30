# from behave import *
# from datetime import datetime

# from src.main.exceptions.TareaNoExiste import TareaNoExiste
# from src.main.exceptions.RecursoNoExiste import RecursoNoExiste

# @given(u'un recurso con ID {id}')
# def step_impl(context, id):
#     context.recurso = Recurso(id)

# @given(u'una tarea con título "{tituloTarea}"')
# def step_impl(context,tituloTarea):
#     context.tarea = Tarea(tituloTarea)

# @given(u'el recurso está asignado a la tarea')
# def step_impl(context):
#     context.tarea.añadirRecurso(context.recurso)

# @given(u'el recurso no tiene horas cargadas en la tarea')
# def step_impl(context):
#     context.trabajoRealizado = TrabajoRealizado(context.recurso, context.tarea)

# @given(u'el recurso tiene {cantidadInicial} horas cargadas en la tarea')
# def step_impl(context, cantidadInicial):
#     context.trabajoRealizado = TrabajoRealizado(context.recurso, context.tarea)
#     context.trabajoRealizado.cargarHoras(float(cantidadInicial), datetime.today())

# @given(u'el recurso tiene {cantidadInicial} horas cargadas en la tarea el día {fecha}')
# def step_impl(context, cantidadInicial, fecha):
#     context.trabajoRealizado = TrabajoRealizado(context.recurso, context.tarea)
#     context.trabajoRealizado.cargarHoras(float(cantidadInicial), datetime.strptime(fecha, '%d-%m-%Y'))

# @given(u'el recurso realiza un trabajo sobre una tarea que no existe')
# def step_impl(context):
#     context.trabajoRealizado = TrabajoRealizado(context.recurso, None)

# @given(u'se realiza un trabajo sobre la tarea')
# def step_impl(context):
#     context.trabajoRealizado = TrabajoRealizado(None, context.tarea)

# @when(u'se intenta aumentar {cantidad} la cantidad horas trabajadas superando el límite diario')
# def step_impl(context, cantidad):
#     try:
#         context.trabajoRealizado.aumentarHorasCargadas(float(cantidad))
#     except LimiteDiarioSuperado:
#         print('No se pueden cargar más de 8 horas para un mismo día')

# @when(u'se intenta disminuir las horas trabajadas del recurso a la tarea en {cantidad}')
# def step_impl(context, cantidad):
#     try:
#         context.trabajoRealizado.disminuirHorasCargadas(float(cantidad))
#     except SinHorasCargadas:
#         print('No se puede disminuir la cantidad de horas ingresadas')

# @when(u'se intenta aumentar las horas trabajadas del recurso a la tarea en {cantidad}')
# def step_impl(context, cantidad):
#     context.trabajoRealizado.aumentarHorasCargadas(float(cantidad))

# @when(u'se intenta aumentar {cantidad} horas trabajadas del recurso a una tarea que no existe')
# def step_impl(context, cantidad):
#     try: 
#         context.trabajoRealizado.aumentarHorasCargadas(float(cantidad))
#     except TareaNoExiste:
#         print('La tarea ingresada no existe')

# @when(u'se intenta aumentar {cantidad} horas trabajadas de un recurso que no existe a la tarea')
# def step_impl(context, cantidad):
#     try: 
#         context.trabajoRealizado.aumentarHorasCargadas(float(cantidad))
#     except RecursoNoExiste:
#         print('El recurso ingresado no existe')

# @then(u'la tarea tendrá {cantidadFinal} horas consumidas del recurso')
# def step_impl(context, cantidadFinal):
#     assert context.trabajoRealizado.horasConsumidas() == float(cantidadFinal)

# @then(u'la carga debe ser denegada por ingresar mal la tarea')
# def step_impl(context):
#     assert TareaNoExiste != None

# @then(u'la modificación debe ser denegada por superar la cantidad de horas cargadas a disminuir')
# def step_impl(context):
#     assert SinHorasCargadas != None

# @then(u'la modificación debe ser denegada por superar el límite de carga diario')
# def step_impl(context):
#     assert LimiteDiarioSuperado != None