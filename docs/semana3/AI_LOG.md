# Bitácora de uso de IA — Semana 3

## Proyecto

SensorHub API

## Rama de trabajo

`feature/semana3-sensorhub`

## Objetivo de la semana

Durante la Semana 3 desarrollé SensorHub, una API REST para administrar sensores y sus lecturas. El objetivo principal fue transformar ejercicios aislados en un producto organizado mediante una arquitectura de cuatro capas:

`routers → services → repositories → models`

Además, integré:

- FastAPI
- Pydantic
- SQLAlchemy 2.x
- patrón repositorio
- inyección de dependencias
- validaciones de dominio
- manejo de errores
- pruebas unitarias
- pruebas de integración
- documentación OpenAPI

## Forma en que utilicé la IA

Utilicé la IA como herramienta de análisis, contraste y revisión técnica. No consideré sus respuestas como decisiones finales. Antes de incorporar una propuesta:

1. comparé la sugerencia con los requisitos de la actividad
2. revisé si respetaba la arquitectura existente
3. evalué sus efectos sobre pruebas, tipado y el mantenimiento de la estructura
4. ejecuté Ruff, mypy y pytest
5. acepté, modifiqué o rechacé la propuesta

---

# Decisiones técnicas asistidas por IA

## Decisión 1 — Organización de la arquitectura
Al iniciar SensorHub necesitaba decidir cómo distribuir responsabilidades sin colocar toda la lógica dentro de los endpoints
Mi primera propuesta fue separar los archivos por tipo de recurso:

- sensores
- lecturas
- base de datos
- pruebas

Esta organización era sencilla, pero no definía con precisión dónde debían vivir las reglas de negocio y el acceso a datos

### Propuesta de la IA
La IA propuso utilizar cuatro capas:

- routers para recibir y responder peticiones HTTP
- services para las reglas de negocio
- repositories para la persistencia
- models para las entidades SQLAlchemy

También propuso separar los esquemas Pydantic de los modelos ORM

### Resolución 
Consideré una alternativa más simple en la que los routers llamaran directamente a SQLAlchemy
La descarté porque habría mezclado:

- validación HTTP
- reglas de negocio
- consultas a la base
- manejo de transacciones

La arquitectura por capas implicó crear más archivos, pero permitió que cada parte tuviera una responsabilidad concreta
Adopté la arquitectura de cuatro capas porque coincidía con la actividad y permitía probar los servicios sin depender de FastAPI ni de la base real

La estructura final quedó organizada en:

```text
app/
├── routers/
├── services/
├── repositories/
├── models/
├── schemas/
├── domain/
├── dependencies.py
├── db.py
└── main.py
```

## Decisión 2 — Uso de Protocol para los repositorios
Inicialmente podía hacer que SensorService dependiera directamente de SQLAlchemySensorRepository. Esto funcionaba, pero acoplaba la lógica de negocio a una implementación concreta.

Mi primera opción fue recibir directamente una sesión de SQLAlchemy dentro del servicio y ejecutar ahí las consultas, la ventaja era reducir archivos y llamadas intermedias pero la desventaja era que el servicio conocería detalles de persistencia y sería más difícil probarlo de forma aislada

### Propuesta de la IA

La IA propuso definir contratos mediante typing.Protocol. El servicio dependería de operaciones abstractas como:

create
get
list
update
delete
Debate y comparación

### Resolución
Elegí Protocol porque aplica inversión de dependencias sin agregar una jerarquía de herencia innecesaria
La decisión no se tomó solo porque la IA la sugirió. Se mantuvo porque permitió sustituir el repositorio SQLAlchemy por un fake en las pruebas unitarias sin modificar SensorService


## Decisión 3 — Repositorio fake frente a SQLite en pruebas unitarias
Necesitaba probar las reglas del servicio sin que cada prueba dependiera de una base de datos
Consideré usar SQLite en memoria para todas las pruebas esto habría permitido probar con una tecnología cercana a la implementación final

### Propuesta de la IA
La IA propuso diferenciar:

- pruebas unitarias con repositorios fake
- pruebas de integración con SQLite en memoria

SQLite en memoria seguía involucrando:

- motor SQL
- sesiones
- tablas
- transacciones
- mapeos ORM

Eso hacía que una prueba del servicio también pudiera fallar por problemas de infraestructura, el fake, en cambio, permitía aislar solamente las reglas de negocio

### Resolución
Utilicé ambos enfoques con propósitos distintos:

* fake para pruebas unitarias
* SQLite en memoria para pruebas de integración

Pude comprobar el comportamiento de los servicios de manera rápida y, por separado, verificar el recorrido completo desde FastAPI hasta SQLAlchemy


## Decisión 4 — Separación entre validación estructural y validación de dominio
Debía decidir si todas las validaciones se realizarían en los esquemas Pydantic o si algunas pertenecerían a los servicios
Mi primera idea fue validar tipos, unidades y valores físicos directamente en los esquemas, esto parecía conveniente porque Pydantic podía rechazar la petición antes de entrar al servicio

### Propuesta de la IA
La IA propuso dividir las responsabilidades:Pydantic valida estructura y tipos del cuerpo y el servicio valida reglas que dependen del dominio o de información persistida.
Una lectura contiene un valor, pero su rango válido depende del tipo de sensor almacenado en la base. Por ejemplo, el mismo número puede ser válido para temperatura y no para humedad
El esquema ReadingCreate no conoce por sí solo el tipo del sensor asociado

### Resoclución
Mantuve en Pydantic las validaciones estructurales y coloqué en los servicios las validaciones que requieren consultar el sensor
Defiendo esta decisión porque evita que los esquemas dependan de la base de datos y mantiene una separación clara entre validación de entrada y reglas de negocio


## Decisión 5 — Catálogo centralizado de reglas físicas
Las validaciones de tipo, unidad y rango comenzaban a repetirse entre creación y actualización por lo que consideré colocar condicionales dentro de cada método del servicio:

if sensor_type == "temperature":
    ...
elif sensor_type == "humidity":
    ...

### Propuesta de la IA
La IA sugirió centralizar las reglas en app/domain/sensor_rules.py
Los condicionales eran fáciles de implementar al principio, pero generaban riesgo de inconsistencias entre:

- creación de sensores
- actualización de sensores
- creación de lecturas
- actualización de lecturas

Un catálogo centralizado permite consultar la misma regla desde distintas operaciones

### Resolución
Creé una fuente única de reglas físicas

- Rangos adoptados
- Tipo	Unidad	Rango
* temperatura	°C	-273.15 a 1000
* humedad	%	0 a 100
* presion	kPa	0 a 10000

Los límites superiores de temperatura y presión no pretenden representar todos los sensores reales existentes. Los adopté como límites operativos del alcance actual de SensorHub
La decisión puede modificarse posteriormente sin alterar los servicios porque las reglas están centralizadas


## Decisión 6 — Rechazo explícito de null en PATCH
Los esquemas de actualización tenían campos opcionales para permitir modificaciones parciales, sin embargo, un campo opcional podía significar dos cosas:

- el cliente no envió el campo
- el cliente envió explícitamente null

Inicialmente consideré permitir null y dejar que SQLAlchemy o la base de datos rechazaran el valor

### Propuesta de la IA
La IA propuso distinguir entre campo omitido y campo nulo mediante validadores de Pydantic

### Resolución
Delegar el error a la base habría producido una respuesta menos clara y habría permitido que una petición inválida avanzara demasiado en el sistema
También podía dejar una sesión en estado fallido si no se manejaba correctamente la excepción, por eso permití omitir campos en PATCH, pero rechacé valores nulos explícitos cuando la propiedad no admite NULL

La decisión mejora el contrato de la API porque el cliente recibe un error 422 antes de iniciar una operación de persistencia


## Decisión 7 — Excepciones de dominio frente a HTTPException en servicios
Los servicios necesitaban informar situaciones como:

- sensor inexistente
- código duplicado
- lectura inexistente
- unidad incompatible
- rango temporal inválido

Consideré lanzar HTTPException directamente desde los servicio, esto era sencillo porque FastAPI podía convertirla inmediatamente en una respuesta HTTP

### Propuesta de la IA
La IA propuso crear excepciones de dominio y transformarlas en respuestas HTTP en la capa de FastAPI

### Resolución
Usar HTTPException dentro de los servicios habría hecho que la lógica de negocio dependiera del framework esto complicaría reutilizar los servicios desde:

- una tarea de consola
- un proceso en segundo plano
- otra interfaz distinta de HTTP

Los servicios lanzan excepciones propias y app/main.py las convierte a respuestas HTTP
Aunque requiere más clases y manejadores, mantiene los servicios independientes de FastAPI, considero que esta separación es más coherente con la arquitectura solicitada


## Decisión 8 — Manejo de la relación Sensor y Reading
Durante la implementación apareció un error de SQLAlchemy relacionado con Sensor.readings, al inspeccionar las tablas solo aparecía sensors
Mi primera hipótesis fue que la relación back_populates estaba mal escrita

### Propuesta de la IA
La IA planteó otras posibles causas:

- el modelo Reading no se había importado antes de ejecutar create_all
- la metadata no conocía todas las tablas
- la relación bidireccional no estaba registrada completamente
- Verificación realizada

### Resolución
Revisé:

- imports de modelos
- contenido de Base.metadata
- nombres de back_populates
- tablas creadas por el motor

Mantuve la relación bidireccional y corregí el registro de los modelos antes de crear las tablas
No debía asumir que el error estaba únicamente en la línea mencionada por SQLAlchemy, el problema real estaba relacionado con el momento en que se cargaban los modelos


## Decisión 9 — Base de pruebas aislada
Las pruebas de integración no debían modificar sensorhub.db, consideré crear un archivo SQLite temporal para la suite de pruebas

### Propuesta de la IA
La IA sugirió usar:

- SQLite en memoria
- StaticPool
- una fábrica de sesiones exclusiva
- dependency_overrides
- creación y eliminación de tablas por prueba

### Resolución
Un archivo temporal habría permitido inspeccionar la base después de una falla, pero también podía dejar residuos y provocar dependencia entre ejecuciones. SQLite en memoria era más limpio, pero requería StaticPool para compartir la misma conexión durante la prueba
Elegí SQLite en memoria con StaticPool. Las pruebas atraviesan:

router → dependency → service → repository → SQLAlchemy

sin modificar la base de desarrollo


## Decisión 10 — Uso de herramientas de calidad antes de cada cierre
Durante la semana aparecieron errores de:

- indentación
- imports
- métodos duplicados
- símbolos no definidos
- tipado incompleto
- espacios finales

Mantuve que un cambio no estaba terminado únicamente porque la API iniciara,a ntes de cerrar cada etapa debía comprobar:

- python -m ruff check app tests
- python -m mypy app tests
- python -m pytest
- git diff --check

La IA ayudó a interpretar algunos errores, pero yo ejecuté las verificaciones y confirmé cada corrección al final obtuve:

- Ruff: aprobado
- mypy: aprobado
- pytest: 24 pruebas aprobadas
- cobertura: 92.29 %
- git diff --check: sin errores
- Propuestas de la IA que modifiqué o no acepté directamente


## Sugerencias ramdom que no acepté de la IA
* No acepté realizar cambios que alteraran commits de actividades ya cerradas. Las correcciones se incorporaron en commits posteriores para mantener la trazabilidad
* Modifiqué la propuesta inicial de usar Pydantic para todas las reglas
* Las validaciones que requieren conocer datos persistidos permanecieron en los servicios
* No utilizar únicamente SQLite para todas las pruebas
* No adopté una sola estrategia de pruebas. Separé pruebas unitarias con fake y pruebas de integración con SQLite
* No considerar los rangos físicos como universales: Los rangos definidos se documentaron como reglas operativas del producto y no como límites aplicables a cualquier sensor industrial

## Retrospectiva

### Salió bien
* La separación en capas permitió avanzar de forma incremental sin concentrar toda la lógica en los endpoints
* Las pruebas con repositorios fake facilitaron detectar errores en los servicios antes de integrar SQLAlchemy
* La validación continua con Ruff, mypy y pytest evitó acumular problemas hasta el final
* La documentación automática de FastAPI ayudó a comprobar rutas, esquemas y códigos HTTP

### Salió mal
* En algunos momentos modifiqué archivos completos antes de revisar cuidadosamente el bloque existente
Esto provocó:

- métodos duplicados
- desaparición temporal de métodos
- errores de indentación
- pérdida de tiempo en correcciones evitables

* También avancé en algunos pasos sin verificar inmediatamente:
* La documentación de decisiones se dejó para el final, lo que obligó a reconstruir parte del proceso a partir del historial

## Qué cambiaré la próxima semana
1. Revisar el archivo antes de modificarlo

- Antes de reemplazar un archivo completo ejecutaré una revisión de su contenido y de sus referencias
- Cuando el cambio sea pequeño, modificaré únicamente el bloque necesario

2. Ejecutar pruebas después de cada cambio funcional

- No esperaré hasta completar varios endpoints
- Después de cada modificación relevante ejecutaré al menos:

* python -m ruff check app tests
* python -m mypy app tests
* python -m pytest -q

Trato de hacerlo asi, pero ahora mas seguido.

3. Registrar decisiones durante el desarrollo

- Actualizaré la bitácora al finalizar cada día en lugar de reconstruirla al cierre de la semana

4. Revisar Git antes de cada commit

Antes de cerrar un día ejecutaré:

- git status
- git diff --check
- git diff --stat

Esto permitirá detectar archivos accidentales o cambios ajenos a la actividad

5. Diseñar primero los casos de error

Antes de implementar un endpoint identificaré:

- caso exitoso
- recurso inexistente
- conflicto
- entrada inválida
- restricción de negocio

Con esto podré diseñar simultáneamente el servicio, las excepciones y las pruebas


## Resultado de la Semana 3

SensorHub quedó implementado con:

- arquitectura en cuatro capas
- CRUD de sensores
- CRUD de lecturas
- paginación
- filtros temporales
- validación de tipos y unidades
- rangos físicos
- excepciones de dominio
- inyección de dependencias
- persistencia con SQLAlchemy 2.x
- pruebas unitarias
- pruebas de integración
- documentación Swagger
- cobertura de 92.29 %

El Pull Request permanece abierto en espera de la revisión por pares