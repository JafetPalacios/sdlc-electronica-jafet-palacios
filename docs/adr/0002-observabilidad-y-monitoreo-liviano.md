# ADR 0002: Observabilidad y monitoreo liviano

## Estado

Aceptado

## Contexto

SensorHub debía cubrir tres necesidades operativas relacionadas pero distintas:

- exponer una comprobación simple de vida del proceso
- ofrecer métricas básicas del servicio
- dejar trazabilidad legible por máquinas sobre el tráfico HTTP

El proyecto ya contaba con `FastAPI`, middleware HTTP propio y validaciones automáticas en CI, pero no tenía una decisión formal sobre cómo distinguir `liveness`, métricas y logging estructurado.

También existían restricciones de alcance relevantes:

- no volver pesado `/health` con consultas innecesarias a base de datos
- no introducir dependencias nuevas sólo para logging o métricas básicas
- mantener la solución coherente con la arquitectura existente
- permitir observabilidad útil tanto en desarrollo como en CI/CD y producción

Como alternativa se consideró incorporar una solución de observabilidad más completa con librerías externas para métricas y logging estructurado.
Esa opción podría aportar integración inmediata con ecosistemas más amplios, pero agregaría dependencia adicional, mayor configuración y más superficie de mantenimiento para un requisito que sólo exigía monitoreo básico.

## Decisión

Se adopta una estrategia de observabilidad liviana con tres decisiones explícitas:

- `GET /health` se mantiene como `liveness` del proceso y no consulta la base de datos
- `GET /metrics` expone métricas básicas del proceso y de peticiones HTTP en texto plano con formato compatible con Prometheus simple
- la aplicación emite un evento estructurado JSON por petición HTTP completada y por error no controlado, utilizando únicamente la librería estándar de Python

La configuración operativa de esta observabilidad se controla por entorno:

- `DATABASE_URL` para la conexión a base de datos
- `PORT` para el arranque en contenedor
- `LOG_LEVEL` para el nivel del logger estructurado

## Consecuencias

### Ventajas

- `/health` permanece rápido y estable como señal de vida del proceso
- `/metrics` puede consumirse fácilmente desde automatizaciones y herramientas de monitoreo
- los logs JSON permiten filtrar y procesar eventos por campos como `path`, `status_code` o `duration_ms`
- la solución evita dependencias nuevas y mantiene bajo el costo operativo
- la observabilidad queda integrada en el mismo middleware que ya registraba métricas

### Costes

- las métricas viven en memoria y se reinician cuando el proceso se reinicia
- no se expone un readiness check profundo contra dependencias externas
- la estrategia de logging es deliberadamente básica y no reemplaza una plataforma completa de observabilidad
- si en el futuro se requieren trazas distribuidas o métricas más avanzadas, será necesario ampliar esta decisión
