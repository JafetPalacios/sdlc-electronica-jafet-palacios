from app.domain.alert_strategy import AlertSeverity, ThresholdAlertStrategy


# Estrategia de alerta basada en un umbral configurable
def test_threshold_alert_strategy_classifies_warning_above_threshold() -> None:
    # Creamos la estrategia sin depender de FastAPI, SQLAlchemy o repositorios
    strategy = ThresholdAlertStrategy()

    # Verificamos que un exceso leve quede clasificado como WARNING
    severity = strategy.classify(
        value=31.0,
        threshold=30.0,
    )

    assert severity == AlertSeverity.WARNING


# Exceso significativo sobre el umbral
def test_threshold_alert_strategy_classifies_critical_when_excess_is_high() -> None:
    # Comprobamos la escalada a CRITICAL cuando la desviación supera la tolerancia
    strategy = ThresholdAlertStrategy()

    severity = strategy.classify(
        value=36.0,
        threshold=30.0,
    )

    assert severity == AlertSeverity.CRITICAL


# Valor exactamente igual al umbral
def test_threshold_alert_strategy_returns_none_at_threshold() -> None:
    # Comprobamos que solamente los valores superiores generen una anomalía
    strategy = ThresholdAlertStrategy()

    severity = strategy.classify(
        value=30.0,
        threshold=30.0,
    )

    assert severity is None
