# Bitácora de uso de IA — Semana 5

Esta bitácora registra el uso de herramientas de inteligencia artificial durante la Semana 5 del proyecto, distinguiendo explícitamente las decisiones tomadas de las propuestas, análisis o diagnósticos proporcionados por la IA.
El objetivo es mantener trazabilidad sobre cómo se utilizó la IA como apoyo profesional sin delegar el criterio técnico.

---

### Intervención 1 — Comparación entre prompt pobre y prompt estructurado

Realizar el experimento utilizando conversaciones independientes con diferentes modelos de IA para evitar que el contexto de una respuesta anterior influyera en la siguiente generación. Se reconoce que se utilizaron modelos de IA diferentes, por lo que las diferencias observadas pueden estar influenciadas tanto por la calidad del prompt como por las características particulares de cada modelo. Esta condición se tendrá en cuenta al interpretar los resultados de las tres tareas.

Se ejecutaron dos prompts para resolver la misma tarea de conversión de Celsius a Fahrenheit. El primero fue deliberadamente poco específico y el segundo utilizó la estructura de contexto, tarea, restricciones y entrega indicada para la Semana 5.
Con el prompt pobre, la IA produjo una función matemáticamente correcta, pero decidió por cuenta propia el nombre de la función, los nombres de los parámetros y la inclusión de un ejemplo ejecutable. Tampoco aplicó redondeo a dos decimales.
Con el prompt estructurado, la IA respetó exactamente la firma solicitada, utilizó type hints, añadió el docstring requerido, implementó el redondeo a dos decimales y entregó únicamente la función.

