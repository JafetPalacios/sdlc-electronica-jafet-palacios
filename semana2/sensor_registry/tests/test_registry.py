import pytest

from semana2.sensor_registry.registry import (
    DuplicateSensorError,
    Sensor,
    SensorRegistry,
)


def test_register_allows_retrieving_sensor_by_identifier() -> None:
    registry = SensorRegistry()
    sensor = Sensor(
        identifier="TEMP-001",
        name="Sensor de temperatura",
    )

    registry.register(sensor)

    stored_sensor = registry.get("TEMP-001")

    assert stored_sensor == sensor


def test_register_rejects_duplicate_identifier() -> None:
    registry = SensorRegistry()
    original_sensor = Sensor(
        identifier="TEMP-001",
        name="Sensor principal",
    )
    duplicate_sensor = Sensor(
        identifier="TEMP-001",
        name="Sensor secundario",
    )

    registry.register(original_sensor)

    with pytest.raises(DuplicateSensorError):
        registry.register(duplicate_sensor)

    assert registry.count() == 1
    assert registry.get("TEMP-001") == original_sensor


