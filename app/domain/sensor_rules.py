from dataclasses import dataclass
from typing import Final


# Regla física asociada a un tipo de sensor
# Concentramos la unidad admitida y el intervalo permitido para sus lecturas
# La estructura inmutable evita modificaciones accidentales durante la ejecución
@dataclass(frozen=True)
class SensorRule:                                               # Representamos las restricciones físicas de un tipo de sensor

    unit: str                                                   # Unidad canónica utilizada por SensorHub
    minimum_value: float                                        # Valor mínimo permitido para una lectura
    maximum_value: float                                        # Valor máximo permitido para una lectura


# Catálogo de reglas físicas
# Utilizamos el tipo del sensor como clave para localizar su configuración
# Este catálogo será consultado por la capa de servicio al crear sensores y al registrar o actualizar lecturas
SENSOR_RULES: Final[dict[str, SensorRule]] = {
    "temperature": SensorRule(
        unit="°C",
        minimum_value=-273.15,
        maximum_value=1000.0,
    ),
    "humidity": SensorRule(
        unit="%",
        minimum_value=0.0,
        maximum_value=100.0,
    ),
    "pressure": SensorRule(
        unit="kPa",
        minimum_value=0.0,
        maximum_value=10000.0,
    ),
}