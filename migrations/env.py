from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Importamos la configuración central de base de datos y los modelos ORM de SensorHub
from app.db import DATABASE_URL, Base
from app.models import Alert, Reading, Sensor

# Conservamos referencias explícitas para dejar claro que estos modelos deben registrarse en Base.metadata
REGISTERED_MODELS = (Alert, Reading, Sensor)
# Obtenemos el objeto de configuración de Alembic
config = context.config

# Sobrescribimos la URL definida en alembic.ini con la configuración real de SensorHub
# Esto permite utilizar SQLite localmente o PostgreSQL mediante DATABASE_URL
config.set_main_option("sqlalchemy.url", DATABASE_URL)


# Configuramos el sistema de logging definido en alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Alembic utilizará estos metadatos para comparar los modelos ORM con el esquema real
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Ejecutamos las migraciones sin crear una conexión activa a la base de datos"""

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecutamos las migraciones utilizando una conexión activa a la base de datos"""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()