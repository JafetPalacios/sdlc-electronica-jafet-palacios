# Prueba básica de transacciones con SQLAlchemy
from app.db import SessionLocal
from app.models import Sensor

db = SessionLocal()                             # Creamos una nueva sesión

try:
    # Creamos el primer sensor
    sensor_1 = Sensor(
        code="TEMP-001",
        name="Sensor 1",
        sensor_type="temperature",
        unit="°C",
    )

    # Creamos un segundo sensor con el mismo código
    # Esto provocará un error porque code es UNIQUE
    sensor_2 = Sensor(
        code="TEMP-001",
        name="Sensor 2",
        sensor_type="temperature",
        unit="°C",
    )

    # Agregamos ambos objetos a la sesión
    db.add(sensor_1)
    db.add(sensor_2)

    db.commit()                                 # Intentamos confirmar la transacción

except Exception as error:
   
    db.rollback()                               # Si ocurre cualquier error, revertimos completamente la transacción

    print("Transacción cancelada")
    print(type(error).__name__)
    print(error)

finally:
    
    db.close()                                  # Cerramos la sesión independientemente del resultado