# Etapa de construcción
# Instalamos únicamente las dependencias necesarias para ejecutar SensorHub
FROM python:3.12-slim AS builder

# Evitamos generar archivos bytecode y mantenemos una salida inmediata de logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copiamos primero las dependencias para aprovechar la caché de Docker
COPY requirements.txt .

# Instalamos las dependencias de runtime en un directorio independiente
# Después copiaremos únicamente este directorio a la imagen final
RUN python -m pip install \
    --no-cache-dir \
    --prefix=/install \
    -r requirements.txt


# Etapa final de ejecución
# Partimos nuevamente de una imagen slim limpia para no arrastrar archivos del builder
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Actualizamos los paquetes del sistema para incorporar correcciones de seguridad
# Eliminamos los índices de APT para no conservar archivos innecesarios
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiamos solamente las dependencias instaladas durante la etapa de construcción
COPY --from=builder /install /usr/local

# Copiamos únicamente los archivos necesarios para ejecutar SensorHub
COPY app ./app

# Incluimos la configuración y las migraciones administradas por Alembic
COPY alembic.ini .
COPY migrations ./migrations

# Copiamos el script de inicio encargado de aplicar migraciones y levantar Uvicorn
COPY start.sh ./start.sh

# Documentamos el puerto utilizado localmente por SensorHub
EXPOSE 8000

# Aplicamos las migraciones pendientes y levantamos la API
CMD ["sh", "./start.sh"]