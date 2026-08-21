from app.domain.alert_lifecycle import AlertStatus, can_transition_alert
from app.exceptions import (
    AlertNotFoundError,
    InvalidAlertStatusTransitionError,
    SensorNotFoundError,
)
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

    # Consulta de alertas que aún requieren seguimiento
    def list_active_alerts(self) -> list[Alert]:

        return self._alert_repository.list_active()

    # Cambio de estado de una alerta concreta
    def update_alert_status(
        self,
        *,
        alert_id: int,
        new_status: AlertStatus,
    ) -> Alert:

        alert = self._alert_repository.get_by_id(alert_id)

        if alert is None:
            raise AlertNotFoundError(alert_id)

        if not can_transition_alert(
            current_status=alert.status,
            new_status=new_status,
        ):
            raise InvalidAlertStatusTransitionError(
                alert_id=alert_id,
                current_status=alert.status,
                new_status=new_status,
            )

        alert.status = new_status

        return self._alert_repository.update(alert)
