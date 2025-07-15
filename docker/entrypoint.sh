#!/bin/bash
set -e

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "🧱 Applying database migrations..."
python manage.py migrate

echo "🚀 Running initial setup..."
python manage.py init_app

echo "🔥 Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000