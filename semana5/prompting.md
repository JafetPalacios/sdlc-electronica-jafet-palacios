# Semana 5 — Prompting efectivo

## Objetivo

Analizar cómo la calidad y precisión de un prompt afectan el código generado por una herramienta de inteligencia artificial mediante tres tareas reales del proyecto SensorHub. Para cada tarea se comparará un prompt pobre contra un prompt estructurado utilizando:

- Contexto
- Tarea
- Restricciones
- Entrega

Los resultados se conservarán para analizar diferencias, errores, supuestos realizados por la IA y utilidad práctica de cada enfoque.

---

## Tarea 1

### Objetivo de la tarea

Crear una función pura para convertir temperaturas de grados Celsius a grados Fahrenheit, pensada como una utilidad reutilizable para las lecturas de temperatura procesadas por SensorHub. La tarea permitirá comparar cuánto debe asumir la IA cuando recibe una instrucción ambigua frente a un prompt que especifica el contexto técnico, la interfaz esperada y las restricciones de implementación.

### Prompt pobre

Haz una función para convertir Celsius a Fahrenheit

### Resultado del prompt pobre

### Resultado del prompt pobre

```python
def celsius_a_fahrenheit(celsius: float) -> float:
    """Convierte grados Celsius a Fahrenheit."""
    return (celsius * 9 / 5) + 32


# Ejemplo de uso:
temp_c = 25.0
temp_f = celsius_a_fahrenheit(temp_c)
print(f"{temp_c}°C equivalen a {temp_f}°F")  # Resultado: 77.0°F
```

### Análisis del resultado

La respuesta implementa correctamente la fórmula matemática de conversión de Celsius a Fahrenheit y, aunque el prompt no lo solicitó, incorpora type hints y un docstring. Esto muestra que un prompt poco específico puede producir un resultado aparentemente adecuado cuando la tarea es sencilla.
Sin embargo, la IA tuvo que asumir varios aspectos que no estaban definidos. Eligió por iniciativa propia el nombre `celsius_a_fahrenheit`, utilizó nombres de variables en español y añadió un ejemplo ejecutable con `print`, aunque únicamente se había solicitado una función.
El resultado tampoco establece un redondeo a dos decimales ni permite determinar si la implementación está pensada para Python 3.12.
La función generada sí es pura porque su resultado depende únicamente del argumento recibido y no modifica estado externo. Sin embargo, la respuesta completa incluye código de demostración con efectos secundarios mediante `print`, algo innecesario si el objetivo era recibir exclusivamente la función.
El resultado evidencia que, ante requisitos incompletos, la IA rellena los espacios faltantes con decisiones plausibles. Algunas coincidieron con lo que podría necesitar el proyecto, como los type hints, pero esto ocurrió por inferencia del modelo y no porque el prompt garantizara esos requisitos.

### Prompt bueno

CONTEXTO:
API SensorHub desarrollada con FastAPI y Python 3.12 para la gestión de sensores y sus lecturas. El proyecto utiliza type hints completos y mantiene utilidades pequeñas con responsabilidades específicas

TAREA:
Escribe una función pura llamada celsius_to_fahrenheit(c: float) -> float para convertir una temperatura expresada en grados Celsius a grados Fahrenheit. La función se incorporará en semana5/conversions.py.

RESTRICCIONES:
- Usa Python 3.12
- Mantén exactamente la firma celsius_to_fahrenheit(c: float) -> float
- Incluye type hints completos
- Incluye un docstring en español que describa la responsabilidad de la función
- No utilices dependencias externas
- Redondea el resultado a 2 decimales
- No agregues ejemplos de uso, pruebas, clases ni código adicional
- No modifiques la interfaz solicitada

ENTREGA:
Devuelve únicamente la función solicitada, sin explicación adicional.

### Resultado del prompt bueno

```
def celsius_to_fahrenheit(c: float) -> float:
    """Convierte una temperatura de grados Celsius a grados Fahrenheit"""
    return round((c * 9 / 5) + 32, 2)
```
### Análisis del resultado

La respuesta cumple de forma directa con los requisitos definidos en el prompt. Utiliza exactamente la firma `celsius_to_fahrenheit(c: float) -> float`, mantiene type hints completos, incorpora un docstring en español y realiza el redondeo a dos decimales mediante `round`.
También respeta las restricciones negativas establecidas: no introduce dependencias externas, ejemplos de uso, pruebas, clases ni explicaciones adicionales. La salida contiene únicamente la función solicitada.
A diferencia del prompt pobre, la IA ya no tuvo que decidir por cuenta propia aspectos importantes de la interfaz o del formato de entrega. El nombre de la función, el parámetro, el tipo de retorno, el redondeo y el alcance de la respuesta fueron establecidos explícitamente antes de generar el código.
La implementación sigue siendo pequeña y pura, ya que depende únicamente del valor recibido y no produce efectos secundarios ni modifica estado externo.

### Comparación y conclusión

Ambos prompts produjeron una conversión matemáticamente correcta, pero la diferencia principal está en el control sobre las decisiones tomadas por la IA.
Con el prompt pobre, la IA tuvo que inferir la interfaz y el formato de entrega. Eligió el nombre `celsius_a_fahrenheit`, decidió utilizar type hints y un docstring sin que se le solicitaran y añadió código de ejemplo con una llamada a `print`. Además, no implementó el requisito de redondear el resultado a dos decimales.
Con el prompt bueno, las decisiones relevantes quedaron definidas explícitamente mediante contexto, tarea, restricciones y formato de entrega. Como resultado, la función respetó exactamente la firma requerida, incorporó el redondeo solicitado y no añadió elementos fuera del alcance.
El experimento muestra que un prompt pobre puede producir código funcional, especialmente cuando la tarea es sencilla, pero no garantiza que el resultado respete las necesidades reales del proyecto. Un prompt bien estructurado reduce las suposiciones del modelo y hace que el resultado sea más predecible, verificable y fácil de integrar.

---

## Tarea 2

### Objetivo de la tarea

Refactorizar `SensorService` para reducir la duplicación existente al recuperar un sensor por identificador y comprobar que exista.
Actualmente `get_sensor`, `update_sensor` y `delete_sensor` realizan de forma independiente la consulta `get_by_id` y lanzan `SensorNotFoundError` cuando el sensor no existe. La tarea permitirá comparar una solicitud genérica de refactorización frente a otra que delimite exactamente qué duplicación debe eliminarse y qué comportamiento debe permanecer intacto.

### Prompt pobre

Refactoriza este servicio para eliminar código repetido y mejorarlo (pegué el contenido completo de `app/services/sensor_service.py`)

### Resultado del prompt pobre

Para refactorizar el servicio de forma limpia, aplicamos los siguientes principios de diseño de software:

1. Método `helper _get_sensor_or_raise`: Extrae la búsqueda repetida por ID (`get_sensor`, `update_sensor`, `delete_sensor`) y el lanzamiento de `SensorNotFoundError`.

2. Método `helper _ensure_code_is_unique`: Centraliza la validación de duplicidad de código (`create_sensor` y `update_sensor`).

3. Construcción dinámica de la entidad: Simplifica la instanciación de Sensor a partir del esquema `Pydantic` en `create_sensor`.

4. Limpieza de comentarios y formato: Elimina el formateo con tabuladores excesivos hacia la derecha y reemplaza los comentarios ruidosos con docstrings claros por método.

Código Refactorizado
```Python
from app.domain.sensor_rules import SENSOR_RULES
from app.exceptions import (
    InvalidSensorUnitError,
    SensorCodeConflictError,
    SensorHasReadingsError,
    SensorNotFoundError,
    UnsupportedSensorTypeError,
)
from app.models import Sensor
from app.repositories.sensor_repository import SensorRepository
from app.schemas import SensorCreate, SensorUpdate


class SensorService:
    """Servicio de aplicación para coordinar las reglas de negocio e iteraciones con el repositorio de sensores."""

    def __init__(self, repository: SensorRepository) -> None:
        self._repository = repository

    # --- Helpers privados (DRY) ---

    def _get_sensor_or_raise(self, sensor_id: int) -> Sensor:
        """Obtiene un sensor por su ID o lanza SensorNotFoundError si no existe."""
        sensor = self._repository.get_by_id(sensor_id)
        if sensor is None:
            raise SensorNotFoundError(sensor_id)
        return sensor

    def _ensure_code_is_unique(self, code: str) -> None:
        """Verifica que el código no esté en uso por otro sensor."""
        if self._repository.get_by_code(code) is not None:
            raise SensorCodeConflictError(code)

    def _validate_sensor_rule(self, sensor_type: str, unit: str) -> None:
        """Valida que el tipo de sensor exista en el catálogo y la unidad sea compatible."""
        rule = SENSOR_RULES.get(sensor_type)
        if rule is None:
            raise UnsupportedSensorTypeError(sensor_type)

        if unit != rule.unit:
            raise InvalidSensorUnitError(
                sensor_type=sensor_type,
                received_unit=unit,
                expected_unit=rule.unit,
            )

    # --- Métodos públicos del servicio ---

    def create_sensor(self, sensor_data: SensorCreate) -> Sensor:
        """Crea un nuevo sensor asegurando reglas físicas y unicidad de código."""
        self._validate_sensor_rule(
            sensor_type=sensor_data.sensor_type,
            unit=sensor_data.unit,
        )
        self._ensure_code_is_unique(sensor_data.code)

        sensor = Sensor(**sensor_data.model_dump())
        return self._repository.create(sensor)

    def list_sensors(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Sensor]:
        """Obtiene una lista paginada de sensores."""
        return self._repository.list(limit=limit, offset=offset)

    def get_sensor(self, sensor_id: int) -> Sensor:
        """Recupera un sensor por su identificador único."""
        return self._get_sensor_or_raise(sensor_id)

    def update_sensor(
        self,
        sensor_id: int,
        sensor_data: SensorUpdate,
    ) -> Sensor:
        """Actualiza parcialmente un sensor aplicando validaciones de tipo, unidad y código."""
        sensor = self._get_sensor_or_raise(sensor_id)
        update_data = sensor_data.model_dump(exclude_unset=True)

        # Validar la combinación final de tipo de sensor y unidad
        final_sensor_type = update_data.get("sensor_type", sensor.sensor_type)
        final_unit = update_data.get("unit", sensor.unit)
        self._validate_sensor_rule(
            sensor_type=final_sensor_type,
            unit=final_unit,
        )

        # Validar cambio de código si fue provisto y es distinto al actual
        new_code = update_data.get("code")
        if new_code is not None and new_code != sensor.code:
            self._ensure_code_is_unique(new_code)

        # Actualizar dinámicamente los campos modificados
        for field_name, field_value in update_data.items():
            setattr(sensor, field_name, field_value)

        return self._repository.update(sensor)

    def delete_sensor(self, sensor_id: int) -> None:
        """Elimina un sensor si existe y no cuenta con lecturas registradas."""
        sensor = self._get_sensor_or_raise(sensor_id)

        if sensor.readings:
            raise SensorHasReadingsError(sensor_id)

        self._repository.delete(sensor)
```

Principales mejoras logradas
* Eliminación de duplicación: Las 3 llamadas a `get_by_id` con su verificación de `None` se redujeron a una única función reutilizable `(_get_sensor_or_raise)`.

* Cohesión de código: La verificación de unicidad de código ahora es responsabilidad de `_ensure_code_is_unique`.

* Legibilidad e mantenibilidad: Los comentarios inline muy lejanos hacia la derecha impedían una lectura cómoda; se reemplazaron por docstrings semánticos estándar en Python.

### Análisis del resultado

La respuesta identificó correctamente una duplicación real en `SensorService`: `get_sensor`, `update_sensor` y `delete_sensor` recuperaban el sensor mediante `get_by_id` y repetían la comprobación que lanza `SensorNotFoundError`. Para resolverla, la IA propuso `_get_sensor_or_raise`, una extracción coherente con el problema observado.
Sin embargo, debido a que el prompt únicamente solicitó refactorizar el servicio para eliminar código repetido y mejorarlo, la IA amplió el alcance por iniciativa propia. Además de extraer `_get_sensor_or_raise`, creó `_ensure_code_is_unique`, modificó la construcción explícita de `Sensor` por `Sensor(**sensor_data.model_dump())` y reemplazó gran parte de los comentarios existentes por docstrings.
Algunas de estas modificaciones pueden ser razonables, pero no eran necesarias para resolver la duplicación que motivó la tarea. En particular, cambiar la construcción explícita de la entidad por un desempaquetado completo del esquema introduce una decisión adicional sobre el acoplamiento entre `SensorCreate` y `Sensor`. Esta modificación requeriría comprobar que ambos mantienen exactamente los mismos campos y que ningún cambio futuro del esquema pudiera introducir datos que el modelo ORM no deba recibir.
La extracción de `_ensure_code_is_unique` también reduce repetición entre creación y actualización, aunque modifica una segunda responsabilidad que el prompt no había identificado explícitamente. Antes de aceptarla sería necesario verificar que conserva exactamente la semántica de ambos flujos.
La respuesta también realizó cambios de estilo y documentación sin conocer las convenciones específicas del proyecto. Los docstrings y comentarios generados no respetan necesariamente el formato utilizado actualmente en SensorHub, lo que demuestra que una instrucción genérica como "mejorarlo" permite que la IA interprete libremente qué aspectos debe modificar.
El resultado evidencia que un prompt de refactorización poco delimitado puede producir código aparentemente más limpio, pero también aumentar innecesariamente el alcance del cambio. En una base de código real esto incrementa la superficie de revisión y el riesgo de introducir modificaciones de comportamiento no relacionadas con el objetivo original.

### Prompt bueno

CONTEXTO:
SensorHub es una API desarrollada con FastAPI y Python 3.12. La lógica de negocio de sensores está concentrada en `SensorService`, que recibe mediante inyección un `SensorRepository`. El servicio utiliza excepciones de dominio y forma parte de una arquitectura en capas, por lo que esta refactorización no debe modificar su interfaz pública ni trasladar responsabilidades a otras capas.

TAREA:
Refactoriza `SensorService` para eliminar únicamente la duplicación existente en `get_sensor`, `update_sensor` y `delete_sensor` al recuperar un sensor mediante `self._repository.get_by_id(sensor_id)` y lanzar `SensorNotFoundError` cuando no existe.
Extrae esa lógica a un método privado llamado `_get_sensor_or_raise(self, sensor_id: int) -> Sensor` y reutilízalo exclusivamente donde corresponda.

RESTRICCIONES:
- Usa Python 3.12
- Mantén exactamente las firmas de todos los métodos públicos
- No cambies el comportamiento observable del servicio
- No modifiques `_validate_sensor_rule`
- No refactorices la validación de unicidad de código
- No cambies la construcción explícita de `Sensor` en `create_sensor`
- No agregues dependencias
- No modifiques los modelos, esquemas, repositorios ni excepciones
- Conserva los comentarios existentes salvo los estrictamente necesarios para integrar el nuevo método
- Los comentarios nuevos deben estar en español y explicar únicamente decisiones o bloques relevantes
- No realices otras mejoras, limpiezas de estilo ni refactorizaciones fuera del alcance solicitado

ENTREGA:
Devuelve únicamente el contenido completo refactorizado de `app/services/sensor_service.py`, sin explicación adicional.

### Resultado del prompt bueno

```python
from app.domain.sensor_rules import SENSOR_RULES
from app.exceptions import (
    InvalidSensorUnitError,
    SensorCodeConflictError,
    SensorHasReadingsError,
    SensorNotFoundError,
    UnsupportedSensorTypeError,
)
from app.models import Sensor
from app.repositories.sensor_repository import SensorRepository
from app.schemas import SensorCreate, SensorUpdate


# Servicio de aplicación para sensores
# Concentramos aquí las reglas de negocio relacionadas con los sensores
# Coordinamos el repositorio sin depender directamente de FastAPI o SQLAlchemy
# Esto permite reutilizar y probar la lógica de negocio de forma independiente
class SensorService:
    # Inicialización del servicio
    def __init__(self, repository: SensorRepository) -> None:                                           # Recibimos el repositorio mediante el constructor

        self._repository = repository                                                                   # Conservamos el contrato del repositorio sin conocer cómo persiste los datos


    # Recuperación de sensores
    def _get_sensor_or_raise(self, sensor_id: int) -> Sensor:                                           # Centralizamos la consulta por identificador y la validación de existencia

        sensor = self._repository.get_by_id(sensor_id)

        if sensor is None:
            raise SensorNotFoundError(sensor_id)

        return sensor


    # Validación de reglas físicas
    def _validate_sensor_rule(                                                                          # Comprobamos que el tipo de sensor exista dentro del catálogo y que la unidad enviada corresponda con la unidad definida
        self,
        sensor_type: str,
        unit: str,
    ) -> None:

        rule = SENSOR_RULES.get(sensor_type)                                                            # Buscamos la configuración asociada al tipo recibido

        if rule is None:                                                                                # Rechazamos tipos que no forman parte del catálogo
            raise UnsupportedSensorTypeError(sensor_type)

        if unit != rule.unit:                                                                           # Rechazamos unidades incompatibles con el tipo seleccionado
            raise InvalidSensorUnitError(
                sensor_type=sensor_type,
                received_unit=unit,
                expected_unit=rule.unit,
            )


    # Creación de sensores
    def create_sensor(self, sensor_data: SensorCreate) -> Sensor:                                       # Registramos sensores nuevos únicamente cuando su código público está disponible

        self._validate_sensor_rule(                                                                     # Validamos que el tipo y la unidad pertenezcan al catálogo físico
            sensor_type=sensor_data.sensor_type,
            unit=sensor_data.unit,
        )

        existing_sensor = self._repository.get_by_code(                                                 # Consultamos si ya existe un sensor con el código recibido
            sensor_data.code,
        )

        if existing_sensor is not None:                                                                 # Interrumpimos la operación cuando el código ya está registrado
            raise SensorCodeConflictError(sensor_data.code)

        sensor = Sensor(                                                                                # Construimos la entidad ORM con los datos validados por Pydantic
            code=sensor_data.code,
            name=sensor_data.name,
            sensor_type=sensor_data.sensor_type,
            unit=sensor_data.unit,
        )

        return self._repository.create(sensor)                                                          # Delegamos la inserción y recuperación del estado final al repositorio

    # Consulta paginada
    def list_sensors(                                                                                   # Recuperamos una colección limitada de sensores
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Sensor]:

        return self._repository.list(                                                                   # Enviamos al repositorio el límite y el desplazamiento solicitados
            limit=limit,
            offset=offset,
        )

    # Consulta individual
    def get_sensor(self, sensor_id: int) -> Sensor:                                                     # Recuperamos un sensor concreto mediante su identificador interno
                                                                                                        # Transformamos la ausencia del registro en una excepción de dominio

        return self._get_sensor_or_raise(sensor_id)

    # Actualización de sensores
    def update_sensor(                                                                                  # Modificamos únicamente los campos enviados explícitamente por el cliente
        self,                                                                                           # Conservamos sin cambios cualquier campo omitido en la petición PATCH
        sensor_id: int,
        sensor_data: SensorUpdate,
    ) -> Sensor:

        sensor = self._get_sensor_or_raise(sensor_id)

        update_data = sensor_data.model_dump(                                                           # Extraemos únicamente los campos incluidos en la petición
            exclude_unset=True,                                                                         # exclude_unset evita sobrescribir valores que el cliente no envió
        )

        # Construimos la combinación final que tendría el sensor
        final_sensor_type = update_data.get(                                                            # Usamos los valores actuales cuando el cliente no envía un cambio
            "sensor_type",
            sensor.sensor_type,
        )
        final_unit = update_data.get(
            "unit",
            sensor.unit,
        )

        # Validamos la combinación final antes de modificar la entidad
        self._validate_sensor_rule(
            sensor_type=final_sensor_type,
            unit=final_unit,
        )

        new_code = update_data.get("code")                                                              # Obtenemos el nuevo código cuando forma parte de la actualización

        if new_code is not None and new_code != sensor.code:                                            # Validamos la unicidad únicamente cuando el código realmente cambia
            existing_sensor = self._repository.get_by_code(new_code)

            if existing_sensor is not None:                                                             # Impedimos asignar un código que ya pertenece a otro sensor
                raise SensorCodeConflictError(new_code)

        for field_name, field_value in update_data.items():                                             # Aplicamos dinámicamente cada modificación permitida por el esquema
            setattr(
                sensor,
                field_name,
                field_value,
            )

        return self._repository.update(sensor)                                                          # Delegamos la confirmación de cambios y la recarga al repositorio

    # Eliminación de sensores
    def delete_sensor(self, sensor_id: int) -> None:                                                    # Eliminamos un sensor únicamente cuando existe y no conserva lecturas
                                                                                                        # Protegemos así la integridad de los datos históricos asociados
        sensor = self._get_sensor_or_raise(sensor_id)

        if sensor.readings:                                                                             # Comprobamos si existen lecturas relacionadas con el sensor
            raise SensorHasReadingsError(sensor_id)

        self._repository.delete(sensor)                                                                 # Delegamos la eliminación definitiva y el commit al repositorio
```

### Análisis del resultado

La respuesta se mantuvo dentro del alcance definido por el prompt. La IA creó únicamente el método privado `_get_sensor_or_raise(self, sensor_id: int) -> Sensor` para centralizar la consulta mediante `get_by_id` y el lanzamiento de `SensorNotFoundError` cuando el sensor no existe.
Después reutilizó ese método exclusivamente en `get_sensor`, `update_sensor` y `delete_sensor`, que eran los tres puntos identificados previamente como duplicados.
A diferencia del resultado obtenido con el prompt pobre, no creó un helper adicional para validar la unicidad del código, no modificó `_validate_sensor_rule` y conservó la construcción explícita de la entidad `Sensor` en `create_sensor`. También mantuvo las firmas de los métodos públicos y no introdujo nuevas dependencias ni cambios en otras capas.
La modificación propuesta es pequeña y localizada. Por inspección del código, el comportamiento esperado de las operaciones se conserva: los mismos tres métodos siguen recuperando un sensor por identificador y siguen produciendo `SensorNotFoundError` cuando este no existe, pero ahora la lógica común está concentrada en un único método privado.
La respuesta también respetó la restricción de no realizar una limpieza general del servicio. Los comentarios existentes se conservaron en gran medida y únicamente se añadió documentación relacionada con el nuevo helper.
Aunque la propuesta parece conservar el comportamiento, no puede considerarse validada únicamente mediante inspección. Si se decidiera integrar esta refactorización en el proyecto, sería necesario ejecutar las pruebas existentes, Ruff y mypy para comprobar que el cambio no introdujo regresiones.

### Comparación y conclusión

Los dos resultados detectaron correctamente la duplicación relacionada con la recuperación de sensores y propusieron `_get_sensor_or_raise` como solución. La diferencia principal estuvo en el alcance de los cambios realizados por cada IA.
El prompt pobre utilizó expresiones abiertas como "eliminar código repetido y mejorarlo". Como consecuencia, la IA interpretó libremente qué significaba mejorar el servicio y realizó modificaciones adicionales: creó `_ensure_code_is_unique`, cambió la construcción explícita de `Sensor` por `Sensor(**sensor_data.model_dump())` y sustituyó parte de la documentación existente.
Estas propuestas no son necesariamente incorrectas, pero amplían la superficie del cambio y obligan a revisar decisiones que no formaban parte del problema original.
El prompt bueno identificó exactamente la duplicación que debía eliminarse y estableció límites explícitos sobre las partes que no debían modificarse. El resultado se concentró en introducir `_get_sensor_or_raise` y reutilizarlo en los tres métodos correspondientes, conservando el resto de la implementación.
La comparación muestra que las restricciones negativas son especialmente importantes al solicitar refactorizaciones. No basta con indicar qué debe cambiar; especificar qué debe permanecer intacto ayuda a producir cambios pequeños, revisables y con menor riesgo de introducir modificaciones no relacionadas.
En esta tarea también se utilizaron modelos de IA diferentes, por lo que las diferencias observadas pueden estar influenciadas tanto por la estructura de los prompts como por las características de cada modelo. La comparación se interpreta teniendo presente esta limitación.

---

## Tarea 3

### Objetivo de la tarea

Explicar el flujo completo de creación de una lectura en SensorHub, desde la recepción de `POST /sensors/{sensor_id}/readings` en el router hasta la persistencia y construcción de la respuesta.La tarea permitirá comparar una solicitud de explicación genérica frente a un prompt que especifique qué responsabilidades, validaciones y colaboraciones entre capas deben identificarse sin inventar comportamiento que no esté presente en el código.

### Prompt pobre

Explícame cómo funciona la creación de una lectura en este código (le dí el contenido completo de `app/routers/readings.py` y `app/services/reading_service.py`)

### Resultado del prompt pobre

El proceso de creación de una lectura se divide en dos capas principales: la capa de transporte (`Router de FastAPI`) y la capa de aplicación/negocio (`ReadingService`).El flujo paso a paso funciona de la siguiente manera:

1. Entrada de la Petición y Validación (`Capa de Router`)El proceso comienza en la función de ruta `@router.post("/sensors/{sensor_id}/readings")`:

1. Recepción de Parámetros:
* `sensor_id`: Extraído directamente de la URL. FastAPI valida que sea un entero (`int`).
* `reading_data`: Objeto Pydantic (`ReadingCreate`) recibido en el cuerpo JSON del HTTP request. FastAPI valida automáticamente los tipos y el formato del payload. Si la estructura es inválida, se detiene la ejecución devolviendo un código `422 Unprocessable Content`.

2. Inyección de Dependencias:
* FastAPI inyecta la instancia de `ReadingService` a través de `ReadingServiceDependency` (`get_reading_service`).

3. Delegación: El router llama al método
* `service.create_reading`(`sensor_id, reading_data`).

2. Lógica de Negocio y Reglas Físicas (Capa de Servicio)
Dentro del método `ReadingService.create_reading`:

1. Verificación de Existencia del Sensor Propietario:
```Python
sensor = self._sensor_repository.get_by_id(sensor_id)
if sensor is None:
    raise SensorNotFoundError(sensor_id)
```
Consulte al repositorio de sensores si el `sensor_id` existe. Si no se encuentra, se detiene lanzando `SensorNotFoundError`, lo que FastAPI traduce a una respuesta con status `404 Not Found`.

2. Validación del Valor de la Lectura (`_validate_reading_value`):
```Python
self._validate_reading_value(
    sensor_type=sensor.sensor_type,
    value=reading_data.value,
)
```
* Obtiene las reglas físicas asociadas al tipo de sensor (`SENSOR_RULES.get(sensor_type)`).
* Verifica si el valor enviado (`reading_data.value`) se encuentra dentro de los límites permitidos (`rule.minimum_value` y `rule.maximum_value`).
* Si está fuera de rango, lanza `ReadingValueOutOfRangeError`.

3. Construcción e Inserción de la Entidad:
```Python
reading = Reading(
    sensor_id=sensor_id,
    value=reading_data.value,
)
return self._reading_repository.create(reading)
```
Crea la entidad ORM `Reading` asociándole el `sensor_id` y el valor. La fecha/timestamp se omite explícitamente en el constructor para que la base de datos la autogenere al insertar. Finalmente, el repositorio inserta el registro y retorna la entidad persistida.

3. Formateo y Respuesta

1. Retorno al Router: El servicio entrega el objeto ORM `Reading` resultante al controlador.

2. Serialización a DTO:
```Python
return ReadingResponse.model_validate(reading)
```
`ReadingResponse.model_validate` toma la entidad ORM y la convierte al esquema DTO público.

3. Respuesta HTTP: FastAPI serializa la respuesta en formato JSON, devolviendo un código de estado `201 Created`.

¿Te gustaría profundizar en algún aspecto específico del flujo?

### Análisis del resultado

La respuesta reconstruyó correctamente el flujo principal de creación de una lectura y distinguió las responsabilidades generales del router y de `ReadingService`. Identificó la recepción de `sensor_id` y `ReadingCreate`, la inyección de `ReadingService`, la delegación hacia `create_reading`, la comprobación de existencia del sensor, la validación física del valor, la construcción de `Reading`, la persistencia mediante el repositorio y la conversión final a `ReadingResponse`.
También reconoció correctamente que la validación del valor de la lectura pertenece al servicio y utiliza las reglas definidas en `SENSOR_RULES`. Esto permite distinguir la validación estructural de los datos recibidos de las reglas de negocio relacionadas con el tipo de sensor y sus límites físicos.
Sin embargo, la explicación contiene afirmaciones que no pueden demostrarse únicamente con `app/routers/readings.py` y `app/services/reading_service.py`. La más importante es afirmar que `SensorNotFoundError` es traducida por FastAPI a una respuesta `404 Not Found`. El router documenta una posible respuesta 404, pero en los archivos proporcionados no aparece el manejador de excepciones responsable de realizar esa traducción, por lo que la IA está infiriendo una parte de la infraestructura que no puede observar directamente.
Algo similar ocurre cuando se afirma que la base de datos autogenera el timestamp. El comentario existente en `ReadingService` indica que ese es el comportamiento esperado, pero los archivos proporcionados no incluyen el modelo `Reading`, la configuración de la columna ni la implementación del repositorio. Por lo tanto, puede describirse como una intención documentada en el código, pero no comprobarse completamente a partir de estos dos archivos.
La respuesta también utiliza el término DTO para describir `ReadingResponse`, aunque el proyecto proporcionado únicamente permite comprobar que se trata de un esquema utilizado como contrato público de respuesta. El término no afecta al flujo explicado, pero es una interpretación adicional introducida por la IA.
El resultado muestra que un prompt genérico puede producir una explicación clara y técnicamente plausible, pero no obliga al modelo a distinguir entre comportamiento directamente observable, comportamiento documentado mediante comentarios e inferencias sobre componentes que no recibió. En documentación técnica, esta diferencia es importante porque una explicación convincente puede presentar como hechos detalles que todavía requieren verificación.

### Prompt bueno

CONTEXTO:
SensorHub es una API desarrollada con FastAPI y Python 3.12 utilizando una arquitectura en capas. Se proporcionan únicamente `app/routers/readings.py` y `app/services/reading_service.py`. No debes asumir cómo están implementados los repositorios, modelos, dependencias o manejadores globales de excepciones que no aparecen en estos archivos.

TAREA:
Explica paso a paso el flujo de creación de una lectura cuando se recibe `POST /sensors/{sensor_id}/readings`, desde la entrada al router hasta la construcción de la respuesta.
La explicación debe identificar claramente qué responsabilidad corresponde al router, cuál corresponde a `ReadingService` y cuáles operaciones son delegadas a repositorios.

RESTRICCIONES:
- Basa la explicación únicamente en el código proporcionado
- Distingue la validación realizada por FastAPI/Pydantic de las reglas de negocio ejecutadas por `ReadingService`
- Explica la comprobación de existencia del sensor
- Explica la validación del valor mediante `_validate_reading_value`
- Explica la construcción de la entidad `Reading`
- Explica la llamada a `ReadingRepository.create`
- Explica la conversión final mediante `ReadingResponse.model_validate`
- Identifica las excepciones de dominio que pueden originarse durante el flujo
- No afirmes cómo se transforman las excepciones de dominio en respuestas HTTP si esa implementación no aparece en el código proporcionado
- No inventes detalles de SQLAlchemy, commits, transacciones o implementación interna de los repositorios
- Si un comportamiento solo aparece indicado mediante un comentario, señálalo como comportamiento documentado pero no verificado con los archivos disponibles
- No propongas refactorizaciones ni modificaciones al código

ENTREGA:
Devuelve una explicación técnica estructurada y concisa del flujo. Separa claramente:
1. Entrada y validación HTTP
2. Lógica de aplicación y reglas de negocio
3. Persistencia delegada
4. Construcción de la respuesta
5. Aspectos que no pueden confirmarse con los archivos proporcionados

### Resultado del prompt bueno

1. Entrada y validación HTTP

El flujo comienza en:

`POST /sensors/{sensor_id}/readings`

FastAPI dirige la petición a `create_reading`:

```python
def create_reading(
    sensor_id: int,
    reading_data: ReadingCreate,
    service: ReadingServiceDependency,
) -> ReadingResponse:
```
Antes de ejecutar la lógica del endpoint, FastAPI/Pydantic se encargan de construir y validar los argumentos declarados:

* `sensor_id` debe poder interpretarse como `int`
* el cuerpo de la petición debe poder convertirse a `ReadingCreate`
* `service` se obtiene mediante la dependencia `Depends(get_reading_service)`

La implementación de `get_reading_service` no fue proporcionada, por lo que solo puede confirmarse que el router solicita un `ReadingService` mediante esa dependencia. No puede determinarse cómo se construyen sus repositorios o demás dependencias.

Superada esta validación de entrada, el router delega la operación al servicio:

```python
reading = service.create_reading(
    sensor_id,
    reading_data,
)
```
En este punto termina la responsabilidad principal del router respecto a la creación: recibe datos ya interpretados según sus tipos y delega las reglas de negocio a `ReadingService`.

2. Lógica de aplicación y reglas de negocio

`ReadingService.create_reading` recibe:

```python
sensor_id: int
reading_data: ReadingCreate
```
Comprobación de existencia del sensor

La primera operación es:

```python
sensor = self._sensor_repository.get_by_id(sensor_id)
```

Por tanto, `ReadingService` delega al `SensorRepository` la búsqueda del sensor propietario.

Después comprueba explícitamente el resultado:

```python
if sensor is None:
    raise SensorNotFoundError(sensor_id)
```

Si el repositorio indica que el sensor no existe, el flujo se detiene mediante la excepción de dominio `SensorNotFoundError`.

No puede afirmarse cómo dicha excepción se convierte posteriormente en una respuesta HTTP porque los manejadores globales de excepciones no fueron proporcionados.

Validación del valor de la lectura

Si el sensor existe, el servicio ejecuta:

```python
self._validate_reading_value(
    sensor_type=sensor.sensor_type,
    value=reading_data.value,
)
```

Esta es una regla de negocio, distinta de la validación estructural realizada previamente por FastAPI/Pydantic.

`_validate_reading_value` consulta:

```python
rule = SENSOR_RULES.get(sensor_type)
```

Si encuentra una regla, comprueba que el valor esté dentro del intervalo:

```python
if value < rule.minimum_value or value > rule.maximum_value:
    raise ReadingValueOutOfRangeError(...)
```

Por tanto, un valor fuera del rango permitido origina la excepción de dominio `ReadingValueOutOfRangeError`.

Si no existe una regla para `sensor_type`, el método hace:

```python
if rule is None:
    return
```

El comentario indica que el tipo habría sido validado previamente durante la creación del sensor y que este caso protege frente a datos antiguos. Esa intención está documentada mediante comentarios, pero no puede verificarse con los dos archivos proporcionados.

Construcción de `Reading`

Una vez validado el valor, el servicio construye:

```python
reading = Reading(
    sensor_id=sensor_id,
    value=reading_data.value,
)
```

En consecuencia, el servicio es responsable de construir la entidad que se entregará a persistencia utilizando:

* el identificador del sensor recibido en la ruta
* el valor validado procedente de `ReadingCreate`

El comentario afirma que el timestamp será generado por la base de datos al persistir la lectura. Ese comportamiento no puede verificarse porque no se proporcionaron ni el modelo `Reading` ni la configuración de persistencia.

3. Persistencia delegada

Después de construir `Reading`, `ReadingService` ejecuta:

```python
return self._reading_repository.create(reading)
```

La responsabilidad está separada de esta forma:

* `ReadingService` decide qué lectura puede crearse
* `ReadingRepository` recibe la entidad para realizar la operación de creación correspondiente

Con los archivos disponibles solo puede confirmarse que se llama a:

```python
ReadingRepository.create(reading)
```
y que su resultado se devuelve desde `create_reading`.

No puede determinarse:

* cómo se almacena físicamente la lectura
* si utiliza SQLAlchemy
* si realiza `commit`
* si utiliza `flush` o `refresh`
* qué transacciones intervienen
* cómo obtiene un identificador
* si realmente recarga la entidad después de persistirla

El comentario del servicio dice que el repositorio delega la "inserción y recuperación del estado final", pero esa implementación no está disponible para verificarla.

4. Construcción de la respuesta

El objeto devuelto por `ReadingService.create_reading` regresa al router:

```python
reading = service.create_reading(...)
```

El router lo convierte explícitamente al esquema público:

```python
return ReadingResponse.model_validate(reading)
```

Por tanto, la respuesta expuesta por el endpoint no se construye devolviendo directamente `Reading`, sino mediante `ReadingResponse`.

El flujo final es:

Reading
   |
   v
ReadingResponse.model_validate(reading)
   |
   v
ReadingResponse
   |
   v
respuesta del endpoint

Además, el endpoint declara:

```python
response_model=ReadingResponse
status_code=status.HTTP_201_CREATED
```

Por lo que la operación exitosa está configurada con código HTTP `201 Created` y un contrato de respuesta `ReadingResponse`.

Durante este flujo de negocio pueden originarse explícitamente estas excepciones de dominio:

* `SensorNotFoundError`, si el sensor indicado no existe
* `ReadingValueOutOfRangeError`, si el valor no pertenece al rango permitido para el tipo de sensor

La transformación concreta de estas excepciones en códigos o cuerpos HTTP no está presente en los archivos proporcionados.

5. Aspectos que no pueden confirmarse con los archivos proporcionados

No es posible determinar a partir de `readings.py` y `reading_service.py`:

* cómo `get_reading_service` construye `ReadingService`
* qué implementación concreta utilizan `SensorRepository` y `ReadingRepository`
* cómo se implementa `SensorRepository.get_by_id`
* cómo se implementa `ReadingRepository.create`
* si existe SQLAlchemy detrás de los repositorios
* cómo se manejan commits, transacciones, sesiones o recargas
* cómo se genera realmente el timestamp de `Reading`
* cómo se asigna el identificador de una lectura
* cómo `ReadingResponse` está configurado internamente para validar el objeto recibido
* cómo `SensorNotFoundError` y `ReadingValueOutOfRangeError` se transforman en respuestas HTTP

En síntesis, el flujo verificable es:

POST /sensors/{sensor_id}/readings
        |
        v
FastAPI/Pydantic
valida y construye los parámetros
        |
        v
Router create_reading
        |
        v
ReadingService.create_reading
        |
        +--> SensorRepository.get_by_id(sensor_id)
        |        |
        |        +--> None -> SensorNotFoundError
        |
        +--> _validate_reading_value(...)
        |        |
        |        +--> fuera de rango -> ReadingValueOutOfRangeError
        |
        +--> Reading(sensor_id=..., value=...)
        |
        +--> ReadingRepository.create(reading)
        |
        v
Router
ReadingResponse.model_validate(reading)
        |
        v
201 Created

### Análisis del resultado

La respuesta siguió el alcance definido por el prompt y estructuró la explicación según las responsabilidades del router, el servicio y los repositorios.
En la entrada HTTP distinguió correctamente la interpretación de `sensor_id`, la construcción de `ReadingCreate` y la resolución de `ReadingServiceDependency`. También señaló explícitamente que la implementación de `get_reading_service` no estaba disponible, evitando asumir cómo se construyen realmente los repositorios y demás dependencias.
En la capa de aplicación identificó correctamente dos reglas diferentes. Primero, `SensorRepository.get_by_id` se utiliza para comprobar que exista el sensor propietario y puede originarse `SensorNotFoundError`. Después, `_validate_reading_value` aplica una regla de negocio basada en `SENSOR_RULES` y puede producir `ReadingValueOutOfRangeError` cuando el valor queda fuera de los límites permitidos.
La explicación también diferenció correctamente la construcción de `Reading` de su persistencia. `ReadingService` crea la entidad con los datos ya validados y delega posteriormente la operación a `ReadingRepository.create`. La IA evitó afirmar cómo funciona internamente esa persistencia y enumeró explícitamente aspectos que no pueden confirmarse, como el uso de SQLAlchemy, commits, sesiones, `flush`, `refresh` o transacciones.
Respecto al timestamp, la respuesta indicó que su generación por parte de la base de datos aparece documentada mediante un comentario del servicio, pero reconoció que no puede verificarse sin consultar el modelo y la configuración de persistencia.
Finalmente, identificó correctamente que el router transforma el objeto recibido del servicio mediante `ReadingResponse.model_validate` y que el endpoint declara `ReadingResponse` como contrato público junto con el estado HTTP `201 Created`.
A diferencia del resultado del prompt pobre, la respuesta no presentó como hechos confirmados comportamientos pertenecientes a componentes que no habían sido proporcionados. Esto demuestra que establecer explícitamente los límites de evidencia ayuda a obtener explicaciones técnicas más precisas y auditables.

### Comparación y conclusión

Ambos resultados reconstruyeron correctamente el flujo general de creación de una lectura y reconocieron las principales responsabilidades del router y de `ReadingService`.
El prompt pobre produjo una explicación clara y técnicamente plausible, pero permitió que la IA completara algunos detalles mediante inferencias. Por ejemplo, afirmó directamente que `SensorNotFoundError` se traduce a una respuesta HTTP `404 Not Found`, aunque los archivos proporcionados no incluían el manejador encargado de realizar esa conversión. También describió como comportamiento efectivo la generación del timestamp por parte de la base de datos, cuando en los archivos disponibles ese detalle únicamente aparecía documentado mediante un comentario.
El prompt estructurado estableció explícitamente que la explicación debía basarse únicamente en los archivos proporcionados y que debía distinguir entre comportamiento observable, comportamiento documentado e información no verificable. Como resultado, la IA mantuvo la explicación dentro de esa frontera y señaló qué aspectos requerirían consultar otros componentes del proyecto.
También separó con mayor precisión la validación estructural realizada por FastAPI/Pydantic de las reglas de negocio aplicadas por `ReadingService`, y evitó inventar detalles internos de los repositorios, las transacciones o el manejo global de excepciones.
La comparación muestra que un buen prompt para explicar código no solo debe indicar qué partes describir. También debe establecer qué evidencia puede utilizar la IA y exigir que identifique aquello que no puede confirmar. Esto reduce el riesgo de obtener documentación técnicamente convincente pero parcialmente basada en suposiciones.
Al igual que en las tareas anteriores, las respuestas fueron generadas mediante modelos de IA diferentes. Por esta razón, las diferencias observadas pueden estar influenciadas tanto por la estructura del prompt como por las características particulares de cada modelo.