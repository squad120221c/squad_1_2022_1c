from fastapi import FastAPI
from src.main.router.RegistroDeHorasRouter import router as cargaDeHorasRouter

app = FastAPI() #Instancia de la clase FastAPI

app.include_router(cargaDeHorasRouter)