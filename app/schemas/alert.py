from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domain.alert_lifecycle import AlertStatus
from app.domain.alert_strategy import AlertSeverity


# Contrato de entrada para modificar el estado de una alerta
class AlertStatusUpdate(BaseModel):

    status: AlertStatus


# Contrato público utilizado al devolver una alerta
class AlertResponse(BaseModel):

    # Permitimos construir la respuesta directamente desde el modelo ORM
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    sensor_id: int
    reading_id: int
    value: float
    threshold: float
    severity: AlertSeverity
    status: AlertStatus
    created_at: datetime
