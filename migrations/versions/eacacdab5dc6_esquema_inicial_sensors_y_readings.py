"""Migración inicial para crear las tablas sensors y readings"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# Identificadores utilizados por Alembic para ordenar el historial de migraciones
revision: str = "eacacdab5dc6"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Creamos el esquema inicial de SensorHub"""

    # Creamos primero sensors porque readings depende de esta tabla mediante una llave foránea
    op.create_table(
        "sensors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("sensor_type", sa.String(length=30), nullable=False),
        sa.Column("unit", sa.String(length=20), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Creamos un índice único para impedir códigos de sensor duplicados
    op.create_index(
        op.f("ix_sensors_code"),
        "sensors",
        ["code"],
        unique=True,
    )

    # Creamos readings después de sensors para poder establecer correctamente la llave foránea
    op.create_table(
        "readings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sensor_id", sa.Integer(), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["sensor_id"],
            ["sensors.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Revertimos completamente el esquema inicial de SensorHub"""

    # Eliminamos primero readings porque mantiene una referencia hacia sensors
    op.drop_table("readings")

    # Eliminamos el índice antes de retirar la tabla sensors
    op.drop_index(
        op.f("ix_sensors_code"),
        table_name="sensors",
    )

    op.drop_table("sensors")