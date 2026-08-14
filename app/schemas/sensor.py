from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Esquemas de entrada
# Definimos los contratos utilizados para recibir y validar los datos enviados
# por el cliente antes de entregarlos a la capa de servicio
class SensorCreate(BaseModel):

    # Código público
    code: str = Field(                                  # Identificamos al sensor mediante un código único dentro de SensorHub
        min_length=1,                                   # Limitamos su longitud para mantener consistencia con la columna de la base
        max_length=50,
        examples=["TEMP-01"],
    )

    # Nombre descriptivo
    name: str = Field(                                      # Conservamos una etiqueta legible que permita reconocer el sensor
        min_length=1,                                       # dentro de la aplicación y en las respuestas de la API
        max_length=100,
        examples=["Sensor de temperatura del laboratorio"],
    )

    # Tipo de sensor
    sensor_type: str = Field(                               # Indicamos la categoría o magnitud física asociada al dispositivo como temperatura, humedad o presión
        min_length=1,
        max_length=30,
        examples=["temperature"],
    )

    # Unidad de medida
    unit: str = Field(                                      # Especificamos la unidad utilizada para interpretar correctamente los valores registrados por el sensor
        min_length=1,
        max_length=20,
        examples=["C"],
    )

# Representamos los campos permitidos al actualizar un sensor
class SensorUpdate(BaseModel):

    # Código público actualizado
    code: str | None = Field(                               # Permitimos omitir este campo porque el endpoint utiliza PATCH
        default=None,                                       # El servicio valida que se aunico cuando el cliente envía un nuevo código
        min_length=1,
        max_length=50,
        examples=["TEMP-02"],
    )

    # Nombre descriptivo actualizado
    name: str | None = Field(                               # Conservamos el valor actual cuando el cliente no envía este campo
        default=None,
        min_length=1,
        max_length=100,
        examples=["Sensor de temperatura actualizado"],
    )

    # Tipo de sensor actualizado
    sensor_type: str | None = Field(                        # Permitimos modificar la categoría del sensor sin reemplazar los demás campos del registro
        default=None,
        min_length=1,
        max_length=30,
        examples=["temperature"],
    )

    # Unidad de medida actualizada
    unit: str | None = Field(                               # Permitimos corregir o cambiar la unidad utilizada por el sensor
        default=None,
        min_length=1,
        max_length=20,
        examples=["°C"],
    )

    @field_validator(
        "code",
        "name",
        "sensor_type",
        "unit",
    )
    @classmethod
    def reject_null_fields(cls, value: str | None) -> str:  # Rechazamos null en los campos enviados explícitamente

        if value is None:
            raise ValueError(
                "Los campos de un sensor no pueden ser nulos"
            )

        return value


# Esquemas de salida
# Definimos la estructura pública devuelta por los endpoints de sensores
# De esta forma evitamos exponer directamente el modelo interno de SQLAlchemy
class SensorResponse(BaseModel):                                # Representamos un sensor devuelto por la API

    model_config = ConfigDict(                                  # Permitimos construir la respuesta desde los atributos del modelo ORM
        from_attributes=True,                                   # Esto nos permite utilizar model_validate directamente con una entidad Sensor
    )

    id: int                                                     # Identificador interno generado por la base de datos

    code: str                                                   # Código público único del sensor
    name: str                                                   # Nombre descriptivo utilizado para reconocer el sensor
    sensor_type: str                                            # Categoría o magnitud física asociada al sensor
    unit: str                                                   # Unidad utilizada para interpretar sus lecturas
    created_at: datetime                                        # Fecha y hora generadas cuando registramos el sensor