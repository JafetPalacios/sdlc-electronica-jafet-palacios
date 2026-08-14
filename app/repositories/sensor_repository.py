from typing import Protocol

from app.models import Sensor


# Contrato de persistencia para sensores
# Definimos las operaciones que cualquier repositorio de sensores debe implementar
# Mantenemos este contrato estable aunque cambie la base de datos
# Esto permite que los servicios dependan de una interfaz y no de SQLAlchemy
class SensorRepository(Protocol):

    # Operaciones de creación: Registramos un sensor nuevo y devolvemos su estado persistido
    def create(self, sensor: Sensor) -> Sensor:

        ...

    # Operaciones de consulta individual: Buscamos sensores mediante su identificador interno o su código público
    def get_by_id(self, sensor_id: int) -> Sensor | None:               # Identificador interno

        ...

    def get_by_code(self, code: str) -> Sensor | None:                  # Código público

        ...

    # Operaciones de consulta paginada: Recuperamos una colección limitada de sensores
    def list(
        self,
        *,
        limit: int = 50,                                                # limit controla la cantidad máxima de resultados
        offset: int = 0,                                                # offset indica cuántos registros omitimos desde el inicio
    ) -> list[Sensor]:

        ...

    # Operaciones de actualización: Persistimos los cambios realizados previamente sobre un sensor existente y devolvemos el sensor con su estado definitivo después de guardarlo
    def update(self, sensor: Sensor) -> Sensor:

        ...

    # Operaciones de eliminación: Eliminamos de forma definitiva un sensor almacenado
    def delete(self, sensor: Sensor) -> None:

        ...