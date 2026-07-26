"""Pruebas del administrador de alertas"""

import pytest

from semana2.eval1.alert_manager import (
    AlertManager,
    AlertStrategy,
    ConsoleAlertStrategy,
)
from semana2.eval1.anomaly_detector import Anomaly, AnomalyType


class RecordingAlertStrategy(AlertStrategy):
    """Estrategia de prueba que registra las anomalías recibidas"""

    def __init__(self) -> None:
        """Inicializa el registro de anomalías"""
        self.alerts: list[Anomaly] = []

    def send(self, anomaly: Anomaly) -> None:
        """Registra la anomalía recibida"""
        self.alerts.append(anomaly)


def test_alert_manager_delegates_to_injected_strategy() -> None:
    """Verificamos que el administrador use la estrategia inyectada"""
    strategy = RecordingAlertStrategy()
    manager = AlertManager(strategy=strategy)
    anomaly = Anomaly(
        sensor_id="SENSOR-01",
        anomaly_type=AnomalyType.TEMPERATURE,
        measured_value=35.1,
        threshold=35.0,
    )

    manager.send(anomaly)

    assert strategy.alerts == [anomaly]

def test_console_strategy_writes_formatted_alert(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Verificamos que la estrategia escriba una alerta en consola"""
    strategy = ConsoleAlertStrategy()
    anomaly = Anomaly(
        sensor_id="SENSOR-01",
        anomaly_type=AnomalyType.TEMPERATURE,
        measured_value=35.1,
        threshold=35.0,
    )

    strategy.send(anomaly)

    captured = capsys.readouterr()

    assert captured.out == (
        "ALERTA | sensor=SENSOR-01 | tipo=temperature | "
        "valor=35.1 | umbral=35.0\n"
    )
