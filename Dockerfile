# Docker-команда FROM вказує базовий образ контейнера
FROM python:3.13-slim

# Встановлюємо Poetry
ENV POETRY_VERSION=2.1.3
RUN pip install --upgrade pip \
    && pip install poetry==$POETRY_VERSION

# Вимикаємо створення віртуального середовища всередині poetry (бо воно не потрібно в Docker)
ENV POETRY_VIRTUALENVS_CREATE=false

# Встановимо змінну середовища
ENV APP_HOME=/app

# Встановимо робочу директорію всередині контейнера
WORKDIR $APP_HOME

# Копіюємо файли проєкту
COPY pyproject.toml poetry.lock* README.md ./
# Встановлюємо залежності
RUN poetry install --no-root --no-interaction --no-ansi

# Скопіюємо інші файли в робочу директорію контейнера
COPY . .

# запускаємо
CMD ["python", "main.py"]
