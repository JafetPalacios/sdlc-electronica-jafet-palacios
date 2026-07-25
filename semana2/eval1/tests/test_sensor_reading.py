"""Pruebas del modelo de lecturas ambientales."""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from semana2.eval1.sensor_reading import SensorReading


def test_sensor_reading_preserves_environmental_data() -> None:
    """Verificamos que una lectura conserve todos los datos recibidos."""
    captured_at = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)

    reading = SensorReading(
        sensor_id="SENSOR-01",
        temperature=25.5,
        humidity=60.0,
        captured_at=captured_at,
    )

    # Comprobamos el contrato público del modelo, no su implementación interna.
    assert reading.sensor_id == "SENSOR-01"
    assert reading.temperature == 25.5
    assert reading.humidity == 60.0
    assert reading.captured_at == captured_at


def test_sensor_reading_is_immutable() -> None:
    """Verificamos que una lectura no pueda modificarse después de crearla."""
    reading = SensorReading(
        sensor_id="SENSOR-01",
        temperature=25.5,
        humidity=60.0,
        captured_at=datetime(2026, 7, 25, 12, 0, tzinfo=UTC),
    )

    # Usamos setattr para comprobar la protección en tiempo de ejecución.
    with pytest.raises(FrozenInstanceError):
        setattr(reading, "temperature", 30.0)  # noqa: B010
