from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domain.reading_statistics import ReadingStatistics
from app.models import Reading
from app.repositories.reading_repository import ReadingRepository


# Implementación concreta del repositorio de lecturas
# Utilizamos SQLAlchemy para ejecutar las operaciones definidas en
# ReadingRepository y mantener aislada la lógica de persistencia
class SqlAlchemyReadingRepository(ReadingRepository):

    # Recibimos la sesión de base de datos utilizada en la petición actual
    def __init__(self, db: Session) -> None:

        self._db = db                                   # Conservamos la sesión para ejecutar consultas y transacciones

    # Operaciones de creación: Insertamos nuevas lecturas y recuperamos los valores generados automáticamente por la base de datos
    def create(self, reading: Reading) -> Reading:

        self._db.add(reading)                           # Añadimos la entidad a la sesión para preparar el INSERT
        self._db.commit()                               # Confirmamos la transacción para guardar el registro
        self._db.refresh(reading)                       # Recargamos la entidad para obtener el id y timestamp generados

        return reading

    # Operaciones de consulta individua: Buscamos una lectura mediante su identificador interno

    def get_by_id(self, reading_id: int) -> Reading | None:

        return self._db.get(Reading, reading_id)       # Utilizamos Session.get porque consultamos directamente la clave primaria

    # Operaciones de consulta por sensor: Recuperamos las lecturas pertenecientes a un sensor y permitimos aplicar filtros temporales y paginación sobre el resultado
    def list_for_sensor(
        self,
        sensor_id: int,
        *,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Reading]:                                 # Listamos lecturas de un sensor con filtros y paginación

        statement = select(Reading).where(              # Construimos la consulta base utilizando el sensor propietario
            Reading.sensor_id == sensor_id,
        )

        # Aplicamos el límite inferior del rango temporal cuando fue solicitado
        if start_date is not None:
            statement = statement.where(
                Reading.timestamp >= start_date,
            )

        # Aplicamos el límite superior del rango temporal cuando fue solicitado
        if end_date is not None:
            statement = statement.where(
                Reading.timestamp <= end_date,
            )

        # Ordenamos antes de paginar para obtener resultados consistentes y utilizamos el id como segundo criterio cuando dos lecturas comparten fecha
        statement = (
            statement.order_by(
                Reading.timestamp,
                Reading.id,
            )
            .limit(limit)
            .offset(offset)
        )

        return list(self._db.scalars(statement).all())              # Ejecutamos la consulta y convertimos el resultado en una lista

    # Operaciones de agregación por sensor: Calculamos estadísticas dentro de un rango temporal opcional
    def get_statistics_for_sensor(
        self,
        sensor_id: int,
        *,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> ReadingStatistics:

        statement = select(
            func.count(Reading.id),
            func.min(Reading.value),
            func.max(Reading.value),
            func.avg(Reading.value),
        ).where(
            Reading.sensor_id == sensor_id,
        )

        if start_date is not None:
            statement = statement.where(
                Reading.timestamp >= start_date,
            )

        if end_date is not None:
            statement = statement.where(
                Reading.timestamp <= end_date,
            )

        count, minimum_value, maximum_value, average_value = self._db.execute(
            statement,
        ).one()

        return ReadingStatistics(
            sensor_id=sensor_id,
            count=int(count),
            minimum_value=float(minimum_value) if minimum_value is not None else None,
            maximum_value=float(maximum_value) if maximum_value is not None else None,
            average_value=float(average_value) if average_value is not None else None,
        )

    # Operaciones de actualización: Confirmamos los cambios realizados previamente sobre una entidad administrada por la sesión actual
    def update(self, reading: Reading) -> Reading:

        self._db.commit()                                           # Confirmamos los cambios pendientes sobre la entidad
        self._db.refresh(reading)                                   # Sincronizamos la instancia con los valores almacenados

        return reading

    # Operaciones de eliminación: Eliminamos una lectura existente y confirmamos la transacción
    def delete(self, reading: Reading) -> None:

        self._db.delete(reading)                                    # Marcamos la entidad para su eliminación
        self._db.commit()                                           # Confirmamos la transacción para ejecutar el DELETE
