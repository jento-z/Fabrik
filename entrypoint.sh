#!/bin/bash
set -e

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Testing Django configuration..."
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabrik.settings'); import django; django.setup(); from django.conf import settings; print('Django configured successfully')" || {
    echo "ERROR: Django configuration failed!"
    exit 1
}

echo "Running gunicorn..."
# Render sets PORT environment variable (defaults to 10000)
# For local dev, use PORT=8000 in docker-compose.yml
PORT=${PORT:-10000}
echo "Binding to port: $PORT"
echo "Environment check:"
echo "  PORT=$PORT"
echo "  SECRET_KEY=${SECRET_KEY:+SET}"
echo "  DATABASE_URL=${DATABASE_URL:+SET}"
# Use fewer workers for free tier (1 worker, 4 threads = better for low memory)
# Add --access-logfile - to see all requests
exec gunicorn fabrik.wsgi:application --bind 0.0.0.0:${PORT} --workers=1 --threads=4 --timeout=300 --access-logfile - --log-level info