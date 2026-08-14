## Semblanza
Mi nombre es Jafet de los Angeles Palacios Guatzozón
Actualmente, soy estudiante de último semestre de Ingeniería Biomédica y pasante en el laboratorio de Robótica Médica y Bioseñales del Instituto Politecnico Nacional (IPN). Previamente, inicié estudiando Instrumentación Electrónica pero cambié de carrera en 2023. 
Tengo experiencia en electrónica y programación. He trabajado con microcontroladores, sensores, comunicación de datos, desarrollo de software y lenguajes como C, C#, Python y un poco de Java. También he participado en proyectos relacionados con instrumentación biomédica, análisis de señales, sistemas IoT y visualización 3D. 
Ademas de mi experiencia técnica, he desarrollado habilidades de liderazgo y organización como presidenta de la Rama Estudiantil IEEE FIE-UV, he participando en la coordinación de eventos académicos, impartido talleres, concursos tecnológicos y actividades de divulgación científica. 
Del programa EDSIA espero fortalecer mis conocimientos en programación, pruebas, documentación y desarrollo estructurado de proyectos. Mi objetivo es mejorar mi capacidad para crear código más confiable, seguro y eficientes, además de adquirir experiencia práctica que pueda aplicar en proyectos profesionales y de investigación.



## Reflexión sobre SOLID

Durante esta semana aplicamos los principios SOLID al dominio de sensores y al desarrollo de un driver UART modernizado.

S - El principio de responsabilidad única permitió separar la configuración, el procesamiento de mensajes, los parsers y la persistencia en clases independientes. Esto facilita comprender, probar y modificar cada componente sin afectar responsabilidades no relacionadas.

O - El principio abierto/cerrado se aplicó mediante la clase abstracta `MessageParser`. El dispositivo UART puede trabajar con diferentes protocolos, como Modbus y NMEA, sin modificar la implementación de `UartDevice`. Para agregar un protocolo nuevo solamente sería necesario crear otro parser que implemente el método `parse()`.

L - La sustitución de Liskov se cumple porque `ModbusParser` y `NMEAParser` pueden utilizarse donde se espera un `MessageParser`. Ambos respetan el mismo contrato de entrada y salida.

I - La segregación de interfaces evita que las clases dependan de operaciones que no necesitan. En el driver, el dispositivo únicamente requiere que el parser proporcione el método `parse()`.

D - La inversión de dependencias se aplicó al inyectar la configuración y el parser en `UartDevice`. La clase no crea internamente un parser concreto, por lo que depende de una abstracción y no directamente de Modbus o NMEA.

La principal ventaja observada es que el sistema resulta más fácil de probar y extender. Cada clase puede validarse de forma aislada y es posible incorporar nuevos protocolos o mecanismos de persistencia con cambios mínimos.


---

# Semana 4 - DevOps, CI/CD y despliegue de SensorHub

[![CI Semana 4](https://github.com/JafetPalacios/sdlc-electronica-jafet-palacios/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/JafetPalacios/sdlc-electronica-jafet-palacios/actions/workflows/ci.yml)

Durante la Semana 4 se preparó SensorHub para ejecutarse de forma reproducible mediante contenedores, integración continua y despliegue automático

La aplicación utiliza:

- FastAPI para la API REST
- SQLAlchemy para persistencia
- Alembic para migraciones
- PostgreSQL como base de datos
- Docker para contenerización
- Docker Compose para el entorno local completo
- GitHub Actions para integración continua
- Render para despliegue público y entrega continua

### Producción

SensorHub se encuentra desplegado públicamente en:

https://sensorhub-api-clx6.onrender.com

Endpoints principales:

- Health check: https://sensorhub-api-clx6.onrender.com/health
- Swagger UI: https://sensorhub-api-clx6.onrender.com/docs

La versión desplegada actualmente es:

`0.1.1`

### Ejecución local con Docker

1. Construir la imagen:

`docker build -t sensorhub:dev .`

2. Ejecutar únicamente la API:

`docker run --rm -p 8000:8000 sensorhub:dev`

Para el funcionamiento completo con PostgreSQL se recomienda utilizar Docker Compose

### Ejecución con Docker Compose

1. Crear un archivo `.env` local tomando como referencia `.env.example`

2. Después levantar la aplicación y PostgreSQL:

`docker compose up --build`

3. La API queda disponible en:

`http://localhost:8000`

Endpoints locales:

`http://localhost:8000/health`
`http://localhost:8000/docs`

Docker Compose espera a que PostgreSQL esté disponible antes de iniciar la API

4. Durante el arranque se ejecutan automáticamente las migraciones mediante:

`alembic upgrade head`

### Migraciones

1. Crear una nueva migración después de modificar los modelos:

`alembic revision --autogenerate -m "descripcion de la migracion"`

2. Aplicar todas las migraciones pendientes:

`alembic upgrade head`

3. Consultar la revisión actual:

`alembic current`

### Integración continua

El workflow se encuentra en:

`.github/workflows/ci.yml`

El pipeline ejecuta automáticamente:

Ruff
  |
  v
mypy
  |
  v
pytest + cobertura

La cobertura mínima requerida es 80 % y la cobertura validada durante la Semana 4 fue 91.63 %. También se realizó una prueba deliberada de regresión para comprobar que GitHub Actions bloqueara un cambio defectuoso

El flujo observado fue:

CI verde
    |
    v
regresión intencional
    |
    v
CI rojo
    |
    v
corrección
    |
    v
CI verde
Entrega continua

Render está configurado con Auto-Deploy sobre la rama de trabajo de la Semana 4

La entrega continua fue validada mediante el cambio:

`SensorHub 0.1.0 -> 0.1.1`

El flujo comprobado fue:

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

Después del despliegue automático se verificó públicamente:

{
  "status": "ok",
  "service": "SensorHub API",
  "version": "0.1.1"
}

Las credenciales y datos sensibles no se almacenan directamente en el repositorio

La aplicación utiliza:

`DATABASE_URL`

para configurar la conexión a la base de datos

En desarrollo local las variables se cargan desde .env, archivo excluido del control de versiones

El repositorio contiene .env.example únicamente como referencia de configuración

En producción DATABASE_URL se configura directamente mediante las variables de entorno de Render



## Un detalle sobre el badge

He puesto explícitamente:

`?branch=feature%2Fsemana4-devops`

porque esa era la rama que contiene y ejecuta nuestro workflow.

Eso hace que el badge represente la CI que realmente estoy entregando en ese momento. Cuando resolví el requisito final de main, cambié el badge para que represente main.

## Rollback

Si una versión desplegada introduce un fallo, se identifica el commit responsable y se crea un `revert` en `main`

```bash
git switch main
git pull --ff-only origin main
git revert <commit_defectuoso>
git push origin main
```
