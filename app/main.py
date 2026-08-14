from typing import Final

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions import (
    InvalidDateRangeError,
    InvalidSensorUnitError,
    ReadingNotFoundError,
    ReadingValueOutOfRangeError,
    SensorCodeConflictError,
    SensorHasReadingsError,
    SensorNotFoundError,
    UnsupportedSensorTypeError,
)
from app.routers.readings import router as readings_router
from app.routers.sensors import router as sensors_router

# Metadatos principales de la aplicación
# Centralizamos el nombre y la versión para reutilizarlos en FastAPI y en el endpoint de estado
APP_TITLE: Final[str] = "SensorHub API"
APP_VERSION: Final[str] = "0.1.2"


app = FastAPI(                                                          # Creación de la aplicación
    title=APP_TITLE,                                                    # Configuramos la instancia principal de FastAPI con los metadatos expuestos en Swagger y OpenAPI
    version=APP_VERSION,
    description="API REST para administrar sensores y sus lecturas",
)

# Registro de routers
# Incorporamos los endpoints de sensores y lecturas a la aplicación principal
# Cada router conserva sus propias rutas, etiquetas y contratos de respuesta
app.include_router(sensors_router)
app.include_router(readings_router)


# ==========[     Manejadores de errores de sensores     ]==========

# Convertimos un sensor inexistente en una respuesta HTTP 404
@app.exception_handler(SensorNotFoundError)                                 # Transformamos excepciones del dominio en respuestas HTTP
async def handle_sensor_not_found(                                          # Evitamos que los servicios dependan directamente de FastAPI
    request: Request,
    exc: SensorNotFoundError,
) -> JSONResponse:

    _ = request                                                             # Conservamos la petición disponible para futuras tareas de auditoría

    return JSONResponse(                                                    # Devolvemos el mensaje de dominio con el código HTTP correspondiente
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc),
        },
    )


# Convertimos un código duplicado en una respuesta HTTP 409
@app.exception_handler(SensorCodeConflictError)
async def handle_sensor_code_conflict(
    request: Request,
    exc: SensorCodeConflictError,
) -> JSONResponse:

    _ = request                                                             # Conservamos la petición disponible para futuras tareas de trazabilidad

    return JSONResponse(                                                    # Informamos que la operación entra en conflicto con un recurso existente
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": str(exc),
        },
    )


# Convertimos una eliminación bloqueada en una respuesta HTTP 409
@app.exception_handler(SensorHasReadingsError)
async def handle_sensor_has_readings(
    request: Request,
    exc: SensorHasReadingsError,
) -> JSONResponse:

    _ = request                                                             # Conservamos la petición disponible para futuras tareas de trazabilidad

    return JSONResponse(                                                    # Informamos que el sensor no puede eliminarse por sus relaciones existentes
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": str(exc),
        },
    )


#==========[     Manejadores de errores de lecturas     ]==========
# Convertimos los errores propios de las lecturas en respuestas HTTP claras

# Convertimos una lectura inexistente en una respuesta HTTP 404
@app.exception_handler(ReadingNotFoundError)
async def handle_reading_not_found(
    request: Request,
    exc: ReadingNotFoundError,
) -> JSONResponse:

    _ = request                                                                 # Conservamos la petición disponible para futuras tareas de trazabilidad

    return JSONResponse(                                                        # Devolvemos el mensaje del dominio con el código HTTP correspondiente
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc),
        },
    )


#==========[     Manejadores de errores de filtros     ]==========

# Convertimos un rango temporal inválido en una respuesta HTTP 400
@app.exception_handler(InvalidDateRangeError)
async def handle_invalid_date_range(
    request: Request,
    exc: InvalidDateRangeError,
) -> JSONResponse:

    _ = request

    return JSONResponse(                                                          # Informamos que la combinación de fechas recibida no es válida
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": str(exc),
        },
    )


# Endpoint de estado
@app.get(                                                                       # Proporcionamos una ruta simple para comprobar que la API está disponible
    "/health",                                                                  # No consulta la base de datos ni ejecuta lógica de negocio
    summary="Verificar el estado de la API",
    description=(
        "Devuelve información básica para confirmar que "
        "el servicio está disponible"
    ),
    tags=["Sistema"],
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
)

# Devolvemos el estado actual de la API
def health_check() -> dict[str, str]:

    return {                                                                    # Exponemos información mínima sobre el servicio en ejecución
        "status": "ok",
        "service": APP_TITLE,
        "version": APP_VERSION,
    }


#==========[     Manejadores de errores de reglas físicas     ]==========
# Convertimos validaciones del dominio en respuestas HTTP 422 porque los datos tienen un formato válido pero no cumplen las reglas del producto

# Convertimos un tipo no admitido en una respuesta HTTP 422
@app.exception_handler(UnsupportedSensorTypeError)
async def handle_unsupported_sensor_type(
    request: Request,
    exc: UnsupportedSensorTypeError,
) -> JSONResponse:

    _ = request                                                                 # Conservamos la petición disponible para futuras tareas de trazabilidad

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "detail": str(exc),
        },
    )

# Convertimos una unidad incompatible en una respuesta HTTP 422
@app.exception_handler(InvalidSensorUnitError)
async def handle_invalid_sensor_unit(
    request: Request,
    exc: InvalidSensorUnitError,
) -> JSONResponse:

    _ = request                                                                   # Conservamos la petición disponible para futuras tareas de trazabilidad

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "detail": str(exc),
        },
    )

# Convertimos una lectura fuera de rango en una respuesta HTTP 422
@app.exception_handler(ReadingValueOutOfRangeError)
async def handle_reading_value_out_of_range(
    request: Request,
    exc: ReadingValueOutOfRangeError,
) -> JSONResponse:

    _ = request                                                                 # Conservamos la petición disponible para futuras tareas de trazabilidad

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "detail": str(exc),
        },
    )