from enum import StrEnum
from typing import Final


# Estados permitidos para el ciclo de vida de una alerta
class AlertStatus(StrEnum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


# Conservamos las alertas que siguen abiertas para atención operativa
ACTIVE_ALERT_STATUSES: Final[tuple[AlertStatus, AlertStatus]] = (
    AlertStatus.OPEN,
    AlertStatus.ACKNOWLEDGED,
)


# Definimos las transiciones permitidas para evitar reaperturas implícitas
VALID_ALERT_STATUS_TRANSITIONS: Final[dict[AlertStatus, set[AlertStatus]]] = {
    AlertStatus.OPEN: {
        AlertStatus.ACKNOWLEDGED,
        AlertStatus.RESOLVED,
    },
    AlertStatus.ACKNOWLEDGED: {
        AlertStatus.RESOLVED,
    },
    AlertStatus.RESOLVED: set(),
}


# Comprobamos si una transición de estado respeta la política del dominio
def can_transition_alert(
    *,
    current_status: AlertStatus,
    new_status: AlertStatus,
) -> bool:

    return new_status in VALID_ALERT_STATUS_TRANSITIONS[current_status]
