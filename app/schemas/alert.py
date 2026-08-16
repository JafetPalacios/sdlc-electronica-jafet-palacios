from datetime import datetime

from pydantic import BaseModel, ConfigDict


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
    created_at: datetime