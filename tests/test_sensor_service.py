import pytest

from app.exceptions import SensorCodeConflictError
from app.schemas import SensorCreate, SensorUpdate
from app.services.sensor_service import SensorService
from tests.fakes.fake_sensor_repository import FakeSensorRepository

# Pruebas unitarias del servicio de sensores
# Utilizamos FakeSensorRepository para evaluar la lógica de negocio sin depender de SQLite, SQLAlchemy o una base de datos externa

# Creación exitosa
def test_create_sensor_success() -> None:                                   # Verificamos que el servicio construya y almacene correctamente un sensor cuando el código público todavía no está registrado

    repository = FakeSensorRepository()                                     # Preparamos un repositorio aislado para esta prueba
    service = SensorService(repository)                                     # Construimos el servicio inyectando el repositorio en memoria

    sensor_data = SensorCreate(                                             # Definimos los datos de entrada que normalmente recibiríamos desde la API
        code="TEMP-001",
        name="Sensor de temperatura",
        location="Laboratorio de electrónica",
        sensor_type="temperature",
        unit="°C",
    )

    created_sensor = service.create_sensor(sensor_data)                     # Ejecutamos la operación de creación mediante la capa de servicio

    assert created_sensor.id == 1                                           # Comprobamos que el repositorio haya simulado el id autoincremental

    # Verificamos que los datos principales se conservaron correctamente
    assert created_sensor.code == "TEMP-001"
    assert created_sensor.name == "Sensor de temperatura"
    assert created_sensor.sensor_type == "temperature"
    assert created_sensor.unit == "°C"

    stored_sensors = repository.list()                                      # Confirmamos que el sensor quedó almacenado en el repositorio

    assert len(stored_sensors) == 1
    assert stored_sensors[0] is created_sensor


# Código duplicado
def test_create_sensor_duplicate_code() -> None:                            # Verificamos que el servicio rechace la creación de un segundo sensor cuando otro registro ya utiliza el mismo código público

    repository = FakeSensorRepository()                                     # Preparamos un repositorio aislado y el servicio bajo prueba
    service = SensorService(repository)

    service.create_sensor(                                                  # Registramos el primer sensor que ocupará el código TEMP-001
        SensorCreate(
            code="TEMP-001",
            name="Sensor 1",
            location="Laboratorio de electrónica",
            sensor_type="temperature",
            unit="°C",
        )
    )

    # Intentamos registrar otro sensor con el mismo código
    with pytest.raises(                                                     # Esperamos una excepción de dominio y comprobamos su mensaje
        SensorCodeConflictError,
        match="Ya existe un sensor con el código TEMP-001",
    ):
        service.create_sensor(
            SensorCreate(
                code="TEMP-001",
                name="Sensor 2",
                location="Laboratorio de electrónica",
                sensor_type="temperature",
                unit="°C",
            )
        )

    stored_sensors = repository.list()                                      # Confirmamos que el intento fallido no agregó un segundo sensor

    assert len(stored_sensors) == 1
    assert stored_sensors[0].name == "Sensor 1"


# Listado de sensores
def test_list_sensors() -> None:                                        # Verificamos que el servicio devuelva los sensores registrados respetando el orden conservado por el repositorio falso

    repository = FakeSensorRepository()                                 # Preparamos un repositorio aislado y el servicio bajo prueba
    service = SensorService(repository)

    # Registramos el primer sensor
    service.create_sensor(
        SensorCreate(
            code="TEMP-001",
            name="Sensor 1",
            location="Laboratorio de electrónica",
            sensor_type="temperature",
            unit="°C",
        )
    )

    # Registramos el segundo sensor
    service.create_sensor(
        SensorCreate(
            code="TEMP-002",
            name="Sensor 2",
            location="Laboratorio de electrónica",
            sensor_type="temperature",
            unit="°C",
        )
    )

    sensors = service.list_sensors()                                            # Solicitamos al servicio la colección completa

    assert len(sensors) == 2                                                    # Confirmamos la cantidad de sensores devueltos

    # Verificamos que el orden y los códigos sean los esperados
    assert sensors[0].code == "TEMP-001"
    assert sensors[1].code == "TEMP-002"

# Creación de sensor con umbral de alerta
def test_create_sensor_with_alert_threshold() -> None:
    # Preparamos un repositorio aislado y el servicio bajo prueba
    repository = FakeSensorRepository()
    service = SensorService(repository)

    # Solicitamos la creación de un sensor con un umbral de alerta configurable
    sensor_data = SensorCreate(
        code="TEMP-ALERT-001",
        name="Sensor de temperatura con alerta",
        location="Laboratorio de electrónica",
        sensor_type="temperature",
        unit="°C",
        alert_threshold=30.0,
    )

    created_sensor = service.create_sensor(sensor_data)

    # Confirmamos que el umbral forme parte del estado del sensor creado
    assert created_sensor.alert_threshold == 30.0

# Actualización del umbral de alerta
def test_update_sensor_alert_threshold() -> None:
    # Preparamos un sensor existente con un umbral inicial
    repository = FakeSensorRepository()
    service = SensorService(repository)

    sensor = service.create_sensor(
        SensorCreate(
            code="TEMP-ALERT-002",
            name="Sensor de temperatura",
            location="Laboratorio de electrónica",
            sensor_type="temperature",
            unit="°C",
            alert_threshold=30.0,
        )
    )

    # Solicitamos modificar únicamente el umbral configurado
    updated_sensor = service.update_sensor(
        sensor.id,
        SensorUpdate(
            alert_threshold=35.0,
        ),
    )

    assert updated_sensor.alert_threshold == 35.0


# Creación de sensor con ubicación
def test_create_sensor_with_location() -> None:
    # Preparar un repositorio aislado y el servicio bajo prueba
    repository = FakeSensorRepository()
    service = SensorService(repository)

    # Solicitar la creación de un sensor indicando su ubicación física
    sensor_data = SensorCreate(
        code="TEMP-LOCATION-001",
        name="Sensor de temperatura",
        location="Laboratorio de electrónica",
        sensor_type="temperature",
        unit="°C",
    )

    created_sensor = service.create_sensor(sensor_data)

    # Verificar que la ubicación forme parte del estado persistido del sensor
    assert created_sensor.location == "Laboratorio de electrónica"

# Creación de sensor activo por defecto
def test_create_sensor_is_active_by_default() -> None:
    # Preparar un repositorio aislado y el servicio bajo prueba
    repository = FakeSensorRepository()
    service = SensorService(repository)

    # Crear un sensor sin indicar explícitamente su estado
    sensor_data = SensorCreate(
        code="TEMP-ACTIVE-001",
        name="Sensor de temperatura",
        location="Laboratorio de electrónica",
        sensor_type="temperature",
        unit="°C",
    )

    created_sensor = service.create_sensor(sensor_data)

    # Verificar que todo sensor nuevo comience habilitado para operar
    assert created_sensor.is_active is True

# Desactivación de sensor
def test_update_sensor_can_deactivate_sensor() -> None:
    # Preparar un repositorio aislado y el servicio bajo prueba
    repository = FakeSensorRepository()
    service = SensorService(repository)

    # Crear un sensor activo que posteriormente será deshabilitado
    sensor = service.create_sensor(
        SensorCreate(
            code="TEMP-DEACTIVATE-001",
            name="Sensor de temperatura",
            location="Laboratorio de electrónica",
            sensor_type="temperature",
            unit="°C",
        )
    )

    assert sensor.is_active is True

    # Solicitar únicamente el cambio de estado operativo
    updated_sensor = service.update_sensor(
        sensor.id,
        SensorUpdate(
            is_active=False,
        ),
    )

    # Verificar que el sensor permanezca almacenado pero quede inactivo
    assert updated_sensor.is_active is False

    persisted_sensor = repository.get_by_id(sensor.id)

    assert persisted_sensor is not None
    assert persisted_sensor.is_active is False

# Actualización de la ubicación del sensor
def test_update_sensor_location() -> None:
    # Preparar un sensor existente con una ubicación inicial
    repository = FakeSensorRepository()
    service = SensorService(repository)

    sensor = service.create_sensor(
        SensorCreate(
            code="TEMP-LOCATION-UPDATE-001",
            name="Sensor de temperatura",
            location="Laboratorio de electrónica",
            sensor_type="temperature",
            unit="°C",
        )
    )

    # Solicitar únicamente el cambio de ubicación física
    updated_sensor = service.update_sensor(
        sensor.id,
        SensorUpdate(
            location="Laboratorio de instrumentación",
        ),
    )

    # Verificar que la nueva ubicación quede conservada
    assert updated_sensor.location == "Laboratorio de instrumentación"