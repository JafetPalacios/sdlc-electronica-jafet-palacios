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



## Entrada 2: Aplicación de SRP, OCP, LSP, ISP y DIP al dominio de sensores

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

#### ISP

Ejemplo incorrecto: 
Le pedí una interfaz demasiado grande que exige leer, calibrar y conectarse, pero con un sensor que solo puedan leer
La IA creó un protocolo grande llamado BadSensorInterface que exigía tres métodos:

* read()
* calibrate()
* connect()

También se creó BadBasicTemperatureSensor, que únicamente podía leer, pero estaba obligado a implementar calibrate() y connect() lanzando NotImplementedError.

Ejemplo correcto: 
Pedí que ahora separara la interfáz para para solo llamarlas dependiendo del sensor. Y que creara 2 sensores: uno que solo leyera y otro que hiciera todo
La IA dividió la interfaz grande en tres protocolos:

* ReadableSensor
* CalibratableSensor
* ConnectableSensor

Tambien creó:

BasicTemperatureSensor, que solo implementa lectura.
AdvancedTemperatureSensor, que implementa lectura, calibración y conexión.

También se propuso funciones consumidoras específicas:

* read_sensor()
* calibrate_sensor()
* connect_sensor()

Cada función depende únicamente del protocolo que necesita.


#### DIP

Ejemplo incorrecto:
Solicité a la IA un ejmplo completo. Decidí conservar el ejemplo incorrecto que me dió porque demuestra que una clase puede funcionar, pero no por eso es una solución corecta.
La IA creó BadDataProcessor, que construye directamente una instancia de:

JsonFileRepository

Esto une al procesador con una implementación concreta de almacenamiento.

Ejemplo correcto:
Solicité a la IA tecnicas para hacer el ejercicio de manera correcta y me dio opciones como:

* Inyección por método
* Inyección por constructor
* Inyección mediante atributo o setter
* Pasar una función en lugar de un objeto
* Patrón Strategy
* Factory
* Registro de implementaciones
* Service Locator

Decidí utilizar inyección por constructor en lugar de crear el repositorio dentro de DataProcessor porque la dependencia queda visible y puede elegirse desde el exterior y esto facilita:

* cambiar implementaciones;
* probar el procesador;
* utilizar repositorios simulados;
* evitar acoplamiento con una clase concreta.

La IA creó un protocolo DataRepository con el método save(value: float) -> str
También se creó dos repositorios concretos

* MemoryRepository
* JsonFileRepository

Finalmente, DataProcessor recibió el repositorio mediante el constructor:
DataProcessor(repository)


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

Se crearon 10 tests:

* Dos para SRP.
* Dos para OCP.
* Dos para LSP.
* Dos para ISP.
* Dos para DIP.

Los tests verificaron:

* que el ejemplo incorrecto de SRP leyera y guardara en una misma operación;
* que el diseño correcto separara lectura y persistencia;
* que el formateador incorrecto para OCP dependiera de tipos conocidos;
* que el diseño correcto aceptara un formateador nuevo;
* que el sensor incorrecto de LSP rompiera el contrato de porcentaje;
* que la clase correcta pudiera sustituir a la clase base;
* que en el ejemplo incorrecto de ISP el sensor puede leer, pero falla al intentar calibrarse o conectarse;
* que el sensor básico puede utilizarse únicamente mediante un contrato, mientras que el sensor avanzado puede utilizarse con los tres contratos;
* que el ejemplo incorrecto de DIP siempre utiliza el repositorio JSON concreto;
* que el diseño correcto pueda trabajar con MemoryRepository y JsonFileRepository sin modificar su implementación.

### Verificaciones finales

La actividad terminó con:

todos los tests aprobados
mypy sin errores
ruff sin errores
 
