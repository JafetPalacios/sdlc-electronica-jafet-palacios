# Bitácora de IA - Semana 4

## Contexto

La Semana 4 se enfoca en DevOps, contenerización y CI/CD. El objetivo es llevar SensorHub desde una ejecución local verificada hasta una aplicación contenerizada, integrada con PostgreSQL, validada mediante CI y desplegada con CD
La estrategia de trabajo que se pide en la actividad será incremental: no se avanza al siguiente peldaño hasta verificar que el anterior funciona correctamente.

---

## Intervención 1 - Validación del entorno y funcionamiento local

Se busca comprobar que el proyecto SensorHub se encuentra estable localmente antes de comenzar con Docker. Se verificó que el repositorio se encontraba en la rama:

`feature/semana3-sensorhub`

La rama se encontraba sincronizada con su correspondiente rama remota

### Validación de calidad local

Se ejecutaron las siguientes comprobaciones:

* python -m ruff check app tests
* python -m mypy app tests
* python -m pytest --cov=app --cov-report=term-missing

### Resultados:

* Ruff sin errores
* mypy sin errores en 33 archivos fuente
* 24 pruebas ejecutadas correctamente
* cobertura total de 92.29 %
* cobertura mínima requerida: 80 %

### Validación de ejecución local

Se levantó la API con Uvicorn y se verificaron manualmente los endpoints principales

* GET /health

### Resultado:

* HTTP 200
* servicio: SensorHub API
* versión: 0.1.0
* estado: ok


### Conclusión

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

### La IA me ayudó a:

- excluir del contexto de construcción el entorno virtual, cachés de herramientas, archivos de cobertura, bases SQLite locales y archivos del editor
- copiar primero `requirements.txt` para aprovechar la caché de capas de Docker
- instalar las dependencias antes de copiar el código fuente
- copiar únicamente el directorio `app/` dentro de la imagen en lugar de copiar todo el repositorio
- exponer el puerto 8000
- ejecutar Uvicorn escuchando en `0.0.0.0` para permitir conexiones desde fuera del contenedor
- mantener SQLite durante esta primera validación y dejar la migración a PostgreSQL para el siguiente peldaño con Docker Compose


Decidí seguir una estrategia incremental. Primero validaría que SensorHub funcionara correctamente dentro de Docker usando la configuración actual con SQLite. Después de comprobar este punto, continuaría con Docker Compose y PostgreSQL

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

`powershell
docker build -t sensorhub:dev .`

---

## Intervención 3 - Integración de SensorHub con PostgreSQL mediante Docker Compose

Decidí mantener el avance de forma incremental y no crear directamente toda la infraestructura de Compose sin comprobar antes cada dependencia

También decidí separar las credenciales locales del repositorio mediante un archivo `.env` ignorado por Git y mantener una plantilla `.env.example` versionable

### Apoyo solicitado a la IA

Consulté a la IA cómo adaptar SensorHub para dejar de depender exclusivamente de SQLite y permitir el uso de PostgreSQL mediante variables de entorno. También solicité apoyo para preparar Docker Compose y para verificar que la API estuviera realmente conectándose a PostgreSQL, no únicamente arrancando correctamente

### La IA me ayudó a:

- instalar `psycopg[binary]` como driver de PostgreSQL
- modificar `app/db.py` para obtener `DATABASE_URL` desde una variable de entorno
- mantener SQLite como fallback cuando `DATABASE_URL` no está definida
- normalizar URLs `postgres://` y `postgresql://` hacia `postgresql+psycopg://`
- aplicar `check_same_thread=False` únicamente cuando se utiliza SQLite
- crear un archivo `.env` local excluido de Git
- crear `.env.example` sin secretos reales como referencia de configuración
- utilizar el nombre del servicio `db` como host de PostgreSQL dentro de Docker Compose
- validar la conexión desde el propio contenedor de la API mediante SQLAlchemy y una consulta `SELECT 1`
- comprobar directamente en PostgreSQL la existencia de las tablas `sensors` y `readings`

### Implementación

Instalé el driver PostgreSQL:

`powershell
python -m pip install "psycopg[binary]"`

Antes de introducir Docker Compose ejecuté:

* python -m ruff check app tests
* python -m mypy app tests
* python -m pytest

### Resultados:

* Ruff sin errores
* mypy sin errores
* 24 pruebas superadas
* cobertura total de 91.68 %

Esto permitió confirmar que la nueva configuración de base de datos no rompió el funcionamiento local con SQLite

Validación de normalización de DATABASE_URL

### Probé los formatos:

* postgres://sensor:secret@db:5432/sensorhub
* postgresql://sensor:secret@db:5432/sensorhub

En ambos casos la aplicación los normalizó correctamente a:

postgresql+psycopg://sensor:secret@db:5432/sensorhub

### Configuración segura

Agregué .env a .gitignore para evitar incluir credenciales locales en el historial

También creé .env.example como plantilla versionable sin utilizar la contraseña real del entorno local

Verifiqué que Git ignorara correctamente .env mediante:

git check-ignore -v .env

### Docker Compose

Creé docker-compose.yml con dos servicios:

* api
* db

El servicio api se construye utilizando el Dockerfile del proyecto y recibe DATABASE_URL mediante variables de entorno

El servicio db utiliza la imagen postgres:16 y persiste sus datos mediante un volumen administrado por Docker

Dentro de la URL de conexión utilicé db como host porque Docker Compose resuelve los servicios por nombre dentro de su red interna

Antes de iniciar los servicios validé la configuración con:

`docker compose config`

La configuración fue interpretada correctamente

### Ejecución

Levanté la infraestructura mediante:

`docker compose up --build`

Docker creó correctamente:

* la imagen de la API
* la imagen de PostgreSQL
* la red interna de Compose
* el volumen persistente
* el contenedor de la API
* el contenedor de PostgreSQL

PostgreSQL terminó su inicialización mostrando:

`database system is ready to accept connections`

La API inició correctamente con Uvicorn

### Validación de la conexión real con PostgreSQL

Verifiqué el estado de los servicios mediante:

`docker compose ps`

Ambos contenedores permanecieron activos

Después ejecuté desde el propio contenedor de la API una conexión utilizando el engine de SQLAlchemy:

`docker compose exec api python -c "from sqlalchemy import text; from app.db import engine; connection = engine.connect(); print('DATABASE_URL:', engine.url.render_as_string(hide_password=True)); print('SELECT 1:', connection.execute(text('SELECT 1')).scalar()); connection.close()"`

Resultado:

`DATABASE_URL: postgresql+psycopg://sensor:***@db:5432/sensorhub`
`SELECT 1: 1`

Esto confirmó que SensorHub estaba conectado realmente a PostgreSQL mediante SQLAlchemy y psycopg

### Validación del esquema

Consulté directamente PostgreSQL con:

`docker compose exec db psql -U sensor -d sensorhub -c "\dt"`

Se encontraron las tablas:

`readings`
`sensors`

### Validación de la API

Finalmente verifiqué:

`Invoke-WebRequest http://127.0.0.1:8000/health -UseBasicParsing`
`Invoke-WebRequest http://127.0.0.1:8000/docs -UseBasicParsing`

### Resultados:

`/health respondió HTTP 200`
`/docs respondió HTTP 200`

### Conclusión

La IA me ayudó a definir una transición controlada desde SQLite hacia PostgreSQL, manteniendo compatibilidad local. También me ayudó a comprobar la conexión real entre la API y PostgreSQL mediante una consulta ejecutada desde SQLAlchemy, evitando asumir que el simple arranque de los contenedores era suficiente evidencia. Con estas verificaciones confirmé que SensorHub funciona correctamente con Docker Compose y PostgreSQL.

---

## Intervención 4 - Inicialización y validación de migraciones con Alembic

Antes de comenzar con GitHub Actions revisé nuevamente la guía de la Semana 4 y detecté que faltaba realizar el cierre correspondiente a Alembic

Decidí detener el avance hacia CI y completar primero este requisito para respetar la estrategia de trabajo incremental definida para la semana

También decidí no aplicar directamente una migración inicial sobre la base PostgreSQL que ya estaba en uso, porque las tablas `sensors` y `readings` ya existían y eso podía impedir validar correctamente la creación del esquema desde cero

### Apoyo solicitado a la IA

Consulté a la IA cómo incorporar Alembic al proyecto sin romper la configuración existente de SQLite y PostgreSQL

También solicité apoyo para configurar correctamente `migrations/env.py`, generar una migración inicial real y comprobar que dicha migración pudiera reconstruir una base PostgreSQL vacía

### La IA me recomendó:

- inicializar Alembic mediante `alembic init migrations`
- reutilizar la configuración centralizada de `DATABASE_URL` definida en `app/db.py`
- configurar `target_metadata` con `Base.metadata`
- importar los modelos ORM para que `sensors` y `readings` quedaran registrados en los metadatos
- eliminar `Base.metadata.create_all()` de `app/main.py` para evitar que FastAPI y Alembic compitieran por la administración del esquema
- generar la migración inicial utilizando temporalmente una base SQLite vacía para evitar que la autogeneración comparara contra una base que ya contenía las tablas
- revisar y limpiar el archivo generado por Alembic para mantener comentarios y documentación en español
- copiar `alembic.ini` y `migrations/` dentro de la imagen Docker para poder ejecutar migraciones desde el contenedor
- probar `alembic upgrade head` contra una instancia PostgreSQL temporal e independiente antes de aplicarlo en otros entornos

### Implementación

Inicialicé Alembic mediante:

`alembic init migrations`

configuré `migrations/env.py` para utilizar:

* DATABASE_URL
* Base.metadata
* los modelos Reading y Sensor

También eliminé de app/main.py la creación automática del esquema mediante:

 `Base.metadata.create_all(...)`

A partir de este cambio, la responsabilidad de administrar la estructura de la base de datos queda delegada a Alembic

Después de retirar `create_all()` ejecuté:

* python -m ruff check app tests migrations
* python -m mypy app tests migrations --ignore-missing-imports
* python -m pytest

### Resultados:

* Ruff sin errores
* mypy sin errores
* 24 pruebas superadas
* cobertura total de 91.63 %

Esto confirmó que separar la administración del esquema mediante Alembic no rompió el comportamiento existente de SensorHub

Para evitar generar una migración vacía contra una base que ya contenía las tablas, utilicé temporalmente:

`$env:DATABASE_URL="sqlite:///./alembic_temp.db"`

Luego ejecuté:

`alembic revision --autogenerate -m "esquema inicial: sensors y readings"`

Alembic detectó:

* sensors
* readings
* ix_sensors_code

y generó la revisión:

`eacacdab5dc6`

La migración fue revisada y ajustada únicamente en formato, comentarios y documentación, manteniendo la lógica generada por Alembic. Posteriormente eliminé la base temporal alembic_temp.db

### Incorporación de Alembic en la imagen Docker
Actualicé el Dockerfile para copiar:

* alembic.ini
* migrations/

dentro de la imagen

Después reconstruí la imagen y confirmé que los archivos de migración estuvieran disponibles dentro del contenedor. Para evitar modificar el volumen principal de desarrollo creé una instancia PostgreSQL temporal utilizando un nombre de proyecto Compose diferente:

`docker compose -p sensorhub-migration-test up -d db`

Verifiqué que PostgreSQL estuviera listo mediante:

`docker compose -p sensorhub-migration-test exec db pg_isready -U sensor -d sensorhub`

El servidor respondió que estaba aceptando conexiones. Posteriormente ejecuté desde el contenedor de la API:

`docker compose -p sensorhub-migration-test run --rm api alembic upgrade head`

Alembic ejecutó correctamente:

* Running upgrade -> eacacdab5dc6
* Validación del esquema creado

Consulté las tablas de PostgreSQL mediante:

`docker compose -p sensorhub-migration-test exec db psql -U sensor -d sensorhub -c "\dt"`

Se encontraron:

* alembic_version
* readings
* sensors


### Conclusión

La revisión de la guía me permitió detectar que todavía faltaba cerrar la integración de Alembic antes de comenzar CI

La IA me apoyó en la configuración de Alembic, la separación de responsabilidades respecto a create_all(), la generación controlada de la migración inicial y la estrategia para validarla en una base PostgreSQL completamente limpia

Con esta prueba confirmé que el esquema de SensorHub puede reconstruirse desde cero mediante migraciones versionadas y que la imagen Docker contiene todo lo necesario para ejecutar Alembic

El cierre de Docker Compose, PostgreSQL y migraciones quedó validado antes de continuar con GitHub Actions

---

## Intervención 5 - Preparación del pipeline de CI con GitHub Actions

Decidí mantener el mismo proceso incremental utilizado durante los pasos anteriores y no considerar terminado el pipeline únicamente por haber creado el archivo de configuración. Primero debía comprobar localmente que los mismos comandos que posteriormente ejecutaría GitHub Actions continuaran funcionando correctamente. También mantuve el requisito de que el pipeline utilizara Python 3.12, la misma versión configurada para el proyecto

### Apoyo solicitado a la IA

Solicité apoyo a la IA para preparar el pipeline de integración continua de SensorHub conforme a los requisitos de la Semana 4

El pipeline debía validar automáticamente:

- estilo y errores comunes mediante Ruff
- tipado estático mediante mypy
- pruebas automatizadas mediante pytest
- cobertura mínima del 80 %
- crear el workflow:

`.github/workflows/ci.yml`

### La IA me ayudó a:

- utilizar `actions/checkout@v4` para obtener el código del repositorio
- utilizar `actions/setup-python@v5` con Python 3.12
- instalar las dependencias exclusivamente desde `requirements.txt`
- ejecutar las herramientas mediante `python -m` para asegurar que utilizaran el mismo intérprete configurado en el runner
- ejecutar Ruff sobre `app`, `tests` y `migrations`
- ejecutar mypy sobre `app`, `tests` y `migrations`
- ejecutar pytest utilizando la configuración existente de `pyproject.toml`
- mantener el requisito de cobertura dentro de `pyproject.toml`, donde ya está configurado `--cov-fail-under=80`
- activar el workflow en pushes a `main` y en pull requests

La IA también indicó que un push directo a `feature/semana4-devops` no ejecutaría actualmente el evento `push`, ya que este está limitado a `main`

Por esta razón, una ejecución real podrá obtenerse mediante un pull request hacia `main` o posteriormente mediante un push a `main`

### Implementación

Creé la estructura:

.github/
└── workflows/
    └── ci.yml


El workflow quedó organizado en un job que utiliza un runner ubuntu-latest

Las etapas configuradas fueron:

Checkout
    |
    v
Python 3.12
    |
    v
Instalación de dependencias
    |
    v
Ruff
    |
    v
mypy
    |
    v
pytest


---

## Intervención 6 - Primera ejecución real del pipeline de CI

Decidí mantener la Semana 4 en su propia rama de trabajo `feature/semana4-devops` y no integrar todavía Semana 3 ni Semana 4 en `main`. Para poder validar CI directamente sobre la rama de entrega de la Semana 4, ajusté el workflow para que también se ejecutara cuando existieran pushes sobre `feature/semana4-devops`

### Apoyo solicitado a la IA

Consulté a la IA cómo validar GitHub Actions sin tener que mezclar todavía los cambios de Semana 3 y Semana 4 con la rama `main`. También solicité apoyo para interpretar el resultado mostrado por GitHub Actions después del primer push que disparó el workflow

La IA propuso modificar el trigger del workflow para mantener:

- ejecución sobre `main`
- ejecución sobre `feature/semana4-devops`
- ejecución sobre pull requests

La configuración quedó preparada para permitir validar CI directamente sobre la rama de trabajo de la Semana 4

### Implementación

Actualicé el workflow para utilizar:

yaml
on:
  push:
    branches:
      - main
      - feature/semana4-devops
  pull_request:


  Después realicé el commit:

`98dec01 ci: ejecutar pipeline en la rama de semana 4`

y lo envié al repositorio remoto mediante git push. El push sobre `feature/semana4-devops` disparó automáticamente la primera ejecución real del `workflow CI`

GitHub Actions mostró:

- Workflow: CI
- Ejecución: #1
- Evento: push
- Rama: feature/semana4-devops
- Commit: 98dec01
- Estado: Success
- Duración total: 36 s
- Job: test
- Duración del job: 32 s

La ejecución terminó correctamente en un runner de GitHub
GitHub mostró una anotación relacionada con Node.js indicando que algunas acciones utilizadas por el workflow apuntan a Node.js 20 y están siendo ejecutadas sobre Node.js 24
La advertencia no provocó ningún fallo y el estado final de la ejecución fue Success

Decidí mantenerla registrada como observación técnica, pero no bloquear el avance de la Semana 4 porque no afecta las validaciones requeridas del proyecto

### Resultado

Con esta ejecución confirmé que el pipeline funciona fuera de mi entorno local y puede ejecutar correctamente los controles automatizados desde GitHub Actions

---

## Intervención 7 - Preparación y validación del arranque de producción

Antes de configurar el despliegue público decidí validar localmente que SensorHub pudiera iniciar desde una base PostgreSQL completamente limpia sin depender de la creación automática de tablas desde FastAPI. También mantener las migraciones como parte obligatoria del proceso de arranque para que cualquier entorno nuevo pueda actualizar su esquema antes de levantar la API
Para evitar interferencias con otros servicios locales utilicé un proyecto temporal de Docker Compose y, durante la validación, cambié temporalmente el puerto publicado de la API de 8000 a 8001

### Apoyo solicitado a la IA

Solicité apoyo a la IA para preparar un flujo de arranque adecuado para producción y comprobar que PostgreSQL, Alembic y Uvicorn se iniciaran en el orden correcto. También consulté los errores encontrados cuando el puerto 8000 estaba ocupado y cuando el contenedor de la API no llegaba a iniciar

La IA me ayudó a:

- crear un script `start.sh`
- ejecutar `alembic upgrade head` antes de iniciar Uvicorn
- utilizar `set -e` para impedir que la aplicación continúe si falla una migración
- utilizar la variable `PORT` cuando sea proporcionada por la plataforma de despliegue
- mantener el puerto 8000 como valor local por defecto
- copiar `start.sh` dentro de la imagen Docker
- utilizar el script como comando de inicio del contenedor
- agregar un `healthcheck` al servicio PostgreSQL de Docker Compose
- configurar `depends_on` con `condition: service_healthy`
- validar todo el proceso utilizando una base PostgreSQL temporal y vacía

Actualicé el Dockerfile para copiar `start.sh` dentro de la imagen. También sustituí el comando directo de Uvicorn por `sh ./start.sh`. De esta forma el mismo contenedor administra primero las migraciones y después inicia la aplicación

Modifiqué `docker-compose.yml` para agregar un healthcheck basado en `pg_isready`. También cambié la dependencia de la API para utilizar:

depends_on:
  db:
    condition: service_healthy

Esto evita que Alembic intente conectarse antes de que PostgreSQL esté disponible

### Prueba de arranque

Definí temporalmente `$env:API_PORT="8001"` levanté el proyecto mediante `docker compose -p sensorhub-startup-test up --build`

Comprobé el estado de los servicios:

api -> Up
db -> Up (healthy)

Verifiqué el endpoint:

http://localhost:8001/health

### Resultado:

status: ok
service: SensorHub API
version: 0.1.0

También validé:

http://localhost:8001/docs con resultado HTTP 200


Consulté la tabla:

`alembic_version`

y confirmé la revisión:

`eacacdab5dc6`

También comprobé que PostgreSQL contuviera:

- alembic_version
- readings
- sensors

Después de finalizar las pruebas eliminé el entorno temporal utilizado para la validación y posteriormente confirmé que no quedaran:

* contenedores asociados a sensorhub-startup-test
* volúmenes asociados a sensorhub-startup-test

Con esta prueba confirmé que SensorHub puede iniciar desde una base PostgreSQL vacía siguiendo automáticamente el flujo:

PostgreSQL
    |
    v
healthcheck
    |
    v
Alembic
    |
    v
Uvicorn
    |
    v
SensorHub

El proyecto quedó preparado para que el siguiente paso sea configurar el despliegue público

---

## Intervención 8 - Validación de CI mediante un fallo intencional

Al revisar nuevamente la guía de la Semana 4 detecté que faltaba realizar el ejercicio del Día 3 en el que se solicita romper deliberadamente una prueba para observar cómo GitHub Actions bloquea el cambio. Decidí detener temporalmente el trabajo de despliegue y completar esta validación antes de continuar. Como ya tenía cambios pendientes relacionados con producción, decidí no mezclarlos con el experimento de CI

Guardé temporalmente los cambios de producción mediante:
`git stash push -u -m "Preparación de producción pendiente antes de prueba CI roja"` Esto permitió dejar el árbol de trabajo limpio y realizar la prueba de CI de forma aislada. Una vez realizada la prueba fallida realicé el commit:

`116e30c test: provocar fallo controlado para validar CI`

y lo envié al repositorio remoto. El push ejecutó automáticamente el workflow de CI y la ejecución correspondiente mostró:

CI #3
Commit: 116e30c
Rama: feature/semana4-devops
Estado: Failure
Duración: 30 s

Con esto confirmé que GitHub Actions detectó correctamente el cambio defectuoso y bloqueó el pipeline.

---

## Intervención 9 - Despliegue público de SensorHub en Render

Después de validar localmente el arranque completo con PostgreSQL, Alembic y Uvicorn decidí desplegar SensorHub utilizando Render

Decidí mantener el despliegue conectado a la rama:

`feature/semana4-devops`

para poder completar y revisar la Semana 4 sin integrar todavía los cambios en main

Creé una instancia PostgreSQL administrada en Render con la siguiente configuración general:

* Name: sensorhub-db
* Database: sensorhub
* User: sensorhub
* Region: Oregon (US West)
* PostgreSQL Version: 18
* Instance Type: Free
* Storage: 1 GB

Mantuve deshabilitados:

* Storage Autoscaling
* High Availability

Render proporcionó una Internal Database URL que utilicé directamente como variable de entorno del servicio web. No almacené ni publiqué esta credencial dentro del repositorio

Configuré un nuevo Web Service conectado al repositorio del proyecto. La configuración utilizada fue:

* Language: Docker
* Branch: feature/semana4-devops
* Region: Oregon (US West)
* Root Directory: vacío
* Dockerfile Path: ./Dockerfile
* Instance Type: Free

Inicialmente Render detectó automáticamente el proyecto como una aplicación Python y propuso comandos genéricos basados en Poetry y Gunicorn. Como el proyecto ya cuenta con una estrategia de contenedores propia, cambié manualmente el runtime a Docker para utilizar el Dockerfile versionado en el repositorio

Configuré:

`DATABASE_URL`

utilizando directamente la Internal Database URL generada por Render

### Migraciones y arranque

No configuré un comando adicional de pre-deploy porque las migraciones ya forman parte del flujo definido en start.sh

El proceso de inicio ejecuta:

`alembic upgrade head`

antes de levantar:

`python -m uvicorn app.main:app`

### Resultado del despliegue

Render construyó correctamente la imagen Docker
Durante los logs de despliegue se observó:

* Context impl PostgresqlImpl
* Will assume transactional DDL
* Running upgrade -> eacacdab5dc6

Después inició correctamente la aplicación:

* Started server process
* Application startup complete
* Uvicorn running on http://0.0.0.0:10000

Esto confirmó que start.sh utilizó correctamente la variable PORT proporcionada por Render

Render posteriormente indicó:

* Your service is live
* URL pública

La API quedó disponible en:

https://sensorhub-api-clx6.onrender.com
Validación de /health

Render ejecutó repetidamente el health check y obtuvo:

`GET /health HTTP/1.1 200 OK`

También validé manualmente:

https://sensorhub-api-clx6.onrender.com/health

Resultado:

{
  "status": "ok",
  "service": "SensorHub API",
  "version": "0.1.0"
}

Validación de Swagger

También validé públicamente:

https://sensorhub-api-clx6.onrender.com/docs

La documentación Swagger UI cargó correctamente

### Resultado

Con esta prueba confirmé que SensorHub funciona fuera de mi entorno local con:

Docker
    |
    v
Render
    |
    v
PostgreSQL administrado
    |
    v
Alembic
    |
    v
Uvicorn
    |
    v
API pública

El despliegue público quedó validado mediante /health, /docs y los logs de migración y arranque

### Problema detectado antes de la prueba

Antes de realizar la prueba de CD observé que un commit anterior había ejecutado correctamente GitHub Actions, pero Render no había iniciado un nuevo despliegue automático

Revisé:

- la rama configurada
- Auto-Deploy
- Build Filters
- los eventos del servicio

La configuración del Web Service era correcta, sin embargo, Render no registraba ningún evento para el nuevo commit

Con apoyo de la IA revisé la sección de credenciales Git utilizadas por Render. Detecté que la credencial de GitHub inicialmente solo tenía acceso a:

`JafetPalacios/render-blueprint-demo`

y no al repositorio:

`JafetPalacios/sdlc-electronica-jafet-palacios`

Actualicé la autorización de GitHub para permitir a Render acceder explícitamente al repositorio del proyecto. Después de actualizar la credencial, Render mostró correctamente:

`JafetPalacios/sdlc-electronica-jafet-palacios`

dentro de los repositorios autorizados para despliegue

Modifiqué en app/main.py:

`APP_VERSION: Final[str] = "0.1.0"`

por:

`APP_VERSION: Final[str] = "0.1.1"`

Como el contrato del endpoint /health también valida la versión, actualicé la prueba correspondiente para esperar: `0.1.1`

Antes de enviar el cambio ejecuté:

`python -m pytest`
`git diff --check`

Realicé el commit:

`6aecf07 feat: actualizar versión de SensorHub a 0.1.1`

El push disparó GitHub Actions automáticamente. Esto confirmó que el cambio continuaba cumpliendo los controles de calidad antes del despliegue
Render detectó automáticamente el mismo commit y creó un nuevo despliegue. No fue necesario utilizar Manual Deploy ni el Deploy Hook
Después del despliegue consulté nuevamente:

https://sensorhub-api-clx6.onrender.com/health

La respuesta fue:

{
  "status": "ok",
  "service": "SensorHub API",
  "version": "0.1.1"
}

Esto confirmó que el código correspondiente al commit 6aecf07 había llegado efectivamente al entorno público

### Resultado

La secuencia completa observada fue:

Cambio en código
    |
    v
git push
    |
    v
GitHub Actions
    |
    v
CI en verde
    |
    v
Render Auto-Deploy
    |
    v
producción actualizada
    |
    v
/health -> 0.1.1

Con esta prueba quedó validada la entrega continua de SensorHub desde la rama `feature/semana4-devops`
La actualización de producción quedó trazada tanto en GitHub Actions como en el historial de deploys de Render

---

## Intervención 11 - Validación final de CD desde main


Después de validar Auto-Deploy desde la rama `feature/semana4-devops`, revisé nuevamente la rúbrica de Semana 4. Detecté que el criterio de entrega continua solicitaba específicamente demostrar que un push a `main` actualizara producción automáticamente. Por esta razón decidí integrar el trabajo de Semana 4 en `main` y repetir la prueba de CD desde esa rama

Antes de realizar la integración comprobé la relación entre:

main
feature/semana3-sensorhub
feature/semana4-devops

La comparación mostró que Semana 4 contenía completamente los cambios de Semana 3 y agregaba 13 commits adicionales. Creé un Pull Request desde `feature/semana4-devops` hacia `main`
Para demostrar que un nuevo push a main modificaba producción actualicé la versión pública de SensorHub:

`0.1.1 -> 0.1.2`

Modifiqué la versión central de la aplicación y actualicé el test del endpoint `/health`

* GitHub Actions detectó automáticamente el cambio en `main`
* Render detectó el mismo commit y realizó automáticamente el despliegue
* Después del despliegue consulté `https://sensorhub-api-clx6.onrender.com/health`. La respuesta fue:

{
  "status": "ok",
  "service": "SensorHub API",
  "version": "0.1.2"
}

Con esta prueba quedó demostrado que la entrega continua funciona directamente desde main, cumpliendo el criterio solicitado en la rúbrica de Semana 4

---

## Intervención 12 - Auditoría final de la rúbrica base y endurecimiento del entorno

Después de completar el despliegue continuo desde `main`, decidí revisar nuevamente toda la guía de Semana 4 para comprobar que no quedara ningún detalle pendiente que pudiera afectar la rúbrica final

La revisión se centró en:

- contenerización
- reproducibilidad
- seguridad
- documentación
- rollback
- consistencia entre desarrollo local, CI y producción

### Validación de Docker Compose

Ejecuté:

```powershell
docker compose config
docker compose ps -a
```

La configuración de Compose fue válida y mostró correctamente:

* api
* db
* pgdata
* DATABASE_URL
* service_healthy

Durante esta revisión detecté que existía un contenedor antiguo de la API detenido y que PostgreSQL seguía activo con un volumen persistente creado antes de finalizar la integración con Alembic
Decidí recrear los contenedores utilizando los archivos actuales de main sin eliminar inicialmente el volumen

Durante el arranque se produjo el error:

`./start.sh: 2: set: Illegal option -`

Consulté el error con la IA y se diagnosticó que `start.sh` estaba siendo materializado en Windows con finales de línea CRLF aunque Git lo almacenaba internamente con LF

Lo confirmé mediante:

`git ls-files --eol start.sh` que dió como resultado `i/lf    w/crlf    start.sh`

La IA recomendó añadir una política explícita en `.gitattributes`

Creé:

`*.sh text eol=lf`

y convertí físicamente `start.sh` a LF

La verificación posterior mostró:

`i/lf    w/lf    attr/text eol=lf    start.sh`

Reconstruí nuevamente el entorno:

```docker compose down
docker compose up -d --build
```

Docker reutilizó correctamente la caché de capas y únicamente reconstruyó el archivo modificado

PostgreSQL quedó:

`healthy`

y la API inició correctamente. Sin embargo, durante el arranque Alembic produjo:

`psycopg.errors.DuplicateTable: relation "sensors" already exists`

Revisé la base persistida y comprobé que contenía:

* sensors
* readings

pero no existía:

`alembic_version`

Esto confirmó que el volumen había sido creado antes de que Alembic quedara como administrador único del esquema

Consulté además:

* columnas
* índices
* constraints
* cantidad de registros

El esquema coincidía con la migración inicial y ambas tablas estaban vacías

Resultado:

sensors  = 0
readings = 0

Como el volumen no contenía datos útiles, decidí eliminarlo y comprobar el escenario realmente importante para la entrega: crear todo el entorno desde cero únicamente mediante Docker Compose y Alembic

Ejecuté:

`docker compose down -v`
`docker compose up -d --build`

Resultado:

`PostgreSQL healthy`
`API Up`

Los logs mostraron:

* Running upgrade -> eacacdab5dc6
* Application startup complete
* Uvicorn running on http://0.0.0.0:8000
* Validación funcional desde una base limpia

Comprobé:

`Invoke-RestMethod http://localhost:8000/health`
`(Invoke-WebRequest -UseBasicParsing http://localhost:8000/docs).StatusCode`

Resultado:

* status  : ok
* service : SensorHub API
* version : 0.1.2

y:

200

También verifiqué en PostgreSQL:

`SELECT * FROM alembic_version;`

Resultado:

`eacacdab5dc6`

Las tablas creadas fueron:

* alembic_version
* readings
* sensors

Con esta prueba confirmé que el proyecto puede levantarse desde un entorno completamente limpio mediante:

Docker Compose
    |
    v
PostgreSQL
    |
    v
Alembic
    |
    v
SensorHub

### Corrección persistente de scripts Linux

Después de validar el funcionamiento real, registré la política de finales de línea mediante el commit:

`0873e8d fix: asegurar finales de línea LF en scripts de Docker`

Durante la auditoría detecté que el badge del README todavía apuntaba a:

`feature/semana4-devops`

aunque la rama definitiva del proyecto ya era `main`

Lo actualicé para que el badge represente el pipeline real de main

Commit:

`94044c7 docs: actualizar badge de CI para main`

También detecté que todas las dependencias estaban fijadas excepto `psycopg[binary]`. La versión utilizada correctamente durante los builds era 3.3.4, decidí fijarla como `psycopg[binary]==3.3.4`. Antes de registrarla ejecuté:

* python -m pip install -r requirements.txt
* python -m ruff check app tests migrations
* python -m mypy app tests migrations --ignore-missing-imports
* python -m pytest

Resultados:

* Ruff: OK
* mypy: OK
* 24 pruebas superadas
* Cobertura: 91.63 %

Commit:

`60e2e24 chore: fijar versión de psycopg para builds reproducibles`

### Estrategia de rollback

La guía también pedía poder explicar cómo recuperar producción ante un despliegue defectuoso. Consulté a la IA cuál era el procedimiento más seguro

La recomendación fue utilizar:

`git revert <commit_defectuoso>`
`git push origin main`

en lugar de:

`git reset --hard`
`git push --force`

porque git revert conserva el historial, deja trazabilidad, vuelve a pasar por CI y permite que Render haga Auto-Deploy de la corrección. También documenté que una migración de base de datos debe analizarse por separado antes de utilizar un posible `alembic downgrade` para evitar pérdida de datos. La estrategia quedó documentada en README mediante:

`7614fd0 docs: documentar estrategia de rollback`

### Resultado

Después de estas comprobaciones confirmé que los criterios obligatorios de Semana 4 estaban cubiertos:

Contenerización          cumplido
CI                       cumplido
Producción               cumplido
CD desde main            cumplido
Seguridad                cumplido
Rollback documentado     cumplido
Cobertura >= 80 %        cumplido
Bitácora                 actualizada

La cobertura validada se mantuvo en:

91.63 %

Con esto quedó consolidado el cumplimiento de la rúbrica base antes de comenzar las extensiones de Alto Potencial

---

## Intervención 13 - Implementación de extensiones de Alto Potencial

Después de confirmar que la rúbrica base estaba completa, decidí implementar también las extensiones de Alto Potencial indicadas en la guía. El plan seguido fue:

* multi-stage build
* Trivy
* PostgreSQL real en CI
* issue automático ante fallo en main
* GitHub Environment con protección

En esta intervención registro las extensiones completadas antes de configurar el GitHub Environment

### Extensión 1 - Build multi-stage

La guía proponía una imagen multi-stage menor a 200 MB. Primero medí la imagen existente:

`docker image ls sdlc-electronica-jafet-palacios-api`
`docker image inspect sdlc-electronica-jafet-palacios-api:latest --format "{{.Size}}"`

Resultado inicial:

`Content size: 98.8 MB`
`Size: 98,788,917 bytes`

Aunque la imagen ya estaba por debajo de 200 MB, todavía no utilizaba multi-stage
Detecté que requirements.txt contenía tanto dependencias de producción como herramientas utilizadas únicamente por desarrollo y CI

Separé:

`requirements.txt`

para runtime:

* fastapi
* uvicorn
* sqlalchemy
* alembic
* pydantic
* psycopg

y creé:

`requirements-dev.txt`

con:

* -r requirements.txt
* httpx
* pytest
* pytest-cov
* ruff
* mypy

Después validé:

* python -m pip install -r requirements-dev.txt
* python -m ruff check app tests migrations
* python -m mypy app tests migrations --ignore-missing-imports
* python -m pytest

Resultados:

* Ruff: OK
* mypy: OK
* 24 pruebas superadas
* Cobertura: 91.63 %

También actualicé GitHub Actions para instalar `requirements-dev.txt` en el job de pruebas
Convertí el Dockerfile a dos etapas:

builder
    |
    v
runtime

En builder se instalan únicamente las dependencias de producción en `/install` y la etapa final copia únicamente esas dependencias junto con:

* app/
* alembic.ini
* migrations/
* start.sh

La imagen final no incluye herramientas de desarrollo. Parta la medición de la imagen optimizada
Construí desde cero mediante `docker compose build --no-cache api`

Resultado:

`Content size: 62.3 MB`
`Size: 62,341,440 bytes`

Antes:   98.8 MB
Después: 62.3 MB

La reducción aproximada fue 36.9 %

También confirmé dentro del runtime:

* pytest: None
* ruff: None
* mypy: None
* httpx: None

Esto demostró que las herramientas de desarrollo ya no estaban presentes en producción.
Levanté Compose y comprobé:

`api: Up`
`db: healthy`

El primer intento de consultar /health se hizo antes de que Uvicorn terminara de iniciar. Después de esperar el arranque completo, los logs mostraron:

`Application startup complete`
`Uvicorn running on http://0.0.0.0:8000`

y validé:

`/health -> 200`
`/docs   -> 200`
`version -> 0.1.2`

La extensión quedó registrada en:

`1607a81 feat: optimizar imagen con build multi-stage`

### Extensión 2 - Escaneo de vulnerabilidades con Trivy

Decidí integrar Trivy directamente en GitHub Actions porque no estaba instalado localmente. Agregué un job `security` que:

* construye la imagen de producción
* ejecuta Trivy
* analiza vulnerabilidades de sistema operativo y librerías
* considera severidades HIGH y CRITICAL
* bloquea el pipeline mediante exit-code: 1
* ignora únicamente vulnerabilidades sin corrección disponible

Utilicé:

`aquasecurity/trivy-action@v0.35.0`

en lugar de seguir una referencia mutable como master

Commit:

`2813e7b ci: agregar escaneo de vulnerabilidades con Trivy`

GitHub Actions ejecutó:

* CI #19
* Rama: main
* Estado: Success

Con esto confirmé que el análisis de seguridad estaba integrado y no detectó vulnerabilidades bloqueantes bajo el criterio configurado

### Extensión 3 - PostgreSQL real y smoke test en GitHub Actions

La siguiente extensión consistió en comprobar SensorHub contra PostgreSQL real dentro de CI, en lugar de depender únicamente de SQLite durante los tests. Agregué el job `smoke-postgres`con `postgres:16` como service container.
La configuración utilizó una base temporal exclusiva de CI y una DATABASE_URL local al runner. El flujo implementado fue:

PostgreSQL 16
      |
      v
healthcheck
      |
      v
alembic upgrade head
      |
      v
SELECT 1
      |
      v
alembic_version
      |
      v
sensors + readings

El smoke test verifica:

* SELECT 1 = 1
* revision = eacacdab5dc6
* alembic_version existe
* sensors existe
* readings existe

Commit:

`8fae1e8 ci: validar migraciones con PostgreSQL real`

GitHub Actions ejecutó:

* CI #20
* Rama: main
* Estado: Success

Esto confirmó que las migraciones funcionan realmente contra PostgreSQL dentro del pipeline

### Extensión 4 - Issue automático cuando falle CI en main

La guía proponía crear automáticamente un issue si falla main. Para implementarlo creé:

`.github/workflows/ci-failure-issue.yml`

El workflow escucha `workflow_run` del workflow `CI` y únicamente actúa cuando:

* conclusion == failure
* head_branch == main

Configuré permisos mínimos:

* issues: write
* contents: read

El workflow:

* obtiene la ejecución fallida
* genera un título con el SHA
* incluye el enlace al workflow
* verifica si ya existe un issue equivalente
* evita duplicados
* crea el issue cuando corresponde

Commit:

`395950a ci: crear issue automático ante fallos en main`

No quise romper código real ni introducir una regresión en producción solo para comprobar esta automatización. Por recomendación de la IA añadí un mecanismo manual mediante `workflow_dispatch` con el input `simulate_failure`. El paso de fallo solo puede ejecutarse cuando:

* event_name == workflow_dispatch
* simulate_failure == true

Por tanto, los pushes y pull requests normales no se ven afectados

Commit:

`2e5147f ci: permitir simulación manual de fallo controlado`

Desde GitHub Actions ejecuté manualmente:

* Workflow: CI
* Branch: main
* simulate_failure: true

Resultado:

* CI #23
* Evento: workflow_dispatch
* Estado: Failure intencional

Los jobs mostraron:

* test            Failure
* security        Success
* smoke-postgres  Success

Esto confirmó que únicamente falló el paso de simulación mientras Trivy y PostgreSQL continuaban funcionando correctamente
Después del fallo, el workflow `Reportar fallo de CI` se ejecutó automáticamente

Resultado:

* Reportar fallo de CI #3
* Estado: Success

GitHub creó automáticamente el issue:

`CI falló en main - 2e5147f`

Con esto quedó demostrado el flujo completo:

CI falla en main
       |
       v
workflow_run
       |
       v
Reportar fallo de CI
       |
       v
Issue automático

La prueba fue deliberada, controlada y no requirió introducir código defectuoso ni realizar un despliegue de producción fallido

Estado de las extensiones

Al finalizar esta intervención quedaron completadas y verificadas:

Multi-stage < 200 MB             completado
Imagen final 62.3 MB             completado
Separación runtime/dev           completado
Trivy                            completado
PostgreSQL real en CI            completado
Smoke test de migraciones        completado
Issue automático ante fallo      completado
Prueba controlada del issue      completado

La única extensión pendiente de este bloque es GitHub Environment con protección que se realizará como una intervención separada para conservar la trazabilidad.
