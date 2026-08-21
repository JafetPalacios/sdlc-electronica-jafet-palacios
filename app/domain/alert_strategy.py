from enum import StrEnum
from typing import Protocol


class AlertSeverity(StrEnum):
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


# Contrato para estrategias de detección de anomalías
# Permitimos sustituir el criterio utilizado sin modificar al servicio que lo consume
class AlertStrategy(Protocol):

    # Clasificamos la severidad de una lectura según el criterio recibido
    def classify(
        self,
        *,
        value: float,
        threshold: float,
    ) -> AlertSeverity | None:

        ...


# Estrategia de detección basada en un umbral superior
class ThresholdAlertStrategy:

    def __init__(
        self,
        *,
        critical_excess_ratio: float = 0.2,
    ) -> None:

        self._critical_excess_ratio = critical_excess_ratio

    # Clasificamos la lectura únicamente cuando supera el umbral configurado
    def classify(
        self,
        *,
        value: float,
        threshold: float,
    ) -> AlertSeverity | None:

        if value <= threshold:
            return None

        critical_threshold = threshold + self._calculate_critical_margin(
            threshold,
        )

        if value >= critical_threshold:
            return AlertSeverity.CRITICAL

        return AlertSeverity.WARNING

    # Calculamos un margen configurable para distinguir WARNING de CRITICAL
    def _calculate_critical_margin(
        self,
        threshold: float,
    ) -> float:

        margin = abs(threshold) * self._critical_excess_ratio

        if margin == 0:
            return 1.0

        return margin
