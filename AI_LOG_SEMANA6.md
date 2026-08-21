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

Durante la validación contra PostgreSQL real del viernes 21 de agosto de 2026 apareció una discrepancia no visible en SQLite: el modelo estaba persistiendo el nombre del enum (`OPEN`) mientras la migración había creado el constraint con los valores requeridos (`open`, `acknowledged`, `resolved`). Se corrigió el modelo para persistir los valores públicos del enum y se repitió la validación real hasta dejarla en verde.

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
