# Líneas 1-5: Importaciones
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
- ¿Qué importamos?

Column, Integer, String, DateTime: Tipos de datos para las columnas
relationship: Para definir relaciones entre tablas (ej: User tiene muchos Projects)
datetime: Para fechas
Base: La clase base que creamos en database.py


# Línea 7-10: Definir la clase
class User(Base):
    """
    Modelo de Usuario
    Representa la tabla 'users' en la base de datos
    """
    __tablename__ = "users"
    
<Desglose:
class User(Base):: Crea la clase User que hereda de Base
__tablename__ = "users": El nombre de la tabla en la BD será "users"

Resultado: Se creará una tabla llamada users en task_manager.db

# Líneas 13-17: Definir columnas
id = Column(Integer, primary_key=True, index=True)
username = Column(String, unique=True, index=True, nullable=False)
email = Column(String, unique=True, index=True, nullable=False)
hashed_password = Column(String, nullable=False)
created_at = Column(DateTime, default=datetime.utcnow)
Cada línea explicada:
1. id
pythonid = Column(Integer, primary_key=True, index=True)

Integer: Tipo de dato (número entero)
primary_key=True: Es la clave primaria (identificador único)
index=True: Crea un índice para búsquedas más rápidas

Analogía: Es como el DNI de una persona, único e irrepetible.

2. username
pythonusername = Column(String, unique=True, index=True, nullable=False)

String: Tipo texto
unique=True: No puede haber dos usuarios con el mismo username
index=True: Índice para búsquedas rápidas
nullable=False: NO puede ser NULL (obligatorio)

Ejemplo: "juan123", "maria_dev"

3. email
pythonemail = Column(String, unique=True, index=True, nullable=False)

Similar a username
unique=True: Cada email es único

Ejemplo: "juan@example.com"

4. hashed_password
pythonhashed_password = Column(String, nullable=False)
```
- Guarda la contraseña **hasheada** (encriptada)
- **NUNCA** guardamos contraseñas en texto plano

**Ejemplo de hash:**
```
Contraseña: "MiPassword123"
Hash: "$2b$12$KIXxY5v8Zy9U.../abc123xyz..."
¿Por qué hashed_password y no password?
Para recordar que NUNCA guardamos la contraseña real, solo el hash.

5. created_at
pythoncreated_at = Column(DateTime, default=datetime.utcnow)

DateTime: Tipo fecha y hora
default=datetime.utcnow: Valor por defecto = fecha y hora actual (UTC)

Resultado: Cuando creas un usuario, automáticamente se guarda cuándo se creó.
Ejemplo: 2026-02-11 14:30:45

# Línea 20-21: Relación con Projects
projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
```

**¿Qué hace?**
Define la relación: **Un usuario tiene muchos proyectos**.

<Desglose>
- `relationship("Project")`: Se relaciona con el modelo `Project` (que crearemos después)
- `back_populates="owner"`: El nombre del atributo en `Project` que apunta de vuelta a `User`
- `cascade="all, delete-orphan"`: Si borras un usuario, se borran todos sus proyectos automáticamente

**Analogía:** 
```
Usuario "Juan" → tiene → [Proyecto1, Proyecto2, Proyecto3]
Cómo se usa:
python# Obtener todos los proyectos de un usuario
usuario = db.query(User).filter(User.id == 1).first()
proyectos_de_usuario = usuario.projects  # ← Lista de proyectos
```

---

## 🎨 **Visualización de la tabla `users`:**
```
┌────────────────────────────────────────────────────┐
│                  TABLA: users                       │
├────┬───────────┬──────────────────┬─────────────────┤
│ id │ username  │ email            │ hashed_password │ created_at
├────┼───────────┼──────────────────┼─────────────────┤
│ 1  │ juan123   │ juan@mail.com    │ $2b$12$KI...   │ 2026-02-11 14:30:45
│ 2  │ maria_dev │ maria@mail.com   │ $2b$12$Xy...   │ 2026-02-11 15:22:10
│ 3  │ pedro99   │ pedro@mail.com   │ $2b$12$Ab...   │ 2026-02-11 16:45:33
└────┴───────────┴──────────────────┴─────────────────┘