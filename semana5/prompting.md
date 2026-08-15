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

Refactoriza este servicio para eliminar código repetido y mejorarlo (pegué el contenido completo de app/services/sensor_service.py)

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

Pendiente de definir

### Prompt pobre

Pendiente

### Resultado del prompt pobre

Pendiente

### Análisis del resultado

Pendiente

### Prompt bueno

CONTEXTO:
Pendiente

TAREA:
Pendiente

RESTRICCIONES:
Pendiente

ENTREGA:
Pendiente

### Resultado del prompt bueno

Pendiente

### Análisis del resultado

Pendiente

### Comparación y conclusión

Pendiente
