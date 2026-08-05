from pydantic import BaseModel


# Creamos un Schema de Pydantic, es decir, un contrato
# Representamos una lectura recibida desde un sensor
class ReadingCreate(BaseModel):                         # Solo existe para intercambiar datos con el cliente
    
    sensor_id: str
    value: float
    unit: str