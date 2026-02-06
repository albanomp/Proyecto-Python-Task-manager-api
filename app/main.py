from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_tables

# Crear la aplicación FastAPI
app = FastAPI(
    title="Task Manager API",
    description="Sistema de gestión de tareas y proyectos con autenticación JWT",
    version="1.0.0"
)

# Configurar CORS (permitir peticiones desde frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="app/statics"), name="static")

# Evento de inicio: crear tablas en la base de datos
@app.on_event("startup")
def startup_event():
    """Se ejecuta al iniciar la aplicación"""
    print("🚀 Iniciando aplicación...")
    create_tables()
    print("✅ Tablas de base de datos creadas/verificadas")

# Ruta de prueba
@app.get("/")
def read_root():
    """Endpoint de prueba"""
    return {
        "message": "Bienvenido a Task Manager API",
        "status": "running",
        "docs": "/docs"
    }

# Ruta de health check
@app.get("/health")
def health_check():
    """Verifica que la API está funcionando"""
    return {"status": "healthy"}