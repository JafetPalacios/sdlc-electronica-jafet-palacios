# Usamos Python 3.12 en una imagen slim para mantener compatibilidad con el proyecto y reducir el tamaño final
FROM python:3.12-slim

# Evitamos generar archivos bytecode y hacemos que los logs se escriban inmediatamente en la salida del contenedor
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Definimos el directorio de trabajo de SensorHub dentro del contenedor
WORKDIR /app

# Copiamos primero las dependencias para aprovechar la caché de capas de Docker
# Si solo cambia el código de la aplicación, Docker puede reutilizar la instalación de dependencias
COPY requirements.txt .

# Instalamos las dependencias sin conservar la caché local de pip dentro de la imagen
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copiamos únicamente el código necesario para ejecutar SensorHub
COPY app ./app

# Copiamos la configuración y el historial de migraciones para administrar el esquema con Alembic
COPY alembic.ini .
COPY migrations ./migrations

# Copiamos el script que prepara la base de datos y arranca SensorHub
COPY start.sh ./start.sh

# Documentamos el puerto en el que Uvicorn expondrá la API
EXPOSE 8000

# Ejecutamos el arranque de producción que aplica migraciones antes de levantar la API
CMD ["sh", "./start.sh"]
