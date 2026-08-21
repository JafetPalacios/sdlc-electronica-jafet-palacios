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

    # Ubicación física
    location: str = Field(                                    # Identificar el lugar donde se encuentra instalado el sensor
        min_length=1,
        max_length=150,
        examples=["Laboratorio de electrónica"],
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

    # Umbral opcional utilizado por la estrategia de detecci?n de anomal?as
    alert_threshold: float | None = Field(
        default=None,
        description="Umbral superior configurable para generar alertas",
        examples=[30.0],
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

        # Umbral opcional utilizado para modificar o desactivar la detección de anomalías
    alert_threshold: float | None = Field(
        default=None,
        description="Umbral superior configurable para generar alertas",
        examples=[35.0],
    )

    # Estado operativo
    is_active: bool | None = Field(                       # Permitir activar o desactivar un sensor mediante PATCH
        default=None,
        description="Indica si el sensor está habilitado para recibir nuevas lecturas",
        examples=[False],
    )

    # Ubicación física actualizada
    location: str | None = Field(                         # Permitir modificar el lugar donde se encuentra instalado el sensor
        default=None,
        min_length=1,
        max_length=150,
        examples=["Laboratorio de instrumentación"],
    )

    @field_validator("is_active")
    @classmethod
    def reject_null_is_active(cls, value: bool | None) -> bool:
        # Rechazar null cuando el cliente envía explícitamente el estado
        if value is None:
            raise ValueError(
                "El estado activo de un sensor no puede ser nulo"
            )

        return value

    @field_validator(
        "code",
        "name",
        "location",
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
    location: str                                               # Exponer la ubicación física registrada para el sensor
    is_active: bool                                             # Indicar si el sensor está habilitado para recibir nuevas lecturas

        # Umbral superior configurado para detectar anomalías en las lecturas
    alert_threshold: float | None

    created_at: datetime                                        # Fecha y hora generadas cuando registramos el sensor
