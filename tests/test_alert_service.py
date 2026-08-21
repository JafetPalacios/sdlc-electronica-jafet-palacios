from unittest.mock import Mock

import pytest

from app.domain.alert_lifecycle import AlertStatus
from app.exceptions import AlertNotFoundError, InvalidAlertStatusTransitionError
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


# Consulta de alertas activas
def test_list_active_alerts_returns_repository_results() -> None:
    # Preparamos el servicio con un repositorio aislado de alertas
    sensor_repository = FakeSensorRepository()
    alert_repository = Mock()

    expected_alert = Alert(
        sensor_id=1,
        reading_id=1,
        value=31.0,
        threshold=30.0,
    )

    alert_repository.list_active.return_value = [
        expected_alert,
    ]

    service = AlertService(
        alert_repository,
        sensor_repository,
    )

    alerts = service.list_active_alerts()

    alert_repository.list_active.assert_called_once_with()
    assert alerts == [expected_alert]


# Cambio de estado válido
def test_update_alert_status_changes_open_to_acknowledged() -> None:
    # Preparamos una alerta abierta que debe poder reconocerse
    sensor_repository = FakeSensorRepository()
    alert_repository = Mock()

    alert = Alert(
        sensor_id=1,
        reading_id=1,
        value=31.0,
        threshold=30.0,
        status=AlertStatus.OPEN,
    )
    alert.id = 7

    alert_repository.get_by_id.return_value = alert
    alert_repository.update.side_effect = lambda persisted_alert: persisted_alert

    service = AlertService(
        alert_repository,
        sensor_repository,
    )

    updated_alert = service.update_alert_status(
        alert_id=alert.id,
        new_status=AlertStatus.ACKNOWLEDGED,
    )

    alert_repository.update.assert_called_once_with(alert)
    assert updated_alert.status == AlertStatus.ACKNOWLEDGED


# Transición inválida
def test_update_alert_status_rejects_resolved_to_open_transition() -> None:
    # Preparamos una alerta ya resuelta que no debe reabrirse
    sensor_repository = FakeSensorRepository()
    alert_repository = Mock()

    alert = Alert(
        sensor_id=1,
        reading_id=1,
        value=31.0,
        threshold=30.0,
        status=AlertStatus.RESOLVED,
    )
    alert.id = 9

    alert_repository.get_by_id.return_value = alert

    service = AlertService(
        alert_repository,
        sensor_repository,
    )

    with pytest.raises(
        InvalidAlertStatusTransitionError,
        match="No se puede cambiar la alerta",
    ):
        service.update_alert_status(
            alert_id=alert.id,
            new_status=AlertStatus.OPEN,
        )

    alert_repository.update.assert_not_called()


# Alerta inexistente
def test_update_alert_status_raises_when_alert_does_not_exist() -> None:
    # Confirmamos que el servicio informe la inexistencia antes de intentar actualizar
    sensor_repository = FakeSensorRepository()
    alert_repository = Mock()
    alert_repository.get_by_id.return_value = None

    service = AlertService(
        alert_repository,
        sensor_repository,
    )

    with pytest.raises(
        AlertNotFoundError,
        match="No existe una alerta con id 999",
    ):
        service.update_alert_status(
            alert_id=999,
            new_status=AlertStatus.ACKNOWLEDGED,
        )
