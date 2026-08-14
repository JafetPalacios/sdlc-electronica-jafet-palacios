#!/bin/sh
set -e

# Aplicamos todas las migraciones pendientes antes de iniciar la API
alembic upgrade head

# Iniciamos SensorHub escuchando en todas las interfaces
# Utilizamos PORT cuando la plataforma lo proporciona y 8000 como valor local por defecto
exec python -m uvicorn app.main:app \
    --host 0.0.0.0 \
    --port "${PORT:-8000}"