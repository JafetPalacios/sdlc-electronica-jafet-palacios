from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import get_alert_service
from app.schemas import AlertResponse, AlertStatusUpdate
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


# Consulta de alertas activas
@router.get(
    "/alerts/active",
    response_model=list[AlertResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar alertas activas",
    description=(
        "Devuelve únicamente las alertas que siguen activas "
        "y todavía requieren atención operativa"
    ),
)
def list_active_alerts(
    service: AlertServiceDependency,
) -> list[AlertResponse]:

    alerts = service.list_active_alerts()

    return [
        AlertResponse.model_validate(alert)
        for alert in alerts
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


# Cambio de estado de una alerta concreta
@router.patch(
    "/alerts/{alert_id}",
    response_model=AlertResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar el estado de una alerta",
    description=(
        "Cambia el estado de una alerta respetando "
        "las transiciones válidas definidas por SensorHub"
    ),
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "La alerta solicitada no existe",
        },
        status.HTTP_409_CONFLICT: {
            "description": "La transición de estado solicitada no es válida",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "El identificador o el estado recibido no son válidos",
        },
    },
)
def update_alert_status(
    alert_id: int,
    alert_data: AlertStatusUpdate,
    service: AlertServiceDependency,
) -> AlertResponse:

    alert = service.update_alert_status(
        alert_id=alert_id,
        new_status=alert_data.status,
    )

    return AlertResponse.model_validate(alert)
