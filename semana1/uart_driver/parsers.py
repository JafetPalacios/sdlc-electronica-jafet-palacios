from abc import ABC, abstractmethod

class MessageParser(ABC):
    @abstractmethod
    def parse(self, message: bytes) -> dict[str, object]:                       # Declaramos la operación que deberán implementar los parsers
        ...

class ModbusParser(MessageParser):
    def parse(self, message: bytes) -> dict[str, object]:
        # Validamos que existan al menos la dirección y el código de función
        if len(message) < 2:
            raise ValueError("Modbus message must contain at least 2 bytes")

        address = message[0]                                                   # Extraemos la dirección del dispositivo desde el primer byte
        function_code = message[1]                                             # Extraemos el código de función desde el segundo byte
        data = message[2:]                                                     # Conservamos los bytes restantes como datos de la trama

        return {
            "protocol": "modbus",
            "address": address,
            "function_code": function_code,
            "data": data,
        }
    
class NMEAParser(MessageParser):
    def parse(self, message: bytes) -> dict[str, object]:
        # Convertimos los bytes recibidos a texto ASCII.
        try:
            sentence = message.decode("ascii").strip()
        except UnicodeDecodeError as error:
            raise ValueError("NMEA message must contain ASCII text") from error

        # Verificamos que la sentencia comience con el símbolo requerido.
        if not sentence.startswith("$"):
            raise ValueError("NMEA message must start with '$'")

        body = sentence[1:]                                                     # Eliminamos el símbolo inicial
        content, separator, checksum = body.partition("*")                      # Separamos el contenido y el checksum opcional
        parts = content.split(",")                                              # Separamos los campos mediante comas
        sentence_type = parts[0]                                                # El primer campo identifica el tipo de sentencia

        if not sentence_type:
            raise ValueError("NMEA sentence type is required")

        return {
            "protocol": "nmea",
            "sentence_type": sentence_type,
            "fields": parts[1:],
            "checksum": checksum if separator else None,
        }
    
