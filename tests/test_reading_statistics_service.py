from datetime import datetime

from app.domain.reading_statistics import ReadingStatistics
from app.models import Reading, Sensor
from app.services.reading_service import ReadingService
from tests.fakes.fake_reading_repository import FakeReadingRepository
from tests.fakes.fake_sensor_repository import FakeSensorRepository


# Estadísticas de lecturas desde la capa de servicio
def test_get_statistics_for_sensor_returns_aggregated_values() -> None:
    # Preparamos un sensor y varias lecturas para comprobar la agregación
    sensor_repository = FakeSensorRepository()
    reading_repository = FakeReadingRepository()

    sensor = sensor_repository.create(
        Sensor(
            code="TEMP-STATS-001",
            name="Sensor con estadísticas",
            sensor_type="temperature",
            unit="°C",
        )
    )

    reading_repository.create(
        Reading(
            sensor_id=sensor.id,
            value=10.0,
            timestamp=datetime(2026, 8, 20, 10, 0, 0),
        )
    )
    reading_repository.create(
        Reading(
            sensor_id=sensor.id,
            value=20.0,
            timestamp=datetime(2026, 8, 20, 11, 0, 0),
        )
    )
    reading_repository.create(
        Reading(
            sensor_id=sensor.id,
            value=30.0,
            timestamp=datetime(2026, 8, 20, 12, 0, 0),
        )
    )

    service = ReadingService(
        reading_repository,
        sensor_repository,
    )

    statistics = service.get_statistics_for_sensor(
        sensor.id,
        start_date=datetime(2026, 8, 20, 10, 30, 0),
        end_date=datetime(2026, 8, 20, 12, 0, 0),
    )

    assert statistics == ReadingStatistics(
        sensor_id=sensor.id,
        count=2,
        minimum_value=20.0,
        maximum_value=30.0,
        average_value=25.0,
    )


# Estadísticas vacías
def test_get_statistics_for_sensor_returns_empty_aggregates_when_no_data() -> None:
    # Comprobamos que el contrato sea estable aunque el rango no produzca lecturas
    sensor_repository = FakeSensorRepository()
    reading_repository = FakeReadingRepository()

    sensor = sensor_repository.create(
        Sensor(
            code="TEMP-STATS-EMPTY-001",
            name="Sensor sin lecturas en rango",
            sensor_type="temperature",
            unit="°C",
        )
    )

    service = ReadingService(
        reading_repository,
        sensor_repository,
    )

    statistics = service.get_statistics_for_sensor(sensor.id)

    assert statistics == ReadingStatistics(
        sensor_id=sensor.id,
        count=0,
        minimum_value=None,
        maximum_value=None,
        average_value=None,
    )
