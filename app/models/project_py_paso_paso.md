pythonfrom sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class Project(Base):
    """
    Modelo de Proyecto
    Representa la tabla 'projects' en la base de datos
    Un proyecto pertenece a un usuario y contiene múltiples tareas
    """
    __tablename__ = "projects"
    
    # Columnas
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")


# Líneas 1-5: Importaciones
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
Nuevos imports respecto a User:

Text: Tipo de dato para textos largos (descripciones)
ForeignKey: Para crear relaciones entre tablas

- ¿Qué es un ForeignKey?
Es una "llave foránea" que apunta a otra tabla. Es como decir "este proyecto pertenece al usuario con id X".

# Líneas 7-13: Definir la cl
class Project(Base):
    """
    Modelo de Proyecto
    Representa la tabla 'projects' en la base de datos
    Un proyecto pertenece a un usuario y contiene múltiples tareas
    """
    __tablename__ = "projects"
Similar a User:

Hereda de Base
El nombre de la tabla será projects


Líneas 16-20: Definir columnas
1. id - Identificador único
pythonid = Column(Integer, primary_key=True, index=True)
Igual que en User: Identificador único del proyecto.

2. title - Título del proyecto
pythontitle = Column(String(200), nullable=False)
Desglose:

String(200): Texto de máximo 200 caracteres
nullable=False: Obligatorio (no puede ser NULL)

Ejemplos:

"Rediseño de la web"
"App móvil de delivery"
"Sistema de inventario"

¿Por qué 200 caracteres?
Es suficiente para títulos descriptivos pero no excesivamente largos.

3. description - Descripción opcional
pythondescription = Column(Text, nullable=True)
```

**Desglose:**
- `Text`: Texto sin límite de tamaño (para descripciones largas)
- `nullable=True`: **Opcional** (puede ser NULL)

**¿Text vs String?**
- `String`: Textos cortos (ej: títulos, nombres)
- `Text`: Textos largos (ej: descripciones, contenido)

**Ejemplo:**
```
"Este proyecto consiste en rediseñar completamente 
la página web de la empresa, implementando un diseño 
moderno y responsive. Incluye actualización de contenidos, 
optimización SEO y mejora de la experiencia de usuario."

4. user_id - ¿A quién pertenece este proyecto? ⭐ IMPORTANTE
user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
```

**Desglose:**
- `Integer`: Es un número (el id del usuario)
- `ForeignKey("users.id")`: **Clave foránea** que apunta a la columna `id` de la tabla `users`
- `nullable=False`: Obligatorio (todo proyecto DEBE tener un dueño)

**¿Qué hace ForeignKey?**
Crea una relación entre tablas:
```
Tabla: projects                    Tabla: users
┌────┬───────────┬─────────┐      ┌────┬──────────┐
│ id │ title     │ user_id │      │ id │ username │
├────┼───────────┼─────────┤      ├────┼──────────┤
│ 1  │ Web App   │    2    │──────│ 2  │ juan123  │
│ 2  │ Mobile    │    2    │──────│ 2  │ juan123  │
│ 3  │ Backend   │    5    │──────│ 5  │ maria_dev│
└────┴───────────┴─────────┘      └────┴──────────┘
        ↑
        └─ Este número apunta al id del usuario
Resultado:

El proyecto 1 pertenece al usuario 2 (juan123)
El proyecto 2 pertenece al usuario 2 (juan123)
El proyecto 3 pertenece al usuario 5 (maria_dev)

Analogía: Es como escribir el DNI del dueño en cada proyecto.

5. created_at - Fecha de creación
pythoncreated_at = Column(DateTime, default=datetime.utcnow)
Igual que en User:

Se guarda automáticamente cuándo se creó el proyecto


# Líneas 23-24: Relaciones ⭐⭐ MUY IMPORTANTE
Relación 1: owner - Conexión con User
pythonowner = relationship("User", back_populates="projects")
- ¿Qué hace?
Crea una relación bidireccional entre Project y User.
<Desglose:
relationship("User"): Se relaciona con el modelo User
back_populates="projects": Nombre del atributo en User que apunta de vuelta aquí

Cómo se usa:
# Obtener el dueño de un proyecto
proyecto = db.query(Project).filter(Project.id == 1).first()
dueño = proyecto.owner  # ← Objeto User completo
print(dueño.username)   # "juan123"

# O al revés (desde User):
usuario = db.query(User).filter(User.id == 2).first()
proyectos = usuario.projects  # ← Lista de Project
print(proyectos[0].title)     # "Web App"
```

**Visualización:**
```
Project                      User
┌──────────────┐            ┌──────────┐
│ id: 1        │            │ id: 2    │
│ title: "Web" │  .owner →  │ username │
│ user_id: 2   │            │          │
└──────────────┘            └──────────┘
                   ↑
                   └─ La relación permite navegar fácilmente

Relación 2: tasks - Conexión con Task
tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
- ¿Qué hace?
Define que un proyecto tiene muchas tareas.
<Desglose:
relationship("Task"): Se relaciona con el modelo Task (que crearemos después)
back_populates="project": Nombre del atributo en Task que apunta de vuelta
cascade="all, delete-orphan": IMPORTANTE - Si borras un proyecto, se borran todas sus tareas

- ¿Qué es cascade?
Define qué pasa cuando borras un proyecto:

"all, delete-orphan": Borra todas las tareas huérfanas (sin proyecto padre)

Ejemplo:
# Si borras un proyecto
db.delete(proyecto)
db.commit()

# Automáticamente se borran TODAS sus tareas
# No quedan tareas "huérfanas" sin proyecto
Cómo se usa:
# Obtener todas las tareas de un proyecto
proyecto = db.query(Project).filter(Project.id == 1).first()
tareas = proyecto.tasks  # ← Lista de Task
for tarea in tareas:
    print(tarea.title)
```

**Visualización:**
```
Project: "Web App"
├─ Task 1: "Diseñar mockups"
├─ Task 2: "Programar frontend"
└─ Task 3: "Testing"

Si borras "Web App" → Se borran automáticamente las 3 tareas
```

---

## 🎨 **Visualización de la tabla `projects`:**
```
┌────────────────────────────────────────────────────────────────┐
│                       TABLA: projects                           │
├────┬─────────────────┬──────────────────┬─────────┬────────────┤
│ id │ title           │ description      │ user_id │ created_at │
├────┼─────────────────┼──────────────────┼─────────┼────────────┤
│ 1  │ Web App         │ Rediseño web...  │    2    │ 2026-02-11 │
│ 2  │ Mobile App      │ App de delivery  │    2    │ 2026-02-11 │
│ 3  │ Backend API     │ API REST...      │    5    │ 2026-02-12 │
└────┴─────────────────┴──────────────────┴─────────┴────────────┘
                                                ↓
                                         Apunta a users.id