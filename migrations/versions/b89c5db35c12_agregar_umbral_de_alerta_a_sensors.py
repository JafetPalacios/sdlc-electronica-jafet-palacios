"""Agrega el umbral de alerta configurable a sensors"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# Identificadores utilizados por Alembic para ordenar el historial de migraciones
revision: str = "b89c5db35c12"
down_revision: str | Sequence[str] | None = "eacacdab5dc6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Agregamos el umbral configurable a la tabla sensors"""

    # Conservamos la columna nullable para mantener compatibles los sensores existentes
    op.add_column(
        "sensors",
        sa.Column(
            "alert_threshold",
            sa.Float(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Eliminamos el umbral configurable de la tabla sensors"""

    op.drop_column(
        "sensors",
        "alert_threshold",
    )