from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app

# Configuración de la base de datos de pruebas
# Utilizamos SQLite en memoria para mantener las pruebas aisladas
# StaticPool permite reutilizar la misma conexión durante cada prueba
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)


# Fábrica de sesiones para pruebas
TestingSessionLocal = sessionmaker(                     # Creamos sesiones separadas de las utilizadas por la aplicación real
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False,                             # expire_on_commit=False permite consultar entidades después de confirmar cambios
)


# Sesión aislada por prueba
@pytest.fixture                                         # Creamos todas las tablas antes de cada escenario y las eliminamos después para evitar contaminación entre pruebas
def db_session() -> Generator[Session, None, None]:

    Base.metadata.create_all(                           # Creamos las tablas registradas en la metadata
        bind=test_engine,
    )

    session = TestingSessionLocal()                     # Abrimos una sesión conectada únicamente a la base de pruebas

    try:
        yield session                                    # Entregamos la sesión al escenario que la solicite
    finally:
        session.close()                                  # Cerramos la sesión antes de eliminar las tablas

        Base.metadata.drop_all(                         # Restablecemos completamente la base para la siguiente prueba
            bind=test_engine,
        )


# Cliente HTTP de pruebas
@pytest.fixture                                         # Sustituimos get_db para que la API utilice la sesión temporal y restauramos las dependencias al finalizar cada escenario
def client(
    db_session: Session,
) -> Generator[TestClient, None, None]:

    def override_get_db() -> Generator[Session, None, None]:    # Entregamos a FastAPI la sesión activa de la prueba

        yield db_session

    app.dependency_overrides[get_db] = override_get_db  # Reemplazamos la dependencia real únicamente durante esta prueba

    try:
        with TestClient(app) as test_client:            # Creamos el cliente que ejecutará las peticiones contra la aplicación
            yield test_client
    finally:
        app.dependency_overrides.clear()                # Eliminamos los reemplazos para no afectar pruebas posteriores