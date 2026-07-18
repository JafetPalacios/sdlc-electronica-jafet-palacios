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



## Entrada 2: Aplicación de SRP, OCP y LSP al dominio de sensores

**Fecha:** 18 de julio de 2026

### Prompt utilizado

Solicité orientación paso a paso para desarrollar ejemplos prácticos de los principios SOLID SRP, OCP y LSP en el dominio de sensores.
La actividad debía incluir, para cada principio:

* un ejemplo incorrecto;
* un ejemplo correcto;
* dos pruebas con `pytest`;
* validación con `mypy`;
* revisión con `ruff`.

#### SRP

Ejemplo incorrecto:
Propuse utilizar una clase que leyera y guardara la temperatura.
La IA generó una clase `BadTemperatureSensor` que lee una temperatura y también la guarda en un archivo.

Ejemplo correcto:
Propuse utilizar una clase que leyera y otra que guardara la temperatura
La IA generó:
* Una clase `TemperatureSensor` encargada únicamente de obtener la lectura.
* Una clase `ReadingFileWriter` encargada únicamente de escribir valores en archivos.

#### OCP

Ejemplo incorrecto:
Propuse que generara una clase que lee un sensor y además le diera formato
La IA propuso utilizar una cadena de condiciones como ejemplo incorrecto:
* Una clase `BadSensorFormatter` con condiciones para cada tipo de sensor.

Ejemplo correcto:
Propuse definir el comportamiento del formato y crear nuevas clases que implemente un protocolo 
La IA propuso:
* Un `Protocol` llamado `ReadingFormatter`.
* Clases independientes para temperatura y humedad.
* Una función `format_sensor_reading()` que trabaja con cualquier formateador compatible.
* Una clase adicional `PressureFormatter` creada dentro del test para demostrar que el sistema puede extenderse sin modificar el código existente.

#### LSP

Ejemplo incorrecto:
No se me ocurría un ejemplo, asi que le pedí a la IA  un ejemplo de una clase que hereda de otra pero no cumple con el contrato de la clase padre
La IA propuso utilizar sensores de porcentaje: 
* Una clase base `PercentageSensor` que devuelve porcentajes entre 0 y 100.
* Una clase hija `BadRawHumiditySensor` que devuelve un valor crudo, rompiendo el significado esperado.

Ejemplo correcto:
Le pedí que basado en el ejemplo anterior creara una clase que respeta el contrato de la clase padre y devuelve un porcentaje válido
La IA generó:
* Una clase `HumidityPercentageSensor` que devuelve un porcentaje válido.
* Una función `read_percentage()` que acepta sensores compatibles y valida que la lectura se encuentre entre 0 y 100.

### Mi decisión sobre la forma de trabajo

Decidí desarrollar cada principio por separado y no escribir toda la solución de una vez.
Para cada principio seguí esta secuencia:

1. Crear el ejemplo incorrecto.
2. Ejecutarlo manualmente.
3. Crear el ejemplo correcto.
4. Comprender la diferencia entre ambos.
5. Crear dos tests.
6. Ejecutar los tests antes de continuar.

La razón es porque considero que separar cada principio me permite entender qué problema resolvía cada uno.
También evitó mezclar conceptos diferentes y facilitó localizar errores durante las pruebas.


### Pruebas realizadas

Se crearon seis tests:

* Dos para SRP.
* Dos para OCP.
* Dos para LSP.

Los tests verificaron:

* que el ejemplo incorrecto de SRP leyera y guardara en una misma operación;
* que el diseño correcto separara lectura y persistencia;
* que el formateador incorrecto dependiera de tipos conocidos;
* que el diseño correcto aceptara un formateador nuevo;
* que el sensor incorrecto de LSP rompiera el contrato de porcentaje;
* que la clase correcta pudiera sustituir a la clase base.

### Verificaciones finales

La actividad terminó con:

```text
6 tests aprobados
mypy sin errores
ruff sin errores
```

