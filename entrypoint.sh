#!/bin/bash
set -e

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Running gunicorn..."
PORT=${PORT:-8000}
exec gunicorn fabrik.wsgi:application --bind 0.0.0.0:${PORT} --workers=2 --timeout=300 --threads=2