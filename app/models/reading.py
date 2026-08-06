from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

# Importamos el modelo Sensor únicamente durante el análisis de tipos
# Evitamos así una importación circular durante la ejecución de la aplicación
if TYPE_CHECKING:
    from app.models.sensor import Sensor


# Representamos una lectura registrada por un sensor
class Reading(Base):

    __tablename__ = "readings"                              # Definimos el nombre físico de la tabla dentro de la base de datos

    # Identificador principal, SQLAlchemy crea una clave primaria autoincremental al tratarse de un entero
    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    # Sensor propietario de la lectura
    sensor_id: Mapped[int] = mapped_column(                 # Relacionamos cada lectura con un registro existente de la tabla sensors
        ForeignKey("sensors.id"),                           # Impedimos valores nulos porque toda lectura debe pertenecer a un sensor
        nullable=False,
    )

    # Valor medido
    value: Mapped[float] = mapped_column(                   # Almacenamos el dato numérico producido por el sensor
        nullable=False,                                     # La unidad y las validaciones físicas se controlan en capas superiores
    )

    # Momento de registro
    timestamp: Mapped[datetime] = mapped_column(            # Conservamos la fecha y hora en la que la base de datos inserta la lectura
        DateTime(timezone=True),                            # Delegamos el valor inicial al servidor para mantener un origen temporal común
        server_default=func.now(),
        nullable=False,
    )

    # Relación ORM con Sensor
    sensor: Mapped[Sensor] = relationship(                  # Permitimos acceder al sensor propietario mediante reading.sensor
        back_populates="readings",                          # Mantiene sincronizada la relación inversa sensor.readings
    )