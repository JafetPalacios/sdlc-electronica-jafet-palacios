"""Pruebas del detector configurable de anomalías ambientales"""

from datetime import UTC, datetime

from semana2.eval1.anomaly_detector import (
    Anomaly,
    AnomalyDetector,
    AnomalyType,
)
from semana2.eval1.sensor_reading import SensorReading


def test_detects_temperature_above_injected_threshold() -> None:
    """Verificamos una anomalía cuando la temperatura supera el límite"""
    detector = AnomalyDetector(
        temperature_threshold=35.0,
        humidity_threshold=80.0,
    )
    reading = SensorReading(
        sensor_id="SENSOR-01",
        temperature=35.1,
        humidity=60.0,
        captured_at=datetime(2026, 7, 25, 12, 0, tzinfo=UTC),
    )

    anomalies = detector.detect(reading)

    assert anomalies == (
        Anomaly(
            sensor_id="SENSOR-01",
            anomaly_type=AnomalyType.TEMPERATURE,
            measured_value=35.1,
            threshold=35.0,
        ),
    )

def test_detects_humidity_above_injected_threshold() -> None:
    """Verificamos una anomalía cuando la humedad supera el límite"""
    detector = AnomalyDetector(
        temperature_threshold=35.0,
        humidity_threshold=80.0,
    )
    reading = SensorReading(
        sensor_id="SENSOR-02",
        temperature=25.0,
        humidity=80.1,
        captured_at=datetime(2026, 7, 25, 12, 0, tzinfo=UTC),
    )

    anomalies = detector.detect(reading)

    assert anomalies == (
        Anomaly(
            sensor_id="SENSOR-02",
            anomaly_type=AnomalyType.HUMIDITY,
            measured_value=80.1,
            threshold=80.0,
        ),
    )
