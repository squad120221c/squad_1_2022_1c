#Creo el modelo de peewee, lo usaremos para nuestras tablas en la base de datos 
# y también para poder realizar consultas, insertar datos, actualizarlos, etc.

import peewee
from src.main.utils.db import db

class RegistroDeHoras(peewee.Model):
    codigo_carga = peewee.AutoField()
    nombre_proyecto = peewee.CharField()
    nombre_tarea = peewee.CharField()   
    nombre_recurso = peewee.CharField() 
    fecha_trabajada = peewee.DateField()
    cantidad = peewee.IntegerField()
    codigo_proyecto = peewee.IntegerField()
    codigo_tarea = peewee.IntegerField()
    codigo_recurso = peewee.IntegerField()

    #Contendrá la conexión a la base de datos
    class Meta:
        database = db