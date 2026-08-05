from app.models import Sensor
from app.repositories.sensor_repository import SensorRepository
from app.schemas import SensorCreate


# Contiene la lógica de negocio relacionada con los sensores
class SensorService:
   
    # Guardamos el repositorio sin importar cómo persista los datos
    def __init__(self, repository: SensorRepository) -> None:
        
        self._repository = repository

    # Crea un nuevo sensor validando que el código no exista
    def create_sensor(self, sensor_data: SensorCreate) -> Sensor:
        
        existing_sensor = self._repository.get_by_code(sensor_data.code)        # Verificamos si ya existe un sensor con el mismo código

        if existing_sensor is not None:
            raise ValueError("Ya existe un sensor con ese código")

        # Construimos el modelo de dominio a partir del schema recibido
        sensor = Sensor(
            code=sensor_data.code,
            name=sensor_data.name,
            sensor_type=sensor_data.sensor_type,
            unit=sensor_data.unit,
        )

        return self._repository.create(sensor)                                  # Delegamos la persistencia al repositorio

    
    # Obtiene todos los sensores registrados
    def list_sensors(self) -> list[Sensor]:
        
        return self._repository.list()                                          # Delegamos la consulta al repositorio