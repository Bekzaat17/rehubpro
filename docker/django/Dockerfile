FROM python:3.11-slim

# --- Основные переменные окружения ---
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Almaty \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# --- Установка зависимостей системы ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libssl-dev \
    libcairo2 \
    libglib2.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libxml2 \
    libxslt1.1 \
    libjpeg-dev \
    libpng-dev \
    zlib1g-dev \
    curl \
    tzdata \
    netcat-openbsd \
 && ln -sf /usr/share/zoneinfo/$TZ /etc/localtime \
 && echo "$TZ" > /etc/timezone \
 && rm -rf /var/lib/apt/lists/*

# --- Копируем зависимости и устанавливаем Python-пакеты ---
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# --- Копируем проект ---
COPY . .

# --- Скрипты ---
RUN chmod +x docker/entrypoint.sh docker/wait_for_migrations.sh

# --- Старт ---
ENTRYPOINT ["sh", "docker/entrypoint.sh"]