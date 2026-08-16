from app.domain.alert_strategy import ThresholdAlertStrategy


# Estrategia de alerta basada en un umbral configurable
def test_threshold_alert_strategy_detects_value_above_threshold() -> None:
    # Creamos la estrategia sin depender de FastAPI, SQLAlchemy o repositorios
    strategy = ThresholdAlertStrategy()

    # Verificamos que una lectura superior al umbral sea considerada anómala
    result = strategy.is_anomaly(
        value=31.0,
        threshold=30.0,
    )

    assert result is True