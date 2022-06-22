# squad_1_2022_1c

## API REST con python

Para la API se utilizó FastAPI y Uvicorn como servidor

FastAPI es un framework para crear APIs con Python 3.6+ basado en sugerencias de tipo estándar de Python.

Uvicorn es una implementación de servidor web ASGI para Python.

```
pip install fastapi
```
```
pip install "uvicorn[standard]"
```

Desplegar la app con el servidor uvicorn de manera local

```
uvicorn src.main.controller:app
```
