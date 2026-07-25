"""Modelo utilizado para representar lecturas ambientales de sensores."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class SensorReading:
    """Representa una lectura de temperatura y humedad.

    Attributes:
        sensor_id: Identificador del sensor que generó la lectura.
        temperature: Temperatura registrada en grados Celsius.
        humidity: Humedad relativa registrada en porcentaje.
        captured_at: Fecha y hora en que se obtuvo la lectura.
    """

    # Conservamos juntos los datos que pertenecen a una misma medición.
    sensor_id: str
    temperature: float
    humidity: float
    captured_at: datetime
