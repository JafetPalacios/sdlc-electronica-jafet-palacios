from dataclasses import dataclass
from enum import Enum
from typing import Protocol

class SensorType(Enum):
    
    # Definimos los tipos de sensores permitidos
    TEMPERATURA = "temperatura"
    HUMEDAD = "humedad"
    PRESION = "presion"

@dataclass(frozen=True)
class Reading:
    sensor_type: SensorType                                 # Guardamos el tipo de sensor que produjo la lectura
    value: float                                            # Guardamos el valor numérico medido
    unit: str                                               # Guardamos la unidad de medida

class Sensor(Protocol):
    def read(self) -> Reading:                              # Exige que cualquier sensor tenga un método read() y que dicho método devuelva un objeto Reading
        ...                                                 # Indica que este método debe existir, pero aquí no se implementa, ya que es un protocolo y no una clase concreta

class TemperatureSensor:
    def read(self) -> Reading:
        # Devolvemos una lectura simulada de temperatura.
        return Reading(
            sensor_type=SensorType.TEMPERATURA,
            value=23.5,
            unit="C",
        )
    
def read_sensor(sensor: Sensor) -> Reading:
    return sensor.read()                                     # Leemos cualquier objeto que cumpla con el protocolo Sensor y devolvemos la lectura obtenida

# Primera función pura: La función únicamente lee del sensor y devuelve la lectura sin modificarla ni depender de ningún estado externo
def celsius_to_fahrenheit(reading: Reading) -> float:
        return (reading.value * 9 / 5) + 32                 # Convertimos el valor de Celsius a Fahrenheit sin modificar la lectura

# Segunda función pura: La función únicamente compara el valor de una lectura con un umbral y devuelve un booleano
def exceeds_threshold(reading: Reading, threshold: float) -> bool:
    return reading.value > threshold                        # Comprobamos si el valor de la lectura supera el límite recibido

# Tercera función pura: La función únicamente aplica un desplazamiento a un valor de lectura y devuelve una nueva lectura
def apply_offset(reading: Reading, offset: float) -> Reading:
    # Creamos una lectura nueva con el valor corregido.
    return Reading(
        sensor_type=reading.sensor_type,
        value=reading.value + offset,
        unit=reading.unit,
    )

# Cuarta función pura: La función únicamente verifica si el valor de una lectura está dentro de un rango permitido y devuelve un booleano
def is_within_range(
    reading: Reading,
    minimum: float,
    maximum: float,
) -> bool:
    return minimum <= reading.value <= maximum              # Comprobamos si la lectura está dentro del rango permitido

# Quinta función pura: La función únicamente calcula la diferencia entre el valor de una lectura y un valor objetivo y devuelve la diferencia
def difference_from_target(reading: Reading, target: float) -> float:
    return reading.value - target                           # Calculamos la diferencia entre la lectura y el valor objetivo.