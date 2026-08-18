from typing import Protocol


# Contrato para estrategias de detección de anomalías
# Permitimos sustituir el criterio utilizado sin modificar al servicio que lo consume
class AlertStrategy(Protocol):

    # Evaluamos si un valor debe considerarse anómalo según el criterio recibido
    def is_anomaly(
        self,
        *,
        value: float,
        threshold: float,
    ) -> bool:

        ...


# Estrategia de detección basada en un umbral superior
class ThresholdAlertStrategy:

    # Consideramos anómala únicamente una lectura que supere el umbral configurado
    def is_anomaly(
        self,
        *,
        value: float,
        threshold: float,
    ) -> bool:

        return value > threshold