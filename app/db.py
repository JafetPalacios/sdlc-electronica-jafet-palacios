import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


# Configuración de conexión
# Obtenemos la URL de conexión desde una variable de entorno
# Si no existe, mantenemos SQLite como opción local por defecto
def get_database_url() -> str:

    url = os.getenv("DATABASE_URL", "sqlite:///./sensorhub.db")

    if url.startswith("postgres://"):                                                   # Normalizamos URLs entregadas por algunos proveedores para usar psycopg
        return url.replace("postgres://", "postgresql+psycopg://", 1)

    if url.startswith("postgresql://") and "+psycopg" not in url:                       # Añadimos explícitamente el driver psycopg cuando la URL usa postgresql://
        return url.replace("postgresql://", "postgresql+psycopg://", 1)

    return url


DATABASE_URL = get_database_url()

connect_args = (                                                                        # Configuramos argumentos específicos solo cuando trabajamos con SQLite
    {"check_same_thread": False}                                                        # PostgreSQL no utiliza check_same_thread
    if DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(                                                                 # Creamos el motor utilizando la URL correspondiente al entorno actual
    DATABASE_URL,
    connect_args=connect_args,
)


# Fábrica de sesiones
# Creamos una configuración reutilizable para generar sesiones de base de datos
# Cada sesión representa una unidad de trabajo independiente

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


# Clase base declarativa
# Todos los modelos ORM heredan de esta clase
# SQLAlchemy utiliza su metadata para registrar las tablas y relaciones
class Base(DeclarativeBase):
    """Definimos la clase base para los modelos ORM de SensorHub"""


# Dependencia de sesión
# Proporcionamos una sesión independiente por petición
# FastAPI ejecuta el bloque previo a yield antes del endpoint y ejecuta finally cuando termina la petición
def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()                         # Creamos una nueva sesión usando la configuración de SessionLocal

    try:

        yield db                                # Entregamos la sesión al repositorio o servicio que la solicite
    finally:

        db.close()                              # Cerramos la sesión aunque la petición termine correctamente o con error