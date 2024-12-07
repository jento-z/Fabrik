#!/bin/bash
set -e

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Running gunicorn..."
gunicorn fabrik.wsgi --timeout=300

echo "Starting server..."
exec "$@"