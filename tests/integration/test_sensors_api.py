from typing import cast

from fastapi import status
from fastapi.testclient import TestClient


# Pruebas de integración para sensores
# Verificamos el comportamiento completo de la API utilizando TestClient y la base SQLite temporal configurada en tests/conftest.py
def create_sensor(
    client: TestClient,
    *,
    code: str = "TEMP-001",
    name: str = "Sensor de temperatura",
    location: str = "Laboratorio de electrónica",
    sensor_type: str = "temperature",
    unit: str = "°C",
) -> dict[str, object]:

    response = client.post(                                         # Enviamos una petición real al endpoint de creación
        "/sensors/",
        json={
            "code": code,
            "name": name,
            "location": location,
            "sensor_type": sensor_type,
            "unit": unit,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED          # Confirmamos que el recurso auxiliar fue creado correctamente

    response_data = cast(
    dict[str, object],
    response.json(),
)

    return response_data


# Creación exitosa
def test_create_sensor_success(client: TestClient) -> None:         # Verificamos el registro exitoso de un sensor mediante la API

    response = client.post(
        "/sensors/",
        json={
            "code": "TEMP-001",
            "name": "Sensor de temperatura",
            "location": "Laboratorio de electrónica",
            "sensor_type": "temperature",
            "unit": "°C",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()

    assert response_data["id"] == 1
    assert response_data["code"] == "TEMP-001"
    assert response_data["name"] == "Sensor de temperatura"
    assert response_data["sensor_type"] == "temperature"
    assert response_data["unit"] == "°C"
    assert response_data["created_at"] is not None
    assert response_data["location"] == "Laboratorio de electrónica"
    assert response_data["is_active"] is True

# Código duplicado: Verificamos que un código duplicado produzca HTTP 409
def test_create_sensor_duplicate_code_returns_409(
    client: TestClient,
) -> None:

    create_sensor(client)

    response = client.post(
        "/sensors/",
        json={
            "code": "TEMP-001",
            "name": "Sensor duplicado",
            "location": "Laboratorio de electrónica",
            "sensor_type": "temperature",
            "unit": "°C",
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {
        "detail": "Ya existe un sensor con el código TEMP-001",
    }


# Reglas físicas: Verificamos que un tipo desconocido produzca HTTP 422
def test_create_sensor_with_unsupported_type_returns_422(
    client: TestClient,
) -> None:

    response = client.post(
        "/sensors/",
        json={
            "code": "VOLT-001",
            "name": "Sensor de voltaje",
            "location": "Laboratorio de electrónica",
            "sensor_type": "voltage",
            "unit": "V",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json() == {
        "detail": "El tipo de sensor voltage no está admitido",
    }

# Verificamos que una unidad incompatible produzca HTTP 422
def test_create_sensor_with_invalid_unit_returns_422(
    client: TestClient,
) -> None:

    response = client.post(
        "/sensors/",
        json={
            "code": "TEMP-002",
            "name": "Sensor con unidad incorrecta",
            "location": "Laboratorio de electrónica",
            "sensor_type": "temperature",
            "unit": "K",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json() == {
        "detail": (
            "La unidad K no es válida para el tipo "
            "temperature; se esperaba °C"
        ),
    }


# Consulta individual: Verificamos la consulta de un sensor existente
def test_get_sensor_success(client: TestClient) -> None:

    created_sensor = create_sensor(client)
    sensor_id = created_sensor["id"]

    response = client.get(
        f"/sensors/{sensor_id}",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["code"] == "TEMP-001"

# Verificamos que un sensor inexistente produzca HTTP 404
def test_get_missing_sensor_returns_404(
    client: TestClient,
) -> None:

    response = client.get(
        "/sensors/999999",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "No existe un sensor con id 999999",
    }


# Actualización: Verificamos la actualización parcial de un sensor
def test_update_sensor_success(client: TestClient) -> None:

    created_sensor = create_sensor(client)
    sensor_id = created_sensor["id"]

    response = client.patch(
        f"/sensors/{sensor_id}",
        json={
            "name": "Sensor actualizado",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert response_data["name"] == "Sensor actualizado"
    assert response_data["code"] == "TEMP-001"
    assert response_data["sensor_type"] == "temperature"
    assert response_data["unit"] == "°C"

# Verificamos que una combinación física inválida produzca HTTP 422
def test_update_sensor_with_incompatible_rule_returns_422(
    client: TestClient,
) -> None:

    created_sensor = create_sensor(client)
    sensor_id = created_sensor["id"]

    response = client.patch(
        f"/sensors/{sensor_id}",
        json={
            "sensor_type": "humidity",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json() == {
        "detail": (
            "La unidad °C no es válida para el tipo "
            "humidity; se esperaba %"
        ),
    }


# Borrado físico deshabilitado
def test_delete_sensor_is_not_allowed(client: TestClient) -> None:
    # Crear un sensor que debe conservarse aunque el cliente intente eliminarlo
    created_sensor = create_sensor(client)
    sensor_id = created_sensor["id"]

    # Intentar utilizar una operación que ya no forma parte del contrato de SensorHub
    response = client.delete(
        f"/sensors/{sensor_id}",
    )

    # Verificar que la API no exponga borrado físico de sensores
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    # Confirmar que el sensor continúe disponible después del intento
    get_response = client.get(
        f"/sensors/{sensor_id}",
    )

    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json()["id"] == sensor_id


# Umbral de alerta en el contrato público
def test_create_sensor_with_alert_threshold_returns_threshold(
    client: TestClient,
) -> None:
    # Registramos un sensor con un umbral configurable
    response = client.post(
        "/sensors/",
        json={
            "code": "TEMP-ALERT-API-001",
            "name": "Sensor de temperatura con alerta",
            "location": "Laboratorio de electrónica",
            "sensor_type": "temperature",
            "unit": "°C",
            "alert_threshold": 30.0,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()

    # Confirmamos que el contrato público exponga el umbral persistido
    assert response_data["alert_threshold"] == 30.0

# Desactivación mediante actualización parcial
def test_deactivate_sensor_success(client: TestClient) -> None:
    # Crear un sensor activo antes de solicitar su desactivación
    created_sensor = create_sensor(client)
    sensor_id = created_sensor["id"]

    response = client.patch(
        f"/sensors/{sensor_id}",
        json={
            "is_active": False,
        },
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    # Verificar que el recurso continúe existiendo pero cambie su estado
    assert response_data["id"] == sensor_id
    assert response_data["is_active"] is False

    get_response = client.get(
        f"/sensors/{sensor_id}",
    )

    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json()["is_active"] is False
