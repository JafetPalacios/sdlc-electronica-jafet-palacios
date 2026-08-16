from datetime import UTC, datetime

import pytest

from app.exceptions import InvalidDateTimezoneError, InvalidPaginationError
from app.models import Sensor
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
