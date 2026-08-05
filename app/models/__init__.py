# Exponemos los modelos ORM desde un único punto de importación
from app.models.reading import Reading
from app.models.sensor import Sensor

# Definimos explícitamente los modelos públicos del paquete
__all__ = ["Reading", "Sensor"]