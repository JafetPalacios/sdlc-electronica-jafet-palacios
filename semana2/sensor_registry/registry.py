from dataclasses import dataclass


@dataclass(frozen=True)
class Sensor:
    identifier: str
    name: str


class SensorRegistry:
    def __init__(self) -> None:
        self._sensors: dict[str, Sensor] = {}

    def register(self, sensor: Sensor) -> None:
        self._sensors[sensor.identifier] = sensor

    def get(self, identifier: str) -> Sensor:
        return self._sensors[identifier]
