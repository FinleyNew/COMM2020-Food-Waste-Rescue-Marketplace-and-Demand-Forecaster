#!/bin/bash

set -e

export PYTHONPATH=$PYTHONPATH:.

export POSTGRES_SERVER=db

echo "Running migrations..."
alembic upgrade head

python -m app.db.seed_data

echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload