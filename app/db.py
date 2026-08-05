from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = "sqlite:///./sensorhub.db"               # Indicamos que SQLite guardará los datos en un archivo llamado sensorhub.db

engine = create_engine(                                 # Motor administra la comunicación entre SQLAlchemy y SQLite
    DATABASE_URL,
    connect_args={"check_same_thread": False},          # SQLite limita normalmente cada conexión al hilo donde fue creada. FastAPI puede atender una petición usando distintos hilos, por lo que desactivamos esa restricción
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):                            # Todos los modelos ORM heredarán de esta clase class Sensor(Base) Así SQLAlchemy podrá registrar las tablas y sus metadatos
    """Clase base para los modelos ORM de SensorHub"""

# Proporciona una sesión de base de datos por petición
def get_db() -> Generator[Session, None, None]:
    
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()