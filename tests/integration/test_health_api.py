import pytest
from fastapi import status
from fastapi.testclient import TestClient

import app.main as main_module


# Prueba de integración del estado de la API
# Verificamos que el endpoint de salud exponga la información básica configurada en la aplicación principal
def test_health_check(client: TestClient) -> None:

    response = client.get("/health")                                # Consultamos el endpoint que indica la disponibilidad del servicio
    assert response.status_code == status.HTTP_200_OK               # Confirmamos que la API responda correctamente

    assert response.json() == {                                     # Verificamos el contrato público del endpoint
        "status": "ok",
        "service": "SensorHub API",
        "version": "0.1.2",
    }


# Prueba de integración de métricas básicas del servicio
def test_metrics_endpoint_exposes_uptime_and_request_counters(
    client: TestClient,
) -> None:

    health_response = client.get("/health")
    assert health_response.status_code == status.HTTP_200_OK

    response = client.get("/metrics")

    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"].startswith("text/plain")

    metrics_text = response.text

    assert "sensorhub_uptime_seconds " in metrics_text
    assert (
        'sensorhub_http_requests_total{method="GET",path="/health",status_code="200"} '
        in metrics_text
    )
    assert (
        'sensorhub_http_request_duration_seconds_count{method="GET",path="/health",status_code="200"} '
        in metrics_text
    )


# Prueba de integración de observabilidad básica
# Comprobamos que cada petición deje un log estructurado con información operativa útil
def test_health_request_emits_structured_log(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:

    logged_events: list[dict[str, object]] = []

    def fake_log_event(event: str, **fields: object) -> None:

        logged_events.append(
            {
                "event": event,
                **fields,
            }
        )

    monkeypatch.setattr(
        main_module,
        "log_event",
        fake_log_event,
    )

    response = client.get("/health")

    assert response.status_code == status.HTTP_200_OK

    assert logged_events
    assert logged_events[0]["event"] == "http_request_completed"
    assert logged_events[0]["method"] == "GET"
    assert logged_events[0]["path"] == "/health"
    assert logged_events[0]["status_code"] == status.HTTP_200_OK
    duration_ms = logged_events[0]["duration_ms"]

    assert isinstance(duration_ms, int | float)
    assert duration_ms >= 0
