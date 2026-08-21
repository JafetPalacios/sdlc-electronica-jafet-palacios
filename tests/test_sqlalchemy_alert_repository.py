from sqlalchemy.orm import Session

from app.domain.alert_lifecycle import AlertStatus
from app.domain.alert_strategy import AlertSeverity
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
        location="Laboratorio de electrónica",
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
        severity=AlertSeverity.WARNING,
        status=AlertStatus.OPEN,
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
    assert stored_alert.severity == AlertSeverity.WARNING
    assert stored_alert.status == AlertStatus.OPEN


# Consulta de alertas pertenecientes a un sensor
def test_list_alerts_for_sensor_returns_only_matching_alerts(
    db_session: Session,
) -> None:
    # Creamos dos sensores para comprobar que el repositorio filtre correctamente
    first_sensor = Sensor(
        code="TEMP-ALERT-LIST-001",
        name="Primer sensor con alertas",
        location="Laboratorio de electrónica",
        sensor_type="temperature",
        unit="°C",
        alert_threshold=30.0,
    )

    second_sensor = Sensor(
        code="TEMP-ALERT-LIST-002",
        name="Segundo sensor con alertas",
        location="Laboratorio de electrónica",
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
        severity=AlertSeverity.WARNING,
        status=AlertStatus.OPEN,
    )

    second_alert = Alert(
        sensor_id=second_sensor.id,
        reading_id=second_reading.id,
        value=41.0,
        threshold=40.0,
        severity=AlertSeverity.CRITICAL,
        status=AlertStatus.OPEN,
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
    assert alerts[0].severity == AlertSeverity.WARNING
    assert alerts[0].status == AlertStatus.OPEN


# Consulta de alertas activas
def test_list_active_alerts_returns_only_unresolved_alerts(
    db_session: Session,
) -> None:
    first_sensor = Sensor(
        code="TEMP-ALERT-ACTIVE-DB-001",
        name="Sensor con alerta abierta",
        location="Laboratorio de electrónica",
        sensor_type="temperature",
        unit="°C",
        alert_threshold=30.0,
    )
    second_sensor = Sensor(
        code="TEMP-ALERT-ACTIVE-DB-002",
        name="Sensor con alerta reconocida",
        location="Laboratorio de electrónica",
        sensor_type="temperature",
        unit="°C",
        alert_threshold=30.0,
    )
    third_sensor = Sensor(
        code="TEMP-ALERT-ACTIVE-DB-003",
        name="Sensor con alerta resuelta",
        location="Laboratorio de electrónica",
        sensor_type="temperature",
        unit="°C",
        alert_threshold=30.0,
    )

    db_session.add_all(
        [
            first_sensor,
            second_sensor,
            third_sensor,
        ]
    )
    db_session.commit()
    db_session.refresh(first_sensor)
    db_session.refresh(second_sensor)
    db_session.refresh(third_sensor)

    first_reading = Reading(
        sensor_id=first_sensor.id,
        value=31.0,
    )
    second_reading = Reading(
        sensor_id=second_sensor.id,
        value=32.0,
    )
    third_reading = Reading(
        sensor_id=third_sensor.id,
        value=33.0,
    )

    db_session.add_all(
        [
            first_reading,
            second_reading,
            third_reading,
        ]
    )
    db_session.commit()
    db_session.refresh(first_reading)
    db_session.refresh(second_reading)
    db_session.refresh(third_reading)

    repository = SqlAlchemyAlertRepository(db_session)

    repository.create(
        Alert(
            sensor_id=first_sensor.id,
            reading_id=first_reading.id,
            value=31.0,
            threshold=30.0,
            severity=AlertSeverity.WARNING,
            status=AlertStatus.OPEN,
        )
    )
    repository.create(
        Alert(
            sensor_id=second_sensor.id,
            reading_id=second_reading.id,
            value=32.0,
            threshold=30.0,
            severity=AlertSeverity.WARNING,
            status=AlertStatus.ACKNOWLEDGED,
        )
    )
    repository.create(
        Alert(
            sensor_id=third_sensor.id,
            reading_id=third_reading.id,
            value=33.0,
            threshold=30.0,
            severity=AlertSeverity.CRITICAL,
            status=AlertStatus.RESOLVED,
        )
    )

    alerts = repository.list_active()

    assert [alert.status for alert in alerts] == [
        AlertStatus.OPEN,
        AlertStatus.ACKNOWLEDGED,
    ]


# Persistencia de cambio de estado
def test_update_alert_persists_status_change(
    db_session: Session,
) -> None:
    sensor = Sensor(
        code="TEMP-ALERT-UPDATE-DB-001",
        name="Sensor para cambio de estado",
        location="Laboratorio de electrónica",
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

    repository = SqlAlchemyAlertRepository(db_session)

    alert = repository.create(
        Alert(
            sensor_id=sensor.id,
            reading_id=reading.id,
            value=31.0,
            threshold=30.0,
            severity=AlertSeverity.WARNING,
            status=AlertStatus.OPEN,
        )
    )

    alert.status = AlertStatus.ACKNOWLEDGED

    updated_alert = repository.update(alert)
    persisted_alert = repository.get_by_id(alert.id)

    assert updated_alert.status == AlertStatus.ACKNOWLEDGED
    assert persisted_alert is not None
    assert persisted_alert.status == AlertStatus.ACKNOWLEDGED
