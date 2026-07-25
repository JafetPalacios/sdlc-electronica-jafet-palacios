from semana2.sensor_registry.registry import Sensor, SensorRegistry


def test_register_allows_retrieving_sensor_by_identifier() -> None:
    registry = SensorRegistry()
    sensor = Sensor(
        identifier="TEMP-001",
        name="Sensor de temperatura",
    )

    registry.register(sensor)

    stored_sensor = registry.get("TEMP-001")

    assert stored_sensor == sensor

