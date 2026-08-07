from datetime import datetime
from typing import Protocol

from app.models import Reading


# Contrato de persistencia para lecturas
class ReadingRepository(Protocol):

    # Operaciones de creación
    # Registramos nuevas lecturas y devolvemos el estado final generado por la implementación concreta del repositorio
    def create(self, reading: Reading) -> Reading:

        ...

    # Operaciones de consulta individual
    # Recuperamos una lectura mediante su identificador interno y devolvemos None cuando el registro solicitado no existe

    def get_by_id(self, reading_id: int) -> Reading | None:

        ...

    # Operaciones de consulta por sensor
    # Recuperamos lecturas pertenecientes a un sensor concreto yermitimos limitar el resultado por fechas y aplicar paginación
    def list_for_sensor(
        self,
        sensor_id: int,
        *,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Reading]:                             # Listamos lecturas de un sensor aplicando filtros y paginación

        ...

    # Operaciones de actualización
    # Persistimos los cambios realizados previamente sobre una entidad existente y devolvemos la lectura actualizada con su estado definitivo
    def update(self, reading: Reading) -> Reading:

        ...

    # Operaciones de eliminación
    # Eliminamos de forma definitiva una lectura previamente almacenada
    def delete(self, reading: Reading) -> None:

        ...