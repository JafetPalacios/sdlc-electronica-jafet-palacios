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