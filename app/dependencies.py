from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.sqlalchemy_reading_repository import (
    SqlAlchemyReadingRepository,
)
from app.repositories.sqlalchemy_sensor_repository import (
    SqlAlchemySensorRepository,
)
from app.services.reading_service import ReadingService
from app.services.sensor_service import SensorService

# Dependencia reutilizable de sesión
# Representamos una sesión de SQLAlchemy que FastAPI obtiene mediante get_db
# Centralizamos esta declaración para no repetir Annotated y Depends en cada función encargada de construir servicios
DatabaseSession = Annotated[
    Session,
    Depends(get_db),
]


# Construcción del servicio de lecturas
def get_reading_service(                                                # Creamos los repositorios concretos que ReadingService necesita
    db: DatabaseSession,                                                # Utilizamos la misma sesión durante toda la petición para mantener
) -> ReadingService:                                                    # una única unidad de trabajo entre las operaciones relacionadas

    reading_repository = SqlAlchemyReadingRepository(db)                # Creamos el repositorio responsable de consultar y persistir lecturas
    sensor_repository = SqlAlchemySensorRepository(db)                  # Creamos el repositorio utilizado para comprobar sensores propietarios

    return ReadingService(                                              # Inyectamos ambos repositorios mediante los contratos esperados
        reading_repository=reading_repository,                          # El servicio queda desacoplado de la creación concreta de dependencias
        sensor_repository=sensor_repository,
    )


# Construcción del servicio de sensores
def get_sensor_service(                                                 # Creamos el repositorio concreto que SensorService necesita
    db: DatabaseSession,                                                # Reutilizamos la sesión generada para la petición actual
) -> SensorService:

    sensor_repository = SqlAlchemySensorRepository(db)                  # Creamos el repositorio responsable de consultar y persistir sensores

    return SensorService(sensor_repository)                             # Inyectamos el repositorio en el servicio de aplicación. El servicio depende del contrato y no directamente de SQLAlchemy