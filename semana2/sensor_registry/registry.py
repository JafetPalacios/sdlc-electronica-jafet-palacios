from dataclasses import dataclass


class DuplicateSensorError(ValueError):
    pass


class SensorNotFoundError(LookupError):
    pass


@dataclass(frozen=True)
class Sensor:
    identifier: str
    name: str


class SensorRegistry:
    def __init__(self) -> None:
        self._sensors: dict[str, Sensor] = {}

    def register(self, sensor: Sensor) -> None:
        self._ensure_identifier_is_available(sensor.identifier)
        self._sensors[sensor.identifier] = sensor

    def get(self, identifier: str) -> Sensor:
        try:
            return self._sensors[identifier]
        except KeyError as error:
            raise SensorNotFoundError(identifier) from error

    def count(self) -> int:
        return len(self._sensors)

    def _ensure_identifier_is_available(self, identifier: str) -> None:
        if identifier in self._sensors:
            raise DuplicateSensorError(identifier)
