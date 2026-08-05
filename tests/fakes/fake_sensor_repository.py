from app.models import Sensor
from app.repositories.sensor_repository import SensorRepository


# Repositorio de sensores en memoria para pruebas
class FakeSensorRepository(SensorRepository):

    def __init__(self) -> None:
        
        self._sensors: list[Sensor] = []                # Almacenamos los sensores únicamente en memoria
        self._next_id = 1                               # Simulamos el autoincremento de la base de datos


    # Guarda un sensor en memoria
    def create(self, sensor: Sensor) -> Sensor:

        print("FakeRepository.create()")

        sensor.id = self._next_id                       # Simulamos el comportamiento de la base asignando un id
        self._next_id += 1
        self._sensors.append(sensor)

        return sensor

    # Busca un sensor por id
    def get_by_id(self, sensor_id: int) -> Sensor | None:
        

        for sensor in self._sensors:
            if sensor.id == sensor_id:
                return sensor

        return None


    # Busca un sensor por código
    def get_by_code(self, code: str) -> Sensor | None:

        for sensor in self._sensors:
            if sensor.code == code:
                return sensor

        return None

    # Devuelve todos los sensores
    def list(self) -> list[Sensor]:

        return list(self._sensors)


    # Actualiza un sensor existente
    def update(self, sensor: Sensor) -> Sensor:
       
        return sensor

    # Elimina un sensor
    def delete(self, sensor: Sensor) -> None:

        self._sensors.remove(sensor)