# Bitácora de uso de IA — Semana 5

Esta bitácora registra el uso de herramientas de inteligencia artificial durante la Semana 5 del proyecto, distinguiendo explícitamente las decisiones tomadas de las propuestas, análisis o diagnósticos proporcionados por la IA.
El objetivo es mantener trazabilidad sobre cómo se utilizó la IA como apoyo profesional sin delegar el criterio técnico.

---

### Intervención 1 — Comparación entre prompt pobre y prompt estructurado

Realizar el experimento utilizando conversaciones independientes con diferentes modelos de IA para evitar que el contexto de una respuesta anterior influyera en la siguiente generación. Se reconoce que se utilizaron modelos de IA diferentes, por lo que las diferencias observadas pueden estar influenciadas tanto por la calidad del prompt como por las características particulares de cada modelo. Esta condición se tendrá en cuenta al interpretar los resultados de las tres tareas.

### Tarea 1
Se ejecutaron dos prompts para resolver la misma tarea de conversión de Celsius a Fahrenheit. El primero fue deliberadamente poco específico y el segundo utilizó la estructura de contexto, tarea, restricciones y entrega indicada para la Semana 5.
Con el prompt pobre, la IA produjo una función matemáticamente correcta, pero decidió por cuenta propia el nombre de la función, los nombres de los parámetros y la inclusión de un ejemplo ejecutable. Tampoco aplicó redondeo a dos decimales.
Con el prompt estructurado, la IA respetó exactamente la firma solicitada, utilizó type hints, añadió el docstring requerido, implementó el redondeo a dos decimales y entregó únicamente la función.

### Tarea 2

Utilizar una tarea real de refactorización sobre `SensorService` para continuar el ejercicio de comparación entre prompts. Se mantuvo la estrategia de utilizar modelos de IA diferentes y conversaciones independientes para cada generación.

El prompt pobre solicitó de forma general refactorizar el servicio para eliminar código repetido y mejorarlo. El prompt estructurado identificó específicamente la duplicación existente al recuperar sensores por identificador en `get_sensor`, `update_sensor` y `delete_sensor`. También estableció que debía extraerse únicamente esa lógica a `_get_sensor_or_raise` y definió explícitamente qué elementos del servicio debían permanecer sin cambios.
Con el prompt pobre, la IA identificó correctamente la duplicación principal, pero amplió el alcance de la refactorización. Además de `_get_sensor_or_raise`, propuso `_ensure_code_is_unique`, modificó la construcción de la entidad `Sensor` y realizó cambios generales de documentación y estilo.
Con el prompt estructurado, la IA concentró la modificación en `_get_sensor_or_raise` y su utilización en los tres métodos indicados. Conservó la validación de unicidad, `_validate_sensor_rule`, la construcción explícita de `Sensor`, las firmas públicas y las demás responsabilidades del servicio.

### Tarea 3

Se utilizó como tercera tarea la explicación del flujo real de creación de una lectura en SensorHub, desde `POST /sensors/{sensor_id}/readings` hasta la construcción de `ReadingResponse`.

El prompt pobre solicitó únicamente explicar cómo funcionaba la creación de una lectura a partir de `app/routers/readings.py` y `app/services/reading_service.py`.
La IA reconstruyó correctamente la mayor parte del flujo, pero presentó algunas inferencias como comportamientos confirmados. Entre ellas se encontró la traducción de `SensorNotFoundError` a HTTP 404, aunque el manejador de excepciones no había sido proporcionado. También describió la generación del timestamp por parte de la base de datos como comportamiento efectivo a partir de un comentario del servicio.
El prompt estructurado indicó explícitamente qué responsabilidades debían explicarse y estableció que no podían asumirse detalles pertenecientes a archivos no proporcionados. También solicitó diferenciar la validación de FastAPI/Pydantic de las reglas de negocio y distinguir entre comportamiento verificable, comportamiento documentado y aspectos no confirmables.


### Intervención 2 — Instalación y preparación de Aider

Después de completar los módulos 3 y 4 de GitHub Copilot Fundamentals, continuar con la actividad de Aider, manteniendo el repositorio en la rama `feature/semana5-ia-copilot` y con el árbol de trabajo limpio antes de permitir que una herramienta asistida por IA interactúe con Git.

Se solicitó acompañamiento para instalar Aider debido a que en el primer intento de instalar `aider-install` falló debido a un timeout durante una descarga desde `files.pythonhosted.org`. En un segundo intento, aumentando el tiempo de espera, la descarga de `uv` fue detenida por `pip` debido a una discrepancia de hash. La IA recomendó no omitir la comprobación de integridad y eliminar la caché local de `pip` antes de realizar una nueva descarga. Después de limpiar la caché y forzar una descarga sin reutilizar archivos almacenados, `aider-install 0.2.0` y `uv 0.12.5` se instalaron correctamente. Posteriormente, `aider-install` creó la instalación aislada de Aider.
Se siguió el procedimiento de recuperación sin desactivar las verificaciones de integridad. Después de comprobar que la caché estaba limpia, se repitió la descarga y se continuó con la instalación únicamente cuando esta terminó correctamente. También se agregó temporalmente `C:\Users\Jafet\.local\bin` al `PATH` de la sesión actual para poder utilizar el ejecutable instalado. Aider quedó instalado correctamente en la versión `0.86.2` y disponible mediante `C:\Users\Jafet\.local\bin\aider.exe`. `uv` quedó disponible en la versión `0.12.5`.

### Intervención 3 — Primer cambio de código asistido con Aider

La idea principal era realizar el ejercicio solicitado con Aider sobre `semana5/conversions.py`, manteniendo una separación clara entre los cambios manuales previos y los cambios producidos por la herramienta.
Antes de iniciar la edición se decidió guardar temporalmente las modificaciones manuales de `.gitignore` y `AI_LOG_SEMANA5.md` mediante `git stash`, con el objetivo de dejar el árbol de trabajo limpio y poder identificar con precisión los commits generados durante la sesión de Aider.
También se decidió utilizar `gemini/gemini-3.6-flash` después de comprobar que `gemini/gemini-2.5-pro` ya no estaba disponible para usuarios nuevos mediante el endpoint utilizado.

### Apoyo de la IA
Se solicitó a Aider crear en `semana5/conversions.py` una función pura con la firma exacta `celsius_to_fahrenheit(c: float) -> float`
La función debía convertir grados Celsius a Fahrenheit, redondear el resultado a dos decimales, utilizar Python 3.12, incluir un docstring en español y no incorporar dependencias, ejemplos, pruebas, clases ni código adicional.

Aider creó inicialmente `semana5/conversions.py` como archivo vacío y generó automáticamente el commit `4ee43f7 feat: agrega módulo de conversiones para la semana 5`

Posteriormente generó la implementación solicitada:

```python
def celsius_to_fahrenheit(c: float) -> float:
    """Convierte una temperatura de grados Celsius a Fahrenheit"""
    return round((c * 9 / 5) + 32, 2)
```
Durante el proceso, Gemini respondió temporalmente con un error HTTP 503 debido a alta demanda. Aider realizó un reintento automático y consiguió completar la edición.

La implementación final quedó registrada mediante el commit `9afc2a2 feat: agregar función celsius_to_fahrenheit para conversión de clima`
Este segundo commit incluye explícitamente: Co-authored-by: aider (gemini/gemini-3.6-flash) <aider@aider.chat>

### Revisión realizada

Se revisó manualmente el contenido generado antes de considerarlo válido. La implementación conserva exactamente la firma solicitada, utiliza únicamente operaciones estándar de Python, realiza el redondeo a dos decimales y mantiene una responsabilidad única sin efectos secundarios.
No fue necesario modificar manualmente el código generado por Aider. Posteriormente se ejecutaron las siguientes verificaciones:

* Ruff sobre semana5/conversions.py
* mypy sobre semana5/conversions.py
* comprobaciones funcionales para 0 °C, 100 °C y -40 °C
* suite completa de pytest

### Resultado verificado

* Ruff terminó con All checks passed.
* mypy terminó sin problemas de tipado.
* Las conversiones verificadas produjeron los resultados esperados:

0 °C -> 32 °F
100 °C -> 212 °F
-40 °C -> -40 °F

* La suite completa terminó con 24 pruebas aprobadas.
* La cobertura global obtenida fue de 91.63 %
* No se detectaron regresiones relacionadas con el cambio generado.
* Los commits producidos durante la sesión de Aider fueron publicados en la rama feature/semana5-ia-copilot.

### Comparación entre Aider y Copilot

Aider proporcionó una trazabilidad Git más explícita durante la modificación del proyecto. El cambio generado quedó asociado directamente con commits realizados durante la sesión y el commit que contiene la implementación identifica a Aider y al modelo utilizado mediante Co-authored-by.
Aider también trabajó directamente sobre el archivo del repositorio y presentó el diff antes de finalizar el proceso, lo que facilita revisar qué modificación pretende aplicar.
Otra ventaja observada fue su capacidad de mantener el contexto del repositorio y trabajar sobre archivos concretos desde una interfaz de terminal integrada con Git.

Pero, su integración automática con Git también requiere mayor atención. Durante el ejercicio creó un commit intermedio únicamente para registrar el archivo vacío antes de aplicar la modificación, lo que produjo dos commits para un cambio técnicamente muy pequeño.
Además, la experiencia depende directamente de la disponibilidad del proveedor externo. Durante la sesión se encontró primero un modelo que ya no estaba disponible para usuarios nuevos y posteriormente un error temporal HTTP 503 por alta demanda.
La configuración inicial también requirió instalar herramientas adicionales, configurar un proveedor, gestionar una API key y controlar archivos auxiliares generados por Aider.

En comparación, Copilot ofrece una interacción más inmediata dentro del editor para sugerencias y consultas pequeñas, mientras que Aider proporciona una integración más fuerte con el repositorio y una trazabilidad Git más visible.
Se consideró válido el cambio producido por Aider después de revisar manualmente su implementación y verificarlo mediante Ruff, mypy, pruebas funcionales y la suite completa. Aider resulta especialmente útil cuando se busca que una modificación asistida por IA quede directamente relacionada con el historial del repositorio, pero su automatización de Git debe revisarse cuidadosamente para evitar commits innecesarios o cambios que no hayan sido evaluados por el desarrollador.

### Intervención 4 — Code review asistido y validación de paginación en ReadingService

La actividad consistió en realizar un code review asistido por IA sobre `ReadingService` y evaluar manualmente cada hallazgo antes de modificar el código. Se decidió no aceptar automáticamente las recomendaciones generadas. Cada hallazgo se contrastó con los esquemas, modelos, repositorios, reglas de dominio y excepciones existentes en SensorHub. También se decidió implementar las correcciones aceptadas utilizando un ciclo TDD, comenzando por pruebas que demostraran el comportamiento faltante antes de modificar la implementación.

### Consulta realizada a la IA

Se solicitó revisar `ReadingService` buscando riesgos relacionados con SOLID, mantenibilidad, casos borde, lógica, integridad de datos, seguridad, rendimiento y comportamiento del servicio fuera de FastAPI. Posteriormente se solicitó proponer exactamente cinco casos de prueba adicionales que no duplicaran la cobertura existente.

La IA produjo cinco hallazgos durante el code review. Después de verificarlos contra el código real:

- un hallazgo fue aceptado
- dos fueron modificados después de precisar su alcance o severidad
- dos fueron rechazados

Uno de los hallazgos modificados detectó que `ReadingService.list_readings_for_sensor` dependía de las restricciones de paginación del router y no protegía directamente las invariantes `1 <= limit <= 100` y `offset >= 0`. La IA también propuso cinco casos borde adicionales. La propuesta de paginación fue modificada para separar las tres invariantes en pruebas independientes.

### Decisión

Se decidió incorporar validación defensiva de paginación dentro de `ReadingService` para que sus reglas se mantengan incluso cuando el servicio sea utilizado directamente sin pasar por FastAPI. Se rechazó corregir silenciosamente límites excesivos y se mantuvieron las mismas reglas que utiliza actualmente la API:

- `1 <= limit <= 100`
- `offset >= 0`

Se creó `InvalidPaginationError` como excepción específica de dominio. También se creó `FakeReadingRepository` para permitir pruebas unitarias del servicio sin depender de SQLAlchemy o una base de datos.

### Ciclo TDD verificado

El primer estado rojo ocurrió porque `InvalidPaginationError` todavía no existía y pytest no pudo importar la excepción.
Después de definir únicamente el contrato de la excepción, las tres pruebas llegaron a ejecutarse pero fallaron porque `ReadingService` todavía no lanzaba `InvalidPaginationError`.
Finalmente se incorporó la validación mínima en `list_readings_for_sensor` y las tres pruebas quedaron verdes:

- `test_list_readings_rejects_limit_below_minimum`
- `test_list_readings_rejects_limit_above_maximum`
- `test_list_readings_rejects_negative_offset`

Durante la implementación, mypy detectó accidentalmente que se había eliminado parte del flujo original de `list_readings_for_sensor`. El error `Missing return statement` permitió identificar que faltaban la comprobación del sensor y la delegación final al repositorio. Se restauró el comportamiento original y se conservó únicamente la nueva validación.

### Resultado

* Ruff terminó correctamente sobre `app` y `tests`.
* mypy terminó sin problemas en 35 archivos.
* Las tres nuevas pruebas unitarias fueron aprobadas.
* La suite completa terminó con 27 pruebas aprobadas.
* La cobertura global fue de 91.75 %
* No se detectaron regresiones en los casos existentes.


### Intervención 5 — Generación de casos borde y corrección temporal mediante TDD

Continuar utilizando los hallazgos previamente auditados para generar nuevas pruebas antes de modificar el código. Se decidió utilizar la IA como fuente de propuestas de casos borde, pero revisar cada propuesta antes de incorporarla. También se decidió no convertir automáticamente una fecha naive a UTC, porque hacerlo implicaría asumir información temporal que el cliente no proporcionó.

### Consulta realizada a la IA

Se solicitó proponer exactamente cinco casos adicionales para `ReadingService`, priorizando casos borde, invariantes de negocio, comportamiento directo del servicio y errores que pudieran quedar ocultos por las validaciones del router. La IA propuso casos relacionados con:

- paginación inválida
- combinación de fechas naive y aware
- actualización de una lectura cuyo sensor propietario no existe
- sensores históricos sin regla física registrada
- eliminación de una lectura inexistente

### Análisis de las propuestas de la IA

La propuesta de paginación fue modificada para separar tres invariantes diferentes en pruebas independientes. La propuesta temporal también fue modificada. La IA sugirió inicialmente una prueba que esperara el `TypeError` actual, pero se decidió no convertir un error accidental en el comportamiento esperado del sistema. En su lugar se definió como comportamiento deseado una excepción explícita de dominio: `InvalidDateTimezoneError`.
También se detectó que la IA hizo referencia incorrecta a la numeración de algunos hallazgos del code review, por lo que esa información se corrigió durante la revisión humana.

### Ciclo TDD temporal verificado

El primer estado rojo ocurrió porque `InvalidDateTimezoneError` todavía no existía. Después de crear únicamente la excepción, la prueba pudo ejecutarse y reprodujo el defecto real:

`TypeError: can't compare offset-naive and offset-aware datetimes`

Posteriormente se añadió una validación en `ReadingService` que comprueba si `start_date` y `end_date` utilizan de manera consistente información de zona horaria antes de compararlas. La prueba unitaria quedó entonces verde.
Se añadió además una prueba de integración para comprobar el mismo caso a través de la API. Esta prueba volvió a quedar roja porque la nueva excepción de dominio escapaba de FastAPI al no existir todavía un manejador HTTP.
Finalmente se registró un manejador de `InvalidDateTimezoneError` que transforma la excepción en HTTP 400 y la prueba de integración quedó verde.

### Decisión

Se decidió rechazar únicamente la mezcla de fechas naive y aware. No se realizó ninguna conversión automática de fechas naive a UTC y no se impuso todavía que todo SensorHub utilice exclusivamente UTC, ya que esas decisiones requerirían una política temporal más amplia. La corrección quedó limitada al defecto demostrado durante el code review. Se incorporaron cinco pruebas nuevas:

- tres pruebas unitarias de invariantes de paginación
- una prueba unitaria de incompatibilidad temporal
- una prueba de integración de incompatibilidad temporal

Las pruebas nuevas finalizaron correctamente.
* Ruff terminó sin errores.
* mypy terminó sin problemas en 35 archivos.
* La suite completa terminó con 29 pruebas aprobadas.
* La cobertura global fue de 91.81 %, superior al mínimo requerido de 80 %.

Se mantuvo una advertencia de deprecación proveniente de `Starlette TestClient` y `httpx`, no relacionada con los cambios realizados durante esta actividad.

### Intervención 6 — Elaboración del ADR 0001 con apoyo de IA

Documentar formalmente la arquitectura actual de SensorHub mediante un Architecture Decision Record. La decisión arquitectónica ya existía en el proyecto y consiste en mantener la separación:

`routers -> services -> repositories -> models`

con servicios que dependen de contratos de repositorio definidos mediante `Protocol`. La intención del ADR fue formalizar y justificar una decisión ya implementada, no solicitar a la IA que eligiera una arquitectura nueva.

### Consulta realizada a la IA

Se proporcionaron a la IA notas basadas en el estado real de SensorHub, incluyendo:

- responsabilidades de routers, services, repositories y models
- uso de `Protocol` en `SensorRepository` y `ReadingRepository`
- necesidad de probar reglas de negocio sin una base de datos real
- aislamiento de FastAPI y SQLAlchemy
- utilización de repositorios falsos en pruebas unitarias
- costes derivados de mantener más capas y abstracciones
- alternativa de concentrar HTTP, negocio y persistencia en los routers

Se solicitó redactar un borrador de ADR utilizando únicamente estas notas y estructurarlo mediante:

- Estado
- Contexto
- Decisión
- Consecuencias

### Propuesta de la IA

La IA generó un borrador que mantuvo la arquitectura existente como decisión principal e identificó correctamente tanto sus ventajas como sus costes.
El borrador también presentó como alternativa una arquitectura más directa en la que los routers accedieran a SQLAlchemy y concentraran las reglas de negocio. No se detectaron tecnologías, patrones o requisitos relevantes inventados fuera de las notas proporcionadas.

### Revisión

El borrador generado por IA no se incorporó directamente. Se modificó para indicar expresamente que el ADR formaliza una arquitectura que ya está implementada en SensorHub. También se precisó que los contratos definidos mediante `Protocol` permiten que los servicios trabajen contra abstracciones sin conocer las implementaciones concretas de persistencia.
Se redujeron algunas repeticiones entre Contexto, Decisión y Consecuencias sin modificar la decisión arquitectónica. No se incorporaron microservicios, CQRS, DDD ni otros patrones que no forman parte de la decisión documentada.

### Decisión

Mantener y formalizar la arquitectura:

`routers -> services -> repositories -> models`

* Los servicios seguirán dependiendo de contratos de repositorio definidos mediante `Protocol`.
* FastAPI permanecerá principalmente en los routers y SQLAlchemy permanecerá detrás de los repositorios.
* Se acepta que esta separación introduce más archivos, abstracciones y coordinación entre capas a cambio de facilitar pruebas unitarias, reducir acoplamiento y mantener diferenciadas las responsabilidades.

### Resultado

Se creó:

`docs/adr/0001-arquitectura-en-capas.md`

El ADR documenta el contexto, la alternativa considerada, la decisión adoptada y sus consecuencias positivas y negativas. La ubicación y el contenido del archivo fueron revisados manualmente antes de incorporarlos al repositorio.

### Intervención 7 — Umbral configurable y estrategia de detección de anomalías mediante TDD

Comenzar la funcionalidad de detección de anomalías aplicando TDD estricto y conservar la arquitectura desacoplada utilizada por SensorHub.
Se decidió que el umbral fuera configurable individualmente por sensor mediante `alert_threshold`. También se decidió que el umbral fuera opcional. Un valor `None` representa que el sensor no tiene configurada una detección basada en umbral. La decisión buscó conservar compatibilidad con los sensores existentes y evitar asignarles artificialmente un valor de alerta.

### Consulta realizada a la IA

Se solicitó avanzar paso a paso desde el comportamiento más pequeño, escribiendo primero pruebas que fallaran antes de modificar la implementación.
La IA propuso separar el criterio de detección mediante un contrato `AlertStrategy` y una primera implementación `ThresholdAlertStrategy`, de manera que el criterio pueda sustituirse posteriormente sin modificar al consumidor. También propuso incorporar `alert_threshold` al modelo y a los contratos de sensores de forma incremental mediante TDD.

### Primer ciclo TDD — Estrategia de detección

Se escribió primero una prueba para comprobar que una estrategia basada en umbral considerara anómalo un valor superior al límite configurado.

**El estado RED produjo:**

`ModuleNotFoundError: No module named 'app.domain.alert_strategy'`

Después se implementaron:

- `AlertStrategy` mediante `Protocol`
- `ThresholdAlertStrategy`

La implementación mínima utiliza la regla:

`value > threshold`

**La prueba quedó en GREEN.**

### Segundo ciclo TDD — Creación de sensor con umbral

Se añadió una prueba que intentó crear un sensor con `alert_threshold=30.0`.

**El primer RED produjo:**

`AttributeError: 'Sensor' object has no attribute 'alert_threshold'`

Se incorporó el nuevo atributo al modelo `Sensor` y se comenzó a propagar desde `SensorService`. Durante la implementación se detectó que `SensorCreate` todavía no contenía el nuevo campo. pytest y mypy mostraron que el contrato estaba incompleto.

mypy reportó:

`"SensorCreate" has no attribute "alert_threshold"` y `Unexpected keyword argument "alert_threshold" for "SensorCreate"`

Al corregir el esquema se introdujo accidentalmente una segunda definición de `SensorCreate` dentro de `SensorUpdate`, provocando un `IndentationError`.
La IA ayudó a localizar la duplicación y se decidió restaurar únicamente `app/schemas/sensor.py` desde el último commit válido para volver a aplicar solamente el cambio necesario. Después de reparar el archivo, la prueba de creación con umbral quedó en GREEN y Ruff y mypy finalizaron correctamente.

### Tercer ciclo TDD — Actualización del umbral

Se añadió una prueba para modificar un sensor existente desde `30.0` hasta `35.0`. 

**El RED confirmó que** `SensorUpdate` ignoraba todavía el nuevo campo:

`assert 30.0 == 35.0`

Se incorporó `alert_threshold` a `SensorUpdate`.

No fue necesario modificar la lógica de `SensorService.update_sensor`, ya que el mecanismo existente basado en `model_dump(exclude_unset=True)` y `setattr` admitió automáticamente el nuevo campo. Se decidió no incluir `alert_threshold` dentro del validador que rechaza valores nulos para otros atributos, porque `None` tiene un significado válido: desactivar el umbral. **La prueba quedó en GREEN.**

### Cuarto ciclo TDD — Contrato HTTP

Se añadió una prueba de integración para crear un sensor mediante `POST /sensors/` con `alert_threshold=30.0` y comprobar que el valor apareciera en la respuesta.

**El estado RED produjo:**

`KeyError: 'alert_threshold'`

La creación y persistencia ya funcionaban, pero `SensorResponse` no exponía todavía el atributo. Se incorporó `alert_threshold: float | None` al esquema de respuesta y **la prueba quedó en GREEN.**

### Validación del esquema persistente

Aunque todas las pruebas pasaban, se decidió comprobar también la base SQLite utilizada por la aplicación. La inspección mostró que el modelo SQLAlchemy ya contenía `alert_threshold`, pero la tabla física `sensors` todavía conservaba únicamente:

`id, code, name, sensor_type, unit, created_at`

Esto confirmó que las pruebas construían correctamente un esquema nuevo desde los metadatos, pero que la base persistente necesitaba una migración.

Se comprobó que existía la migración inicial `eacacdab5dc6`. La base `sensorhub.db` contenía el mismo esquema representado por esa revisión, pero no tenía la tabla `alembic_version`. Antes de modificarla se verificaron:

- columnas de `sensors`
- índice único `ix_sensors_code`
- columnas de `readings`
- clave foránea `readings.sensor_id -> sensors.id`
- configuración de `target_metadata = Base.metadata`

También se creó una copia de seguridad de la base antes de adoptar el historial. Después de comprobar la equivalencia se ejecutó `alembic stamp eacacdab5dc6`. El `stamp` registró el estado existente sin volver a ejecutar la migración inicial.
Se utilizó `alembic revision --autogenerate` y Alembic detectó únicamente `Detected added column 'sensors.alert_threshold'`. Se generó la revisión `b89c5db35c12`. La migración candidata fue revisada manualmente antes de aplicarla. Se confirmó que únicamente agregaba una columna nullable `alert_threshold` y que su `downgrade` eliminaba exclusivamente esa columna. Se mantuvo `nullable=True` para preservar la compatibilidad con sensores históricos. Después se aplicó `alembic upgrade head`. La base quedó en `b89c5db35c12 (head)`. La inspección física confirmó la nueva columna y preservó los sensores existentes con `alert_threshold = NULL`.

### Decisión

Mantener un umbral opcional por sensor y encapsular el criterio de detección detrás de `AlertStrategy`.
La primera estrategia concreta será `ThresholdAlertStrategy`.
La configuración del umbral forma parte del sensor, mientras que la decisión de considerar anómala una lectura queda separada detrás de una estrategia intercambiable.
Se decidió además versionar mediante Alembic cualquier modificación persistente del esquema en lugar de depender de `Base.metadata.create_all()` para evolucionar tablas existentes.

### Resultado

La validación final del bloque produjo:

- Ruff sin errores en `app`, `tests` y `migrations`
- mypy sin errores en 37 archivos
- 33 pruebas aprobadas
- cobertura global de 91.95 %
- Alembic en `b89c5db35c12 (head)`
- columna `sensors.alert_threshold` presente físicamente
- sensores históricos preservados con umbral nulo
- una advertencia existente de `Starlette TestClient` y `httpx`, no relacionada con los cambios realizados

## Intervención 8 — Generación, persistencia y consulta de alertas mediante TDD

Continuar la funcionalidad de anomalías iniciada en la intervención anterior hasta conseguir que una lectura que supere el umbral configurado genere una alerta persistente y que dichas alertas puedan consultarse posteriormente mediante la API. Como decisión del estudiante, se mantuvo la arquitectura existente de SensorHub:

`routers -> services -> repositories -> models`

También se mantuvo la decisión previa de separar el criterio de detección mediante `AlertStrategy`, evitando incorporar directamente la comparación del umbral como una responsabilidad fija de la persistencia o del router.

### Consulta realizada a la IA

Se solicitó continuar estrictamente paso a paso mediante TDD, sin implementar la funcionalidad completa de una sola vez y verificando cada comportamiento antes de avanzar. La se indicó a la IA desarrollar la funcionalidad en ciclos pequeños:

1. comprobar que `ReadingService` pueda generar una alerta cuando una lectura supere el umbral
2. crear la persistencia concreta de alertas mediante un repositorio SQLAlchemy
3. conectar el repositorio y la estrategia con el flujo HTTP existente
4. incorporar la consulta de alertas por sensor
5. crear una capa `AlertService`
6. exponer la consulta mediante un endpoint HTTP
7. comprobar los casos de frontera
8. versionar la nueva tabla mediante Alembic y verificar su reversibilidad

La propuesta fue aceptada y aplicada de forma incremental, conservando evidencia de los estados RED y GREEN.

### Primer ciclo TDD — Generación de alerta desde `ReadingService`

Se escribió primero una prueba unitaria para comprobar que una lectura superior al umbral provocara la creación de una alerta. La prueba utilizó un sensor de temperatura con `alert_threshold = 30.0` y una lectura `value = 31.0` También se utilizó un `Mock` como colaborador observable para comprobar que el servicio solicitara la persistencia de exactamente una alerta.

**El estado RED produjo:**

`TypeError: ReadingService.__init__() got an unexpected keyword argument 'alert_repository'`

El error confirmó que `ReadingService` todavía no admitía colaboradores relacionados con alertas.
Para llevar el escenario a GREEN se incorporaron:

- el modelo `Alert`
- el contrato `AlertRepository`
- las dependencias opcionales `alert_repository` y `alert_strategy` dentro de `ReadingService`
- la creación de una alerta después de persistir la lectura y obtener su identificador

La alerta conserva:

- `sensor_id`
- `reading_id`
- `value`
- `threshold`
- `created_at`

Se decidió conservar el valor observado y el umbral dentro de la alerta para disponer de una evidencia histórica del criterio utilizado en el momento de la detección.

La evaluación quedó delegada a:

`self._alert_strategy.is_anomaly(...)`

en lugar de introducir directamente la comparación dentro de `ReadingService`.

**La prueba quedó en GREEN.**
Posteriormente se ejecutaron todas las pruebas unitarias existentes de `ReadingService` y se confirmó que los cuatro comportamientos anteriores continuaban funcionando. El archivo quedó con 5 pruebas aprobadas.

### Segundo ciclo TDD — Persistencia concreta de alertas

Se creó una prueba para comprobar que una implementación SQLAlchemy pudiera persistir una entidad `Alert` y recuperar posteriormente los valores generados por la base de datos.

**El estado RED produjo:**

`ModuleNotFoundError: No module named 'app.repositories.sqlalchemy_alert_repository'` Se implementó `SqlAlchemyAlertRepository` siguiendo el mismo patrón utilizado por los repositorios existentes:

`add -> commit -> refresh`

La implementación quedó detrás del contrato `AlertRepository`. La prueba confirmó que:

- se generó un identificador para la alerta
- se generó `created_at`
- la entidad quedó almacenada físicamente
- `sensor_id`, `reading_id`, `value` y `threshold` conservaron los valores originales

**La prueba quedó en GREEN.**

### Tercer ciclo TDD — Integración de alertas con el flujo HTTP de lecturas

Aunque `ReadingService` ya podía generar alertas en pruebas unitarias y `SqlAlchemyAlertRepository` podía persistirlas, todavía no estaban conectados dentro de la composición real de dependencias de FastAPI. Se escribió una prueba de integración que:

1. creó un sensor mediante `POST /sensors/`
2. configuró `alert_threshold=30.0`
3. registró una lectura con `value=31.0`
4. consultó directamente la base temporal para comprobar que existiera una alerta

La lectura se creó correctamente mediante HTTP, pero la base no contenía ninguna alerta.

**El estado RED produjo:**

`assert 0 == 1`

La causa fue que `get_reading_service()` todavía construía `ReadingService` únicamente con los repositorios de lecturas y sensores.

Se modificó `app/dependencies.py` para construir también:

- `SqlAlchemyAlertRepository`
- `ThresholdAlertStrategy`

y se inyectaron ambos en `ReadingService`.

Se mantuvo la decisión arquitectónica de seleccionar la implementación concreta de la estrategia en el punto de composición y no dentro del servicio. De esta forma `ReadingService` sigue dependiendo del contrato `AlertStrategy`.

**La prueba de integración quedó en GREEN.**

### Cuarto ciclo TDD — Consulta de alertas por sensor en persistencia

Para permitir la consulta posterior de alertas se escribió una prueba que creó dos sensores con sus respectivas alertas y solicitó únicamente las pertenecientes al primero.

**El estado RED produjo:**

`AttributeError: 'SqlAlchemyAlertRepository' object has no attribute 'list_for_sensor'`

Se añadió al contrato `AlertRepository`:

`list_for_sensor(sensor_id: int) -> list[Alert]`

y se implementó la operación en `SqlAlchemyAlertRepository` mediante una consulta filtrada por `sensor_id`. También se definió un orden determinista utilizando:

`Alert.created_at` y posteriormente: `Alert.id` como segundo criterio.

Las dos pruebas del repositorio, creación y consulta, quedaron en GREEN.

### Quinto ciclo TDD — Capa de servicio para alertas

Se decidió no conectar el router directamente con `SqlAlchemyAlertRepository`, ya que esto rompería el patrón arquitectónico utilizado por SensorHub. Se escribió primero una prueba para una nueva capa `AlertService`.

**El estado RED produjo:**

`ModuleNotFoundError: No module named 'app.services.alert_service'`

Se creó `AlertService` dependiendo exclusivamente de:

- `AlertRepository`
- `SensorRepository`

El servicio comprueba primero que el sensor solicitado exista y después delega la consulta de sus alertas al repositorio. Se mantuvo el mismo comportamiento utilizado en otras consultas del proyecto:

- sensor inexistente -> `SensorNotFoundError`
- sensor existente sin resultados -> lista vacía

**La prueba quedó en GREEN.**

### Sexto ciclo TDD — Consulta HTTP de alertas

Se creó una prueba de integración para el nuevo comportamiento: `GET /sensors/{sensor_id}/alerts`

La prueba generó primero una alerta real mediante: `POST /sensors/{sensor_id}/readings`

y después intentó recuperarla mediante la nueva ruta.

**El estado RED produjo:**

`assert 404 == 200`

El `404` confirmó que todavía no existía ninguna ruta registrada para consultar alertas. Para llevar el escenario a GREEN se incorporaron:

- `AlertResponse`
- `get_alert_service()`
- `app/routers/alerts.py`
- el registro de `alerts_router` en `app/main.py`

El router conserva únicamente responsabilidades HTTP:

- recibe `sensor_id`
- obtiene `AlertService` mediante dependencia
- delega la consulta al servicio
- convierte los modelos ORM a `AlertResponse`

No realiza consultas directas mediante SQLAlchemy.

**La prueba quedó en GREEN.**

Durante la validación Ruff detectó un único problema de orden de imports en `app/routers/alerts.py`:

`I001 Import block is un-sorted or un-formatted`
Se utilizó `ruff --fix` exclusivamente sobre ese archivo. Después Ruff y mypy finalizaron sin errores.

### Pruebas de frontera y regresión

Después de completar los ciclos RED -> GREEN se agregaron pruebas adicionales para fijar explícitamente comportamientos que la implementación ya satisfacía. Estas pruebas no se registraron artificialmente como nuevos ciclos RED porque la funcionalidad correspondiente ya estaba implementada.

Se comprobaron los siguientes casos:

- `value > threshold` genera una alerta
- `value == threshold` no genera una alerta
- un sensor existente sin alertas responde `200` con `[]`
- consultar alertas de un sensor inexistente responde `404`

La regla final de `ThresholdAlertStrategy` permanece:

`value > threshold`

Por lo tanto, un valor exactamente igual al umbral no se considera anómalo.
Las pruebas específicas de dominio, servicio, repositorio, lecturas e integración HTTP produjeron `25 passed`

### Migración de la tabla `alerts`

Después de comprobar el comportamiento en la base SQLite temporal de pruebas se decidió versionar también la nueva estructura de persistencia mediante Alembic. La base real se encontraba correctamente en `b89c5db35c12 (head)` y existía un único head. Se actualizó `migrations/env.py` para registrar explícitamente `Alert, Reading, Sensor` y se comprobó que `Base.metadata` contenía `['alerts', 'readings', 'sensors']`. Después se ejecutó `alembic revision --autogenerate -m "crear tabla de alertas"`. Alembic detectó exclusivamente `Detected added table 'alerts'`. Se generó la revisión `ccdeecc8c528` con `down_revision = "b89c5db35c12"`. La migración candidata fue revisada manualmente antes de aplicarse. Se confirmó que únicamente creaba la tabla `alerts` con:

- `id`
- `sensor_id`
- `reading_id`
- `value`
- `threshold`
- `created_at`
- clave foránea `sensor_id -> sensors.id`
- clave foránea `reading_id -> readings.id`

El `downgrade()` únicamente elimina la tabla `alerts`. Se limpiaron los comentarios genéricos generados por Alembic y se mantuvo la misma semántica de la migración. Ruff detectó inicialmente el orden de imports y lo corrigió mediante `--fix`.

### Respaldo y aplicación de la migración

Antes de ejecutar DDL sobre la base persistente se creó el respaldo
Después se aplicó:

`alembic upgrade head`

Alembic ejecutó:

`b89c5db35c12 -> ccdeecc8c528`

La revisión aplicada y el head quedaron ambos en:

`ccdeecc8c528 (head)`

La inspección física de SQLite confirmó las tablas:

- `alembic_version`
- `alerts`
- `readings`
- `sensors`

La tabla `alerts` quedó formada por:

- `id INTEGER`
- `sensor_id INTEGER`
- `reading_id INTEGER`
- `value FLOAT`
- `threshold FLOAT`
- `created_at DATETIME DEFAULT CURRENT_TIMESTAMP`

También se verificaron físicamente las claves foráneas:

- `sensor_id -> sensors.id`
- `reading_id -> readings.id`

Los sensores existentes permanecieron sin modificaciones:

- `(1, 'TEMP-5771F74A', None)`
- `(2, 'HUM-b4f6fc', None)`

### Verificación de reversibilidad de la migración

Antes de comprobar el `downgrade()` se verificó que la tabla `alerts` no contuviera registros `Alertas almacenadas: 0` se ejecutó `alembic downgrade b89c5db35c12` Alembic realizó `ccdeecc8c528 -> b89c5db35c12`. La inspección física confirmó que `alerts` desapareció mientras permanecieron:

- `alembic_version`
- `readings`
- `sensors`

Los datos históricos de sensores permanecieron intactos. Después se ejecutó nuevamente `alembic upgrade head`. La tabla `alerts` fue recreada y la base regresó a `ccdeecc8c528 (head)`. Con esto se comprobó tanto el camino de actualización como el de reversión de la migración.

### Decisión

Mantener la detección de anomalías distribuida mediante responsabilidades explícitas:

- `Sensor.alert_threshold` almacena la configuración individual del sensor
- `AlertStrategy` define el contrato para decidir si una lectura es anómala
- `ThresholdAlertStrategy` implementa actualmente la comparación por umbral
- `ReadingService` coordina la generación de alertas cuando se registra una lectura
- `AlertRepository` abstrae la persistencia
- `SqlAlchemyAlertRepository` implementa la persistencia concreta
- `AlertService` coordina la consulta de alertas y valida la existencia del sensor
- `alerts_router` expone las operaciones HTTP
- `AlertResponse` define el contrato público de respuesta
- Alembic versiona la tabla persistente `alerts`

La elección de `ThresholdAlertStrategy` se realiza en `app/dependencies.py`, permitiendo sustituirla por otra implementación compatible sin modificar `ReadingService`. Esto conserva el principio abierto/cerrado aplicado a la estrategia de alertas.

### Resultado

La validación final de la funcionalidad produjo:

- 42 pruebas aprobadas
- cobertura global de 93.13 %
- cobertura mínima requerida de 80 % superada
- Ruff sin errores en `app`, `tests` y `migrations`
- mypy sin errores en 46 archivos
- `git diff --check` sin errores
- `AlertStrategy` y `ThresholdAlertStrategy` funcionando
- generación automática de alertas al superar el umbral
- persistencia mediante `SqlAlchemyAlertRepository`
- consulta mediante `GET /sensors/{sensor_id}/alerts`
- comportamiento `200 []` para sensores existentes sin alertas
- comportamiento `404` para sensores inexistentes
- tabla `alerts` presente físicamente
- claves foráneas verificadas
- migración `ccdeecc8c528` comprobada mediante `upgrade`, `downgrade` y nuevo `upgrade`
- base final en `ccdeecc8c528 (head)`
- datos históricos de sensores preservados
- una advertencia existente de `Starlette TestClient` y `httpx`, no relacionada con los cambios realizados

### Trazabilidad de prompts y decisiones

Las consultas de esta intervención se realizaron de forma iterativa a partir de los resultados obtenidos en cada ciclo TDD. Cuando la interacción consistió en continuar a partir de una salida de terminal, se conserva aquí un resumen de la intención del prompt.

| Prompt o consulta realizada | Qué propuso o generó la IA | Qué cambió | Por qué |
|---|---|---|---|
| Continuar la detección de anomalías mediante TDD estricto, avanzando únicamente después de verificar cada comportamiento | Propuso comenzar comprobando que `ReadingService` generara una alerta cuando una lectura superara el umbral e introducir `AlertStrategy` y `AlertRepository` como abstracciones | Se aceptó separar la estrategia y la persistencia mediante contratos | Permite aplicar OCP y mantener `ReadingService` desacoplado de una estrategia concreta y de SQLAlchemy |
| Después del RED `ReadingService.__init__() got an unexpected keyword argument 'alert_repository'`, solicitar la implementación mínima para obtener GREEN | Propuso incorporar el modelo `Alert`, el contrato `AlertRepository` y las dependencias `alert_repository` y `alert_strategy` en `ReadingService` | Se aceptó la propuesta y se decidió conservar en la alerta `sensor_id`, `reading_id`, `value` y `threshold` | Esos datos permiten conocer qué lectura produjo la alerta y conservar el criterio utilizado aunque posteriormente cambie el umbral del sensor |
| Solicité cómo persistir las alertas sin romper la arquitectura existente | Propuso crear `SqlAlchemyAlertRepository` siguiendo el patrón de los repositorios actuales | Se aceptó e implementó primero mediante una prueba que produjo el RED por módulo inexistente | Mantiene la persistencia detrás de `AlertRepository` y reutiliza el patrón ya utilizado por SensorHub |
| Después de que la creación HTTP de una lectura no almacenara ninguna alerta, solicité el diagnóstico | Identificó que `get_reading_service()` todavía no inyectaba `SqlAlchemyAlertRepository` ni `ThresholdAlertStrategy` | Se decidió modificar únicamente `app/dependencies.py` para realizar la composición de esas dependencias | La lógica del servicio y del repositorio ya funcionaba por separado; el problema estaba en el punto de composición |
| Solicité cómo hacer consultables las alertas por sensor manteniendo la arquitectura en capas | Propuso añadir `list_for_sensor()` al repositorio, crear `AlertService`, `AlertResponse` y un router independiente para alertas | Se aceptó crear un servicio y router específicos en lugar de consultar el repositorio directamente desde un endpoint existente | Mantiene el flujo `router -> service -> repository -> model` y evita introducir SQLAlchemy en la capa HTTP |
| Solicité la validación de los casos de frontera | Propuso comprobar igualdad con el umbral, sensor existente sin alertas y sensor inexistente | Se añadieron las pruebas, pero no se registraron como ciclos RED porque la implementación ya satisfacía esos comportamientos | Distinguir pruebas de regresión de ciclos RED reales mantiene una bitácora fiel al proceso realizado |
| Solicité cómo incorporar la nueva tabla `alerts` a la base persistente | Propuso registrar `Alert` en Alembic, utilizar `--autogenerate`, revisar la migración antes de aplicarla y respaldar la base | Se aceptó el procedimiento y no se aplicó la migración hasta comprobar que Alembic detectara únicamente `Added table 'alerts'` | Evita aplicar automáticamente cambios inesperados al esquema existente |
| Solicité una verificación final de la migración | Propuso comprobar físicamente tablas, columnas y claves foráneas y verificar `downgrade` seguido de un nuevo `upgrade` | Se aceptó probar la reversibilidad después de comprobar que la tabla `alerts` contenía cero registros y que existía un respaldo previo | Permite comprobar ambos sentidos de la migración sin poner en riesgo información almacenada |