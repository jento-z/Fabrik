#!/bin/bash
set -e

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Running gunicorn..."
gunicorn fabrik.wsgi:application --bind 0.0.0.0:8000

echo "Starting server..."
exec "$@"