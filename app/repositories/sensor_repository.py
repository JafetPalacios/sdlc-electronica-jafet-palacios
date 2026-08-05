# Este código es el contrato: Todo reposotorio debe i mplementar estas operaciones
# Si la base de datos llega a cambiar, esto no cambiará, porque el contrato se mantiene
from typing import Protocol

from app.models import Sensor


#Define las operaciones de persistencia disponibles para sensores
class SensorRepository(Protocol):

    def create(self, sensor: Sensor) -> Sensor:                 # Guarda un nuevo sensor
        
        ...

    def get_by_id(self, sensor_id: int) -> Sensor | None:       # Busca un sensor por su identificador interno

        ...

    def get_by_code(self, code: str) -> Sensor | None:          # Busca un sensor por su código público

        ...

    def list(self) -> list[Sensor]:                             # Devuelve todos los sensores almacenados

        ...

    def update(self, sensor: Sensor) -> Sensor:                 # Persiste los cambios realizados sobre un sensor

        ...

    def delete(self, sensor: Sensor) -> None:                   # Elimina un sensor almacenado

        ...