# ⚙️ Конфигурация SmartGroupBot

Полное руководство по настройке и конфигурации SmartGroupBot.

## 📋 Обзор

SmartGroupBot использует файл `config.env` для настройки всех параметров. Конфигурация разделена на логические блоки для удобства управления.

## 🔧 Создание конфигурации

```bash
# Копирование примера конфигурации
cp config.env.example config.env

# Редактирование
nano config.env  # или vim, code, etc.
```

## 📝 Параметры конфигурации

### 🤖 Telegram Bot Configuration

#### `TELEGRAM_BOT_TOKEN` (обязательно)
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGhIjKlMnOpQrStUvWxYz
```
- **Описание:** Токен Telegram бота от @BotFather
- **Получение:** 
  1. Напишите [@BotFather](https://t.me/botfather)
  2. Создайте бота командой `/newbot`
  3. Скопируйте полученный токен
- **Безопасность:** Никогда не публикуйте токен в открытом виде

#### `BOT_NAME` (опционально)
```env
BOT_NAME=SmartGroupBot
```
- **Описание:** Отображаемое имя бота
- **По умолчанию:** SmartGroupBot
- **Использование:** В логах и сообщениях

#### `BOT_PERSONALITY` (опционально)
```env
BOT_PERSONALITY=Дружелюбный и умный помощник в групповых чатах
```
- **Описание:** Личность бота для AI-генерации
- **Влияние:** Стиль ответов бота
- **Примеры:**
  - `Профессиональный помощник`
  - `Весёлый собеседник`
  - `Строгий модератор`

---

### 🧠 OpenAI Configuration

#### `OPENAI_API_KEY` (опционально)
```env
OPENAI_API_KEY=sk-1234567890abcdef...
```
- **Описание:** API ключ OpenAI для GPT анализа
- **Получение:**
  1. Регистрация на [OpenAI](https://platform.openai.com)
  2. Создание API ключа
  3. Пополнение баланса (минимум $5)
- **Fallback:** Если не указан, используется fallback режим

#### `OPENAI_MODEL` (опционально)
```env
OPENAI_MODEL=gpt-3.5-turbo
```
- **Описание:** Модель OpenAI для использования
- **По умолчанию:** gpt-3.5-turbo
- **Варианты:**
  - `gpt-3.5-turbo` - быстрый и дешёвый
  - `gpt-4` - более умный, но дорогой
  - `gpt-4-turbo` - баланс скорости и качества

#### `MAX_RESPONSE_TOKENS` (опционально)
```env
MAX_RESPONSE_TOKENS=150
```
- **Описание:** Максимум токенов в ответе
- **По умолчанию:** 150
- **Диапазон:** 50-500
- **Влияние:** Длина ответов бота

---

### 🎯 Bot Behavior Settings

#### `RESPONSE_FREQUENCY` (важно)
```env
RESPONSE_FREQUENCY=5
```
- **Описание:** Частота ответов (раз в N сообщений)
- **По умолчанию:** 5
- **Рекомендации:**
  - `2-3` - очень активный бот
  - `5-7` - умеренно активный
  - `10+` - редкие ответы

#### `MIN_CONTEXT_MESSAGES` (важно)
```env
MIN_CONTEXT_MESSAGES=5
```
- **Описание:** Минимум сообщений для анализа
- **По умолчанию:** 5
- **Логика:** Бот накапливает контекст перед ответом
- **Диапазон:** 2-10

#### `MAX_CONTEXT_MESSAGES` (опционально)
```env
MAX_CONTEXT_MESSAGES=10
```
- **Описание:** Максимум сообщений в контексте
- **По умолчанию:** 10
- **Влияние:** Глубина анализа контекста
- **Память:** Больше = больше RAM

---

### 🗄️ Database Configuration

#### `DATABASE_URL` (важно)
```env
DATABASE_URL=sqlite:///bot_database.db
```
- **Описание:** URL подключения к базе данных
- **Варианты:**
  
  **SQLite (по умолчанию):**
  ```env
  DATABASE_URL=sqlite:///bot_database.db
  DATABASE_URL=sqlite:////absolute/path/to/database.db
  ```
  
  **PostgreSQL:**
  ```env
  DATABASE_URL=postgresql://username:password@localhost:5432/smartbot
  DATABASE_URL=postgresql://user:pass@host:port/dbname
  ```
  
  **MySQL:**
  ```env
  DATABASE_URL=mysql://username:password@localhost:3306/smartbot
  ```

---

### 🌐 Web Dashboard Settings

#### `WEB_HOST` (опционально)
```env
WEB_HOST=0.0.0.0
```
- **Описание:** IP адрес для веб-панели
- **По умолчанию:** 0.0.0.0 (все интерфейсы)
- **Варианты:**
  - `127.0.0.1` - только localhost
  - `0.0.0.0` - все интерфейсы
  - `192.168.1.10` - конкретный IP

#### `WEB_PORT` (опционально)
```env
WEB_PORT=5001
```
- **Описание:** Порт для веб-панели
- **По умолчанию:** 5001
- **Диапазон:** 1024-65535
- **Конфликты:** Избегайте 5000 (macOS AirPlay)

#### `WEB_DEBUG` (опционально)
```env
WEB_DEBUG=false
```
- **Описание:** Режим отладки Flask
- **По умолчанию:** false
- **Production:** Всегда false
- **Development:** true для отладки

---

### 📝 Logging Configuration

#### `LOG_LEVEL` (опционально)
```env
LOG_LEVEL=INFO
```
- **Описание:** Уровень логирования
- **По умолчанию:** INFO
- **Варианты:**
  - `DEBUG` - все сообщения
  - `INFO` - информационные сообщения
  - `WARNING` - предупреждения и ошибки
  - `ERROR` - только ошибки

#### `LOG_FILE_MAX_SIZE` (опционально)
```env
LOG_FILE_MAX_SIZE=10485760
```
- **Описание:** Максимальный размер лог файла (байты)
- **По умолчанию:** 10485760 (10MB)
- **Ротация:** При превышении создаётся новый файл

#### `LOG_FILE_BACKUP_COUNT` (опционально)
```env
LOG_FILE_BACKUP_COUNT=5
```
- **Описание:** Количество backup лог файлов
- **По умолчанию:** 5
- **Хранение:** Старые файлы автоматически удаляются

---

## 🌍 Environment-specific конфигурации

### 🏠 Development
```env
# Активный режим для тестирования
RESPONSE_FREQUENCY=2
MIN_CONTEXT_MESSAGES=2
LOG_LEVEL=DEBUG
WEB_DEBUG=true
OPENAI_API_KEY=  # fallback режим
```

### 🧪 Testing
```env
# Конфигурация для тестов
DATABASE_URL=sqlite:///test_database.db
LOG_LEVEL=WARNING
WEB_PORT=5002
BOT_NAME=TestBot
```

### 🏭 Production
```env
# Продуктовая конфигурация
RESPONSE_FREQUENCY=5
MIN_CONTEXT_MESSAGES=5
LOG_LEVEL=INFO
WEB_DEBUG=false
DATABASE_URL=postgresql://user:pass@prod-db:5432/smartbot
OPENAI_API_KEY=sk-real-production-key
```

---

## 🔒 Безопасность конфигурации

### ✅ Лучшие практики

1. **Никогда не коммитьте config.env**
   ```bash
   # Убедитесь, что файл в .gitignore
   echo "config.env" >> .gitignore
   ```

2. **Используйте переменные окружения в production**
   ```bash
   export TELEGRAM_BOT_TOKEN="your_token"
   export OPENAI_API_KEY="your_key"
   ```

3. **Ограничьте права доступа**
   ```bash
   chmod 600 config.env  # Только владелец может читать
   ```

4. **Валидация токенов**
   ```bash
   # Проверка токена Telegram
   curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"
   ```

### 🚫 Что НЕ делать

- ❌ Публиковать токены в Git
- ❌ Использовать слабые пароли БД  
- ❌ Оставлять WEB_DEBUG=true в production
- ❌ Указывать одинаковые токены для dev/prod

---

## 🔧 Валидация конфигурации

### Скрипт проверки
```bash
#!/bin/bash
# validate_config.sh

echo "🔍 Проверка конфигурации SmartGroupBot..."

# Проверка обязательных параметров
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN не задан"
    exit 1
fi

# Проверка токена Telegram
if ! curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe" | grep -q "ok.*true"; then
    echo "❌ Неверный TELEGRAM_BOT_TOKEN"
    exit 1
fi

# Проверка OpenAI (если задан)
if [ -n "$OPENAI_API_KEY" ]; then
    if ! echo "$OPENAI_API_KEY" | grep -q "^sk-"; then
        echo "⚠️ Подозрительный формат OPENAI_API_KEY"
    fi
fi

echo "✅ Конфигурация выглядит корректно"
```

### Использование
```bash
chmod +x validate_config.sh
source config.env && ./validate_config.sh
```

---

## 🎛️ Динамическая конфигурация

### Изменение параметров без перезапуска

Некоторые параметры можно изменить через веб-панель:

1. **Откройте веб-панель:** http://localhost:5001/config
2. **Измените параметры**
3. **Применить без перезапуска**

**Поддерживаемые параметры:**
- `RESPONSE_FREQUENCY`
- `LOG_LEVEL` 
- `MIN_CONTEXT_MESSAGES`

---

## 🔄 Примеры конфигураций

### Минимальная конфигурация
```env
TELEGRAM_BOT_TOKEN=your_token_here
# Всё остальное - значения по умолчанию
```

### Полная конфигурация
```env
# === SmartGroupBot Configuration ===

# Telegram
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGhIjKlMnOpQrStUvWxYz
BOT_NAME=MySmartBot
BOT_PERSONALITY=Профессиональный помощник в чатах

# OpenAI
OPENAI_API_KEY=sk-1234567890abcdef...
OPENAI_MODEL=gpt-3.5-turbo
MAX_RESPONSE_TOKENS=200

# Поведение
RESPONSE_FREQUENCY=3
MIN_CONTEXT_MESSAGES=4
MAX_CONTEXT_MESSAGES=8

# База данных
DATABASE_URL=postgresql://user:pass@localhost:5432/smartbot

# Веб-панель
WEB_HOST=127.0.0.1
WEB_PORT=8080
WEB_DEBUG=false

# Логирование
LOG_LEVEL=INFO
LOG_FILE_MAX_SIZE=5242880  # 5MB
LOG_FILE_BACKUP_COUNT=3
```

---

## 🆘 Устранение проблем

### Частые ошибки

**1. "Unauthorized" при запуске**
- Проверьте корректность TELEGRAM_BOT_TOKEN
- Убедитесь, что токен не содержит лишних символов

**2. "Connection failed" к базе данных**
- Проверьте DATABASE_URL
- Убедитесь, что БД запущена и доступна

**3. Бот не отвечает в группах**
- Проверьте права бота в @BotFather
- Убедитесь, что Group Privacy выключен

**4. OpenAI ошибки**
- Проверьте валидность API ключа
- Убедитесь в наличии баланса
- Используйте fallback режим при необходимости

### Диагностика
```bash
# Проверка конфигурации
python -c "from config import config; print('✅ Конфигурация загружена')"

# Тест подключения к БД
python -c "from models import DatabaseManager; print('✅ БД доступна')"

# Проверка веб-панели
curl http://localhost:5001/health
```

---

**📞 Поддержка:** При проблемах с конфигурацией обращайтесь в [GitHub Issues](https://github.com/your-username/smartgroupbot/issues) 