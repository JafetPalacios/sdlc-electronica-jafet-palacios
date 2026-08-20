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
