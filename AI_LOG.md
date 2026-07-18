# AI_LOG

## Entrada 1 — Enum, dataclass frozen, Protocol y funciones puras

**Fecha:** 18 de julio de 2026

### Prompt utilizado

Solicité orientación paso a paso para practicar `Enum`, `dataclass(frozen=True)` y `Protocol` mediante ejercicios del dominio de sensores. También pedí crear cinco funciones puras sobre una clase `Reading`, verificarlas con `pytest`, `mypy` y `ruff`, y avanzar únicamente después de completar cada paso. Al final pedí darle estructura a mi bitácora.

### Qué produjo la IA

La IA propuso:

* Un `Enum` llamado `SensorType` para limitar los tipos de sensores permitidos.
* Una `dataclass(frozen=True)` llamada `Reading` para representar lecturas inmutables.
* Un `Protocol` llamado `Sensor` con un método `read()`.
* Una implementación concreta llamada `TemperatureSensor`.
* Cinco funciones puras:

  * `celsius_to_fahrenheit`
  * `exceeds_threshold`
  * `apply_offset`
  * `is_within_range`
  * `difference_from_target`
* Pruebas con `pytest`.
* Verificación estática con `mypy`.
* Revisión de estilo con `ruff`.

Durante la actividad también ayudó a identificar y corregir:

* una función no guardada o no importada;
* el uso incorrecto de paréntesis dentro de una importación;
* una asignación incompatible con `mypy` en el test de inmutabilidad;
* una importación automática e innecesaria de `unittest.result`.

### Mi decisión

Decidí mantener una solución pequeña y construirla progresivamente. En lugar de aceptar una implementación extensa desde el inicio, separé la actividad en pasos individuales para comprender primero cada concepto.

La secuencia propuesta fue:

* Crear y probar el Enum.
* Crear una dataclass.
* Convertir la dataclass en inmutable con frozen=True.
* Crear un Protocol.
* Implementar las cinco funciones puras de una en una.
* Crear los tests progresivamente.
* Verificar los tipos con mypy.
* Revisar el código con ruff.


### Por qué tomé esa decisión

La solución inicial concentraba demasiados conceptos y dificultaba comprender la función de cada elemento. Trabajar paso por paso permitió relacionar cada parte del código con la instrucción de la actividad. También permitió detectar errores pequeños inmediatamente, en lugar de encontrarlos cuando todo el código ya estuviera integrado.