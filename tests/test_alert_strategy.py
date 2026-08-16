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

# Valor exactamente igual al umbral
def test_threshold_alert_strategy_does_not_detect_value_equal_to_threshold() -> None:
    # Comprobamos que solamente los valores superiores generen una anomalía
    strategy = ThresholdAlertStrategy()

    is_anomaly = strategy.is_anomaly(
        value=30.0,
        threshold=30.0,
    )

    assert is_anomaly is False