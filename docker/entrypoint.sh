#!/bin/bash
set -e

# Используем переменную TZ из окружения, если задана
if [ -n "$TZ" ]; then
  echo "🌍 Setting timezone to $TZ"
  ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime
  echo "$TZ" > /etc/timezone
fi

# Ожидаем готовности PostgreSQL
echo "⏳ Waiting for PostgreSQL to be ready at $POSTGRES_HOST:$POSTGRES_PORT..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 0.1
done
echo "✅ PostgreSQL is ready!"

# Если сервис web — собираем статику и запускаем инициализацию
if [ "$SERVICE_NAME" = "web" ]; then
  echo "📦 Collecting static files..."
  python manage.py collectstatic --noinput

  echo "🚀 Running initial setup (init_app)..."
  python manage.py init_app
fi

# Запускаем основной процесс (переданный через CMD или docker-compose command)
exec "$@"