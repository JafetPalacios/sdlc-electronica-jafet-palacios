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