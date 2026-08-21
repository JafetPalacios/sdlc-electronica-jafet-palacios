from collections import defaultdict
from dataclasses import dataclass
from threading import Lock
from time import monotonic


@dataclass(frozen=True)
class HttpMetricKey:

    method: str
    path: str
    status_code: int


# Métricas básicas del servicio expuestas mediante un formato compatible con Prometheus
class ServiceMetrics:

    def __init__(self) -> None:

        self._lock = Lock()
        self.reset()

    # Reiniciamos el estado para mantener pruebas aisladas
    def reset(self) -> None:

        with self._lock:
            self._started_at = monotonic()
            self._requests_total: defaultdict[HttpMetricKey, int] = defaultdict(int)
            self._request_duration_count: defaultdict[HttpMetricKey, int] = defaultdict(int)
            self._request_duration_sum: defaultdict[HttpMetricKey, float] = defaultdict(float)

    # Registramos una observación por petición completada
    def record_request(
        self,
        *,
        method: str,
        path: str,
        status_code: int,
        duration_seconds: float,
    ) -> None:

        key = HttpMetricKey(
            method=method,
            path=path,
            status_code=status_code,
        )

        with self._lock:
            self._requests_total[key] += 1
            self._request_duration_count[key] += 1
            self._request_duration_sum[key] += duration_seconds

    # Serializamos las métricas en texto plano
    def render_prometheus(self) -> str:

        with self._lock:
            uptime_seconds = monotonic() - self._started_at
            requests_total = dict(self._requests_total)
            request_duration_count = dict(self._request_duration_count)
            request_duration_sum = dict(self._request_duration_sum)

        keys = sorted(
            requests_total,
            key=lambda metric_key: (
                metric_key.method,
                metric_key.path,
                metric_key.status_code,
            ),
        )

        lines = [
            "# HELP sensorhub_uptime_seconds Tiempo de actividad del proceso",
            "# TYPE sensorhub_uptime_seconds gauge",
            f"sensorhub_uptime_seconds {uptime_seconds:.6f}",
            "# HELP sensorhub_http_requests_total Total de peticiones HTTP completadas",
            "# TYPE sensorhub_http_requests_total counter",
            "# HELP sensorhub_http_request_duration_seconds_count Cantidad de observaciones de latencia HTTP",
            "# TYPE sensorhub_http_request_duration_seconds_count counter",
            "# HELP sensorhub_http_request_duration_seconds_sum Suma acumulada de latencia HTTP",
            "# TYPE sensorhub_http_request_duration_seconds_sum counter",
        ]

        for key in keys:
            labels = self._format_labels(key)
            lines.append(
                f"sensorhub_http_requests_total{{{labels}}} "
                f"{requests_total[key]}"
            )
            lines.append(
                f"sensorhub_http_request_duration_seconds_count{{{labels}}} "
                f"{request_duration_count[key]}"
            )
            lines.append(
                f"sensorhub_http_request_duration_seconds_sum{{{labels}}} "
                f"{request_duration_sum[key]:.6f}"
            )

        return "\n".join(lines) + "\n"

    # Escapamos etiquetas siguiendo el formato de exposición de Prometheus
    def _format_labels(
        self,
        key: HttpMetricKey,
    ) -> str:

        return (
            f'method="{self._escape_label_value(key.method)}",'
            f'path="{self._escape_label_value(key.path)}",'
            f'status_code="{key.status_code}"'
        )

    def _escape_label_value(
        self,
        value: str,
    ) -> str:

        return value.replace("\\", "\\\\").replace('"', '\\"')


service_metrics = ServiceMetrics()
