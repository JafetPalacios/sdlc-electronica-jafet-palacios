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

# Documentamos el puerto en el que Uvicorn expondrá la API
EXPOSE 8000

# Iniciamos SensorHub escuchando en todas las interfaces del contenedor
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]