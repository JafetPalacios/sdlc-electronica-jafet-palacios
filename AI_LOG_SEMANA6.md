## RF-1 — Gestión del ciclo de vida de sensores

Se establece que los sensores deben incluir ubicación y umbral de alerta y que, en un entorno de producción, no deben eliminarse físicamente sino desactivarse. Se decidió adaptar el comportamiento existente para conservar los sensores y su información histórica mediante un estado operativo `is_active`, eliminando la operación de borrado físico del flujo público de la API. También se decidió que un sensor desactivado debe continuar disponible para consulta, pero no debe aceptar nuevas lecturas.

### Consulta realizada a la IA

Se solicitó apoyo para revisar la implementación existente de SensorHub frente a RF-1, identificar las diferencias con el requisito final y realizar la adaptación mediante un flujo incremental basado en pruebas.

La IA identificó que la implementación existente ya tenía CRUD parcial y `alert_threshold`, pero presentaba las siguientes diferencias respecto a RF-1:

- el modelo no almacenaba la ubicación física del sensor
- no existía un estado para representar sensores desactivados
- la API permitía eliminar sensores físicamente
- la creación de lecturas no distinguía entre sensores activos e inactivos
- la migración y el smoke test de PostgreSQL todavía utilizaban el contrato anterior de Sensor

Se propuso introducir los campos `location` e `is_active`, retirar la operación DELETE del flujo público, rechazar nuevas lecturas de sensores inactivos y preservar los registros existentes mediante una migración Alembic compatible con datos históricos. La implementación se realizó mediante pruebas incrementales que primero demostraron los comportamientos faltantes y después verificaron cada cambio.

### Decisión final

Se adoptó el siguiente comportamiento:

- `location` es obligatorio al crear un sensor y puede modificarse posteriormente
- los sensores nuevos se crean con `is_active = true`
- un sensor puede desactivarse mediante `PATCH`
- un sensor desactivado permanece disponible mediante `GET`
- `DELETE /sensors/{id}` deja de formar parte de la API
- un sensor inactivo no puede recibir nuevas lecturas
- intentar registrar una lectura en un sensor inactivo produce HTTP `409 Conflict`
- los sensores existentes antes de la migración reciben `Ubicación no especificada` e `is_active = true`

### Resultado verificado

Se verificó el comportamiento mediante pruebas unitarias, pruebas de integración, migraciones y una ejecución real con PostgreSQL 16.
Resultados obtenidos:

- 49 pruebas aprobadas
- cobertura total de 93.18 %
- Ruff sin errores
- mypy sin errores
- migración `8f1f8f0a69a8` aplicada correctamente
- downgrade hacia `ccdeecc8c528` validado
- re-aplicación de la migración validada
- datos históricos conservados durante la migración
- `location` e `is_active` creados como `NOT NULL`
- PostgreSQL actualizado correctamente hasta `8f1f8f0a69a8`
- creación de sensor y lectura verificada contra PostgreSQL real
- sensor desactivado conservado y accesible mediante `GET`
- intento de nueva lectura sobre sensor inactivo verificado con HTTP `409`
- respuesta confirmada: `{"detail":"El sensor con id 1 está inactivo"}`

## RF-3 — Consulta de lecturas

Se establece que la consulta de lecturas por sensor debe soportar paginación, `limit`, `offset`, filtro por rango de fechas y un orden estable y determinista. La implementación existente ya validaba paginación, coherencia temporal y delegaba al repositorio un orden por `timestamp` e `id`, pero las pruebas no demostraban todavía los casos más sensibles del requisito: lecturas con el mismo `timestamp` y paginación combinada con filtro temporal inclusivo.

### Consulta realizada a la IA

Se solicitó apoyo para auditar RF-3 sin rehacer comportamiento ya implementado, identificar si existía una brecha real de funcionalidad o sólo de evidencia, y cerrar el requisito con pruebas relevantes en vez de añadir cobertura artificial.

La IA identificó el siguiente resultado de auditoría:

- implementación del servicio y repositorio: completa
- cobertura existente sobre RF-3: parcial
- brecha demostrable: no había pruebas de integración que probaran orden determinista con `timestamp` idéntico ni combinación de rango temporal inclusivo con paginación estable

Se decidió no modificar la lógica de producción porque el código ya cumplía el requisito y, en cambio, añadir pruebas de integración que demostraran explícitamente ese contrato.

### Decisión final

Se adoptó el siguiente comportamiento verificado:

- cuando varias lecturas comparten el mismo `timestamp`, la API responde ordenando por `timestamp` y `id`
- el filtro temporal `from` y `to` es inclusivo
- `limit` y `offset` se aplican sobre un orden estable y determinista
- no fue necesario modificar servicio, repositorio ni router para cumplir RF-3

### Resultado verificado

Se verificó el comportamiento mediante nuevas pruebas de integración y una regresión completa del proyecto.
Resultados obtenidos:

- 55 pruebas aprobadas
- cobertura total de 94.25 %
- Ruff sin errores
- mypy sin errores
- se añadieron pruebas para `timestamp` idéntico con desempate por `id`
- se añadieron pruebas para filtro temporal inclusivo combinado con `limit` y `offset`
- no se requirieron migraciones ni cambios de esquema para cerrar RF-3

## RF-4 — Detección de anomalías con severidad

Se establece que una lectura fuera del umbral configurado del sensor debe generar una alerta y que la solución debe contemplar al menos las severidades `WARNING` y `CRITICAL`. La implementación existente ya detectaba anomalías mediante una estrategia basada en umbral superior y persistía alertas, pero sólo devolvía un booleano y no tenía ninguna forma de clasificar ni almacenar la severidad resultante.

### Consulta realizada a la IA

Se solicitó apoyo para auditar RF-4 a partir del commit base de Semana 6, identificar la brecha demostrable frente al requisito y aplicar el cambio mínimo manteniendo la separación de responsabilidades entre servicio, estrategia de dominio, persistencia y contrato HTTP.

La IA identificó que la solución existente era parcial por las siguientes razones:

- `ThresholdAlertStrategy` sólo respondía si había anomalía, pero no su severidad
- `Alert` no almacenaba severidad en la base de datos
- la API de alertas no exponía severidad
- no existían pruebas que demostraran `WARNING` y `CRITICAL`

Se propuso mantener la decisión de severidad dentro de la estrategia de alertas para no acoplar `ReadingService` a reglas de clasificación. Como el proyecto no definía una política previa para distinguir `WARNING` y `CRITICAL`, se adoptó una regla mínima y explícita: una lectura superior al umbral genera `WARNING` y pasa a `CRITICAL` cuando supera el umbral en un 20 % adicional. La regla se encapsuló por completo en la estrategia para permitir futuros ajustes sin modificar el servicio ni los repositorios.

### Decisión final

Se adoptó el siguiente comportamiento:

- la estrategia de alertas clasifica una lectura como `WARNING`, `CRITICAL` o sin anomalía
- `ReadingService` delega la clasificación a la estrategia y sólo persiste alertas cuando existe severidad
- `Alert` persiste la severidad como campo obligatorio
- `AlertResponse` expone la severidad en la API
- la migración `4a2c4f5d6e7b` agrega la columna `severity` a la tabla `alerts`
- los datos históricos se preservan asignando `WARNING` como valor por defecto durante la migración

### Resultado verificado

Se verificó el comportamiento mediante pruebas unitarias, integración HTTP, persistencia SQLAlchemy, migraciones Alembic y una ejecución real con PostgreSQL 16.
Resultados obtenidos:

- 53 pruebas aprobadas
- cobertura total de 93.48 %
- Ruff sin errores
- mypy sin errores
- `pytest tests/test_alert_strategy.py tests/test_reading_service.py tests/test_sqlalchemy_alert_repository.py tests/integration/test_readings_api.py tests/integration/test_alerts_api.py -q` en verde
- `python -m alembic heads` con un único head: `4a2c4f5d6e7b`
- upgrade Alembic validado sobre SQLite temporal
- downgrade Alembic validado hasta `base`
- upgrade Alembic validado sobre PostgreSQL 16 real
- revisión confirmada en PostgreSQL: `4a2c4f5d6e7b`
- flujo HTTP real validado contra PostgreSQL con alerta `CRITICAL`
- severidad `WARNING` verificada en pruebas unitarias, integración y persistencia
- severidad `CRITICAL` verificada en pruebas unitarias, integración y PostgreSQL real

## RF-5 — Gestión de alertas

Se establece que el sistema debe permitir consultar alertas activas, consultar alertas asociadas a sensores, manejar estados de alerta y cambiar una alerta entre estados válidos usando `open`, `acknowledged` y `resolved`. La implementación existente sólo ofrecía consulta por sensor y no tenía estado, transición ni una definición de qué significaba una alerta activa.

### Consulta realizada a la IA

Se solicitó apoyo para auditar RF-5 a partir del estado alcanzado tras RF-4, identificar la brecha funcional exacta y aplicar el cambio mínimo manteniendo la lógica de ciclo de vida dentro del dominio y sin mezclar responsabilidades entre router, servicio y repositorio.

La IA identificó las siguientes brechas demostrables:

- `Alert` no tenía campo `status`
- no existía endpoint para listar alertas activas
- no existía endpoint para cambiar el estado de una alerta
- no había política explícita de transiciones válidas
- no existían pruebas para listar activas, cambiar estado ni rechazar transiciones inválidas

Se adoptó una política mínima y explícita para cerrar el requisito:

- alertas activas = `open` y `acknowledged`
- transiciones válidas = `open -> acknowledged`, `open -> resolved`, `acknowledged -> resolved`
- no se permiten reaperturas ni transiciones al mismo estado

Durante la validación contra PostgreSQL real apareció una discrepancia no visible en SQLite: el modelo estaba persistiendo el nombre del enum (`OPEN`) mientras la migración había creado el constraint con los valores requeridos (`open`, `acknowledged`, `resolved`). Se corrigió el modelo para persistir los valores públicos del enum y se repitió la validación real hasta dejarla en verde.

### Decisión final

Se adoptó el siguiente comportamiento:

- `GET /alerts/active` devuelve únicamente alertas con estado `open` o `acknowledged`
- `GET /sensors/{sensor_id}/alerts` sigue devolviendo las alertas asociadas al sensor
- `PATCH /alerts/{alert_id}` permite cambiar el estado respetando la política del dominio
- una alerta nueva se crea en estado `open`
- una transición inválida produce conflicto HTTP `409`
- una alerta inexistente produce HTTP `404`
- la migración `6f8a9b0c1d2e` agrega la columna `status` a la tabla `alerts`

### Resultado verificado

Se verificó el comportamiento mediante pruebas unitarias, integración HTTP, persistencia SQLAlchemy, migraciones Alembic y una ejecución real con PostgreSQL 16.
Resultados obtenidos:

- 64 pruebas aprobadas
- cobertura total de 94.53 %
- Ruff sin errores
- mypy sin errores
- `pytest tests/test_alert_service.py tests/test_sqlalchemy_alert_repository.py tests/integration/test_alerts_api.py tests/test_reading_service.py tests/integration/test_readings_api.py -q` en verde
- `python -m alembic heads` con un único head: `6f8a9b0c1d2e`
- upgrade Alembic validado sobre SQLite temporal
- downgrade Alembic validado hasta `base`
- upgrade Alembic validado sobre PostgreSQL 16 real
- revisión confirmada en PostgreSQL: `6f8a9b0c1d2e`
- alerta nueva validada en PostgreSQL con estado inicial `open`
- transición `open -> acknowledged` validada en PostgreSQL real
- listado de alertas activas validado en integración y PostgreSQL real
- transición inválida rechazada con HTTP `409`

## RF-6 — Estadísticas por sensor y periodo

Se establece que debe existir una consulta de estadísticas por sensor y periodo que incluya al menos mínimo, máximo y promedio, manteniendo la lógica dentro de la arquitectura en capas y sin depender directamente de FastAPI. La implementación existente no ofrecía ningún contrato, servicio, repositorio ni endpoint para este comportamiento.

### Consulta realizada a la IA

Se solicitó apoyo para auditar RF-6 después de cerrar RF-5, determinar si existía alguna base reutilizable y aplicar el cambio mínimo con TDD, manteniendo las validaciones temporales coherentes con la consulta paginada de lecturas.

La IA identificó que RF-6 estaba faltante por completo:

- no existía método de servicio para estadísticas
- no existía contrato de repositorio para agregación
- no existía endpoint HTTP para consultar estadísticas
- no existían pruebas unitarias ni de integración para el requisito

Se propuso encapsular el resultado agregado en un objeto de dominio `ReadingStatistics`, reutilizar las mismas validaciones temporales ya existentes para lecturas y delegar la agregación al repositorio de lecturas para preservar la separación entre servicio y persistencia.

### Decisión final

Se adoptó el siguiente comportamiento:

- `GET /sensors/{sensor_id}/readings/stats` devuelve estadísticas agregadas para un sensor
- el endpoint acepta `from` y `to` como rango temporal opcional e inclusivo
- la respuesta expone `count`, `minimum_value`, `maximum_value` y `average_value`
- si el sensor existe pero no hay lecturas en el rango, la API devuelve `count = 0` y agregados `null`
- el servicio reutiliza la validación temporal ya aplicada en la consulta paginada
- la agregación se resuelve en el repositorio mediante funciones SQL y sigue siendo testeable con un fake repository en memoria

### Resultado verificado

Se verificó el comportamiento mediante pruebas unitarias, integración HTTP y regresión completa del proyecto.
Resultados obtenidos:

- 68 pruebas aprobadas
- cobertura total de 94.84 %
- Ruff sin errores
- mypy sin errores
- `pytest tests/test_reading_statistics_service.py tests/integration/test_readings_api.py -q` en verde
- estadísticas con rango temporal validadas en servicio e integración
- contrato de estadísticas vacías validado con `count = 0` y agregados `null`
- no se requirieron migraciones ni cambios de esquema para cerrar RF-6

## RF-7 — Health check y métricas básicas

Se establece que el sistema debe exponer un mecanismo simple de verificación operativa y métricas básicas para observabilidad sin convertir esa comprobación en una operación pesada o dependiente de consultas innecesarias. La implementación existente ya exponía `GET /health` como un liveness liviano, pero todavía no ofrecía ninguna salida de métricas del proceso ni de tráfico HTTP.

### Consulta realizada a la IA

Se solicitó apoyo para auditar RF-7 después de cerrar RF-6, diferenciar si el requisito estaba completamente faltante o sólo incompleto y aplicar el cambio mínimo sin degradar el contrato existente de `health`.

La IA identificó el siguiente resultado de auditoría:

- `GET /health` ya existía y cumplía bien como liveness básico
- no existía endpoint `/metrics`
- no había contadores ni uptime del proceso expuestos para monitoreo
- la cobertura existente sólo validaba `/health`

Se decidió conservar `/health` como comprobación liviana del proceso y añadir un endpoint `/metrics` en texto plano con formato Prometheus simple. También se agregó un middleware mínimo para registrar conteo y latencia por petición sin introducir dependencias externas ni consultas a base de datos dentro del health check.

### Decisión final

Se adoptó el siguiente comportamiento:

- `GET /health` permanece como liveness liviano del servicio
- `GET /metrics` expone `uptime` del proceso
- `GET /metrics` expone contador total de peticiones HTTP por método, ruta y código de estado
- `GET /metrics` expone conteo y suma acumulada de latencia HTTP por método, ruta y código de estado
- las métricas se generan en memoria y se reinician entre pruebas para mantener aislamiento
- no se agregó un readiness check contra base de datos porque el requisito se podía cubrir sin volver pesado el endpoint de salud

### Resultado verificado

Se verificó el comportamiento mediante nuevas pruebas de integración y una regresión completa del proyecto.
Resultados obtenidos:

- 69 pruebas aprobadas
- cobertura total de 94.88 %
- Ruff sin errores
- mypy sin errores
- `GET /health` se mantuvo estable y sin dependencia de base de datos
- `GET /metrics` validado con salida `text/plain`
- `uptime` y contadores por ruta validados en integración
- no se requirieron migraciones ni cambios de esquema para cerrar RF-7

## RNF-3 — CI/CD alineado con Semana 6

Se establece que la integración continua debe ejecutar Ruff, mypy, pytest con cobertura, validaciones de seguridad y un smoke test real con PostgreSQL. Además, la entrega continua debe desplegar a producción en cada push a `main`, evitando confundir una simple marca visual o un `echo` con un despliegue real.

### Consulta realizada a la IA

Se solicitó apoyo para auditar el pipeline heredado de Semana 4, verificar si seguía representando correctamente el estado de Semana 6 y corregir únicamente las brechas demostrables del flujo de CI/CD.

La IA identificó el siguiente resultado de auditoría:

- la CI ya ejecutaba Ruff, mypy, pytest, Trivy y un smoke test con PostgreSQL
- el trigger de `push` todavía incluía la rama histórica `feature/semana4-devops`
- el smoke test seguía esperando explícitamente la revisión Alembic antigua `8f1f8f0a69a8`
- el supuesto paso de producción sólo registraba un `echo` y no hacía ningún despliegue real

Se decidió conservar la estructura general del workflow porque ya cubría los controles principales, pero actualizando únicamente los puntos que habían quedado obsoletos. El cambio mínimo consistió en eliminar el trigger heredado de Semana 4, calcular dinámicamente la cabeza actual de Alembic dentro del smoke test, extender ese smoke para comprobar también `/health` y `/metrics`, y sustituir `production-gate` por un despliegue real a Render mediante API con validación posterior del health check público.

### Decisión final

Se adoptó el siguiente comportamiento:

- la CI se ejecuta en `push` a `main`, `pull_request` y `workflow_dispatch`
- el smoke test PostgreSQL compara la revisión aplicada contra la cabeza real de Alembic en lugar de usar un valor fijo obsoleto
- el smoke test valida arranque de la API, creación de sensor, registro de lectura y exposición de `/metrics`
- la validación de seguridad con Trivy se mantiene sin cambios funcionales
- el job final de `main` ahora inicia un despliegue real en Render usando `RENDER_API_KEY` y `RENDER_SERVICE_ID`
- después del despliegue, el workflow valida el health check público de producción

### Resultado verificado

Se verificó el comportamiento mediante regresión completa local, revisión del workflow actualizado y una ejecución real del smoke test contra PostgreSQL 16 local.
Resultados obtenidos:

- 69 pruebas aprobadas
- cobertura total de 94.88 %
- Ruff sin errores
- mypy sin errores
- smoke PostgreSQL real validado con revisión `6f8a9b0c1d2e`
- smoke PostgreSQL real validó tablas `sensors`, `readings`, `alerts` y `alembic_version`
- smoke PostgreSQL real validó creación de sensor, persistencia de lectura, `/health` y `/metrics`
- el workflow dejó de depender de la rama histórica de Semana 4
- el workflow dejó de depender de una revisión Alembic fija ya obsoleta
- el pseudo-CD basado en `echo` fue reemplazado por despliegue real a Render con espera activa y comprobación de health check
- no se requirieron migraciones ni cambios de esquema para cerrar RNF-3

## RNF-5 — Observabilidad y configuración por entorno

Se establece que la aplicación debe utilizar configuración mediante variables de entorno y emitir logs estructurados. El proyecto ya tomaba `DATABASE_URL` desde el entorno y mantenía `PORT` como variable de ejecución, pero la aplicación todavía no emitía eventos estructurados propios que permitieran observar el tráfico HTTP de forma consistente.

### Consulta realizada a la IA

Se solicitó apoyo para auditar RNF-5 después de cerrar RNF-3, determinar si la brecha estaba en la configuración, en la observabilidad o en ambos frentes, y aplicar el cambio mínimo sin introducir nuevas dependencias.

La IA identificó el siguiente resultado de auditoría:

- la configuración de base de datos ya dependía de `DATABASE_URL`
- el arranque ya respetaba `PORT`
- no existía un logger propio de la aplicación con estructura legible por máquinas
- no había pruebas que demostraran emisión de eventos operativos estructurados

Se decidió conservar la estrategia actual de configuración por entorno y cubrir la brecha restante con una utilidad pequeña de observabilidad basada en la librería estándar. El cambio mínimo consistió en introducir serialización JSON para eventos, configurar el nivel de logs mediante `LOG_LEVEL`, registrar eventos HTTP desde el middleware existente y documentar la nueva variable en `.env.example`.

### Decisión final

Se adoptó el siguiente comportamiento:

- la configuración sensible sigue dependiendo de variables de entorno y no de valores hardcodeados
- la API ahora emite un evento estructurado por petición HTTP completada
- cuando una petición falla por excepción no controlada, la API emite un evento estructurado de error
- cada evento incluye al menos `timestamp`, `level`, `logger`, `event`, `method`, `path`, `status_code`, `duration_ms` y `client_ip`
- el nivel del logger propio de observabilidad se controla mediante `LOG_LEVEL`
- no se introdujeron librerías nuevas para logging estructurado

### Resultado verificado

Se verificó el comportamiento mediante pruebas unitarias, integración HTTP y regresión completa del proyecto.
Resultados obtenidos:

- 71 pruebas aprobadas
- cobertura total de 94.76 %
- Ruff sin errores
- mypy sin errores
- se añadió una prueba unitaria para la serialización JSON de eventos
- se añadió una prueba de integración que demuestra que `/health` dispara un evento estructurado
- `LOG_LEVEL` agregado a `.env.example`
- no se requirieron migraciones ni cambios de esquema para cerrar RNF-5

## RNF-6 — Documentación de entrega final

Se establece que la entrega debe incluir un `README` actualizado, un diagrama de arquitectura, al menos dos ADR y una bitácora consolidada del uso de IA. El repositorio ya contaba con una bitácora consolidada de Semana 6 y con un ADR sobre arquitectura en capas.

### Consulta realizada a la IA

Se solicitó apoyo para auditar RNF-6 una vez cerrados los requisitos técnicos y determinar exactamente qué artefactos documentales seguían incompletos.

La IA identificó el siguiente resultado de auditoría:

- el `README` estaba desfasado respecto al alcance final de Semana 6
- no había un diagrama actual de arquitectura en el `README`
- sólo existía un ADR en `docs/adr`
- la bitácora consolidada de Semana 6 sí existía y ya venía actualizándose.

Se decidió mantener la documentación histórica de semanas anteriores intacta y concentrar el cierre de RNF-6 en tres cambios mínimos: reescribir el `README` como documento final de SensorHub, incorporar un diagrama de arquitectura en Mermaid y agregar un segundo ADR centrado en observabilidad y monitoreo liviano para alcanzar el mínimo exigido.

### Decisión final

Se adoptó el siguiente comportamiento documental:

- el `README` ahora describe el estado final de SensorHub y no sólo la entrega de Semana 4
- el `README` incluye un diagrama de arquitectura en Mermaid
- el `README` documenta variables de entorno, ejecución local, Docker Compose, validaciones y CI/CD actual
- el proyecto ahora cuenta con dos ADR aceptados
- la bitácora consolidada de IA se actualiza.

### Resultado verificado

Se verificó el cierre documental mediante revisión directa de archivos y una regresión completa del proyecto.
Resultados obtenidos:

- 71 pruebas aprobadas
- cobertura total de 94.76 %
- Ruff sin errores
- mypy sin errores
- `README.md` actualizado al alcance final de Semana 6
- diagrama de arquitectura agregado en `README.md`
- segundo ADR agregado en `docs/adr/0002-observabilidad-y-monitoreo-liviano.md`
- bitácora consolidada de IA mantenida en `AI_LOG_SEMANA6.md`
- no se requirieron migraciones ni cambios de esquema para cerrar RNF-6

## RNF-1 — Arquitectura en capas y DIP

Se establece que la solución debe mantener una arquitectura en capas con inversión de dependencias y que la lógica de negocio debe poder probarse sin depender de una base de datos real. La auditoría realizada sobre el estado actual de SensorHub mostró que este requisito ya estaba cubierto por la estructura de código y por la suite de pruebas existente.

### Consulta realizada a la IA

Se solicitó apoyo para auditar RNF-1 al cierre de la Semana 6 y confirmar si aún existía alguna brecha real en la separación por capas o en la testabilidad de los servicios.

La IA identificó el siguiente resultado de auditoría:

- la estructura `routers -> services -> repositories -> models` se mantiene en el proyecto
- `SensorRepository`, `ReadingRepository` y `AlertRepository` están definidos como `Protocol`
- `dependencies.py` inyecta implementaciones concretas únicamente en el borde de FastAPI
- la lógica principal de negocio se prueba con repositorios falsos en `tests/fakes`
- no se encontró evidencia de que los servicios dependan directamente de FastAPI o de una base de datos real para su validación unitaria

Se decidió no modificar código productivo porque no apareció ninguna brecha demostrable frente al requisito.

### Decisión final

Se mantiene la arquitectura actual:

- `routers` para responsabilidades HTTP
- `services` para reglas y coordinación de negocio
- `repositories` para persistencia
- `models` para entidades ORM
- dependencias de servicio resueltas mediante contratos y no mediante implementaciones concretas acopladas

### Resultado verificado

Se verificó el requisito mediante auditoría de código y la regresión completa del proyecto
Resultados obtenidos:

- 71 pruebas aprobadas
- cobertura total de 94.76 %
- Ruff sin errores
- mypy sin errores
- evidencia directa de DIP mediante `Protocol` en los contratos de repositorio
- evidencia de testabilidad sin base real mediante `FakeSensorRepository` y `FakeReadingRepository`
- no se requirieron migraciones ni cambios de esquema para cerrar RNF-1

## RNF-2 — Pruebas y cobertura

Se establece que la solución debe mantener al menos `80 %` de cobertura y combinar pruebas unitarias con pruebas de integración. La auditoría realizada sobre el estado final de la suite mostró que este requisito ya estaba cumplido y además fortalecido durante el cierre incremental de los requisitos funcionales y no funcionales anteriores.

### Consulta realizada a la IA

Se solicitó apoyo para auditar RNF-2 al final de la Semana 6 y confirmar si todavía existía alguna brecha real en cobertura o en la variedad de tipos de prueba ejecutados por el proyecto.

La IA identificó el siguiente resultado de auditoría:

- la suite contiene pruebas unitarias sobre dominio, servicios, repositorios y utilidades
- la suite contiene pruebas de integración HTTP con `TestClient`
- la cobertura global actual supera ampliamente el umbral requerido
- no se detectó necesidad de añadir pruebas artificiales sólo para inflar cobertura

Se decidió no modificar código ni añadir nuevas pruebas para RNF-2 porque no apareció una brecha demostrable frente al requisito.

### Decisión final

Se mantiene el esquema actual de validación:

- pruebas unitarias para reglas de negocio y componentes aislados
- pruebas de integración para contratos HTTP y comportamiento observable
- control automático de cobertura mediante `pytest-cov`

### Resultado verificado

Se verificó el requisito mediante la regresión completa del proyecto.
Resultados obtenidos:

- 71 pruebas aprobadas
- cobertura total de 94.76 %
- Ruff sin errores
- mypy sin errores
- coexistencia confirmada de pruebas unitarias y de integración
- umbral de cobertura `>= 80 %` respetado por el proyecto
- no se requirieron migraciones ni cambios de esquema para cerrar RNF-2

## RNF-4 — Contenedores, PostgreSQL y migraciones

Se establece que el proyecto debe mantener Docker, Docker Compose, PostgreSQL y Alembic, y que las migraciones deben validarse sobre PostgreSQL real preservando el historial razonablemente. La auditoría realizada al estado final del proyecto mostró que este requisito ya estaba cubierto por la infraestructura existente y por las validaciones recientes ejecutadas durante el cierre de la Semana 6.

### Consulta realizada a la IA

Se solicitó apoyo para auditar RNF-4 después de cerrar los cambios funcionales y no funcionales principales, con el fin de confirmar si aún existía alguna brecha real en contenedores, migraciones o validación contra PostgreSQL.

La IA identificó el siguiente resultado de auditoría:

- existe un `Dockerfile` multi-stage para construir y ejecutar SensorHub
- `docker-compose.yml` define la API y PostgreSQL con `healthcheck`
- `start.sh` aplica `alembic upgrade head` antes de iniciar Uvicorn
- Alembic mantiene un único head actual
- el smoke real contra PostgreSQL ya fue validado de nuevo durante RNF-3

Se decidió no modificar archivos de infraestructura porque no apareció ninguna brecha demostrable frente al requisito.

### Decisión final

Se mantiene la infraestructura actual:

- contenedor de aplicación mediante `Dockerfile`
- entorno local completo mediante `docker-compose.yml`
- migraciones administradas por Alembic
- validación real contra PostgreSQL como parte del smoke test del pipeline

### Resultado verificado

Se verificó el requisito mediante auditoría de archivos, comprobación de `alembic heads` y una ejecución real del smoke con PostgreSQL.
Resultados obtenidos:

- 71 pruebas aprobadas
- cobertura total de 94.76 %
- Ruff sin errores
- mypy sin errores
- `python -m alembic heads` confirmó un único head: `6f8a9b0c1d2e`
- `Dockerfile` multi-stage presente y vigente
- `docker-compose.yml` mantiene PostgreSQL con `healthcheck`
- smoke real validado sobre PostgreSQL con migraciones, creación de sensor, persistencia de lectura, `/health` y `/metrics`
- no se requirieron migraciones nuevas ni cambios de esquema para cerrar RNF-4
