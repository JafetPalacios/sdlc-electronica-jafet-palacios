from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import get_alert_service
from app.schemas import AlertResponse
from app.services.alert_service import AlertService

# Configuración del router
# Agrupamos aquí los endpoints cuyo recurso principal es una alerta
router = APIRouter(
    tags=["Alertas"],
)


# Dependencia del servicio de alertas
AlertServiceDependency = Annotated[
    AlertService,
    Depends(get_alert_service),
]


# Consulta de alertas por sensor
@router.get(
    "/sensors/{sensor_id}/alerts",
    response_model=list[AlertResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar las alertas de un sensor",
    description=(
        "Devuelve las alertas registradas para el sensor indicado "
        "después de comprobar que el sensor exista"
    ),
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "El sensor solicitado no existe",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "El identificador recibido no es válido",
        },
    },
)
def list_alerts_for_sensor(
    sensor_id: int,
    service: AlertServiceDependency,
) -> list[AlertResponse]:

    # Delegamos al servicio la validación del sensor y la consulta de alertas
    alerts = service.list_alerts_for_sensor(sensor_id)

    # Convertimos las entidades ORM al contrato público de la API
    return [
        AlertResponse.model_validate(alert)
        for alert in alerts
    ]