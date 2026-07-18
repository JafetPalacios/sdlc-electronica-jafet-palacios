import pytest

from semana1.solid_srp_ocp_lsp import (
    BadRawHumiditySensor,
    BadSensorFormatter,
    BadTemperatureSensor,
    HumidityFormatter,
    HumidityPercentageSensor,
    PercentageSensor,
    ReadingFileWriter,
    TemperatureFormatter,
    TemperatureSensor,
    format_sensor_reading,
    read_percentage,
)

# Test SRP incorrecto
def test_bad_srp_reads_and_saves(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)                                                      # Cambiamos temporalmente al directorio de prueba

    sensor = BadTemperatureSensor()                                                  # Creamos el sensor SPR incorrecto
    value = sensor.read_and_save()                                                   # El mismo método obtiene la lectura y guarda el archivo
    assert value == 23.5                                                             # Verificamos la lectura devuelta
    assert (tmp_path / "temperature.txt").read_text(encoding="utf-8") == "23.5"      # Verificamos que también haya creado el archivo


# Test SRP correcto
def test_good_srp_separates_reading_and_saving(tmp_path) -> None:
    # Creamos por separado el sensor y el escritor de archivos.
    sensor = TemperatureSensor()
    writer = ReadingFileWriter()

    value = sensor.read()                                                           # El sensor solamente obtiene la lectura
    file_path = tmp_path / "temperature.txt"                                        # Construimos una ruta dentro de la carpeta temporal
    writer.save(value, str(file_path))                                              # El escritor se encarga únicamente de guardar la lectura
    assert value == 23.5                                                            # Verificamos que el sensor devolvió la lectura correcta
    assert file_path.read_text(encoding="utf-8") == "23.5"                          # Verificamos que el escritor guardó correctamente el valor


# Test OCP incorrecto
def test_bad_ocp_formats_known_sensor_types() -> None:
    formatter = BadSensorFormatter()                                                 # Creamos el formateador incorrecto
    # Verificamos los dos tipos de sensor soportados actualmente
    assert formatter.format_reading("temperature", 23.5) == (
        "Temperature: 23.5 C"
    )
    assert formatter.format_reading("humidity", 60.0) == (
        "Humidity: 60.0 %"
    )


# Test OCP correcto
def test_good_ocp_accepts_new_formatter() -> None:
    # Creamos un nuevo formateador sin modificar el código existente
    class PressureFormatter:
        def format(self, value: float) -> str:
            return f"Pressure: {value} hPa"

    temperature_formatter = TemperatureFormatter()
    humidity_formatter = HumidityFormatter()
    pressure_formatter = PressureFormatter()

    assert format_sensor_reading(
        temperature_formatter,
        23.5,
    ) == "Temperature: 23.5 C"

    assert format_sensor_reading(
        humidity_formatter,
        60.0,
    ) == "Humidity: 60.0 %"

    assert format_sensor_reading(
        pressure_formatter,
        1013.25,
    ) == "Pressure: 1013.25 hPa"


# Test LSP incorrecto
def test_bad_lsp_breaks_percentage_contract() -> None:
    sensor = BadRawHumiditySensor()                                                 # Creamos un sensor que devuelve un valor crudo en vez de un porcentaje

    # Verificamos que el consumidor rechace el valor fuera del contrato
    with pytest.raises(ValueError):
        read_percentage(sensor)


# Test LSP correcto
def test_good_lsp_allows_substitution() -> None:
    base_sensor = PercentageSensor()                                                # Creamos una instancia de la clase base
    humidity_sensor = HumidityPercentageSensor()                                    # Creamos una instancia de la clase hija correcta

    # Ambas clases pueden usarse mediante la misma función.
    base_value = read_percentage(base_sensor)
    humidity_value = read_percentage(humidity_sensor)

    # Verificamos que ambas devuelvan porcentajes válidos
    assert base_value == 50.0
    assert humidity_value == 50.0