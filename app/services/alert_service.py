from app.exceptions import SensorNotFoundError
from app.models import Alert
from app.repositories.alert_repository import AlertRepository
from app.repositories.sensor_repository import SensorRepository


# Servicio de aplicación para alertas
# Coordinamos la consulta de alertas sin depender de FastAPI o SQLAlchemy
class AlertService:

    # Recibimos las abstracciones necesarias para consultar sensores y alertas
    def __init__(
        self,
        alert_repository: AlertRepository,
        sensor_repository: SensorRepository,
    ) -> None:

        self._alert_repository = alert_repository
        self._sensor_repository = sensor_repository

    # Consulta de alertas pertenecientes a un sensor
    def list_alerts_for_sensor(
        self,
        sensor_id: int,
    ) -> list[Alert]:

        # Comprobamos primero que el sensor solicitado exista
        sensor = self._sensor_repository.get_by_id(sensor_id)

        if sensor is None:
            raise SensorNotFoundError(sensor_id)

        # Delegamos al repositorio la recuperación de las alertas almacenadas
        return self._alert_repository.list_for_sensor(sensor_id)