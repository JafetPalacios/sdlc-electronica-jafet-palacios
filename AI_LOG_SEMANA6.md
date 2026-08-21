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
