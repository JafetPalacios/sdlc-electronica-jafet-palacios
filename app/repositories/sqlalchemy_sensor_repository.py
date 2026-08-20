from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Sensor
from app.repositories.sensor_repository import SensorRepository


# Implementación concreta del repositorio de sensores
# Utilizamos SQLAlchemy para cumplir el contrato definido por SensorRepository
# y mantenemos aislada la lógica de acceso a la base de datos
class SqlAlchemySensorRepository(SensorRepository):

    # Recibimos la sesión de base de datos utilizada en la petición actual
    def __init__(self, db: Session) -> None:

        self._db = db                                                   # Conservamos la sesión para ejecutar consultas y transacciones

    # Operaciones de creación: Insertamos nuevos sensores y recuperamos los valores generados automáticamente por la base de datos
    def create(self, sensor: Sensor) -> Sensor:                         # Guardamos un sensor nuevo y devolvemos su estado persistido

        self._db.add(sensor)                                            # Añadimos la entidad a la sesión para preparar el INSERT
        self._db.commit()                                               # Confirmamos la transacción para guardar el registro
        self._db.refresh(sensor)                                        # Recargamos la entidad para obtener el id y la fecha generados

        return sensor

    # Operaciones de consulta individual: Recuperamos sensores por su identificador interno o por su código público
    def get_by_id(self, sensor_id: int) -> Sensor | None:               # Buscamos un sensor mediante su identificador interno

        return self._db.get(Sensor, sensor_id)                          # Utilizamos Session.get porque consultamos directamente la clave primaria

    def get_by_code(self, code: str) -> Sensor | None:                  # Buscamos un sensor mediante su código público único

        # Construimos una consulta filtrada por el código del sensor
        statement = select(Sensor).where(
            Sensor.code == code,
        )

        return self._db.scalars(statement).one_or_none()                # Esperamos como máximo un resultado porque el código es único

    # Operaciones de consulta paginada: Recuperamos una colección limitada de sensores
    def list(
        self,
        *,
        limit: int = 50,                                                # limit controla la cantidad máxima de resultados
        offset: int = 0,                                                # offset indica cuántos registros omitimos desde el inicio
    ) -> list[Sensor]:                                                  # Listamos sensores aplicando paginación


        # Ordenamos por identificador para obtener resultados consistente y después aplicamos el límite y el desplazamiento solicitados
        statement = (
            select(Sensor)
            .order_by(Sensor.id)
            .limit(limit)
            .offset(offset)
        )

        return list(self._db.scalars(statement).all())                  # Ejecutamos la consulta y convertimos el resultado en una lista

    # Operaciones de actualización: Confirmamos los cambios realizados previamente sobre una entidad administrada por la sesión actual
    def update(self, sensor: Sensor) -> Sensor:                         # Persistimos los cambios de un sensor existente

        self._db.commit()                                               # Confirmamos los cambios pendientes sobre la entidad
        self._db.refresh(sensor)                                        # Sincronizamos la instancia con los valores almacenados

        return sensor
