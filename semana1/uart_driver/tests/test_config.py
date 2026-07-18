import pytest

from dataclasses import FrozenInstanceError
from semana1.uart_driver.config import UartConfig


def test_uart_config_stores_valid_values() -> None:
    # Creamos una configuración UART válida.
    config = UartConfig(
        port="COM3",
        baudrate=9600,
    )

    # Verificamos que almacene correctamente sus valores.
    assert config.port == "COM3"
    assert config.baudrate == 9600


def test_uart_config_rejects_invalid_baudrate() -> None:
    # Verificamos que un baudrate igual a cero sea rechazado.
    with pytest.raises(ValueError):
        UartConfig(
            port="COM3",
            baudrate=0,
        )


def test_uart_config_is_immutable() -> None:
    # Creamos una configuración válida.
    config = UartConfig(
        port="COM3",
        baudrate=9600,
    )

    # Verificamos que no pueda modificarse después de crearla.
    with pytest.raises(FrozenInstanceError):
        setattr(config, "baudrate", 115200)