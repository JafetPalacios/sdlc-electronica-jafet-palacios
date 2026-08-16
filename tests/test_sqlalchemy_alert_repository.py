from sqlalchemy.orm import Session

from app.models import Alert, Reading, Sensor
from app.repositories.sqlalchemy_alert_repository import (
    SqlAlchemyAlertRepository,
)


# Persistencia de una alerta mediante SQLAlchemy
def test_create_alert_persists_alert(
    db_session: Session,
) -> None:
    # Creamos primero las entidades requeridas por las llaves foráneas
    sensor = Sensor(
        code="TEMP-ALERT-DB-001",
        name="Sensor de temperatura con alerta",
        sensor_type="temperature",
        unit="°C",
        alert_threshold=30.0,
    )

    db_session.add(sensor)
    db_session.commit()
    db_session.refresh(sensor)

    reading = Reading(
        sensor_id=sensor.id,
        value=31.0,
    )

    db_session.add(reading)
    db_session.commit()
    db_session.refresh(reading)

    # Construimos la alerta que debe conservar el contexto de la anomalía
    alert = Alert(
        sensor_id=sensor.id,
        reading_id=reading.id,
        value=31.0,
        threshold=30.0,
    )

    repository = SqlAlchemyAlertRepository(db_session)

    created_alert = repository.create(alert)

    # Confirmamos que la persistencia haya generado los campos administrados por la base
    assert created_alert.id is not None
    assert created_alert.created_at is not None

    # Volvemos a consultar la entidad para verificar que quedó almacenada
    stored_alert = db_session.get(
        Alert,
        created_alert.id,
    )

    assert stored_alert is not None
    assert stored_alert.sensor_id == sensor.id
    assert stored_alert.reading_id == reading.id
    assert stored_alert.value == 31.0
    assert stored_alert.threshold == 30.0

# Consulta de alertas pertenecientes a un sensor
def test_list_alerts_for_sensor_returns_only_matching_alerts(
    db_session: Session,
) -> None:
    # Creamos dos sensores para comprobar que el repositorio filtre correctamente
    first_sensor = Sensor(
        code="TEMP-ALERT-LIST-001",
        name="Primer sensor con alertas",
        sensor_type="temperature",
        unit="°C",
        alert_threshold=30.0,
    )

    second_sensor = Sensor(
        code="TEMP-ALERT-LIST-002",
        name="Segundo sensor con alertas",
        sensor_type="temperature",
        unit="°C",
        alert_threshold=40.0,
    )

    db_session.add_all(
        [
            first_sensor,
            second_sensor,
        ]
    )
    db_session.commit()
    db_session.refresh(first_sensor)
    db_session.refresh(second_sensor)

    # Creamos una lectura para cada sensor
    first_reading = Reading(
        sensor_id=first_sensor.id,
        value=31.0,
    )

    second_reading = Reading(
        sensor_id=second_sensor.id,
        value=41.0,
    )

    db_session.add_all(
        [
            first_reading,
            second_reading,
        ]
    )
    db_session.commit()
    db_session.refresh(first_reading)
    db_session.refresh(second_reading)

    # Registramos una alerta asociada a cada sensor
    first_alert = Alert(
        sensor_id=first_sensor.id,
        reading_id=first_reading.id,
        value=31.0,
        threshold=30.0,
    )

    second_alert = Alert(
        sensor_id=second_sensor.id,
        reading_id=second_reading.id,
        value=41.0,
        threshold=40.0,
    )

    repository = SqlAlchemyAlertRepository(db_session)

    repository.create(first_alert)
    repository.create(second_alert)

    # Solicitamos únicamente las alertas del primer sensor
    alerts = repository.list_for_sensor(first_sensor.id)

    assert len(alerts) == 1
    assert alerts[0].id == first_alert.id
    assert alerts[0].sensor_id == first_sensor.id
    assert alerts[0].reading_id == first_reading.id
    assert alerts[0].value == 31.0
    assert alerts[0].threshold == 30.0