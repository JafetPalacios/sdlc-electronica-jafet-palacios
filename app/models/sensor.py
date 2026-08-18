from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

# Importamos Reading únicamente durante la verificación de tipos
# Evitamos así una dependencia circular durante la ejecución
if TYPE_CHECKING:
    from app.models.reading import Reading

# Representamos un sensor registrado dentro de SensorHub
class Sensor(Base):

    __tablename__ = "sensors"                               # Definimos el nombre físico de la tabla en la base de datos

    # Identificador interno
    id: Mapped[int] = mapped_column(                        # Usamos una clave primaria entera que SQLAlchemy genera de forma incremental
        primary_key=True,
    )

    # Código único del sensor
    code: Mapped[str] = mapped_column(                      # Identificamos cada sensor mediante un código que no puede repetirse
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    # Nombre descriptivo
    name: Mapped[str] = mapped_column(                      # Conservamos una etiqueta legible que facilita reconocer el sensor
        String(100),
        nullable=False,
    )

    # Tipo de sensor
    sensor_type: Mapped[str] = mapped_column(               # Indicamos la magnitud o categoría medida como temperatura o humedad
        String(30),
        nullable=False,
    )

    # Unidad de medida
    unit: Mapped[str] = mapped_column(                      # Conservamos la unidad utilizada para interpretar correctamente las lecturas
        String(20),
        nullable=False,
    )

    # Fecha de registro
    created_at: Mapped[datetime] = mapped_column(           # Delegamos la generación del valor a la base de datos para mantener
        DateTime(timezone=True),                            # un origen temporal consistente entre todos los registros
        server_default=func.now(),
        nullable=False,
    )

    # Relación ORM con Reading
    readings: Mapped[list[Reading]] = relationship(         # Permitimos acceder a todas las lecturas mediante sensor.readings
        back_populates="sensor",                            # Mantiene sincronizada la relación inversa reading.sensor
    )

    # Umbral opcional para detección de anomalías
    alert_threshold: Mapped[float | None] = mapped_column(
        nullable=True,
    )