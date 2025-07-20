#!/bin/bash
set -e  # Остановить выполнение скрипта при любой ошибке (fail-fast)

# =============================
# 📦 Сборка статических файлов
# =============================
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# =============================
# 🧱 Применение миграций БД
# =============================
echo "🧱 Applying database migrations..."
python manage.py migrate

# =============================
# 🚀 Инициализация демо-данных
# =============================
# Команда /users/management/commands init_app создаёт справочники, роли, резидентов и т.д.
# По умолчанию она не будет перезаписывать данные, если уже есть пользователи.
# Для принудительной инициализации используй: --force
echo "🚀 Running initial setup..."
python manage.py init_app # Добавь --force при необходимости

# =============================
# 🔥 Запуск Gunicorn-сервера
# =============================
# Используем exec, чтобы заменить текущий процесс скрипта на gunicorn
# Это важно для правильной обработки сигналов (например, в Docker)
# echo "🔥 Starting Gunicorn..."
# exec gunicorn config.wsgi:application --bind 0.0.0.0:8000


echo "🔥 Starting Daphne..."
exec daphne -b 0.0.0.0 -p 8000 config.asgi:application