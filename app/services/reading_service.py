from datetime import datetime

from app.domain.alert_lifecycle import AlertStatus
from app.domain.alert_strategy import AlertStrategy
from app.domain.reading_statistics import ReadingStatistics
from app.domain.sensor_rules import SENSOR_RULES
from app.exceptions import (
    InvalidDateRangeError,
    InvalidDateTimezoneError,
    InvalidPaginationError,
    ReadingNotFoundError,
    ReadingValueOutOfRangeError,
    SensorInactiveError,
    SensorNotFoundError,
)
from app.models import Alert, Reading
from app.repositories.alert_repository import AlertRepository
from app.repositories.reading_repository import ReadingRepository
from app.repositories.sensor_repository import SensorRepository
from app.schemas import ReadingCreate, ReadingUpdate


# Servicio de aplicación para lecturas
# Concentramos aquí las reglas de negocio relacionadas con las lecturas
# Coordinamos los repositorios sin depender directamente de FastAPI o SQLAlchemy
# Esto permite reutilizar y probar la lógica de negocio de forma independiente
class ReadingService:

    # Inicialización del servicio
    def __init__(
        self,
        reading_repository: ReadingRepository,
        sensor_repository: SensorRepository,
        *,
        alert_repository: AlertRepository | None = None,
        alert_strategy: AlertStrategy | None = None,
    ) -> None:

        # Conservamos los repositorios utilizados por las operaciones de lecturas
        self._reading_repository = reading_repository
        self._sensor_repository = sensor_repository

        # Conservamos colaboradores opcionales para detectar y registrar anomalías
        self._alert_repository = alert_repository
        self._alert_strategy = alert_strategy

    # Validación de valores físicos
    def _validate_reading_value(                                                # Comprobamos que cada lectura respete el intervalo definido para el tipo del sensor propietario
        self,
        sensor_type: str,
        value: float,
    ) -> None:

        rule = SENSOR_RULES.get(sensor_type)                                    # Recuperamos la regla física asociada al tipo del sensor

        if rule is None:                                                        # El tipo ya fue validado al crear el sensor
            return                                                              # Este control evita un error inesperado si existen datos antiguos

        if value < rule.minimum_value or value > rule.maximum_value:            # Rechazamos valores inferiores o superiores al intervalo permitido
            raise ReadingValueOutOfRangeError(
                sensor_type=sensor_type,
                value=value,
                minimum_value=rule.minimum_value,
                maximum_value=rule.maximum_value,
            )

    # Validación reutilizable de rangos temporales
    def _validate_date_range_filters(
        self,
        *,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> None:

        if start_date is not None and end_date is not None:
            start_is_aware = start_date.utcoffset() is not None
            end_is_aware = end_date.utcoffset() is not None

            if start_is_aware != end_is_aware:
                raise InvalidDateTimezoneError()

            if start_date > end_date:
                raise InvalidDateRangeError()

    # Recuperación reutilizable del sensor propietario
    def _get_sensor_or_raise(
        self,
        sensor_id: int,
    ) -> object:

        sensor = self._sensor_repository.get_by_id(sensor_id)

        if sensor is None:
            raise SensorNotFoundError(sensor_id)

        return sensor


    # Creación de lecturas
    def create_reading(
        self,
        sensor_id: int,
        reading_data: ReadingCreate,
    ) -> Reading:

        sensor = self._sensor_repository.get_by_id(sensor_id)                   # Consultar el sensor indicado antes de construir la lectura

        if sensor is None:                                                      # Interrumpir la operación cuando el sensor propietario no existe
            raise SensorNotFoundError(sensor_id)

        # Rechazar nuevas lecturas cuando el sensor fue desactivado
        if sensor.is_active is False:
            raise SensorInactiveError(sensor_id)

        self._validate_reading_value(                                           # Validar el valor usando la regla asociada al tipo del sensor
            sensor_type=sensor.sensor_type,
            value=reading_data.value,
        )

        reading = Reading(
            sensor_id=sensor_id,
            value=reading_data.value,
        )

        # Persistir primero la lectura para disponer de su identificador definitivo
        created_reading = self._reading_repository.create(reading)

        severity = None

        # Clasificamos la lectura cuando el sensor tenga un umbral configurado
        if (
            sensor.alert_threshold is not None
            and self._alert_strategy is not None
        ):
            severity = self._alert_strategy.classify(
                value=created_reading.value,
                threshold=sensor.alert_threshold,
            )

        if (
            severity is not None
            and self._alert_repository is not None
        ):
            alert = Alert(
                sensor_id=sensor_id,
                reading_id=created_reading.id,
                value=created_reading.value,
                threshold=sensor.alert_threshold,
                severity=severity,
                status=AlertStatus.OPEN,
            )

            self._alert_repository.create(alert)

        return created_reading

    # Consulta individual
    def get_reading(self, reading_id: int) -> Reading:                          # Recuperamos una lectura concreta mediante su identificador interno

        reading = self._reading_repository.get_by_id(reading_id)                # Consultamos el repositorio sin exponer detalles de persistencia

        if reading is None:                                                     # Informamos de forma explícita cuando la lectura no existe
            raise ReadingNotFoundError(reading_id)

        return reading

    # Consulta paginada por sensor
    def list_readings_for_sensor(                                               # Recuperamos lecturas pertenecientes a un sensor concreto
        self,
        sensor_id: int,
        *,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 50,                                                         # Permitimos aplicar un rango temporal y paginar los resultados
        offset: int = 0,
    ) -> list[Reading]:

        # Protegemos las invariantes de paginación también cuando el servicio
        # se utiliza directamente sin pasar por las validaciones de FastAPI
        if limit < 1 or limit > 100 or offset < 0:
            raise InvalidPaginationError()

        self._validate_date_range_filters(
            start_date=start_date,
            end_date=end_date,
        )

        self._get_sensor_or_raise(sensor_id)                                    # Comprobamos que el sensor solicitado exista aunque no tenga lecturas


        return self._reading_repository.list_for_sensor(                        # Delegamos al repositorio los filtros, el orden y la paginación
            sensor_id,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset,
        )

    # Estadísticas agregadas por sensor
    def get_statistics_for_sensor(
        self,
        sensor_id: int,
        *,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> ReadingStatistics:

        self._validate_date_range_filters(
            start_date=start_date,
            end_date=end_date,
        )

        self._get_sensor_or_raise(sensor_id)

        return self._reading_repository.get_statistics_for_sensor(
            sensor_id,
            start_date=start_date,
            end_date=end_date,
        )

    # Actualización de lecturas
    def update_reading(                                                         # Modificamos únicamente los campos enviados explícitamente por el cliente
        self,                                                                   # Conservamos sin cambios cualquier campo omitido en la petición PATCH
        reading_id: int,
        reading_data: ReadingUpdate,
    ) -> Reading:

        reading = self._reading_repository.get_by_id(reading_id)                # Recuperamos la entidad antes de intentar modificarla

        if reading is None:                                                     # Detenemos la operación cuando el identificador no corresponde a una lectura
            raise ReadingNotFoundError(reading_id)


        update_data = reading_data.model_dump(                                  # Extraemos solamente los campos recibidos en la petición
            exclude_unset=True,                                                 # exclude_unset evita sobrescribir valores que el cliente no envió
        )

        new_value = update_data.get("value")                                    # Validamos el nuevo valor cuando forma parte de la actualización

        if new_value is not None:
            sensor = self._sensor_repository.get_by_id(                         # Recuperamos el sensor propietario para conocer su regla física
                reading.sensor_id,
            )

            if sensor is None:                                                  # Protegemos el servicio ante datos inconsistentes en la base
                raise SensorNotFoundError(reading.sensor_id)


            self._validate_reading_value(                                       # Validamos el nuevo valor antes de modificar la entidad
                sensor_type=sensor.sensor_type,
                value=new_value,
            )

        for field_name, field_value in update_data.items():                     # Aplicamos dinámicamente cada modificación permitida por el esquema
            setattr(
                reading,
                field_name,
                field_value,
            )

        return self._reading_repository.update(reading)                         # Delegamos la confirmación de cambios y la recarga al repositorio

    # Eliminación de lecturas
    def delete_reading(self, reading_id: int) -> None:                          # Eliminamos una lectura concreta después de comprobar que exista

        reading = self._reading_repository.get_by_id(reading_id)                # Recuperamos la lectura antes de solicitar su eliminación

        if reading is None:                                                     # Evitamos ejecutar una eliminación sobre un registro inexistente
            raise ReadingNotFoundError(reading_id)

        self._reading_repository.delete(reading)                                # Delegamos la eliminación definitiva y el commit al repositorio
