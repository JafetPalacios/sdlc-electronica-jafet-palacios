from app.models import Sensor
from app.repositories.sensor_repository import SensorRepository


# Repositorio falso de sensores
# Implementamos el contrato SensorRepository utilizando una lista en memoria
# Esta clase permite probar SensorService sin conectarnos a una base de datos real
# Cada prueba puede crear una instancia nueva y trabajar con datos aislados
class FakeSensorRepository(SensorRepository):                                             # Simulamos la persistencia de sensores completamente en memoria

    # Inicialización del repositorio
    def __init__(self) -> None:                                                           # Preparamos la colección interna y el contador utilizado para generar ids

        self._sensors: list[Sensor] = []                                                  # Conservamos los sensores creados durante la ejecución de la prueba
        self._next_id = 1                                                                 # Simulamos el comportamiento autoincremental de una base de datos

    # Creación de sensores
    def create(self, sensor: Sensor) -> Sensor:                                           # Asignamos un identificador y almacenamos el sensor dentro de la lista

        sensor.id = self._next_id                                                         # Asignamos el siguiente identificador disponible
        self._next_id += 1                                                                # Incrementamos el contador para la siguiente creación
        self._sensors.append(sensor)                                                      # Añadimos el sensor a la colección que representa la persistencia

        return sensor

    # Consulta individual por identificador
    def get_by_id(self, sensor_id: int) -> Sensor | None:                                 # Recorremos la colección hasta localizar un sensor con el id solicitado

        for sensor in self._sensors:                                                      # Comparamos el identificador solicitado con cada sensor almacenado
            if sensor.id == sensor_id:
                return sensor

        return None                                                                       # Devolvemos None cuando no existe una coincidencia

    # Consulta individual por código
    def get_by_code(self, code: str) -> Sensor | None:                                    # Buscamos un sensor utilizando el código público que debe ser único

        for sensor in self._sensors:                                                      # Comparamos el código solicitado con cada sensor almacenado
            if sensor.code == code:
                return sensor

        return None                                                                       # Devolvemos None cuando el código no está registrado

    # Consulta paginada
    def list(                                                                             # Devolvemos únicamente la sección solicitada de la colección interna
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Sensor]:

        end_position = offset + limit                                                     # Calculamos la posición final a partir del desplazamiento y el límite

        return list(                                                                      # Creamos una nueva lista para evitar exponer directamente la colección interna
            self._sensors[offset:end_position]
        )

    # Actualización de sensores
    def update(self, sensor: Sensor) -> Sensor:                                             # Los sensores almacenados son los mismos objetos utilizados por el servicio por ello los cambios ya están reflejados en memoria cuando llegamos aquí

        return sensor

    # Eliminación de sensores
    def delete(self, sensor: Sensor) -> None:                                               # Retiramos de la colección la misma instancia que recibió el servicio

        self._sensors.remove(sensor)                                                        # Quitamos el sensor de la colección utilizada por las pruebas