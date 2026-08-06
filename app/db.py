from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Configuración de conexión
# Indicamos que utilizaremos SQLite y que los datos se almacenarán en el archivo sensorhub.db ubicado en la raíz del proyecto
DATABASE_URL = "sqlite:///./sensorhub.db"


# Motor de base de datos
# El motor administra la comunicación entre SQLAlchemy y SQLite
# Desactivamos check_same_thread porque FastAPI puede atender una petición utilizando hilos distintos durante su ciclo de ejecución

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
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