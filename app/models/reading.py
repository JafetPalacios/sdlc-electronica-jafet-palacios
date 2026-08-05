from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.sensor import Sensor


class Reading(Base):
    """Representa una lectura realizada por un sensor"""

    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True)

    sensor_id: Mapped[int] = mapped_column(                 # Guardamos el id de un sensor existente
        ForeignKey("sensors.id"),
        nullable=False,
    )

    value: Mapped[float] = mapped_column(nullable=False)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    sensor: Mapped[Sensor] = relationship(
    back_populates="readings",
)