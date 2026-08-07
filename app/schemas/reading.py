from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Esquemas de entrada
# Definimos los contratos que validan los datos enviados por el cliente antes de que lleguen a la capa de servicio
class ReadingCreate(BaseModel):                                     # Representamos los datos necesarios para registrar una lectura

    # Valor medido por el sensor
    value: float = Field(                                           # Permitimos números enteros o decimales porque Pydantic los convierte a float
        description="Valor numérico medido por el sensor",          # La validación física del valor se mantiene fuera de este esquema
        examples=[24.5],
    )

# Representamos los campos permitidos al actualizar una lectura
class ReadingUpdate(BaseModel):

    # Nuevo valor de la lectura
    value: float | None = Field(                                    # Definimos el campo como opcional para permitir actualizaciones parciales
        default=None,                                               # Cuando el cliente omite value conservamos el valor actual de la lectura
        description="Nuevo valor numérico de la lectura",
        examples=[25.1],
    )

    @field_validator("value")
    @classmethod
    def reject_null_value(cls, value: float | None) -> float:       # Rechazamos null cuando el cliente envía explícitamente value

        if value is None:
            raise ValueError("El valor de la lectura no puede ser nulo")

        return value


# Esquemas de salida: Definimos la estructura pública que devolvemos desde los endpoints. Evitamos exponer directamente las entidades internas de SQLAlchemy
class ReadingResponse(BaseModel):                                   # Representamos una lectura devuelta por la API

    model_config = ConfigDict(                                      # Permitimos construir el esquema leyendo atributos del modelo ORM
        from_attributes=True,                                       # Esto hace posible usar model_validate directamente sobre una entidad Reading
    )

    id: int                                                         # Identificador interno generado por la base de datos

    sensor_id: int                                                  # Identificador del sensor propietario de la lectura
    value: float                                                    # Valor numérico registrado por el sensor
    timestamp: datetime                                             # Fecha y hora en la que la lectura fue almacenada