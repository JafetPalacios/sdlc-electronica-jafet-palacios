from fastapi import status
from fastapi.testclient import TestClient


# Consulta HTTP de alertas pertenecientes a un sensor
def test_list_alerts_for_sensor_returns_generated_alert(
    client: TestClient,
) -> None:
    # Creamos un sensor con un umbral configurado
    sensor_response = client.post(
        "/sensors/",
        json={
            "code": "TEMP-ALERT-API-001",
            "name": "Sensor de temperatura con alertas",
            "location": "Laboratorio de electrónica",
            "sensor_type": "temperature",
            "unit": "°C",
            "alert_threshold": 30.0,
        },
    )

    assert sensor_response.status_code == status.HTTP_201_CREATED

    sensor_id = sensor_response.json()["id"]

    # Registramos una lectura superior al umbral para generar una alerta
    reading_response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": 31.0,
        },
    )

    assert reading_response.status_code == status.HTTP_201_CREATED

    reading_id = reading_response.json()["id"]

    # Consultamos las alertas registradas para el sensor
    response = client.get(
        f"/sensors/{sensor_id}/alerts",
    )

    assert response.status_code == status.HTTP_200_OK

    alerts = response.json()

    assert len(alerts) == 1

    alert = alerts[0]

    assert alert["sensor_id"] == sensor_id
    assert alert["reading_id"] == reading_id
    assert alert["value"] == 31.0
    assert alert["threshold"] == 30.0
    assert alert["id"] is not None
    assert alert["created_at"] is not None

# Consulta de un sensor existente que todavía no tiene alertas
def test_list_alerts_for_sensor_without_alerts_returns_empty_list(
    client: TestClient,
) -> None:
    # Creamos un sensor válido sin registrar lecturas anómalas
    sensor_response = client.post(
        "/sensors/",
        json={
            "code": "TEMP-ALERT-EMPTY-001",
            "name": "Sensor sin alertas",
            "location": "Laboratorio de electrónica",
            "sensor_type": "temperature",
            "unit": "°C",
            "alert_threshold": 30.0,
        },
    )

    assert sensor_response.status_code == status.HTTP_201_CREATED

    sensor_id = sensor_response.json()["id"]

    response = client.get(
        f"/sensors/{sensor_id}/alerts",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

# Consulta de alertas para un sensor inexistente
def test_list_alerts_for_nonexistent_sensor_returns_not_found(
    client: TestClient,
) -> None:
    # Utilizamos un identificador que no corresponde a ningún sensor creado
    response = client.get(
        "/sensors/999999/alerts",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND