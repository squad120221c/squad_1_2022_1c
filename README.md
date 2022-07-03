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
# Despliegue de la app

La app esta desplegada en Heroku junto con la base de datos PostgreSQL. 

La API está desplegada en https://squad1-rrhh.herokuapp.com/docs 

# BDD

Se utlizó la librerá behave para los Gherkin en Python

Instalar librería behave
```
pip install behave
```
Para correr los tests, posicionarse en el directorio feature y ejecutar el siguiente comando en la consola
```
behave file.feature
```

# Heroku

Para subir la app a Heroku primero descargo Heroku CLI https://devcenter.heroku.com/articles/heroku-cli

Crear requirements.txt con
```
pip freeze > requirements.txt
```

Crear runtime.txt y especificar la versión de Python python-3.9.6

Creo el archivo Procfile y agrego 
```
web: uvicorn src.main.controller:app --host=0.0.0.0 --port=${PORT:-5000}
```

Inicio heroku por consola
```
heroku login
```

Para pushear a Heroku un repositorio que ya existe
```
heroku git:remote -a squad1-rrhh
```

- [👥 Enlace a la API de Recursos Humanos](https://squad1-rrhh.herokuapp.com/docs)

# APIs con las que interactuamos 

- Módulo de Proyecto: https://aninfo-projects.herokuapp.com/docs#/
- Sistema externo de recursos: https://anypoint.mulesoft.com/mocking/api/v1/sources/exchange/assets/754f50e8-20d8-4223-bbdc-56d50131d0ae/recursos-psa/1.0.0/m/api/recursos

## Requests a Apis externas

```
conda install -c anaconda requests
```
```
conda install -c jmcmurray json
```

# Base de datos

Para la base de datos se utlizará PostgreSQL

Descargar PostgreSQL: https://www.postgresql.org/download/

PostgreSQL viene con la interfaz gráfica pgAdmin, donde vamos a poder ver y crear nuestras bases de datos

La base de datos estará subida en https://www.heroku.com/postgres

DB del proyecto: https://data.heroku.com/datastores/c9529228-9ac1-4f95-bfb1-fcd19c9d9913#

## Conexión a la base de datos
```
conda install -c anaconda postgresql
```

- Para conectarnos a la base de datos y hacer consultas usamos psycopg2

Es la librería que hace de puente entre PostgreSQL y Python
```
conda install -c anaconda psycopg2
```

- Para la validación de datos usamos pydantic

- Vamos a usar el ORM peewee: 

```
pip3 install peewee
```

# Referencias: 

https://www.psycopg.org/docs/

https://fastapi.tiangolo.com/advanced/sql-databases-peewee/?h=database

http://docs.peewee-orm.com/en/latest/peewee/quickstart.html#quickstart
