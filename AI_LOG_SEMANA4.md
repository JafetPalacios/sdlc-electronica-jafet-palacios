# Bitácora de IA - Semana 4

## Contexto

La Semana 4 se enfoca en DevOps, contenerización y CI/CD. El objetivo es llevar SensorHub desde una ejecución local verificada hasta una aplicación contenerizada, integrada con PostgreSQL, validada mediante CI y desplegada con CD
La estrategia de trabajo que se pide en la actividad será incremental: no se avanza al siguiente peldaño hasta verificar que el anterior funciona correctamente.

---

## Intervención 1 - Validación del entorno y funcionamiento local

Se busca comprobar que el proyecto SensorHub se encuentra estable localmente antes de comenzar con Docker. Se verificó que el repositorio se encontraba en la rama:

`feature/semana3-sensorhub`

La rama se encontraba sincronizada con su correspondiente rama remota

## Validación de calidad local

Se ejecutaron las siguientes comprobaciones:

* python -m ruff check app tests
* python -m mypy app tests
* python -m pytest --cov=app --cov-report=term-missing

# Resultados:

* Ruff sin errores
* mypy sin errores en 33 archivos fuente
* 24 pruebas ejecutadas correctamente
* cobertura total de 92.29 %
* cobertura mínima requerida: 80 %

## Validación de ejecución local

Se levantó la API con Uvicorn y se verificaron manualmente los endpoints principales

* GET /health

# Resultado:

* HTTP 200
* servicio: SensorHub API
* versión: 0.1.0
* estado: ok


## Conclusión

La primera fase de la Semana 4 queda validada

SensorHub funciona correctamente en local, pasa lint, tipado y pruebas, supera la cobertura mínima exigida y expone correctamente los endpoints /health y /docs


---


## Intervención 2 - Preparación y validación de SensorHub en Docker

Decidí trabajar la Semana 4 en una rama independiente para mantener separados los cambios respecto a la Semana 3 y conservar una trazabilidad más clara en Git. Creé la rama:

`feature/semana4-devops`

También decidí excluir el directorio `getting-started-todo-app/` del seguimiento de Git porque corresponde únicamente a una práctica del tutorial oficial de Docker y no forma parte de SensorHub

### Apoyo solicitado a la IA

Consulté a la IA cómo preparar correctamente el proyecto para contenerizar SensorHub sin incluir archivos locales o innecesarios dentro del contexto de construcción

También solicité apoyo para definir un Dockerfile compatible con la configuración actual del proyecto y con los requisitos de la Semana 4

### Propuestas de la IA

La IA me recomendó:

- crear un archivo `.dockerignore`
- excluir del contexto de construcción el entorno virtual, cachés de herramientas, archivos de cobertura, bases SQLite locales y archivos del editor
- copiar primero `requirements.txt` para aprovechar la caché de capas de Docker
- instalar las dependencias antes de copiar el código fuente
- copiar únicamente el directorio `app/` dentro de la imagen en lugar de copiar todo el repositorio
- exponer el puerto 8000
- ejecutar Uvicorn escuchando en `0.0.0.0` para permitir conexiones desde fuera del contenedor
- mantener SQLite durante esta primera validación y dejar la migración a PostgreSQL para el siguiente peldaño con Docker Compose

### Decisión final

Decidí seguir una estrategia incremental

Primero validaría que SensorHub funcionara correctamente dentro de Docker usando la configuración actual con SQLite

Después de comprobar este punto, continuaría con Docker Compose y PostgreSQL

### Implementación

Creé el archivo `.dockerignore` para excluir elementos que no deben formar parte del contexto de construcción, entre ellos:

- `venv/`
- `.venv/`
- `.git/`
- `.pytest_cache/`
- `.mypy_cache/`
- `.ruff_cache/`
- `__pycache__/`
- archivos de cobertura
- bases SQLite locales
- archivos del editor
- `getting-started-todo-app/`

Posteriormente creé el `Dockerfile` utilizando `python:3.12-slim` como imagen base

La estructura del Dockerfile quedó orientada a aprovechar la caché de capas, copiando primero `requirements.txt`, instalando las dependencias y copiando posteriormente el código de `app/`

Ejecuté:

```powershell
docker build -t sensorhub:dev .

