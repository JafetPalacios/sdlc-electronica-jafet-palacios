from pydantic import BaseModel, Field


# Representa los datos necesarios para registrar un sensor
class SensorCreate(BaseModel):
    
    code: str = Field(min_length=1, max_length=50)              # Limitamos el código para evitar identificadores vacíos o excesivamente largos
    name: str = Field(min_length=1, max_length=100)             # Definimos un nombre legible para identificar el sensor
    sensor_type: str = Field(min_length=1, max_length=30)       # Guardamos el tipo como texto hasta incorporar la validación física completa
    unit: str = Field(min_length=1, max_length=20)              # Guardamos la unidad declarada por el sensor