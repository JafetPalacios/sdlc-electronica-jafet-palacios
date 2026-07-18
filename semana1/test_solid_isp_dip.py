import pytest

from semana1.solid_isp_dip import (
    AdvancedTemperatureSensor,
    BadBasicTemperatureSensor,
    BadDataProcessor,
    BasicTemperatureSensor,
    DataProcessor,
    JsonFileRepository,
    MemoryRepository,
    calibrate_sensor,
    connect_sensor,
    read_sensor,
)

#Test ISP incorrecto: El sensor puede leer, pero no puede calibrar ni conectarse. La interfaz exige más operaciones de las que el sensor necesita
def test_bad_isp_forces_unsupported_operations() -> None:
    sensor = BadBasicTemperatureSensor()                                                # Creamos el sensor básico con la interfaz demasiado grande
    assert sensor.read() == 23.5                                                        # Verificamos que la lectura sí funciona

    # Verificamos que la calibración no está realmente soportada
    with pytest.raises(NotImplementedError):
        sensor.calibrate()

    # Verificamos que la conexión tampoco está soportada
    with pytest.raises(NotImplementedError):
        sensor.connect()


#Test ISP correcto: El sensor básico solo puede leer, mientras que el sensor avanzado puede leer, calibrar y conectarse
def test_good_isp_uses_only_supported_interfaces() -> None:
    basic_sensor = BasicTemperatureSensor()                                             # Creamos un sensor básico que únicamente permite leer
    advanced_sensor = AdvancedTemperatureSensor()                                       # Creamos un sensor avanzado con capacidades adicionales

    assert read_sensor(basic_sensor) == 23.5                                            # El sensor básico puede utilizarse donde solo se requiere lectura
    assert read_sensor(advanced_sensor) == 24.0                                         # El sensor avanzado también puede utilizarse para leer

    # Solo usamos las capacidades avanzadas con el sensor que las soporta
    calibrate_sensor(advanced_sensor)
    connect_sensor(advanced_sensor)


#Test DIP incorrecto: El test siempre recibe un resultado JSON porque no podemos entregar otro repositorio desde fuera
def test_bad_dip_uses_concrete_repository() -> None:
    processor = BadDataProcessor()                                                      # Creamos el procesador que construye internamente su repositorio
    sensor = BasicTemperatureSensor()                                                   # Creamos un sensor básico
    result = processor.process(sensor)                                                  # Procesamos la lectura.
    assert result == '{"value": 23.5}'                                                  # Verificamos el resultado producido por JsonFileRepository


#Test DIP correcto: El test puede recibir cualquier tipo de repositorio, sin depender de la implementación concreta
def test_good_dip_accepts_injected_repositories() -> None:
    sensor = BasicTemperatureSensor()                                                   # Creamos un sensor que proporciona la lectura

    # Creamos un repositorio en memoria y lo inyectamos
    memory_repository = MemoryRepository()
    memory_processor = DataProcessor(memory_repository)
    memory_result = memory_processor.process(sensor)                                     # Procesamos la lectura usando el repositorio en memoria

    # Verificamos el resultado y el valor almacenado.
    assert memory_result == "Stored in memory: 23.5"
    assert memory_repository.values == [23.5]

    json_processor = DataProcessor(JsonFileRepository())                                # Creamos otro procesador con un repositorio distinto
    json_result = json_processor.process(sensor)                                        # Procesamos la misma lectura con la nueva dependencia
    assert json_result == '{"value": 23.5}'                                             # Verificamos que el mismo procesador funciona con otro repositorio

    # El mismo DataProcessor funciona con MemoryRepository() y con JsonFileRepository(). No modificamos esta clase, solo cambiamos el objeto que le entregamos al constructor
    # Eso es inyección de dependencias