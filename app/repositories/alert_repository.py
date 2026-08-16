from typing import Protocol

from app.models import Alert


# Contrato de persistencia para alertas
# Permitimos que el servicio dependa de una abstracción y no de SQLAlchemy
class AlertRepository(Protocol):

    # Registramos una alerta y devolvemos su estado persistido
    def create(self, alert: Alert) -> Alert:

        ...

        # Recuperamos las alertas registradas para un sensor concreto
    def list_for_sensor(self, sensor_id: int) -> list[Alert]:

        ...