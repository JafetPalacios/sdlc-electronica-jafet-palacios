import json

from app.observability import LOGGER_NAME, serialize_log_event


# Prueba unitaria de serialización de eventos
# Comprobamos que la observabilidad emita una estructura JSON estable y legible por máquinas
def test_serialize_log_event_returns_structured_json() -> None:

    serialized_event = serialize_log_event(
        "http_request_completed",
        method="GET",
        path="/health",
        status_code=200,
        duration_ms=1.25,
    )

    payload = json.loads(serialized_event)

    assert payload["logger"] == LOGGER_NAME
    assert payload["level"] == "INFO"
    assert payload["event"] == "http_request_completed"
    assert payload["method"] == "GET"
    assert payload["path"] == "/health"
    assert payload["status_code"] == 200
    assert payload["duration_ms"] == 1.25
    assert "timestamp" in payload
