from app.domain.sensor_rules import SENSOR_RULES
from app.exceptions import (
    InvalidSensorUnitError,
    SensorCodeConflictError,
    SensorNotFoundError,
    UnsupportedSensorTypeError,
)
from app.models import Sensor
from app.repositories.sensor_repository import SensorRepository
from app.schemas import SensorCreate, SensorUpdate


# Servicio de aplicación para sensores
# Concentramos aquí las reglas de negocio relacionadas con los sensores
# Coordinamos el repositorio sin depender directamente de FastAPI o SQLAlchemy
# Esto permite reutilizar y probar la lógica de negocio de forma independiente
class SensorService:
    # Inicialización del servicio
    def __init__(self, repository: SensorRepository) -> None:                                           # Recibimos el repositorio mediante el constructor

        self._repository = repository                                                                   # Conservamos el contrato del repositorio sin conocer cómo persiste los datos


    # Validación de reglas físicas
    def _validate_sensor_rule(                                                                          # Comprobamos que el tipo de sensor exista dentro del catálogo y que la unidad enviada corresponda con la unidad definida
        self,
        sensor_type: str,
        unit: str,
    ) -> None:

        rule = SENSOR_RULES.get(sensor_type)                                                            # Buscamos la configuración asociada al tipo recibido

        if rule is None:                                                                                # Rechazamos tipos que no forman parte del catálogo
            raise UnsupportedSensorTypeError(sensor_type)

        if unit != rule.unit:                                                                           # Rechazamos unidades incompatibles con el tipo seleccionado
            raise InvalidSensorUnitError(
                sensor_type=sensor_type,
                received_unit=unit,
                expected_unit=rule.unit,
            )


    # Creación de sensores
    def create_sensor(self, sensor_data: SensorCreate) -> Sensor:                                       # Registramos sensores nuevos únicamente cuando su código público está disponible

        self._validate_sensor_rule(                                                                     # Validamos que el tipo y la unidad pertenezcan al catálogo físico
            sensor_type=sensor_data.sensor_type,
            unit=sensor_data.unit,
        )

        existing_sensor = self._repository.get_by_code(                                                 # Consultamos si ya existe un sensor con el código recibido
            sensor_data.code,
        )

        if existing_sensor is not None:                                                                 # Interrumpimos la operación cuando el código ya está registrado
            raise SensorCodeConflictError(sensor_data.code)

        sensor = Sensor(                                      # Construir la entidad con los datos validados antes de persistirla
            code=sensor_data.code,
            name=sensor_data.name,
            location=sensor_data.location,
            sensor_type=sensor_data.sensor_type,
            unit=sensor_data.unit,
            alert_threshold=sensor_data.alert_threshold,
            is_active=True,
        )
        return self._repository.create(sensor)                                                          # Delegamos la inserción y recuperación del estado final al repositorio

    # Consulta paginada
    def list_sensors(                                                                                   # Recuperamos una colección limitada de sensores
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Sensor]:

        return self._repository.list(                                                                   # Enviamos al repositorio el límite y el desplazamiento solicitados
            limit=limit,
            offset=offset,
        )

    # Consulta individual
    def get_sensor(self, sensor_id: int) -> Sensor:                                                     # Recuperamos un sensor concreto mediante su identificador interno
                                                                                                        # Transformamos la ausencia del registro en una excepción de dominio

        sensor = self._repository.get_by_id(sensor_id)                                                  # Consultamos el repositorio sin depender de detalles HTTP

        if sensor is None:                                                                              # Informamos de forma explícita cuando el sensor no existe
            raise SensorNotFoundError(sensor_id)

        return sensor

    # Actualización de sensores
    def update_sensor(                                                                                  # Modificamos únicamente los campos enviados explícitamente por el cliente
        self,                                                                                           # Conservamos sin cambios cualquier campo omitido en la petición PATCH
        sensor_id: int,
        sensor_data: SensorUpdate,
    ) -> Sensor:

        sensor = self._repository.get_by_id(sensor_id)                                                  # Recuperamos la entidad antes de intentar modificarla

        if sensor is None:                                                                              # Detenemos la operación cuando el identificador no corresponde a un sensor
            raise SensorNotFoundError(sensor_id)

        update_data = sensor_data.model_dump(                                                           # Extraemos únicamente los campos incluidos en la petición
            exclude_unset=True,                                                                         # exclude_unset evita sobrescribir valores que el cliente no envió
        )

        # Construimos la combinación final que tendría el sensor
        final_sensor_type = update_data.get(                                                            # Usamos los valores actuales cuando el cliente no envía un cambio
            "sensor_type",
            sensor.sensor_type,
        )
        final_unit = update_data.get(
            "unit",
            sensor.unit,
        )

        # Validamos la combinación final antes de modificar la entidad
        self._validate_sensor_rule(
            sensor_type=final_sensor_type,
            unit=final_unit,
        )

        new_code = update_data.get("code")                                                              # Obtenemos el nuevo código cuando forma parte de la actualización

        if new_code is not None and new_code != sensor.code:                                            # Validamos la unicidad únicamente cuando el código realmente cambia
            existing_sensor = self._repository.get_by_code(new_code)

            if existing_sensor is not None:                                                             # Impedimos asignar un código que ya pertenece a otro sensor
                raise SensorCodeConflictError(new_code)

        for field_name, field_value in update_data.items():                                             # Aplicamos dinámicamente cada modificación permitida por el esquema
            setattr(
                sensor,
                field_name,
                field_value,
            )

        return self._repository.update(sensor)                                                          # Delegamos la confirmación de cambios y la recarga al repositorio
