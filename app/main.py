from typing import Final

from fastapi import FastAPI

from app.db import Base, engine
from app.models import Sensor  # noqa: F401  # Registramos el modelo en los metadatos
from app.routers.readings import router as readings_router

APP_TITLE: Final[str] = "SensorHub API"
APP_VERSION: Final[str] = "0.1.0"

app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description="API REST para administrar sensores y sus lecturas",
)

Base.metadata.create_all(bind=engine)

app.include_router(readings_router)


@app.get(
    "/health",
    summary="Verificar el estado de la API",
    tags=["Sistema"],
)
def health_check() -> dict[str, str]:
    """Devuelve el estado actual de la API"""

    return {
        "status": "ok",
        "service": APP_TITLE,
        "version": APP_VERSION,
    }