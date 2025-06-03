# 🐳 Запуск SmartGroupBot в Docker

## 📋 Предварительные требования

1. **Docker и Docker Compose** установлены
2. **Файл config.env** с корректными переменными окружения

## 🚀 Быстрый запуск

### 1. Подготовка переменных окружения

Скопируйте файл `config.env.example` в `config.env` и заполните:

```bash
cp config.env.example config.env
```

Отредактируйте `config.env`:
```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
BOT_NAME=SmartGroupBot
RESPONSE_FREQUENCY=2
LOG_LEVEL=INFO
```

### 2. Создание директорий

```bash
mkdir -p data logs
```

### 3. Запуск

```bash
# Сборка и запуск в фоне
docker-compose up -d --build

# Просмотр логов
docker-compose logs -f smartgroupbot

# Остановка
docker-compose down
```

## 📊 Мониторинг

- **Веб-панель**: http://localhost:5000
- **Логи контейнера**: `docker-compose logs -f smartgroupbot`
- **Healthcheck**: `docker-compose ps`

## 🔧 Полезные команды

```bash
# Пересборка контейнера
docker-compose build --no-cache

# Запуск в интерактивном режиме для отладки
docker-compose run --rm smartgroupbot bash

# Просмотр статуса
docker-compose ps

# Рестарт сервиса
docker-compose restart smartgroupbot

# Просмотр использования ресурсов
docker stats smartgroupbot
```

## 📁 Структура томов (volumes)

- `./data:/app/data` - База данных SQLite
- `./logs:/app/logs` - Файлы логов приложения
- `./smart_bot.log:/app/smart_bot.log` - Основной лог файл

## ⚠️ Важные заметки

1. **Переменные окружения** загружаются из файла `config.env`
2. **База данных** сохраняется в локальной папке `./data`
3. **Логи** доступны как в контейнере, так и локально
4. **Healthcheck** проверяет доступность веб-панели каждые 30 секунд
5. **Автозапуск** при перезагрузке системы (restart: unless-stopped)

## 🐛 Отладка

Если возникают проблемы:

```bash
# Проверить статус контейнера
docker-compose ps

# Посмотреть последние логи
docker-compose logs --tail=50 smartgroupbot

# Зайти в контейнер для отладки
docker-compose exec smartgroupbot bash

# Проверить переменные окружения в контейнере
docker-compose exec smartgroupbot env | grep -E "(TELEGRAM|OPENAI|BOT_)"
``` 