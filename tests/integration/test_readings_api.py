from typing import cast

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.alert_strategy import AlertSeverity
from app.models import Alert


# Pruebas de integración para lecturas
# Verificamos el comportamiento completo de los endpoints de lecturas utilizando la base SQLite temporal configurada para la suite
def create_sensor(
    client: TestClient,
    *,
    code: str = "HUM-001",
    name: str = "Sensor de humedad",
    location: str = "Laboratorio de electrónica",
    sensor_type: str = "humidity",
    unit: str = "%",
) -> dict[str, object]:

    response = client.post(
        "/sensors/",
        json={
            "code": code,
            "name": name,
            "location": location,
            "sensor_type": sensor_type,
            "unit": unit,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    return cast(
        dict[str, object],
        response.json(),
    )

# Registramos una lectura reutilizable para los escenarios de integración
def create_reading(
    client: TestClient,
    sensor_id: object,
    *,
    value: float = 50.0,
) -> dict[str, object]:


    response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": value,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    return cast(
        dict[str, object],
        response.json(),
    )


# Creación de lecturas
def test_create_reading_success(client: TestClient) -> None:                # Verificamos el registro exitoso de una lectura

    sensor = create_sensor(client)
    sensor_id = sensor["id"]

    response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": 55.0,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()

    assert response_data["id"] == 1
    assert response_data["sensor_id"] == sensor_id
    assert response_data["value"] == 55.0
    assert response_data["timestamp"] is not None

# Verificamos que un sensor inexistente produzca HTTP 404
def test_create_reading_for_missing_sensor_returns_404(
    client: TestClient,
) -> None:

    response = client.post(
        "/sensors/999999/readings",
        json={
            "value": 40.0,
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "No existe un sensor con id 999999",
    }

# Verificamos que una lectura fuera de rango produzca HTTP 422
def test_create_reading_out_of_range_returns_422(
    client: TestClient,
) -> None:

    sensor = create_sensor(client)
    sensor_id = sensor["id"]

    response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": 120.0,
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json() == {
        "detail": (
            "El valor 120.0 está fuera del rango permitido "
            "para humidity: 0.0 a 100.0"
        ),
    }


# Consulta de lecturas
def test_get_reading_success(client: TestClient) -> None:           # Verificamos la consulta de una lectura existente

    sensor = create_sensor(client)
    reading = create_reading(
        client,
        sensor["id"],
    )

    response = client.get(
        f"/readings/{reading['id']}",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["value"] == 50.0

# Verificamos que una lectura inexistente produzca HTTP 404
def test_get_missing_reading_returns_404(
    client: TestClient,
) -> None:

    response = client.get(
        "/readings/999999",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "No existe una lectura con id 999999",
    }

# Verificamos el listado paginado de lecturas por sensor
def test_list_readings_for_sensor_success(
    client: TestClient,
) -> None:

    sensor = create_sensor(client)
    sensor_id = sensor["id"]

    create_reading(
        client,
        sensor_id,
        value=30.0,
    )
    create_reading(
        client,
        sensor_id,
        value=60.0,
    )

    response = client.get(
        f"/sensors/{sensor_id}/readings?limit=10&offset=0",
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert len(response_data) == 2
    assert response_data[0]["value"] == 30.0
    assert response_data[1]["value"] == 60.0

# Verificamos que un rango temporal incoherente produzca HTTP 400
def test_list_readings_with_invalid_date_range_returns_400(
    client: TestClient,
) -> None:

    sensor = create_sensor(client)
    sensor_id = sensor["id"]

    response = client.get(
        (
            f"/sensors/{sensor_id}/readings"
            "?from=2026-08-10T00:00:00"
            "&to=2026-08-01T00:00:00"
        ),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "La fecha inicial no puede ser posterior a la fecha final",
    }


# Actualización de lecturas
def test_update_reading_success(client: TestClient) -> None:

    sensor = create_sensor(client)
    reading = create_reading(
        client,
        sensor["id"],
    )

    response = client.patch(
        f"/readings/{reading['id']}",
        json={
            "value": 75.0,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["value"] == 75.0

# Verificamos que una actualización fuera de rango produzca HTTP 422
def test_update_reading_out_of_range_returns_422(
    client: TestClient,
) -> None:

    sensor = create_sensor(client)
    reading = create_reading(
        client,
        sensor["id"],
    )

    response = client.patch(
        f"/readings/{reading['id']}",
        json={
            "value": -10.0,
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json() == {
        "detail": (
            "El valor -10.0 está fuera del rango permitido "
            "para humidity: 0.0 a 100.0"
        ),
    }


# Eliminación de lecturas
def test_delete_reading_success(client: TestClient) -> None:

    sensor = create_sensor(client)
    reading = create_reading(
        client,
        sensor["id"],
    )

    response = client.delete(
        f"/readings/{reading['id']}",
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.text == ""

    get_response = client.get(
        f"/readings/{reading['id']}",
    )

    assert get_response.status_code == status.HTTP_404_NOT_FOUND

# Verificamos que una combinación de fechas con tratamiento temporal incompatible produzca HTTP 400
def test_list_readings_with_mixed_timezone_awareness_returns_400(
    client: TestClient,
) -> None:

    sensor = create_sensor(client)
    sensor_id = sensor["id"]

    response = client.get(
        (
            f"/sensors/{sensor_id}/readings"
            "?from=2026-08-10T00:00:00Z"
            "&to=2026-08-11T00:00:00"
        ),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": (
            "Las fechas del rango deben usar de forma consistente "
            "información de zona horaria"
        ),
    }

# Generación persistente de alerta desde el flujo HTTP de lecturas
def test_create_reading_above_threshold_persists_alert(
    client: TestClient,
    db_session: Session,
) -> None:
    # Registramos un sensor con un umbral activo
    sensor_response = client.post(
        "/sensors/",
        json={
            "code": "TEMP-ALERT-READING-001",
            "name": "Sensor de temperatura con alerta",
            "location": "Laboratorio de electrónica",
            "sensor_type": "temperature",
            "unit": "°C",
            "alert_threshold": 30.0,
        },
    )

    assert sensor_response.status_code == status.HTTP_201_CREATED

    sensor_id = sensor_response.json()["id"]

    # Registramos una lectura que supera el umbral configurado
    reading_response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": 31.0,
        },
    )

    assert reading_response.status_code == status.HTTP_201_CREATED

    reading_id = reading_response.json()["id"]

    # Consultamos directamente la persistencia para comprobar la integración
    alerts = list(
        db_session.scalars(
            select(Alert),
        ).all()
    )

    assert len(alerts) == 1

    alert = alerts[0]

    assert alert.sensor_id == sensor_id
    assert alert.reading_id == reading_id
    assert alert.value == 31.0
    assert alert.threshold == 30.0
    assert alert.severity == AlertSeverity.WARNING


# Generación persistente de alerta crítica desde el flujo HTTP de lecturas
def test_create_reading_far_above_threshold_persists_critical_alert(
    client: TestClient,
    db_session: Session,
) -> None:
    # Registramos un sensor con un umbral activo
    sensor_response = client.post(
        "/sensors/",
        json={
            "code": "TEMP-ALERT-CRITICAL-READING-001",
            "name": "Sensor de temperatura con alerta crítica",
            "location": "Laboratorio de electrónica",
            "sensor_type": "temperature",
            "unit": "°C",
            "alert_threshold": 30.0,
        },
    )

    assert sensor_response.status_code == status.HTTP_201_CREATED

    sensor_id = sensor_response.json()["id"]

    # Registramos una lectura que excede ampliamente el umbral
    reading_response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": 36.0,
        },
    )

    assert reading_response.status_code == status.HTTP_201_CREATED

    alerts = list(
        db_session.scalars(
            select(Alert),
        ).all()
    )

    assert len(alerts) == 1
    assert alerts[0].severity == AlertSeverity.CRITICAL

# Rechazo HTTP de lecturas para sensores inactivos
def test_create_reading_for_inactive_sensor_returns_409(
    client: TestClient,
) -> None:
    # Crear un sensor activo mediante la API
    sensor = create_sensor(
        client,
        code="TEMP-INACTIVE-API-001",
        name="Sensor de temperatura inactivo",
        location="Laboratorio de electrónica",
        sensor_type="temperature",
        unit="°C",
    )

    sensor_id = sensor["id"]

    # Desactivar el sensor antes de intentar registrar telemetría
    deactivate_response = client.patch(
        f"/sensors/{sensor_id}",
        json={
            "is_active": False,
        },
    )

    assert deactivate_response.status_code == status.HTTP_200_OK
    assert deactivate_response.json()["is_active"] is False

    # Intentar registrar una nueva lectura sobre el sensor desactivado
    response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": 25.0,
        },
    )

    # Verificar que el estado actual del sensor impida la operación
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {
        "detail": f"El sensor con id {sensor_id} está inactivo",
    }
