FROM python:3.9-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Создаем директории для данных и логов
RUN mkdir -p /app/data /app/logs

# Устанавливаем права
RUN chmod +x run_all.py

# Переменные окружения по умолчанию
ENV DATABASE_URL=sqlite:///data/bot_database.db
ENV LOG_LEVEL=INFO
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Открываем порты для веб-панели
EXPOSE 5000

# Команда запуска
CMD ["python", "run_all.py"] 