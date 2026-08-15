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
