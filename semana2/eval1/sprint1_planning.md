# Planeación del Sprint 1 — Evaluación 1

## Objetivo del Sprint

Desarrollar el núcleo del sistema de monitoreo ambiental para representar lecturas de sensores, detectar anomalías mediante umbrales configurables y generar alertas utilizando estrategias intercambiables de consola y archivo.

Al finalizar el Sprint, el sistema deberá ser capaz de:

- Representar una lectura inmutable de temperatura y humedad.
- Detectar temperaturas superiores al umbral configurado.
- Detectar humedades superiores al umbral configurado.
- Cambiar los umbrales sin modificar el detector.
- Delegar la generación de alertas a una estrategia.
- Mostrar alertas en consola.
- Conservar alertas en un archivo.

## Historias seleccionadas

| ID | Historia | Prioridad | Puntos |
|---|---|---|---:|
| US-E01 | Crear una lectura de sensor | Must | 3 |
| US-E03 | Detectar temperatura anómala | Must | 3 |
| US-E04 | Detectar humedad anómala | Must | 3 |
| US-E05 | Configurar umbrales de anomalía | Must | 5 |
| US-E06 | Gestionar alertas mediante una estrategia | Must | 5 |
| US-E07 | Mostrar alertas en consola | Should | 2 |
| US-E08 | Guardar alertas en archivo | Should | 3 |

**Total comprometido: 24 puntos**

## Justificación de la selección

### US-E01 — Crear una lectura de sensor

Es la base del dominio. El detector y el gestor de alertas necesitan recibir datos representados mediante una estructura consistente, tipada e inmutable.

### US-E03 y US-E04 — Detectar anomalías

Representan las dos reglas principales del negocio:

- Temperatura superior a 35 °C.
- Humedad superior a 80 %.

Sin estas historias el sistema no podría determinar cuándo generar una alerta.

### US-E05 — Configurar umbrales

Permite inyectar los límites de temperatura y humedad al detector. Esto evita valores rígidos dentro de la implementación y facilita las pruebas automatizadas.

### US-E06 — Gestionar alertas mediante una estrategia

Separa la detección de anomalías del mecanismo utilizado para notificarlas. El gestor dependerá de una abstracción y no de una salida concreta.

### US-E07 — Mostrar alertas en consola

Proporciona una estrategia sencilla para observar las alertas durante el desarrollo y las pruebas.

### US-E08 — Guardar alertas en archivo

Permite conservar evidencia de las anomalías y demuestra que el gestor puede trabajar con otra estrategia sin cambiar su implementación.

## Historias no seleccionadas

Las historias US-E02, US-E09, US-E10, US-E11 y US-E12 permanecen en el backlog para siguientes incrementos.

No se incluyen en este Sprint porque primero necesitamos construir y validar los componentes centrales antes de procesar diez sensores, ejecutar ciclos periódicos o incorporar el simulador.


## Tareas técnicas

| ID | Historia relacionada | Tarea | Estimación |
|---|---|---|---:|
| T-01 | US-E01 | Crear la prueba fallida para construir una lectura válida | 1 h |
| T-02 | US-E01 | Implementar `SensorReading` como una estructura inmutable y tipada | 2 h |
| T-03 | US-E01 | Documentar y refactorizar el modelo de lectura | 1 h |
| T-04 | US-E03 | Crear la prueba fallida para temperatura superior al umbral | 1 h |
| T-05 | US-E04 | Crear la prueba fallida para humedad superior al umbral | 1 h |
| T-06 | US-E05 | Crear pruebas para umbrales personalizados | 1 h |
| T-07 | US-E03, US-E04 y US-E05 | Implementar `AnomalyDetector` con umbrales inyectados | 3 h |
| T-08 | US-E03, US-E04 y US-E05 | Refactorizar y documentar el detector de anomalías | 1 h |
| T-09 | US-E06 | Definir la abstracción `AlertStrategy` y su prueba fallida | 2 h |
| T-10 | US-E06 | Implementar `AlertManager` mediante inyección de dependencias | 2 h |
| T-11 | US-E07 | Crear pruebas e implementar `ConsoleAlertStrategy` | 2 h |
| T-12 | US-E08 | Crear pruebas e implementar `FileAlertStrategy` | 3 h |
| T-13 | US-E06, US-E07 y US-E08 | Refactorizar y documentar las estrategias de alerta | 1 h |
| T-14 | Todas | Ejecutar pruebas, `mypy`, `ruff` y verificar cobertura | 1 h |
| T-15 | Todas | Revisar historial TDD, documentación y criterios de aceptación | 1 h |

**Duración total estimada: 22 horas**

Todas las tareas tienen una duración máxima de 3 horas, por lo que cumplen el límite de 4 horas establecido para la planeación.

## Secuencia de desarrollo

El trabajo se realizará mediante ciclos TDD separados:

1. `SensorReading`
   - Red: prueba para crear una lectura válida.
   - Green: implementación mínima del modelo.
   - Refactor: documentación y mejora de nombres sin alterar el comportamiento.

2. `AnomalyDetector`
   - Red: pruebas para temperatura, humedad y umbrales personalizados.
   - Green: implementación mínima del detector.
   - Refactor: separación de responsabilidades y documentación.

3. `AlertManager`
   - Red: pruebas para delegar alertas a una estrategia.
   - Green: implementación del gestor y de las estrategias de consola y archivo.
   - Refactor: eliminación de duplicación y documentación del contrato.

Cada prueba fallida se registrará en un commit anterior al commit de implementación correspondiente.

## Definition of Done del Sprint

Una historia seleccionada se considera terminada cuando cumple los siguientes criterios:

### Comportamiento

- Todos sus criterios de aceptación están satisfechos.
- Los escenarios Gherkin relacionados se reflejan en pruebas automatizadas.
- El resultado puede observarse mediante la interfaz pública del componente.
- No se agregan funcionalidades fuera del alcance de la historia.

### TDD

- La prueba se escribió antes de la implementación.
- Existe evidencia de la fase Red en el historial de Git.
- Existe un commit posterior con la implementación mínima de la fase Green.
- El refactor conserva todas las pruebas en estado correcto.
- No se escriben pruebas triviales de métodos de acceso sin comportamiento.

### Calidad

- El código incluye anotaciones de tipo.
- Las clases y métodos importantes tienen documentación.
- Las líneas o decisiones no evidentes incluyen comentarios explicativos en español.
- `mypy` termina sin errores.
- `ruff` termina sin errores.
- La cobertura de `semana2` permanece en 80 % o más.

### Control de versiones

- Cada componente se desarrolla en una rama específica.
- Los commits separan pruebas, implementación y refactor.
- Se crea un pull request hacia `main`.
- El pull request contiene una descripción de la evidencia TDD.
- La rama se elimina después del merge.

### Validación final

Antes de considerar terminado el Sprint se ejecutan:

```powershell
python -m pytest
python -m mypy
python -m ruff check .\semana2
```

Los tres comandos deben finalizar correctamente.