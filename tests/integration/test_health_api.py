from fastapi import status
from fastapi.testclient import TestClient


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
