#!/bin/bash
set -euo pipefail

echo "Running database migrations..."
python manage.py migrate --noinput

# One-time superuser creation (skips if already exists or vars unset)
if [[ -n "${DJANGO_SUPERUSER_USERNAME:-}" && -n "${DJANGO_SUPERUSER_PASSWORD:-}" && -n "${DJANGO_SUPERUSER_EMAIL:-}" ]]; then
  echo "Creating superuser if needed..."
  python manage.py createsuperuser --noinput || true
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Render sets PORT environment variable (defaults to 10000)
PORT=${PORT:-10000}
echo "Starting gunicorn on port ${PORT}..."

# Optimized for free tier: single worker, preload Django for faster startup
exec gunicorn fabrik.wsgi:application \
  --bind "0.0.0.0:${PORT}" \
  --workers 1 \
  --timeout 300 \
  --access-logfile - \
  --error-logfile - \
  --forwarded-allow-ips="*" \
  --preload