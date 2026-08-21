from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.alert_lifecycle import AlertStatus
from app.models import Alert


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
    assert alert["severity"] == "WARNING"
    assert alert["status"] == "open"
    assert alert["id"] is not None
    assert alert["created_at"] is not None


# Consulta HTTP de una alerta crítica generada por una lectura muy alta
def test_list_alerts_for_sensor_returns_critical_alert(
    client: TestClient,
) -> None:
    # Creamos un sensor con un umbral configurado
    sensor_response = client.post(
        "/sensors/",
        json={
            "code": "TEMP-ALERT-API-CRITICAL-001",
            "name": "Sensor de temperatura con alerta crítica",
            "location": "Laboratorio de electrónica",
            "sensor_type": "temperature",
            "unit": "°C",
            "alert_threshold": 30.0,
        },
    )

    assert sensor_response.status_code == status.HTTP_201_CREATED

    sensor_id = sensor_response.json()["id"]

    # Registramos una lectura ampliamente superior al umbral
    reading_response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": 36.0,
        },
    )

    assert reading_response.status_code == status.HTTP_201_CREATED

    response = client.get(
        f"/sensors/{sensor_id}/alerts",
    )

    assert response.status_code == status.HTTP_200_OK

    alerts = response.json()

    assert len(alerts) == 1
    assert alerts[0]["severity"] == "CRITICAL"


# Consulta HTTP de alertas activas
def test_list_active_alerts_returns_only_open_and_acknowledged(
    client: TestClient,
    db_session: Session,
) -> None:
    # Creamos un sensor con tres lecturas anómalas para obtener tres alertas
    sensor_response = client.post(
        "/sensors/",
        json={
            "code": "TEMP-ALERT-ACTIVE-001",
            "name": "Sensor para alertas activas",
            "location": "Laboratorio de electrónica",
            "sensor_type": "temperature",
            "unit": "°C",
            "alert_threshold": 30.0,
        },
    )

    assert sensor_response.status_code == status.HTTP_201_CREATED

    sensor_id = sensor_response.json()["id"]

    for value in (31.0, 36.0, 40.0):
        reading_response = client.post(
            f"/sensors/{sensor_id}/readings",
            json={
                "value": value,
            },
        )

        assert reading_response.status_code == status.HTTP_201_CREATED

    alerts = list(
        db_session.scalars(
            select(Alert).order_by(Alert.id),
        ).all()
    )

    alerts[1].status = AlertStatus.ACKNOWLEDGED
    alerts[2].status = AlertStatus.RESOLVED
    db_session.commit()

    response = client.get(
        "/alerts/active",
    )

    assert response.status_code == status.HTTP_200_OK
    assert [alert["status"] for alert in response.json()] == [
        "open",
        "acknowledged",
    ]


# Cambio HTTP de estado válido
def test_update_alert_status_from_open_to_acknowledged(
    client: TestClient,
) -> None:
    # Creamos una alerta abierta mediante el flujo normal de lecturas
    sensor_response = client.post(
        "/sensors/",
        json={
            "code": "TEMP-ALERT-PATCH-001",
            "name": "Sensor para cambio de estado",
            "location": "Laboratorio de electrónica",
            "sensor_type": "temperature",
            "unit": "°C",
            "alert_threshold": 30.0,
        },
    )

    assert sensor_response.status_code == status.HTTP_201_CREATED

    sensor_id = sensor_response.json()["id"]

    reading_response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": 31.0,
        },
    )

    assert reading_response.status_code == status.HTTP_201_CREATED

    alert_response = client.get(
        f"/sensors/{sensor_id}/alerts",
    )

    assert alert_response.status_code == status.HTTP_200_OK

    alert_id = alert_response.json()[0]["id"]

    response = client.patch(
        f"/alerts/{alert_id}",
        json={
            "status": "acknowledged",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "acknowledged"


# Cambio HTTP de estado inválido
def test_update_alert_status_rejects_invalid_transition(
    client: TestClient,
) -> None:
    # Creamos una alerta y la resolvemos antes de intentar una transición inválida
    sensor_response = client.post(
        "/sensors/",
        json={
            "code": "TEMP-ALERT-PATCH-INVALID-001",
            "name": "Sensor para transición inválida",
            "location": "Laboratorio de electrónica",
            "sensor_type": "temperature",
            "unit": "°C",
            "alert_threshold": 30.0,
        },
    )

    assert sensor_response.status_code == status.HTTP_201_CREATED

    sensor_id = sensor_response.json()["id"]

    reading_response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": 36.0,
        },
    )

    assert reading_response.status_code == status.HTTP_201_CREATED

    alerts_response = client.get(
        f"/sensors/{sensor_id}/alerts",
    )

    assert alerts_response.status_code == status.HTTP_200_OK

    alert_id = alerts_response.json()[0]["id"]

    resolve_response = client.patch(
        f"/alerts/{alert_id}",
        json={
            "status": "resolved",
        },
    )

    assert resolve_response.status_code == status.HTTP_200_OK

    invalid_response = client.patch(
        f"/alerts/{alert_id}",
        json={
            "status": "acknowledged",
        },
    )

    assert invalid_response.status_code == status.HTTP_409_CONFLICT

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
