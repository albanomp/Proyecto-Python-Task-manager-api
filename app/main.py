from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from app.database import create_tables

# ---------- Lifespan ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(" Iniciando aplicación...")
    create_tables()
    print(" Tablas listas")
    yield
    print(" Cerrando aplicación...")

# ---------- App ----------
app = FastAPI(
    title="Task Manager API",
    description="Sistema de gestión de tareas y proyectos con autenticación JWT",
    version="1.0.0",
    lifespan=lifespan
)

# ---------- CORS ----------
origins = ["http://localhost:5173", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Static ----------
if os.path.exists("app/statics"):
    app.mount("/static", StaticFiles(directory="app/statics"), name="static")

# ---------- Test Routes ----------
@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a Task Manager API",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
