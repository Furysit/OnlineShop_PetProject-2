# --- Base image ---
FROM python:3.11-slim

# --- Установка системных зависимостей ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl libpq-dev gcc libffi-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# --- Установка Poetry ---
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 - \
 && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# --- Установка рабочей директории ---
WORKDIR /app

# --- Копирование файлов проекта ---
COPY pyproject.toml poetry.lock ./
COPY app ./app

# --- Установка зависимостей без dev-зависимостей ---
RUN poetry config virtualenvs.create false \
 && poetry install --no-dev --no-interaction --no-ansi

# --- Опционально: переменные окружения (если нужно) ---
ENV PYTHONUNBUFFERED=1

# --- Открываем порт (если нужно) ---
EXPOSE 8000

# --- Команда запуска ---
CMD ["poetry", "run", "start"]
