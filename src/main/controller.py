from fastapi import FastAPI
from src.main.router.RegistroDeHorasRouter import router as rrhh
from src.main.router.RecursosRouter import router as recursos
from src.main.utils.settings import apply_middleware

app = FastAPI()
apply_middleware(app)

app.include_router(rrhh)
app.include_router(recursos)