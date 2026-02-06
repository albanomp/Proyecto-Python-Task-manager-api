# Líneas 1-3: Importaciones
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
- ¿Qué hace? Importa las herramientas necesarias de FastAPI.
<Desglose:
FastAPI: La clase principal para crear tu aplicación
StaticFiles: Permite servir archivos estáticos (CSS, JS, imágenes)
CORSMiddleware: Configura CORS (permite que tu frontend se comunique con la API)

Analogía: Es como sacar las herramientas de la caja antes de empezar a trabajar.

# Línea 5: Importar create_tables
from app.database import create_tables
- ¿Qué hace? Importa la función create_tables() que creaste en database.py.
Recuerda: Esta función crea las tablas en la base de datos cuando la aplicación arranca.

# Líneas 8-12: Crear la aplicación FastAPI
app = FastAPI(
    title="Task Manager API",
    description="Sistema de gestión de tareas y proyectos con autenticación JWT",
    version="1.0.0"
)
- ¿Qué hace? Crea la aplicación FastAPI con información de documentación.
<Desglose:
app = FastAPI(...): Crea la instancia de tu aplicación (el objeto principal)
title: Nombre que aparecerá en la documentación automática
description: Descripción del proyecto
version: Versión de tu API

- ¿Dónde se ve esto? Cuando ejecutes la app y vayas a http://localhost:8000/docs, verás estos datos en la parte superior.
Analogía: Es como crear la portada de un libro con título, descripción y versión.

# Líneas 15-22: Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
- ¿Qué hace? Configura CORS para permitir que otros sitios web/aplicaciones se conecten a tu API.
<Desglose:
add_middleware: Añade una capa intermedia que procesa las peticiones
CORSMiddleware: Middleware específico para CORS
allow_origins=["*"]: Permite peticiones desde cualquier origen (* = todos). En producción pondrías URLs específicas como ["https://miapp.com"]
allow_credentials=True: Permite enviar cookies y credenciales
allow_methods=["*"]: Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
allow_headers=["*"]: Permite todos los headers

- ¿Por qué es importante? Sin esto, si creas un frontend (React, Vue, etc.) en localhost:3000, no podría comunicarse con tu API en localhost:8000.
Analogía: Es como poner un letrero en tu tienda que dice "Todos son bienvenidos".

# Línea 25: Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/statics"), name="static")
- ¿Qué hace? Sirve archivos estáticos (CSS, JS, imágenes) desde la carpeta app/statics.
<Desglose:
app.mount(...): "Monta" una ruta para servir archivos
"/static": La URL donde estarán disponibles (ej: http://localhost:8000/static/logo.png)
StaticFiles(directory="app/statics"): Carpeta donde están los archivos
name="static": Nombre interno para referenciar estos archivos

- Ejemplo de uso:
Si tienes app/statics/img/logo.png, puedes acceder a él en http://localhost:8000/static/img/logo.png
Analogía: Es como crear una vitrina donde exhibes tus productos (imágenes, CSS, JS).

# Líneas 28-33: Evento de inicio
@app.on_event("startup")
def startup_event():
    """Se ejecuta al iniciar la aplicación"""
    print("🚀 Iniciando aplicación...")
    create_tables()
    print("✅ Tablas de base de datos creadas/verificadas")
- ¿Qué hace? Define código que se ejecuta una sola vez cuando la aplicación arranca.
<Desglose:
@app.on_event("startup"): Decorador que indica "ejecuta esto al iniciar"
print("🚀 Iniciando aplicación..."): Mensaje en la consola
create_tables(): IMPORTANTE - Crea las tablas en la base de datos (viene de database.py)
print("✅ Tablas..."): Confirmación de que se crearon las tablas

- ¿Cuándo se ejecuta? Solo cuando ejecutas uvicorn app.main:app --reload
Analogía: Es como encender las luces y preparar todo antes de abrir tu tienda.

# Líneas 36-44: Ruta de prueba (endpoint raíz)
@app.get("/")
def read_root():
    """Endpoint de prueba"""
    return {
        "message": "Bienvenido a Task Manager API",
        "status": "running",
        "docs": "/docs"
    }
- ¿Qué hace? Define el endpoint principal de tu API.
<Desglose:
@app.get("/"): Decorador que dice "cuando alguien haga GET a /, ejecuta esta función"
def read_root():: Nombre de la función (puede ser cualquiera)
return {...}: Devuelve un diccionario JSON

- Cómo probarlo: Cuando ejecutes la app, ve a http://localhost:8000/ y verás:
json{
  "message": "Bienvenido a Task Manager API",
  "status": "running",
  "docs": "/docs"
}
Analogía: Es como la página de inicio de un sitio web.

# Líneas 47-51: Health check
@app.get("/health")
def health_check():
    """Verifica que la API está funcionando"""
    return {"status": "healthy"}
- ¿Qué hace? Endpoint simple para verificar que la API está viva.
Para qué sirve: En producción, servicios como Docker o Kubernetes usan este endpoint para verificar que tu app está funcionando.