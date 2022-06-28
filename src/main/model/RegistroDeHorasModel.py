import peewee
from src.main.utils.db import db

class RegistroDeHoras(peewee.Model):
    id_registro_horas = peewee.AutoField()
    nombre_proyecto = peewee.CharField()
    nombre_tarea = peewee.CharField()   
    nombre_recurso = peewee.CharField() 
    fecha_trabajada = peewee.DateField()
    cantidad = peewee.IntegerField()
    id_proyecto = peewee.IntegerField()
    id_tarea = peewee.IntegerField()
    id_recurso = peewee.IntegerField()

    class Meta:
        database = db