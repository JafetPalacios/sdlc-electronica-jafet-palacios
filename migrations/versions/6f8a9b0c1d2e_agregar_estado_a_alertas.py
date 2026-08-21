"""Agrega el estado a la tabla de alertas

Revision ID: 6f8a9b0c1d2e
Revises: 4a2c4f5d6e7b
Create Date: 2026-08-21 00:40:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# Identificadores utilizados por Alembic para mantener la cadena de revisiones
revision: str = "6f8a9b0c1d2e"
down_revision: str | Sequence[str] | None = "4a2c4f5d6e7b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Agregamos el estado operativo requerido por RF-5"""

    op.add_column(
        "alerts",
        sa.Column(
            "status",
            sa.Enum(
                "open",
                "acknowledged",
                "resolved",
                name="alertstatus",
                native_enum=False,
                create_constraint=True,
            ),
            nullable=False,
            server_default=sa.text("'open'"),
        ),
    )


def downgrade() -> None:
    """Eliminamos el estado de alertas al revertir esta revisión"""

    op.drop_column(
        "alerts",
        "status",
    )
