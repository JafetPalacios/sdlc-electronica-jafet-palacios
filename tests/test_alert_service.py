from unittest.mock import Mock

from app.models import Alert, Sensor
from app.services.alert_service import AlertService
from tests.fakes.fake_sensor_repository import FakeSensorRepository


# Consulta de alertas desde la capa de servicio
def test_list_alerts_for_existing_sensor_returns_repository_results() -> None:
    # Preparamos un sensor existente sin utilizar una base de datos real
    sensor_repository = FakeSensorRepository()
    alert_repository = Mock()

    sensor = sensor_repository.create(
        Sensor(
            code="TEMP-ALERT-SERVICE-001",
            name="Sensor con alertas",
            sensor_type="temperature",
            unit="°C",
            alert_threshold=30.0,
        )
    )

    # Simulamos una alerta previamente registrada para el sensor
    expected_alert = Alert(
        sensor_id=sensor.id,
        reading_id=1,
        value=31.0,
        threshold=30.0,
    )

    alert_repository.list_for_sensor.return_value = [
        expected_alert,
    ]

    service = AlertService(
        alert_repository,
        sensor_repository,
    )

    alerts = service.list_alerts_for_sensor(sensor.id)

    # Verificamos que el servicio delegue la consulta al repositorio
    alert_repository.list_for_sensor.assert_called_once_with(sensor.id)

    assert alerts == [expected_alert]