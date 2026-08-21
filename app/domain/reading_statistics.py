from dataclasses import dataclass


# Representamos estadísticas agregadas de lecturas para un sensor y periodo
@dataclass(frozen=True)
class ReadingStatistics:

    sensor_id: int
    count: int
    minimum_value: float | None
    maximum_value: float | None
    average_value: float | None
