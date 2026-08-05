from typing import Final

from fastapi import FastAPI

from app.routers.readings import router as readings_router  # import del router

APP_TITLE: Final[str] = "SensorHub API"
APP_VERSION: Final[str] = "0.1.0"

# Creamos el objeto principal de la aplicación ASGI
app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description="API REST para administrar sensores y sus lecturas",
)

app.include_router(readings_router)                         # Registramos el router

# Decorador: Registra una operación HTTP
@app.get(
    "/health",
    summary="Verificar el estado de la API",
    tags=["Sistema"],
)
def health_check() -> dict[str, str]:                       # Estamos indicando que la función devuelve un diccionario cuyas claves y valores son cadenas
    #Devuelve el estado actual de la API
    return {
        "status": "ok",
        "service": APP_TITLE,
        "version": APP_VERSION,
    }