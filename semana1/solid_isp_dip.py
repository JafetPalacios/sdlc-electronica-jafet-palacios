#==========[     ISP     ]==========
# Ejemplo incorrecto: La clase necesita implementar métodos que no forman parte de su comportamiento real
from typing import Protocol

class BadSensorInterface(Protocol):                                                 # Creamos un contrato que exige tres métodos
    def read(self) -> float:                                                        # Si lo necesitamos
        ...

    def calibrate(self) -> None:                                                    # No lo necesitamos
        ...

    def connect(self) -> None:                                                      # No lo necesitamos              
        ...


class BadBasicTemperatureSensor:                                                    # Representa un sensor sencillo que únicamente puede proporcionar una lectura
    def read(self) -> float:
        return 23.5                                                                 # Devolvemos una lectura simulada de temperatura

    def calibrate(self) -> None:
        raise NotImplementedError("Calibration is not supported")                   # Indicamos que este sensor básico no permite calibración

    def connect(self) -> None:
        raise NotImplementedError("Connection is not supported")                    # Indicamos que este sensor no requiere conexión
    

#Ejemplo correcto ISP: Separamos la interfaz grande en contratos pequeños
class ReadableSensor(Protocol):                                                     # Lee
    def read(self) -> float:
        ...


class CalibratableSensor(Protocol):                                                  # Calibra                                 
    def calibrate(self) -> None:
        ...


class ConnectableSensor(Protocol):                                                   # Conecta
    def connect(self) -> None:
        ...


class BasicTemperatureSensor:                                                       # Este sensor solo sabe leer
    def read(self) -> float:
        return 23.5                                                                 # Devolvemos una lectura simulada de temperatura


class AdvancedTemperatureSensor:                                                    # Este sensor sí ofrece las tres capacidades
    def read(self) -> float:
        return 24.0                                                                 # Devolvemos una lectura simulada de temperatura

    def calibrate(self) -> None:                                                    # Simulamos la calibración del sensor
        return None

    def connect(self) -> None:                                                      # Simulamos la conexión del sensor
        return None
    

def read_sensor(sensor: ReadableSensor) -> float:
    return sensor.read()                                                            # Dependemos únicamente de la capacidad de lectura


def calibrate_sensor(sensor: CalibratableSensor) -> None:
    sensor.calibrate()                                                              # Dependemos únicamente de la capacidad de calibración


def connect_sensor(sensor: ConnectableSensor) -> None:                              # Dependemos únicamente de la capacidad de conexión
    sensor.connect()


#==========[     DIP     ]==========
# El código de alto nivel no debe depender del código de bajo nivel, sino de abstracciones

#Ejemplo incorrecto: crea por sí mismo el repositorio que utilizará
class JsonFileRepository:
    def save(self, value: float) -> str:                                            # Recibe una lectura y devuelve una representación JSON simulada
        return f'{{"value": {value}}}'                                              # Simulamos el guardado de la lectura en formato JSON


class BadDataProcessor:                                                             # Lee un sensor y envía la lectura a un repositorio
    def __init__(self) -> None:
        self.repository = JsonFileRepository()                                      # Creamos directamente una dependencia concreta

    def process(self, sensor: ReadableSensor) -> str:
        value = sensor.read()                                                       # Obtenemos la lectura del sensor
        return self.repository.save(value)                                          # Guardamos la lectura usando el repositorio concreto
    
# BadDataProcessor crea directamente una implementación concreta
# Eso significa que queda unido obligatoriamente a JsonFileRepository
# Si después quisiéramos guardar en memoria, CSV o una base de datos, tendríamos que modificar BadDataProcessor
# Si después quisiéramos guardar en memoria, CSV o una base de datos, tendríamos que modificar BadDataProcessor

# Ejemplo correcto DIP: Ahora DataProcessor no creará internamente un repositorio concreto. Recibirá la dependencia desde fuera
class DataRepository(Protocol):                                                      # Este protocolo establece el contrato mínimo de almacenamiento: el repositorio debe tener un método save()
    def save(self, value: float) -> str:
        ...


class MemoryRepository:
    def __init__(self) -> None:                                                     # Creamos una lista vacía donde almacenaremos las lecturas                     
        self.values: list[float] = []                                               # Inicializamos una lista para conservar las lecturas

    def save(self, value: float) -> str:
        self.values.append(value)                                                   # Guardamos la lectura en memoria
        return f"Stored in memory: {value}"


class DataProcessor:                                                                # Lee un sensor y envía la lectura a un repositorio, pero ahora recibe el repositorio desde fuera
    def __init__(self, repository: DataRepository) -> None:
        self.repository = repository                                                # Recibimos el repositorio desde el exterior

    def process(self, sensor: ReadableSensor) -> str:
        value = sensor.read()                                                       # Obtenemos la lectura del sensor
        return self.repository.save(value)                                          # Delegamos el almacenamiento al repositorio inyectado.

