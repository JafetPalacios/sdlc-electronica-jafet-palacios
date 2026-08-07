from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.dependencies import get_sensor_service
from app.schemas import SensorCreate, SensorResponse, SensorUpdate
from app.services.sensor_service import SensorService

# Configuración del router
# Agrupamos en este router todos los endpoints relacionados con sensores
# El prefijo /sensors se aplica automáticamente a cada ruta declarada aquí
# La etiqueta Sensores permite organizar estos endpoints dentro de Swagger

router = APIRouter(
    prefix="/sensors",
    tags=["Sensores"],
)


# Dependencia del servicio
SensorServiceDependency = Annotated[                                # Indicamos a FastAPI que debe construir SensorService mediante
    SensorService,                                                  # get_sensor_service cada vez que un endpoint lo requiera
    Depends(get_sensor_service),                                    # Esto evita crear repositorios y sesiones directamente dentro del router
]


# Consulta paginada de sensores: Recuperamos una colección de sensores aplicando límite y desplazamiento
# La paginación evita devolver todos los registros en una sola respuesta
@router.get(
    "/",
    response_model=list[SensorResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar sensores",
    description=(
        "Devuelve una colección paginada de sensores registrados "
        "ordenados por su identificador interno"
    ),
    responses={
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "Los parámetros de paginación no son válidos",
        },
    },
)
def list_sensors(
    service: SensorServiceDependency,
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
        description="Cantidad máxima de sensores devueltos",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Cantidad de sensores que se omiten",
    ),
) -> list[SensorResponse]:

    sensors = service.list_sensors(                                 # Solicitamos al servicio únicamente la página requerida
        limit=limit,                                                # limit determina cuántos registros se recuperan
        offset=offset,                                              # offset determina cuántos registros se omiten desde el inicio
    )

    # Transformamos cada modelo ORM al esquema público de respuesta
    return [
        SensorResponse.model_validate(sensor)
        for sensor in sensors
    ]


# Creación de sensores: Registramos un sensor nuevo después de validar que su código sea único
@router.post(
    "/",
    response_model=SensorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un sensor",
    description=(
        "Registra un sensor nuevo después de comprobar que su código público "
        "no esté siendo utilizado por otro sensor"
    ),
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "El código del sensor ya está registrado",
        },
       status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": (
                "Los datos enviados no cumplen el contrato de entrada "
                "o las reglas físicas de tipo y unidad"
            ),
        },
    },
)
def create_sensor(
    sensor_data: SensorCreate,
    service: SensorServiceDependency,
) -> SensorResponse:

    # Entregamos al servicio los datos previamente validados por Pydanti y l servicio verifica que el código sea único antes de persistir el sensor
    sensor = service.create_sensor(sensor_data)

    return SensorResponse.model_validate(sensor)                            # Convertimos el modelo ORM al esquema público expuesto por la API


# Consulta individual: Recuperamos un sensor concreto mediante su identificador interno
@router.get(
    "/{sensor_id}",
    response_model=SensorResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener un sensor",
    description=(
        "Busca un sensor mediante su identificador interno "
        "y devuelve sus datos persistidos"
    ),
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "El sensor solicitado no existe",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "El identificador recibido no tiene un formato válido",
        },
    },
)
def get_sensor(
    sensor_id: int,
    service: SensorServiceDependency,
) -> SensorResponse:

    sensor = service.get_sensor(sensor_id)                                  # Delegamos la búsqueda y el control de inexistencia al servicio
    return SensorResponse.model_validate(sensor)                            # Transformamos el modelo ORM al esquema público de respuesta


# Actualización de sensores: Permitimos modificar parcialmente un sensor existente, solo se aplican los campos enviados explícitamente por el cliente
@router.patch(
    "/{sensor_id}",
    response_model=SensorResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar parcialmente un sensor",
    description=(
        "Modifica únicamente los campos enviados de un sensor existente "
        "y conserva sin cambios los campos omitidos"
    ),
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "El sensor solicitado no existe",
        },
        status.HTTP_409_CONFLICT: {
            "description": "El nuevo código ya pertenece a otro sensor",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": (
                "Los datos enviados no cumplen el contrato de actualización "
                "o la combinación final de tipo y unidad no es válida"
            ),
        },
    },
)
def update_sensor(
    sensor_id: int,
    sensor_data: SensorUpdate,
    service: SensorServiceDependency,
) -> SensorResponse:

    # Entregamos al servicio el identificador y los campos recibidos
    # El servicio valida existencia, que sea unico y persistencia de los cambios
    sensor = service.update_sensor(
        sensor_id,
        sensor_data,
    )

    return SensorResponse.model_validate(sensor)                        # Convertimos la entidad actualizada al esquema público de respuesta


# Eliminación de sensores: Eliminamos un sensor únicamente cuando no conserva lecturas asociada. Esta restricción evita perder información histórica relacionada
@router.delete(
    "/{sensor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un sensor",
    description=(
        "Elimina definitivamente un sensor existente únicamente cuando "
        "no conserva lecturas asociadas"
    ),
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "El sensor fue eliminado correctamente",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "El sensor solicitado no existe",
        },
        status.HTTP_409_CONFLICT: {
            "description": "El sensor conserva lecturas y no puede eliminarse",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "El identificador recibido no tiene un formato válido",
        },
    },
)
def delete_sensor(
    sensor_id: int,
    service: SensorServiceDependency,
) -> None:

    # El servicio comprueba que el sensor exista y que no tenga lecturas
    # Si ambas condiciones se cumplen delega la eliminación al repositorio
    service.delete_sensor(sensor_id)