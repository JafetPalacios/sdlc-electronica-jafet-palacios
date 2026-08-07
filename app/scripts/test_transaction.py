# Prueba manual de transacciones con SQLAlchemy
# Verificamos que una operación con varios INSERT se revierta por completo
# cuando uno de los registros viola una restricción de la base de datos

from app.db import SessionLocal
from app.models import Sensor

# Apertura de la sesión
# Creamos una sesión independiente para ejecutar esta prueba manual
# La sesión concentra los cambios hasta que confirmamos o revertimos la transacción

db = SessionLocal()

try:
    # Primer sensor
    sensor_1 = Sensor(                                              # Este registro utiliza el código TEMP-001 y puede insertarse correctamente
        code="TEMP-001",                                            # mientras no exista previamente otro sensor con el mismo código
        name="Sensor 1",
        sensor_type="temperature",
        unit="°C",
    )

    # Segundo sensor
    sensor_2 = Sensor(                                              # Reutilizamos intencionalmente el código TEMP-001
        code="TEMP-001",                                            # Esto viola la restricción UNIQUE definida sobre Sensor.code
        name="Sensor 2",
        sensor_type="temperature",
        unit="°C",
    )

    # Registro de cambios pendientes
    db.add(sensor_1)                                                # Añadimos ambos modelos a la misma sesión
    db.add(sensor_2)

    # Confirmación de la transacción
    db.commit()                                                     # SQLAlchemy intenta ejecutar ambos INSERT como parte de una misma transacción
                                                                    # La restricción UNIQUE del segundo sensor provoca que commit genere una excepción
# Reversión de la transacción
except Exception as error:                                          # Cancelamos todos los cambios pendientes cuando ocurre cualquier error
                                                                    # Esto evita que la sesión permanezca en estado fallido y garantiza atomicidad
    db.rollback()

    print("Transacción cancelada")
    print(type(error).__name__)
    print(error)

# Cierre de la sesión
finally:

    db.close()                                                      # Liberamos la conexión independientemente de que commit tenga éxito o falle