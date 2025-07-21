FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Установка системных зависимостей для WeasyPrint и прочего
RUN apt-get update && apt-get install -y \
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
    netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем всё приложение
COPY . .

# Делаем скрипты исполняемыми
RUN chmod +x docker/entrypoint.sh
RUN chmod +x docker/wait_for_migrations.sh

# Указываем shell для запуска entrypoint
ENTRYPOINT ["sh", "docker/entrypoint.sh"]