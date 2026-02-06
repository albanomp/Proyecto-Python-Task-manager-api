# Línea 1-3: Importaciones
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ¿Qué hace? Importa las herramientas de SQLAlchemy que necesitamos:

create_engine: Crea la conexión con la base de datos
declarative_base: La clase base de la que heredarán todos tus modelos
sessionmaker: Crea "sesiones" para interactuar con la BD

# Analogía: Es como importar las herramientas de tu caja antes de empezar a trabajar.

# Línea 6: URL de la base de datos

SQLALCHEMY_DATABASE_URL = "sqlite:///./task_manager.db"
- ¿Qué hace? Define dónde se guardará tu base de datos.
<Desglose:

- sqlite:// → Tipo de base de datos (SQLite)
- /./ → En la carpeta actual del proyecto
- task_manager.db → Nombre del archivo de base de datos

Resultado: Se creará un archivo llamado task_manager.db en la raíz de tu proyecto. Ahí se guardarán todos los usuarios, proyectos y tareas.

# Línea 9-12: Crear el "motor" (engine)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
- ¿Qué hace? Crea el motor que conecta Python con la base de datos.
<Desglose:
create_engine(...): Crea la conexión
check_same_thread: False: Necesario solo para SQLite. Permite que varios hilos (threads) usen la misma conexión. FastAPI usa múltiples hilos, así que necesitamos esto.

Analogía: Es como encender el coche. El motor ya está listo, pero aún no conduces.

# Línea 15: Crear SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
- ¿Qué hace? Crea una "fábrica de sesiones".
<Desglose:
sessionmaker: Crea sesiones (conversaciones con la BD)
autocommit=False: No guarda cambios automáticamente (los controlas tú con db.commit())
autoflush=False: No envía cambios automáticamente a la BD antes de hacer queries
bind=engine: Vincula las sesiones al motor que creamos arriba

Analogía: Es como tener un cuaderno donde apuntas las operaciones. Cuando terminas, decides si guardas (commit()) o descartas los cambios.

# Línea 18: Base para los modelos
Base = declarative_base()

- ¿Qué hace? Crea la clase base de la que heredarán todos tus modelos (User, Project, Task).
Cuando crees un modelo harás:
class User(Base):  # ← Hereda de Base
    __tablename__ = "users"
    # ...

Analogía: Es como crear un molde. Todos los modelos seguirán este patrón.

# Línea 21-30: Función get_db()
<def get_db():
    """
    Generador que proporciona una sesión de base de datos.
    Se usa como dependencia en los endpoints de FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

- ¿Qué hace? Es un generador que crea una sesión de BD, la entrega, y luego la cierra automáticamente.

<Desglose:
db = SessionLocal(): Crea una nueva sesión
yield db: "Presta" la sesión al endpoint que la pidió
finally: db.close(): Cierra la sesión cuando termina (¡importante para no dejar conexiones abiertas!)

- Cómo se usa en FastAPI:
# @app.get("/usuarios")
<def listar_usuarios(db: Session = Depends(get_db)):  # ← Aquí se usa
    usuarios = db.query(User).all()
    return usuarios

Analogía: Es como pedir un libro en la biblioteca. Te lo prestan, lo usas, y cuando terminas lo devuelves automáticamente.

# Línea 33-39: Función create_tables()
<ndef create_tables():
    """
    Crea todas las tablas en la base de datos.
    Se llama al iniciar la aplicación.
    """
    Base.metadata.create_all(bind=engine)

- ¿Qué hace? Crea todas las tablas en la base de datos basándose en los modelos que definas.
Desglose:

- Base.metadata: Contiene información de todos los modelos que heredan de Base
- .create_all(bind=engine): Crea las tablas en la BD conectada al engine

<Cuándo se ejecuta: Cuando inicies la aplicación en main.py, esto se ejecutará automáticamente y creará las tablas si no existen.

Analogía: Es como crear las estanterías vacías en un almacén antes de empezar a guardar cosas.

<Resumen de database.py:
Este archivo hace 4 cosas esenciales:

- Define dónde está la BD (SQLALCHEMY_DATABASE_URL)
- Crea la conexión (engine)
- Proporciona sesiones para trabajar con la BD (get_db())
- Crea las tablas automáticamente (create_tables())

