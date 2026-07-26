"""Administración de alertas mediante estrategias intercambiables"""

from abc import ABC, abstractmethod

from semana2.eval1.anomaly_detector import Anomaly


class AlertStrategy(ABC):
    """Contrato para las estrategias de envío de alertas"""

    @abstractmethod
    def send(self, anomaly: Anomaly) -> None:
        """Envía una anomalía mediante un mecanismo específico"""


class ConsoleAlertStrategy(AlertStrategy):
    """Envía alertas mediante la salida estándar"""

    def send(self, anomaly: Anomaly) -> None:
        """Escribe una alerta formateada en consola"""
        print(
            f"ALERTA | sensor={anomaly.sensor_id} | "
            f"tipo={anomaly.anomaly_type.value} | "
            f"valor={anomaly.measured_value} | "
            f"umbral={anomaly.threshold}"
        )


class AlertManager:
    """Delega el envío de alertas a una estrategia inyectada"""

    def __init__(self, strategy: AlertStrategy) -> None:
        """Configura la estrategia utilizada para enviar alertas"""
        self._strategy = strategy

    def send(self, anomaly: Anomaly) -> None:
        """Envía una anomalía usando la estrategia configurada"""
        self._strategy.send(anomaly)