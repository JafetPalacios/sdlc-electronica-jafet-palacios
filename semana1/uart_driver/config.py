# Configuración necesaria para comunicarse por UART
# Evita pasar parámetros sueltos por todo el programa

from dataclasses import dataclass

@dataclass(frozen=True)
class UartConfig:
    port: str                                                           # Guardamos el nombre del puerto serial
    baudrate: int                                                       # Guardamos la velocidad de comunicación en bits por segundo

    def __post_init__(self) -> None:
        # Rechazamos velocidades iguales o menores que cero.
        if self.baudrate <= 0:
            raise ValueError("Baudrate must be greater than zero")