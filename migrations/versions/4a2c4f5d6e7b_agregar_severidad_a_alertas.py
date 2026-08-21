"""Agrega la severidad a la tabla de alertas

Revision ID: 4a2c4f5d6e7b
Revises: 8f1f8f0a69a8
Create Date: 2026-08-20 16:25:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# Identificadores utilizados por Alembic para mantener la cadena de revisiones
revision: str = "4a2c4f5d6e7b"
down_revision: str | Sequence[str] | None = "8f1f8f0a69a8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Agregamos la severidad requerida para clasificar alertas"""

    op.add_column(
        "alerts",
        sa.Column(
            "severity",
            sa.Enum(
                "WARNING",
                "CRITICAL",
                name="alertseverity",
                native_enum=False,
                create_constraint=True,
            ),
            nullable=False,
            server_default=sa.text("'WARNING'"),
        ),
    )


def downgrade() -> None:
    """Eliminamos la severidad al revertir esta revisión"""

    op.drop_column(
        "alerts",
        "severity",
    )
