# Excepciones base del dominio
# Definimos una jerarquía común para representar errores propios de SensorHub
# Esto permite distinguir fallos de negocio de errores técnicos o de infraestructura
class SensorHubError(Exception):
    """Representamos la excepción base del dominio de SensorHub"""

# Excepciones relacionadas con sensores
class SensorNotFoundError(SensorHubError):                              # Agrupamos aquí los errores que pueden ocurrir al consultar, crear, actualizar o eliminar sensores

    def __init__(self, sensor_id: int) -> None:                         # Construimos el error con el identificador del sensor inexistente

        self.sensor_id = sensor_id                                      # Conservamos el identificador para facilitar pruebas y trazabilidad

        super().__init__(                                               # Definimos el mensaje que podrá exponerse desde la capa HTTP
            f"No existe un sensor con id {sensor_id}"
        )

# Indicamos que el código público de un sensor ya está registrado
class SensorCodeConflictError(SensorHubError):

    def __init__(self, code: str) -> None:                              # Construimos el error con el código que produjo el conflicto

        self.code = code                                                # Conservamos el código para facilitar pruebas, auditoría y registro

        super().__init__(                                               # Definimos un mensaje específico para explicar el conflicto
            f"Ya existe un sensor con el código {code}"
        )

# Indicamos que un sensor no puede eliminarse porque conserva lecturas
class SensorHasReadingsError(SensorHubError):

    def __init__(self, sensor_id: int) -> None:                         # Construimos el error con el identificador del sensor relacionado

        self.sensor_id = sensor_id                                      # Conservamos el identificador para facilitar pruebas y trazabilidad

        super().__init__(                                               # Explicamos por qué la operación de eliminación fue rechazada
            f"No se puede eliminar el sensor con id {sensor_id} "
            "porque tiene lecturas asociadas"
        )

# Excepciones relacionadas con lecturas: # Agrupamos aquí los errores propios de las operaciones sobre lecturas
class ReadingNotFoundError(SensorHubError):                             # Indicamos que no existe la lectura solicitada

    def __init__(self, reading_id: int) -> None:                        # Construimos el error con el identificador de la lectura inexistente

        self.reading_id = reading_id                                    # Conservamos el identificador para facilitar pruebas y trazabilidad

        super().__init__(                                               # Definimos el mensaje que podrá transformarse en una respuesta HTTP
            f"No existe una lectura con id {reading_id}"
        )


# Excepciones relacionadas con filtros y consultas
# Agrupamos aquí los errores producidos por combinaciones inválidas de parámetros que no corresponden a un recurso concreto
class InvalidDateRangeError(SensorHubError):                            # Indicamos que la fecha inicial es posterior a la fecha final

    def __init__(self) -> None:                                         # Construimos el error para un rango temporal incoherente

        super().__init__(                                               # Definimos un mensaje claro para explicar la causa de la validación
            "La fecha inicial no puede ser posterior a la fecha final"
        )