# Bitácora de uso de IA — Semana 2

## Entrada 1: Diseño inmutable de SensorReading

### Contexto

La Evaluación 1 requería representar lecturas ambientales con identificador del sensor, temperatura, humedad y fecha de captura

### Consulta realizada

Solicité cómo desarrollar `SensorReading` aplicando TDD estricto y garantizando que cada lectura permaneciera inmutable después de su creación.

### Recomendación de la IA

La IA propuso:

- Utilizar una `dataclass`
- Aplicar `frozen=True` para hacerla inmutable
- Crear primero una prueba para verificar los datos almacenados
- Crear después una prueba que esperara `FrozenInstanceError`
- Separar los commits Red y Green

### Mi decisión

Decidí utilizar `dataclass(frozen=True)` porque una lectura representa una medición ocurrida en un instante específico y no debería cambiar posteriormente

También decidí conservar dos ciclos TDD separados:

1. Creación básica de la lectura
2. Protección contra modificaciones

### Alternativa descartada

Descarté utilizar una clase mutable con métodos para modificar sus atributos porque podría generar inconsistencias durante el análisis de anomalías

### Resultado

El componente quedó validado con dos pruebas aprobadas y cobertura del 100 %


## Entrada 2: Inyección de umbrales en AnomalyDetector

### Contexto

El sistema debía detectar temperaturas superiores a 35 °C y humedades superiores al 80 %

### Consulta realizada

Solicité los pasos fundamentales para llevar a cabo la implementación de `AnomalyDetector` mediante TDD y permitir que los umbrales fueran configurados desde el exterior

### Recomendación de la IA

La IA propuso:

- Crear una enumeración `AnomalyType`
- Representar cada anomalía con una `dataclass(frozen=True)`
- Inyectar los umbrales mediante el constructor
- Devolver las anomalías mediante una tupla
- Desarrollar temperatura y humedad en ciclos TDD independientes

### Mi decisión

Decidí recibir los umbrales mediante el constructor para evitar valores fijos dentro del método `detect`

También decidí implementar la detección de temperatura y humedad por separado para conservar evidencia clara de cada ciclo Red y Green

### Alternativa descartada

Descarté escribir directamente los valores 35 y 80 dentro del detector porque dificultaría cambiar la configuración y probar otros límites

### Resultado

El componente quedó validado con dos pruebas aprobadas y cobertura del 100 %


## Entrada 3: Aplicación del patrón Strategy en AlertManager

### Contexto

La evaluación requería administrar alertas mediante una estrategia abstracta y contar con salidas en consola y archivo

### Consulta realizada

Solicité orientación para implementar `AlertManager`, `ConsoleAlertStrategy` y `FileAlertStrategy` mediante TDD y con responsabilidades separadas

### Recomendación de la IA

La IA propuso:

- Crear una clase abstracta `AlertStrategy`
- Inyectar la estrategia en `AlertManager`
- Crear una estrategia de consola
- Crear una estrategia de archivo
- Abrir el archivo en modo append
- Crear una estrategia auxiliar para verificar la delegación
- Desarrollar cada comportamiento en un ciclo TDD independiente

### Mi decisión

Decidí aplicar el patrón Strategy porque permite cambiar el mecanismo de alerta sin modificar `AlertManager`

También decidí que el administrador únicamente delegara el envío y que cada estrategia controlara su propio mecanismo de salida

### Alternativa descartada

Descarté utilizar condiciones dentro de `AlertManager` para seleccionar entre consola y archivo porque aumentaría el acoplamiento y obligaría a modificar la clase al agregar nuevas estrategias

### Resultado

El componente quedó validado con tres pruebas aprobadas y cobertura del 100 %


## Entrada 4: Conservación de la trazabilidad TDD en Git

### Contexto

Era necesario demostrar que cada prueba fallida fue creada antes de su correspondiente implementación

### Consulta realizada

Solicité orientación para organizar ramas, commits y Pull Requests sin perder la secuencia Red y Green

### Recomendación de la IA

La IA recomendó:

- Crear una rama por componente o cambio documental
- Registrar primero el commit Red
- Registrar después el commit Green
- Utilizar `Create a merge commit`
- Evitar `Squash and merge`
- Ejecutar pytest, mypy y Ruff antes de cada integración
- Eliminar las ramas después de fusionarlas

### Mi decisión

Decidí conservar cada commit de prueba e implementación por separado para demostrar la aplicación real de TDD

También decidí integrar primero cada componente en `feature/evaluacion-1-sprint-1` antes de fusionar la evaluación completa en `main`

### Alternativa descartada

Descarté utilizar squash porque habría combinado los commits Red y Green y se perdería evidencia del orden de desarrollo

### Resultado

El historial conserva ciclos TDD separados para:

- `SensorReading`
- `AnomalyDetector`
- `AlertManager`

La validación global terminó con 11 pruebas aprobadas, cobertura de 97.67 %, mypy sin errores y Ruff sin errores