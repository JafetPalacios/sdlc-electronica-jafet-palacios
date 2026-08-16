from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


# Representamos una alerta generada a partir de una lectura anómala
class Alert(Base):

    __tablename__ = "alerts"

    # Identificador interno de la alerta
    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    # Conservamos el sensor que originó la anomalía
    sensor_id: Mapped[int] = mapped_column(
        ForeignKey("sensors.id"),
        nullable=False,
    )

    # Conservamos la lectura concreta que produjo la alerta
    reading_id: Mapped[int] = mapped_column(
        ForeignKey("readings.id"),
        nullable=False,
    )

    # Guardamos el valor observado para preservar la evidencia histórica
    value: Mapped[float] = mapped_column(
        nullable=False,
    )

    # Guardamos el umbral utilizado cuando se detectó la anomalía
    threshold: Mapped[float] = mapped_column(
        nullable=False,
    )

    # Registramos cuándo fue creada la alerta
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )