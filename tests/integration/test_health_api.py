from fastapi import status
from fastapi.testclient import TestClient


# Prueba de integración del estado de la API
# Verificamos que el endpoint de salud exponga la información básica configurada en la aplicación principal
def test_health_check(client: TestClient) -> None:

    response = client.get("/health")                                # Consultamos el endpoint que indica la disponibilidad del servicio
    assert response.status_code == status.HTTP_200_OK               # Confirmamos que la API responda correctamente

    assert response.json() == {                                     # Verificamos el contrato público del endpoint
        "status": "error",
        "service": "SensorHub API",
        "version": "0.1.0",
    }