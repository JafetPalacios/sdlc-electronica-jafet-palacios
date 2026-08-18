"""Crea la tabla de alertas

Revision ID: ccdeecc8c528
Revises: b89c5db35c12
Create Date: 2026-08-15 22:37:08.784773
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# Identificadores utilizados por Alembic para mantener la cadena de revisiones
revision: str = "ccdeecc8c528"
down_revision: str | Sequence[str] | None = "b89c5db35c12"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Creamos la tabla utilizada para persistir alertas de lecturas anómalas"""

    op.create_table(
        "alerts",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "sensor_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "reading_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "value",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "threshold",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["reading_id"],
            ["readings.id"],
        ),
        sa.ForeignKeyConstraint(
            ["sensor_id"],
            ["sensors.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Eliminamos la tabla de alertas al revertir esta revisión"""

    op.drop_table("alerts")