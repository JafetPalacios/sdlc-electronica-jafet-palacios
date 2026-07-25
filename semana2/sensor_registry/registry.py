"""Modelos y operaciones para administrar un registro de sensores.

El módulo define el modelo inmutable de un sensor, las excepciones propias
del dominio y el registro responsable de almacenar, consultar y eliminar
sensores mediante identificadores únicos.
"""

from dataclasses import dataclass


class DuplicateSensorError(ValueError):
    """Indica que se intentó registrar un identificador ya utilizado."""


class SensorNotFoundError(LookupError):
    """Indica que el sensor solicitado no existe en el registro."""


@dataclass(frozen=True)
class Sensor:
    """Representa un sensor identificado de manera única.

    Attributes:
        identifier: Identificador único utilizado para registrar el sensor.
        name: Nombre descriptivo del sensor.
    """

    identifier: str
    name: str


class SensorRegistry:
    """Administra sensores mediante identificadores únicos."""

    def __init__(self) -> None:
        """Inicializa un registro de sensores vacío."""
        self._sensors: dict[str, Sensor] = {}

    def register(self, sensor: Sensor) -> None:
        """Registra un sensor.

        Args:
            sensor: Sensor que queremos incorporar al registro.

        Raises:
            DuplicateSensorError: Si el identificador ya está registrado.
        """
        self._ensure_identifier_is_available(sensor.identifier)
        self._sensors[sensor.identifier] = sensor

    def get(self, identifier: str) -> Sensor:
        """Obtiene un sensor mediante su identificador.

        Args:
            identifier: Identificador del sensor que queremos consultar.

        Returns:
            El sensor asociado al identificador recibido.

        Raises:
            SensorNotFoundError: Si no existe un sensor con ese identificador.
        """
        try:
            return self._sensors[identifier]
        except KeyError as error:
            # Convertimos el error interno en una excepción del dominio.
            raise SensorNotFoundError(identifier) from error

    def remove(self, identifier: str) -> None:
        """Elimina un sensor mediante su identificador.

        Args:
            identifier: Identificador del sensor que queremos eliminar.

        Raises:
            SensorNotFoundError: Si no existe un sensor con ese identificador.
        """
        try:
            del self._sensors[identifier]
        except KeyError as error:
            # Mantenemos el mismo contrato de error utilizado por get().
            raise SensorNotFoundError(identifier) from error

    def count(self) -> int:
        """Devuelve la cantidad actual de sensores registrados."""
        return len(self._sensors)

    def _ensure_identifier_is_available(self, identifier: str) -> None:
        """Comprueba que un identificador pueda utilizarse.

        Args:
            identifier: Identificador que queremos validar.

        Raises:
            DuplicateSensorError: Si el identificador ya está registrado.
        """
        if identifier in self._sensors:
            raise DuplicateSensorError(identifier)
