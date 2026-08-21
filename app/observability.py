import json
import logging
import os
import sys
from datetime import UTC, datetime
from typing import Final

LOGGER_NAME: Final[str] = "sensorhub.observability"
DEFAULT_LOG_LEVEL: Final[str] = "INFO"
LOG_LEVEL_ENV_VAR: Final[str] = "LOG_LEVEL"


# Configuramos un logger sencillo que emite una línea JSON por evento
def get_observability_logger() -> logging.Logger:

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(_resolve_log_level())
    logger.propagate = False

    if len(logger.handlers) != 1 or not isinstance(logger.handlers[0], logging.StreamHandler):
        logger.handlers.clear()
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)

    return logger


# Serializamos cada evento en una estructura estable y legible por máquinas
def serialize_log_event(
    event: str,
    **fields: object,
) -> str:

    payload = {
        "timestamp": datetime.now(UTC).isoformat(),
        "level": "INFO",
        "logger": LOGGER_NAME,
        "event": event,
        **fields,
    }

    return json.dumps(
        payload,
        ensure_ascii=True,
        separators=(",", ":"),
    )


# Emitimos el evento ya serializado usando el nivel configurado por entorno
def log_event(
    event: str,
    **fields: object,
) -> None:

    get_observability_logger().info(
        serialize_log_event(event, **fields),
    )


def _resolve_log_level() -> int:

    configured_level = os.getenv(LOG_LEVEL_ENV_VAR, DEFAULT_LOG_LEVEL).upper()

    return logging.getLevelNamesMapping().get(
        configured_level,
        logging.INFO,
    )
