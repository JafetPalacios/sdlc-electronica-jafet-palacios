from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.dependencies import get_reading_service
from app.schemas import ReadingCreate, ReadingResponse, ReadingUpdate
from app.services.reading_service import ReadingService

# Configuración del router
# Agrupamos en este router todos los endpoints relacionados con lecturas
# No definimos un prefijo global porque algunas rutas dependen de sensores
# y otras trabajan directamente con el identificador de una lectura

router = APIRouter(
    tags=["Lecturas"],
)

# Dependencia del servicio
ReadingServiceDependency = Annotated[                                   # Indicamos a FastAPI que debe construir ReadingService mediante
    ReadingService,                                                     # get_reading_service cada vez que un endpoint lo requiera
    Depends(get_reading_service),                                       # Esto evita crear repositorios y sesiones directamente dentro del router
]


# Parámetros reutilizables de paginación
LimitQuery = Annotated[                                                 # Centralizamos sus restricciones para mantener el mismo comportamiento
    int,                                                                # en cualquier endpoint que necesite paginar resultados
    Query(
        ge=1,
        le=100,
        description="Cantidad máxima de lecturas devueltas",
    ),
]

OffsetQuery = Annotated[
    int,
    Query(
        ge=0,
        description="Cantidad de lecturas que se omiten",
    ),
]


# Parámetros reutilizables de filtrado temporal
StartDateQuery = Annotated[                                             # Exponemos los nombres públicos from y to en la URL
    datetime | None,                                                    # Internamente utilizamos start_date y end_date para conservar nombres claros
    Query(
        alias="from",
        description="Fecha y hora inicial inclusiva del filtro",
    ),
]

EndDateQuery = Annotated[
    datetime | None,
    Query(
        alias="to",
        description="Fecha y hora final inclusiva del filtro",
    ),
]


# Creación de lecturas: Registramos una lectura dentro del contexto de un sensor existente
@router.post(
    "/sensors/{sensor_id}/readings",
    response_model=ReadingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una lectura para un sensor",
    description=(
        "Registra una nueva lectura asociada al sensor indicado en la ruta "
        "y devuelve la lectura persistida con su identificador y fecha"
    ),
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "El sensor propietario no existe",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "El identificador o el valor recibido no son válidos",
        },
    },
)
def create_reading(
    sensor_id: int,
    reading_data: ReadingCreate,
    service: ReadingServiceDependency,
) -> ReadingResponse:                                           # Registramos una lectura para un sensor existente

    reading = service.create_reading(                           # Entregamos al servicio el identificador del sensor y los datos validados
        sensor_id,                                              # El servicio comprueba que el sensor exista antes de crear la lectura
        reading_data,
    )

    return ReadingResponse.model_validate(reading)              # Transformamos el modelo ORM al esquema público definido para la respuesta


# Consulta individual: Recuperamos una lectura concreta mediante su identificador interno
@router.get(
    "/readings/{reading_id}",
    response_model=ReadingResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener una lectura por identificador",
    description=(
        "Busca una lectura mediante su identificador interno "
        "y devuelve sus datos persistidos"
    ),
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "La lectura solicitada no existe",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "El identificador recibido no tiene un formato válido",
        },
    },
)
def get_reading(
    reading_id: int,
    service: ReadingServiceDependency,
) -> ReadingResponse:                                                   # Obtenemos una lectura mediante su identificador interno

    reading = service.get_reading(reading_id)                           # Delegamos la búsqueda y el control de inexistencia al servicio

    return ReadingResponse.model_validate(reading)                      # Devolvemos únicamente los campos definidos en el contrato público


# Actualización de lecturas: Permitimos modificar parcialmente una lectura existente. Solo se aplican los campos enviados explícitamente por el cliente
@router.patch(
    "/readings/{reading_id}",
    response_model=ReadingResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar parcialmente una lectura",
    description=(
        "Modifica únicamente los campos enviados de una lectura existente "
        "y devuelve su estado actualizado"
    ),
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "La lectura solicitada no existe",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": (
                "El identificador o los datos de actualización no son válidos"
            ),
        },
    },
)
def update_reading(
    reading_id: int,
    reading_data: ReadingUpdate,
    service: ReadingServiceDependency,
) -> ReadingResponse:                                                   # Actualizamos parcialmente una lectura existente

    reading = service.update_reading(                                   # Entregamos al servicio el identificador y los campos recibidos
        reading_id,                                                     # El servicio localiza la entidad, aplica los cambios y los persiste
        reading_data,
    )

    return ReadingResponse.model_validate(reading)                      # Convertimos la entidad actualizada al esquema público de respuesta


# Consulta paginada por sensor: Listamos las lecturas asociadas a un sensor concreto y permitimos filtrar por fecha y controlar la cantidad de resultados
@router.get(
    "/sensors/{sensor_id}/readings",
    response_model=list[ReadingResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar las lecturas de un sensor",
    description=(
        "Devuelve las lecturas asociadas a un sensor con paginación "
        "y filtros temporales opcionales"
    ),
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "La fecha inicial es posterior a la fecha final",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "El sensor solicitado no existe",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "Los parámetros recibidos no son válidos",
        },
    },
)
def list_readings_for_sensor(
    sensor_id: int,
    service: ReadingServiceDependency,
    limit: LimitQuery = 50,
    offset: OffsetQuery = 0,
    start_date: StartDateQuery = None,
    end_date: EndDateQuery = None,
) -> list[ReadingResponse]:                                         # Listamos lecturas de un sensor aplicando filtros y paginación

    readings = service.list_readings_for_sensor(                    # Delegamos al servicio la validación del sensor y del rango temporal
        sensor_id,                                                  # El repositorio se encarga después de aplicar filtros, orden y paginación
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset,
    )

    # Transformamos cada modelo ORM al esquema público de respuesta
    return [
        ReadingResponse.model_validate(reading)
        for reading in readings
    ]


# Eliminación de lecturas: Eliminamos una lectura concreta y respondemos sin cuerpo cuando la operación termina correctamente
@router.delete(
    "/readings/{reading_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una lectura",
    description=(
        "Elimina definitivamente una lectura mediante su identificador interno "
        "y devuelve una respuesta sin contenido"
    ),
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "La lectura fue eliminada correctamente",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "La lectura solicitada no existe",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "El identificador recibido no tiene un formato válido",
        },
    },
)
def delete_reading(
    reading_id: int,
    service: ReadingServiceDependency,
) -> None:                                                      # Eliminamos una lectura existente sin devolver contenido

    service.delete_reading(reading_id)                          # El servicio comprueba que la lectura exista antes de eliminarla