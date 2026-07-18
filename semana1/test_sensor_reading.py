from dataclasses import FrozenInstanceError

import pytest

from semana1.sensor_reading import (
    Reading,
    SensorType,
    TemperatureSensor,
    read_sensor,
    celsius_to_fahrenheit,
    exceeds_threshold,
    apply_offset,
    is_within_range,
    difference_from_target,
)

def test_create_temperature_reading() -> None:
    # Creamos una lectura de temperatura
    reading = Reading(
        sensor_type=SensorType.TEMPERATURA,
        value=23.5,
        unit="C",
    )

    # Verificamos que los datos se hayan guardado correctamente
    assert reading.sensor_type is SensorType.TEMPERATURA
    assert reading.value == 23.5
    assert reading.unit == "C"

def test_reading_is_immutable() -> None:
    # Creamos una lectura de temperatura.
    reading = Reading(
        sensor_type=SensorType.TEMPERATURA,
        value=23.5,
        unit="C",
    )

    # Verificamos que no sea posible modificar su valor
    with pytest.raises(FrozenInstanceError):
        setattr(reading, "value", 30.0)

def test_celsius_to_fahrenheit() -> None:
    # Creamos una lectura de temperatura en Celsius
    reading = Reading(
        sensor_type=SensorType.TEMPERATURA,
        value=23.5,
        unit="C",
    )

    result = celsius_to_fahrenheit(reading)                         # Convertimos la lectura a Fahrenheit
    assert result == 74.3                                           # Verificamos que el resultado sea el esperado

def test_exceeds_threshold() -> None:
    # Creamos una lectura de temperatura.
    reading = Reading(
        sensor_type=SensorType.TEMPERATURA,
        value=23.5,
        unit="C",
    )

    assert exceeds_threshold(reading, 20.0) is True                # Verificamos que supere un límite de 20 grados
    assert exceeds_threshold(reading, 30.0) is False               # Verificamos que no supere un límite de 30 grados

def test_apply_offset() -> None:
    # Creamos una lectura original
    reading = Reading(
        sensor_type=SensorType.TEMPERATURA,
        value=23.5,
        unit="C",
    )

    corrected_reading = apply_offset(reading, -0.5)                # Aplicamos una corrección de calibración
    assert corrected_reading.value == 23.0                         # Verificamos el valor de la nueva lectura
    assert corrected_reading.sensor_type is SensorType.TEMPERATURA # Verificamos que conserve el tipo de sensor y la unidad
    assert corrected_reading.unit == "C"
    assert reading.value == 23.5                                   # Verificamos que la lectura original no haya cambiado

def test_is_within_range() -> None:
    # Creamos una lectura de temperatura.
    reading = Reading(
        sensor_type=SensorType.TEMPERATURA,
        value=23.5,
        unit="C",
    )

    assert is_within_range(reading, 20.0, 25.0) is True             # Verificamos que la lectura esté dentro del rango
    assert is_within_range(reading, 26.0, 30.0) is False            # Verificamos que la lectura esté fuera del rango

def test_difference_from_target() -> None:
    # Creamos una lectura de temperatura
    reading = Reading(
        sensor_type=SensorType.TEMPERATURA,
        value=23.5,
        unit="C",
    )

    assert difference_from_target(reading, 20.0) == 3.5            # Verificamos la diferencia cuando la lectura supera el objetivo
    assert difference_from_target(reading, 25.0) == -1.5           # Verificamos la diferencia cuando la lectura está debajo del objetivo

def test_temperature_sensor_follows_protocol() -> None:
    sensor = TemperatureSensor()                                    # Creamos un sensor concreto
    reading = read_sensor(sensor)                                   # Leemos el sensor mediante una función que depende del Protocol

    # Comprobamos que la lectura devuelta sea correcta.
    assert reading.sensor_type is SensorType.TEMPERATURA
    assert reading.value == 23.5
    assert reading.unit == "C"