import pytest

from app.schemas import SensorCreate
from app.services.sensor_service import SensorService
from tests.fakes.fake_sensor_repository import FakeSensorRepository


# Verifica que el servicio crea correctamente un sensor
def test_create_sensor_success() -> None:

    repository = FakeSensorRepository()                     # Creamos un repositorio en memoria
    service = SensorService(repository)                     # Creamos el servicio utilizando el repositorio fake

    # Definimos los datos de entrada
    sensor = SensorCreate(
        code="TEMP-001",
        name="Sensor de temperatura",
        sensor_type="temperature",
        unit="°C",
    )

    created_sensor = service.create_sensor(sensor)          # Ejecutamos la operación

    # Verificamos que el sensor fue creado correctamente
    assert created_sensor.id == 1
    assert created_sensor.code == "TEMP-001"
    assert created_sensor.name == "Sensor de temperatura"

    assert len(repository.list()) == 1                      # Confirmamos que el repositorio contiene un único sensor


# Verifica que no sea posible crear dos sensores con el mismo código
def test_create_sensor_duplicate_code() -> None:
    
    # Creamos el repositorio y el servicio
    repository = FakeSensorRepository()
    service = SensorService(repository)

    # Registramos el primer sensor
    service.create_sensor(
        SensorCreate(
            code="TEMP-001",
            name="Sensor 1",
            sensor_type="temperature",
            unit="°C",
        )
    )

    # Intentamos registrar otro sensor con el mismo código
    with pytest.raises(ValueError):
        service.create_sensor(
            SensorCreate(
                code="TEMP-001",
                name="Sensor 2",
                sensor_type="temperature",
                unit="°C",
            )
        )


# Verifica que el servicio liste los sensores registrados
def test_list_sensors() -> None:
    
    repository = FakeSensorRepository()
    service = SensorService(repository)

    service.create_sensor(
        SensorCreate(
            code="TEMP-001",
            name="Sensor 1",
            sensor_type="temperature",
            unit="°C",
        )
    )

    service.create_sensor(
        SensorCreate(
            code="TEMP-002",
            name="Sensor 2",
            sensor_type="temperature",
            unit="°C",
        )
    )

    sensors = service.list_sensors()

    assert len(sensors) == 2
    assert sensors[0].code == "TEMP-001"
    assert sensors[1].code == "TEMP-002"