"""Detección configurable de anomalías ambientales"""

from dataclasses import dataclass
from enum import Enum

from semana2.eval1.sensor_reading import SensorReading


class AnomalyType(Enum):
    """Tipos de anomalías ambientales que puede detectar el sistema"""

    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"


@dataclass(frozen=True)
class Anomaly:
    """Describe una anomalía detectada en una lectura ambiental"""

    sensor_id: str
    anomaly_type: AnomalyType
    measured_value: float
    threshold: float


class AnomalyDetector:
    """Detecta anomalías usando límites proporcionados externamente"""

    def __init__(
        self,
        temperature_threshold: float,
        humidity_threshold: float,
    ) -> None:
        """Configura los límites utilizados durante la detección"""
        self._temperature_threshold = temperature_threshold
        self._humidity_threshold = humidity_threshold

    def detect(self, reading: SensorReading) -> tuple[Anomaly, ...]:
        """Devuelve las anomalías encontradas en una lectura"""
        anomalies: list[Anomaly] = []

        # Comparamos contra el umbral inyectado en lugar de fijarlo en el método
        if reading.temperature > self._temperature_threshold:
            anomalies.append(
                Anomaly(
                    sensor_id=reading.sensor_id,
                    anomaly_type=AnomalyType.TEMPERATURE,
                    measured_value=reading.temperature,
                    threshold=self._temperature_threshold,
                )
            )

        if reading.humidity > self._humidity_threshold:
            anomalies.append(
                Anomaly(
                    sensor_id=reading.sensor_id,
                    anomaly_type=AnomalyType.HUMIDITY,
                    measured_value=reading.humidity,
                    threshold=self._humidity_threshold,
                )
            )

        return tuple(anomalies)
