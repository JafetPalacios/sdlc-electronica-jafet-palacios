# ADR 0001: Arquitectura en capas para SensorHub

## Estado

Aceptado

## Contexto

SensorHub es una API desarrollada con FastAPI y Python 3.12.
Durante su desarrollo se adoptó la siguiente organización:

`routers -> services -> repositories -> models`

Cada capa mantiene una responsabilidad diferenciada:

- Los `routers` gestionan responsabilidades HTTP como rutas, parámetros, dependencias y esquemas de respuesta
- Los `services` concentran las reglas de negocio y coordinan operaciones sin depender directamente de FastAPI o SQLAlchemy
- Los `repositories` encapsulan las operaciones de persistencia
- Los `models` representan las entidades persistidas mediante SQLAlchemy

Los contratos `SensorRepository` y `ReadingRepository` están definidos mediante `Protocol`. Esto permite que los servicios trabajen contra abstracciones y no conozcan las implementaciones concretas utilizadas para acceder a los datos.

Esta organización responde a necesidades observadas durante el desarrollo:

- Probar reglas de negocio sin utilizar una base de datos real
- Evitar que FastAPI y SQLAlchemy se propaguen por toda la lógica de negocio
- Poder sustituir implementaciones de persistencia sin modificar los servicios
- Mantener responsabilidades diferenciadas entre transporte HTTP, negocio y persistencia
- Facilitar pruebas unitarias mediante repositorios falsos
- Mantener una estructura que pueda crecer con nuevas funcionalidades

La arquitectura ya cuenta con evidencia práctica dentro del proyecto.
`FakeSensorRepository` permite probar `SensorService` sin utilizar una base de datos y durante la Semana 5 se incorporó `FakeReadingRepository` para probar `ReadingService` bajo el mismo principio.
Las pruebas unitarias construyen los servicios mediante la inyección de repositorios falsos, mientras que la aplicación utiliza implementaciones de repositorio basadas en SQLAlchemy. En ambos casos los servicios trabajan contra los mismos contratos.
Esta separación también permitió incorporar validaciones de negocio a `ReadingService` sin modificar la implementación de persistencia.
Como alternativa se consideró una arquitectura más directa donde los routers accedieran a SQLAlchemy y concentraran también las reglas de negocio.
Esta alternativa reduciría inicialmente la cantidad de archivos y abstracciones, pero aumentaría el acoplamiento entre transporte HTTP, lógica de negocio y persistencia. También dificultaría probar las reglas de negocio de manera aislada y sustituir la infraestructura de persistencia.

## Decisión

Se formaliza y mantiene la arquitectura en capas:

`routers -> services -> repositories -> models`

* Los `routers` concentrarán las responsabilidades relacionadas con HTTP.
* Los `services` concentrarán las reglas de negocio y la coordinación de operaciones sin depender directamente de FastAPI ni de SQLAlchemy.
* Los `repositories` encapsularán las operaciones de persistencia y actuarán como límite entre los servicios y las implementaciones concretas de acceso a datos.
* Los `models` representarán las entidades persistidas mediante SQLAlchemy.
* Los servicios dependerán de contratos de repositorio definidos mediante `Protocol`, como `SensorRepository` y `ReadingRepository`, en lugar de depender directamente de las implementaciones concretas basadas en SQLAlchemy.
* FastAPI permanecerá principalmente en la capa de routers y SQLAlchemy permanecerá detrás de los repositorios.

## Consecuencias

### Ventajas

- Las reglas de negocio pueden probarse sin utilizar una base de datos real
- Los servicios pueden utilizar repositorios falsos durante las pruebas unitarias
- FastAPI no se propaga hacia la lógica de negocio
- SQLAlchemy queda aislado detrás de los repositorios
- Los servicios dependen de abstracciones en lugar de implementaciones concretas de persistencia
- Las implementaciones de persistencia pueden sustituirse sin modificar los servicios mientras mantengan el contrato esperado
- Las responsabilidades de transporte HTTP, negocio y persistencia permanecen diferenciadas
- Las reglas de negocio pueden evolucionar dentro de los servicios sin requerir cambios en la implementación de persistencia

### Costes

- La arquitectura requiere más archivos y abstracciones que una implementación donde transporte, negocio y persistencia estén concentrados
- Una funcionalidad puede requerir cambios coordinados en varias capas
- Las funcionalidades pequeñas implican mayor ceremonia
- Los contratos de repositorio y sus implementaciones deben mantenerse alineados
- Se acepta una mayor complejidad estructural inicial a cambio de conservar la separación de responsabilidades