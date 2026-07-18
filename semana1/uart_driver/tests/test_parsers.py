import pytest

from semana1.uart_driver.parsers import (
    MessageParser,
    ModbusParser,
    NMEAParser,
)

def test_message_parser_cannot_be_instantiated() -> None:                               # Debe fallar porque parse() es abstracto
    # Verificamos que la clase abstracta no pueda crearse directamente.
    with pytest.raises(TypeError):
        MessageParser()


def test_incomplete_parser_cannot_be_instantiated() -> None:                            # Hereda de MessageParser pero no implementa parse() Por eso tampoco puede crearse.
    # Creamos una clase hija que no implementa el método obligatorio.
    class IncompleteParser(MessageParser):
        pass

    # Verificamos que siga siendo abstracta.
    with pytest.raises(TypeError):
        IncompleteParser()


def test_concrete_parser_can_be_instantiated() -> None:                                # Implementa parse() y por eso puede crearse
    # Creamos una implementación mínima del contrato.
    class ConcreteParser(MessageParser):
        def parse(self, message: bytes) -> dict[str, object]:
            return {
                "message": message,
            }

    parser = ConcreteParser()
    result = parser.parse(b"test")

    # Verificamos que la implementación concreta funcione.
    assert result == {
        "message": b"test",
    }


def test_modbus_parser_extracts_address_and_function_code() -> None:                   # Comprueba la dirección y el código de función
    parser = ModbusParser()                                                            # Creamos el parser y procesamos una trama válida
    result = parser.parse(b"\x01\x03\x00\x10")

    # Verificamos los campos principales de la trama
    assert result["protocol"] == "modbus"
    assert result["address"] == 1
    assert result["function_code"] == 3


def test_modbus_parser_preserves_data_bytes() -> None:                                # Comprueba que los datos restantes no se pierdan
    parser = ModbusParser()                                                           # Verificamos que conservemos los bytes posteriores al encabezado
    result = parser.parse(b"\x02\x06\x00\x20")
    assert result["data"] == b"\x00\x20"


def test_modbus_parser_rejects_short_message() -> None:                              # Comprueba que una trama incompleta produzca ValueError
    parser = ModbusParser()                                                          # Verificamos que una trama incompleta sea rechazada

    with pytest.raises(
        ValueError,
        match="Modbus message must contain at least 2 bytes",
    ):
        parser.parse(b"\x01")


def test_nmea_parser_extracts_sentence_type_and_fields() -> None:                   # Extrai correctamente el tipo de sentencia y sus campos
    parser = NMEAParser()                                                           # Procesamos una sentencia NMEA válida
    result = parser.parse(
        b"$GPGGA,123519,4807.038,N,01131.000,E*47"
    )

    # Verificamos el protocolo y el tipo de sentencia
    assert result["protocol"] == "nmea"
    assert result["sentence_type"] == "GPGGA"

    # Verificamos los campos separados por comas
    assert result["fields"] == [
        "123519",
        "4807.038",
        "N",
        "01131.000",
        "E",
    ]


def test_nmea_parser_extracts_optional_checksum() -> None:                          # Que el checksum sea opcional y se almacene cuando existe
    parser = NMEAParser()                                                           # Verificamos una sentencia con checksum
    result_with_checksum = parser.parse(
        b"$GPGGA,123519*47"
    )

    assert result_with_checksum["checksum"] == "47"

    # Verificamos una sentencia sin checksum
    result_without_checksum = parser.parse(
        b"$GPGGA,123519"
    )

    assert result_without_checksum["checksum"] is None


def test_nmea_parser_rejects_message_without_dollar_sign() -> None:                 # Que una sentencia sin $ sea rechazada
    # Verificamos que una sentencia sin el símbolo inicial sea rechazada
    parser = NMEAParser()

    with pytest.raises(
        ValueError,
        match=r"NMEA message must start with '\$'",
    ):
        parser.parse(b"GPGGA,123519")