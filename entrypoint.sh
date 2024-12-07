#!/bin/bash
set -e

echo "Running migrate..."
python manage.py migrate

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Running gunicorn..."
gunicorn fabrik.wsgi --workers=4 --timeout=300

echo "Starting server..."
exec "$@"