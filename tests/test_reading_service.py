from datetime import UTC, datetime
from unittest.mock import Mock

import pytest

from app.domain.alert_strategy import AlertSeverity, ThresholdAlertStrategy
from app.exceptions import (
    InvalidDateTimezoneError,
    InvalidPaginationError,
    SensorInactiveError,
)
from app.models import Sensor
from app.schemas import ReadingCreate
from app.services.reading_service import ReadingService
from tests.fakes.fake_reading_repository import FakeReadingRepository
from tests.fakes.fake_sensor_repository import FakeSensorRepository

# Pruebas unitarias del servicio de lecturas
# Utilizamos repositorios falsos para comprobar las reglas del servicio
# sin depender de FastAPI, SQLAlchemy o una base de datos real


# Construimos un servicio con un sensor válido para las pruebas de listado
def create_service_with_sensor() -> tuple[
    ReadingService,
    FakeReadingRepository,
]:

    sensor_repository = FakeSensorRepository()
    reading_repository = FakeReadingRepository()

    sensor_repository.create(
        Sensor(
            code="HUM-001",
            name="Sensor de humedad",
            sensor_type="humidity",
            unit="%",
        )
    )

    service = ReadingService(
        reading_repository,
        sensor_repository,
    )

    return service, reading_repository

def test_validate_reading_value_skips_unknown_sensor_type() -> None:
    # Reutilizamos el helper existente para obtener un ReadingService aislado
    service, _ = create_service_with_sensor()

    # Verificamos que un tipo histórico sin regla asociada no sea rechazado
    service._validate_reading_value(
        sensor_type="legacy_sensor",
        value=999999.0,
    )


# Límite inferior de paginación
def test_list_readings_rejects_limit_below_minimum() -> None:
    # Comprobamos que el servicio proteja la invariante incluso sin FastAPI
    service, reading_repository = create_service_with_sensor()

    with pytest.raises(InvalidPaginationError):
        service.list_readings_for_sensor(
            sensor_id=1,
            limit=0,
        )

    # Verificamos que una entrada inválida no llegue a persistencia
    assert reading_repository.list_for_sensor_calls == 0


# Límite superior de paginación
def test_list_readings_rejects_limit_above_maximum() -> None:
    # Comprobamos que el servicio mantenga el máximo aceptado por SensorHub
    service, reading_repository = create_service_with_sensor()

    with pytest.raises(InvalidPaginationError):
        service.list_readings_for_sensor(
            sensor_id=1,
            limit=101,
        )

    # Confirmamos que el repositorio no reciba parámetros fuera del contrato
    assert reading_repository.list_for_sensor_calls == 0


# Desplazamiento negativo
def test_list_readings_rejects_negative_offset() -> None:
    # Comprobamos que la paginación nunca utilice desplazamientos negativos
    service, reading_repository = create_service_with_sensor()

    with pytest.raises(InvalidPaginationError):
        service.list_readings_for_sensor(
            sensor_id=1,
            offset=-1,
        )

    # Confirmamos que detenemos la operación antes de consultar persistencia
    assert reading_repository.list_for_sensor_calls == 0


# Fechas con tratamiento de zona horaria incompatible
def test_list_readings_rejects_mixed_timezone_awareness() -> None:
    # Comprobamos que el servicio rechace una combinación temporal ambigua
    # antes de intentar comparar o delegar las fechas al repositorio
    service, reading_repository = create_service_with_sensor()

    start_date = datetime(
        2026,
        8,
        10,
        10,
        0,
        tzinfo=UTC,
    )
    end_date = datetime(
        2026,
        8,
        11,
        10,
        0,
    )

    with pytest.raises(InvalidDateTimezoneError):
        service.list_readings_for_sensor(
            sensor_id=1,
            start_date=start_date,
            end_date=end_date,
        )

    # Verificamos que las fechas incompatibles no alcancen persistencia
    assert reading_repository.list_for_sensor_calls == 0

# Generación de alerta al superar el umbral configurado
def test_create_reading_above_threshold_creates_alert() -> None:
    # Preparamos un sensor con un umbral activo y repositorios aislados
    sensor_repository = FakeSensorRepository()
    reading_repository = FakeReadingRepository()
    alert_repository = Mock()

    sensor = sensor_repository.create(
        Sensor(
            code="TEMP-ALERT-001",
            name="Sensor de temperatura con alerta",
            sensor_type="temperature",
            unit="°C",
            alert_threshold=30.0,
        )
    )

    # Inyectamos la estrategia concreta y el colaborador que registrará alertas
    service = ReadingService(
        reading_repository,
        sensor_repository,
        alert_repository=alert_repository,
        alert_strategy=ThresholdAlertStrategy(),
    )

    reading = service.create_reading(
        sensor.id,
        ReadingCreate(
            value=31.0,
        ),
    )

    # Verificamos que la lectura anómala produzca exactamente una alerta
    alert_repository.create.assert_called_once()

    alert = alert_repository.create.call_args.args[0]

    # Comprobamos que la alerta conserve la evidencia que originó la detección
    assert alert.sensor_id == sensor.id
    assert alert.reading_id == reading.id
    assert alert.value == 31.0
    assert alert.threshold == 30.0
    assert alert.severity == AlertSeverity.WARNING


# Generación de alerta crítica al superar ampliamente el umbral configurado
def test_create_reading_far_above_threshold_creates_critical_alert() -> None:
    # Preparamos un sensor con un umbral activo y repositorios aislados
    sensor_repository = FakeSensorRepository()
    reading_repository = FakeReadingRepository()
    alert_repository = Mock()

    sensor = sensor_repository.create(
        Sensor(
            code="TEMP-ALERT-CRITICAL-001",
            name="Sensor de temperatura con alerta crítica",
            sensor_type="temperature",
            unit="°C",
            alert_threshold=30.0,
        )
    )

    service = ReadingService(
        reading_repository,
        sensor_repository,
        alert_repository=alert_repository,
        alert_strategy=ThresholdAlertStrategy(),
    )

    service.create_reading(
        sensor.id,
        ReadingCreate(
            value=36.0,
        ),
    )

    alert = alert_repository.create.call_args.args[0]

    assert alert.severity == AlertSeverity.CRITICAL

# Rechazo de lecturas para sensores inactivos
def test_create_reading_rejects_inactive_sensor() -> None:
    # Preparar repositorios aislados para probar la regla sin base de datos
    sensor_repository = FakeSensorRepository()
    reading_repository = FakeReadingRepository()

    # Registrar un sensor desactivado que debe conservarse pero no aceptar telemetría
    sensor = sensor_repository.create(
        Sensor(
            code="TEMP-INACTIVE-001",
            name="Sensor de temperatura inactivo",
            location="Laboratorio de electrónica",
            sensor_type="temperature",
            unit="°C",
            is_active=False,
        )
    )

    service = ReadingService(
        reading_repository,
        sensor_repository,
    )

    # Rechazar la ingesta porque el recurso existe pero está deshabilitado
    with pytest.raises(
        SensorInactiveError,
        match=f"El sensor con id {sensor.id} está inactivo",
    ):
        service.create_reading(
            sensor.id,
            ReadingCreate(
                value=25.0,
            ),
        )

    # Confirmar que la operación se detenga antes de persistir una lectura
    assert reading_repository.get_by_id(1) is None
