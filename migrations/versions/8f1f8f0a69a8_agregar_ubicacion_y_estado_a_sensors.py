"""Agregar ubicación y estado operativo a sensors"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# Identificadores utilizados por Alembic para mantener la cadena de revisiones
revision: str = "8f1f8f0a69a8"
down_revision: str | Sequence[str] | None = "ccdeecc8c528"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Agregar ubicación y estado operativo a los sensores"""

    # Agregar primero la ubicación permitiendo valores nulos para conservar
    # compatibilidad con sensores que ya existen en la base de datos
    op.add_column(
        "sensors",
        sa.Column(
            "location",
            sa.String(length=150),
            nullable=True,
        ),
    )

    # Completar los sensores históricos antes de exigir la ubicación
    op.execute(
        sa.text(
            """
            UPDATE sensors
            SET location = 'Ubicación no especificada'
            WHERE location IS NULL
            """
        )
    )

    # Convertir la ubicación en un dato obligatorio después de completar
    # todos los registros existentes
    with op.batch_alter_table("sensors") as batch_op:
        batch_op.alter_column(
            "location",
            existing_type=sa.String(length=150),
            nullable=False,
        )

    # Agregar el estado activo utilizando un default temporal para que
    # todos los sensores históricos permanezcan habilitados
    op.add_column(
        "sensors",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )

    # Retirar el default de migración para que el dominio siga siendo
    # responsable de definir el estado inicial de los sensores nuevos
    with op.batch_alter_table("sensors") as batch_op:
        batch_op.alter_column(
            "is_active",
            existing_type=sa.Boolean(),
            server_default=None,
        )


def downgrade() -> None:
    """Retirar ubicación y estado operativo de los sensores"""

    # Eliminar primero las columnas agregadas por esta revisión
    with op.batch_alter_table("sensors") as batch_op:
        batch_op.drop_column("is_active")
        batch_op.drop_column("location")