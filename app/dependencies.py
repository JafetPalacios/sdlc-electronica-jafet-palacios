from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.domain.alert_strategy import ThresholdAlertStrategy
from app.repositories.sqlalchemy_alert_repository import (
    SqlAlchemyAlertRepository,
)
from app.repositories.sqlalchemy_reading_repository import (
    SqlAlchemyReadingRepository,
)
from app.repositories.sqlalchemy_sensor_repository import (
    SqlAlchemySensorRepository,
)
from app.services.alert_service import AlertService
from app.services.reading_service import ReadingService
from app.services.sensor_service import SensorService

# Dependencia reutilizable de sesión
# Representamos una sesión de SQLAlchemy que FastAPI obtiene mediante get_db
# Centralizamos esta declaración para no repetir Annotated y Depends en cada función encargada de construir servicios
DatabaseSession = Annotated[
    Session,
    Depends(get_db),
]

# Construcción del servicio de alertas
def get_alert_service(
    db: DatabaseSession,
) -> AlertService:

    # Construimos los repositorios concretos que participan en la consulta
    alert_repository = SqlAlchemyAlertRepository(db)
    sensor_repository = SqlAlchemySensorRepository(db)

    # Inyectamos las abstracciones requeridas por el servicio de aplicación
    return AlertService(
        alert_repository=alert_repository,
        sensor_repository=sensor_repository,
    )


# Construcción del servicio de lecturas
def get_reading_service(
    db: DatabaseSession,
) -> ReadingService:

    # Construimos los repositorios concretos utilizando la misma sesión
    reading_repository = SqlAlchemyReadingRepository(db)
    sensor_repository = SqlAlchemySensorRepository(db)
    alert_repository = SqlAlchemyAlertRepository(db)

    # Seleccionamos la estrategia concreta desde el punto de composición
    alert_strategy = ThresholdAlertStrategy()

    return ReadingService(
        reading_repository=reading_repository,
        sensor_repository=sensor_repository,
        alert_repository=alert_repository,
        alert_strategy=alert_strategy,
    )


# Construcción del servicio de sensores
def get_sensor_service(                                                 # Creamos el repositorio concreto que SensorService necesita
    db: DatabaseSession,                                                # Reutilizamos la sesión generada para la petición actual
) -> SensorService:

    sensor_repository = SqlAlchemySensorRepository(db)                  # Creamos el repositorio responsable de consultar y persistir sensores

    return SensorService(sensor_repository)                             # Inyectamos el repositorio en el servicio de aplicación. El servicio depende del contrato y no directamente de SQLAlchemy