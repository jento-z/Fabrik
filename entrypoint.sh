#!/bin/bash
set -e

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Running gunicorn..."
gunicorn fabrik.wsgi --workers=2 --timeout=300 --threads=2

echo "Starting server..."
exec "$@"