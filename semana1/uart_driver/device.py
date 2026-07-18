from semana1.uart_driver.config import UartConfig
from semana1.uart_driver.parsers import MessageParser


class UartDevice:
    def __init__(
        self,
        config: UartConfig,
        parser: MessageParser,
    ) -> None:
        self.config = config                                                # Guardamos la configuración del dispositivo
        self.parser = parser                                                # Guardamos el parser que interpretará los mensajes

    def process_message(self, message: bytes) -> dict[str, object]:
        # Rechazamos mensajes vacíos antes de enviarlos al parser
        if not message:
            raise ValueError("UART message cannot be empty")

        return self.parser.parse(message)                                   # Delegamos la interpretación al parser inyectado