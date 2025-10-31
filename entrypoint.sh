#!/bin/bash
set -e

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Running gunicorn..."
# Render sets PORT environment variable (defaults to 10000)
# For local dev, use PORT=8000 in docker-compose.yml
PORT=${PORT:-10000}
echo "Binding to port: $PORT"
# Use fewer workers for free tier (1 worker, 4 threads = better for low memory)
exec gunicorn fabrik.wsgi:application --bind 0.0.0.0:${PORT} --workers=1 --threads=4 --timeout=300