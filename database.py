from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de la base de datos SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./task_manager.db"

# Crear motor de conexión a base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Crear SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class para los modelos
Base = declarative_base()

# Dependencia para obtener la sesión de base de datos
def get_db():
    """
    Generador que proporciona una sesión de base de datos.
    Se usa como dependencia en los endpoints de FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para crear todas las tablas        
def create_tables():
    """
    Crea todas las tablas en la base de datos.
    Se llama al iniciar la aplicación.
    """
    Base.metadata.create_all(bind=engine)