from typing import Protocol

#==========[     SRP     ]==========
# Ejemplo incorrecto: una clase que lee un sensor y además guarda la lectura. Son dos responsabilidades distintas
class BadTemperatureSensor:
    def read_and_save(self) -> float:
        value = 23.5                                                # Simulamos la lectura del sensor.

        # Simulamos la persistencia de la lectura.
        with open("temperature.txt", "w", encoding="utf-8") as file:
            file.write(str(value))

        return value
    
    
# Ejemplo correcto de SRP: Ahora separaremos las dos responsabilidades
class TemperatureSensor:
    def read(self) -> float:
        return 23.5


class ReadingFileWriter:
    def save(self, value: float, filename: str) -> None:
        # Guardamos la lectura en el archivo indicado
        with open(filename, "w", encoding="utf-8") as file:
            file.write(str(value))

#==========[     OCP     ]==========
#El código debe estar abierto para agregar comportamiento nuevo, pero cerrado para modificar el código que ya funciona

#Ejemplo incorrecto: una clase que lee un sensor y además formatea la lectura. Si queremos agregar un nuevo tipo de sensor, debemos modificar esta clase
class BadSensorFormatter:
    def format_reading(self, sensor_type: str, value: float) -> str:
        # Elegimos el formato mediante condiciones para cada tipo de sensor.
        if sensor_type == "temperature":
            return f"Temperature: {value} C"

        if sensor_type == "humidity":
            return f"Humidity: {value} %"

        raise ValueError("Unsupported sensor type")
    

#Ejemplo correcto de OCP: Ahora podemos agregar nuevos tipos de sensores sin modificar la clase existente, sino creando nuevas clases que implementen el protocolo ReadingFormatter
class ReadingFormatter(Protocol):
    def format(self, value: float) -> str:                                      # Declaramos el comportamiento que debe ofrecer un formateador
        ...

class TemperatureFormatter:
    def format(self, value: float) -> str:
        return f"Temperature: {value} C"                                        # Formateamos una lectura de temperatura


class HumidityFormatter:
    def format(self, value: float) -> str:
        return f"Humidity: {value} %"                                           # Formateamos una lectura de humedad


def format_sensor_reading(
    formatter: ReadingFormatter,
    value: float,
) -> str:
    return formatter.format(value)                                              # Utilizamos cualquier formateador que cumpla el contrato


#==========[     LSP     ]==========
# Indica que una clase hija debe poder sustituir a su clase base sin romper el comportamiento esperado

#Ejemplo incorrecto: una clase que hereda de otra pero no cumple con el contrato de la clase padre
class PercentageSensor:
    def read(self) -> float:
        return 50.0                                                              # Devolvemos un porcentaje válido


class BadRawHumiditySensor(PercentageSensor):                                    # Indica que BadRawHumiditySensor es un tipo de PercentageSensor
    def read(self) -> float:
        return 512.0                                                             # Debería respetar el mismo contrato, pero devuelve un valor fuera del rango esperado
    

#Ejemplo correcto de LSP: Ahora creamos una clase que respeta el contrato de la clase padre y devuelve un porcentaje válido
class HumidityPercentageSensor(PercentageSensor):
    def read(self) -> float:
        return 50.0                                                              # Devolvemos la humedad convertida a porcentaje
    
def read_percentage(sensor: PercentageSensor) -> float:
    value = sensor.read()                                                        # Leemos cualquier sensor que respete el contrato de porcentaje

# Comprobamos que el valor esté dentro del rango esperado.
    if not 0.0 <= value <= 100.0:
        raise ValueError("Percentage must be between 0 and 100")

    return value