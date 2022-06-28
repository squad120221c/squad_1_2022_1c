from src.main.model.RegistroDeHorasModel import RegistroDeHoras
from src.main.utils.db import db

def createTable():
    with db:
        db.create_tables([RegistroDeHoras])