from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Alert
from app.repositories.alert_repository import AlertRepository


# Implementación concreta del repositorio de alertas
# Utilizamos SQLAlchemy sin exponer detalles de persistencia al servicio
class SqlAlchemyAlertRepository(AlertRepository):

    # Recibimos la sesión utilizada durante la operación actual
    def __init__(self, db: Session) -> None:

        self._db = db

    # Registramos una alerta y recuperamos los valores generados por la base
    def create(self, alert: Alert) -> Alert:

        self._db.add(alert)
        self._db.commit()
        self._db.refresh(alert)

        return alert

        # Recuperamos las alertas pertenecientes al sensor solicitado
    def list_for_sensor(self, sensor_id: int) -> list[Alert]:

        statement = (
            select(Alert)
            .where(
                Alert.sensor_id == sensor_id,
            )
            .order_by(
                Alert.created_at,
                Alert.id,
            )
        )

        # Convertimos el resultado de SQLAlchemy en una lista independiente
        return list(self._db.scalars(statement).all())