from fastapi import FastAPI
from src.main.router.RegistroDeHorasRouter import router as cargaDeHorasRouter
from src.main.utils.settings import apply_middleware

app = FastAPI() #Instancia de la clase FastAPI
apply_middleware(app)

app.include_router(cargaDeHorasRouter)