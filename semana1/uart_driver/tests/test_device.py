import pytest

from semana1.uart_driver.config import UartConfig
from semana1.uart_driver.device import UartDevice
from semana1.uart_driver.parsers import ModbusParser, NMEAParser


def test_uart_device_stores_config_and_parser() -> None:                        # UartDevice almacene la configuración y el parser inyectados
    # Creamos las dependencias del dispositivo.
    config = UartConfig(
        port="COM3",
        baudrate=9600,
    )
    parser = ModbusParser()

    # Inyectamos la configuración y el parser.
    device = UartDevice(
        config=config,
        parser=parser,
    )

    # Verificamos que el dispositivo conserve sus dependencias.
    assert device.config == config
    assert device.parser is parser


def test_uart_device_processes_message_with_injected_parser() -> None:          # Comprueba que pueda procesar un mensaje usando el parser recibido
    # Configuramos el dispositivo para procesar mensajes NMEA.
    config = UartConfig(
        port="COM4",
        baudrate=4800,
    )
    device = UartDevice(
        config=config,
        parser=NMEAParser(),
    )

    result = device.process_message(
        b"$GPGGA,123519*47"
    )

    # Verificamos que el parser inyectado interprete el mensaje.
    assert result["protocol"] == "nmea"
    assert result["sentence_type"] == "GPGGA"
    assert result["checksum"] == "47"


def test_uart_device_rejects_empty_message() -> None:                          # Rechace mensajes vacíos antes de enviarlos al parser
    # Creamos un dispositivo con un parser válido.
    config = UartConfig(
        port="COM3",
        baudrate=9600,
    )
    device = UartDevice(
        config=config,
        parser=ModbusParser(),
    )

    # Verificamos que un mensaje vacío sea rechazado.
    with pytest.raises(
        ValueError,
        match="UART message cannot be empty",
    ):
        device.process_message(b"")