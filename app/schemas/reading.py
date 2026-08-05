from pydantic import BaseModel


# Representamos una lectura recibida desde un sensor
class ReadingCreate(BaseModel):
    
    sensor_id: str
    value: float
    unit: str