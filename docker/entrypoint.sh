#!/bin/bash

# Ждём готовности БД
echo "⏳ Waiting for PostgreSQL to be ready..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 0.1
done
echo "✅ PostgreSQL is ready!"

# Если это контейнер web — выполняем collectstatic и init_app
if [ "$SERVICE_NAME" = "web" ]; then
  echo "📦 Collecting static files..."
  python manage.py collectstatic --noinput

  echo "🚀 Running initial setup (init_app)..."
  python manage.py init_app
fi

# Запускаем то, что передано как CMD или через `docker-compose command`
exec "$@"