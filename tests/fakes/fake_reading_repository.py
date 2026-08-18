from datetime import UTC, datetime

from app.models import Reading
from app.repositories.reading_repository import ReadingRepository


# Repositorio falso de lecturas
# Implementamos el contrato ReadingRepository utilizando una lista en memoria
# Esto nos permite probar ReadingService sin depender de SQLAlchemy o una base de datos real
class FakeReadingRepository(ReadingRepository):

    # Inicializamos el almacenamiento y los contadores utilizados por las pruebas
    def __init__(self) -> None:

        self._readings: list[Reading] = []
        self._next_id = 1

        # Registramos llamadas relevantes para comprobar que el servicio
        # detenga una operación antes de delegarla cuando corresponda
        self.list_for_sensor_calls = 0
        self.delete_calls = 0

    # Simulamos la creación y los valores que normalmente generaría la base de datos
    def create(self, reading: Reading) -> Reading:

        reading.id = self._next_id
        self._next_id += 1

        # Simulamos el timestamp generado por la persistencia utilizando UTC
        if reading.timestamp is None:
            reading.timestamp = datetime.now(UTC)

        self._readings.append(reading)

        return reading

    # Buscamos una lectura mediante su identificador interno
    def get_by_id(self, reading_id: int) -> Reading | None:

        for reading in self._readings:
            if reading.id == reading_id:
                return reading

        return None

    # Aplicamos en memoria los filtros y la paginación definidos por el contrato
    def list_for_sensor(
        self,
        sensor_id: int,
        *,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Reading]:

        self.list_for_sensor_calls += 1

        readings = [
            reading
            for reading in self._readings
            if reading.sensor_id == sensor_id
        ]

        if start_date is not None:
            readings = [
                reading
                for reading in readings
                if reading.timestamp >= start_date
            ]

        if end_date is not None:
            readings = [
                reading
                for reading in readings
                if reading.timestamp <= end_date
            ]

        # Conservamos el mismo criterio de orden utilizado por el repositorio SQLAlchemy
        readings.sort(
            key=lambda reading: (
                reading.timestamp,
                reading.id,
            )
        )

        return readings[offset : offset + limit]

    # Devolvemos la misma entidad porque las modificaciones ocurren sobre el objeto en memoria
    def update(self, reading: Reading) -> Reading:

        return reading

    # Eliminamos la entidad y registramos que la operación llegó al repositorio
    def delete(self, reading: Reading) -> None:

        self.delete_calls += 1
        self._readings.remove(reading)