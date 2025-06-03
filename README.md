# 🤖 SmartGroupBot

Умный Telegram бот для групповых чатов с поддержкой AI анализа контекста и генерации ответов.

## ✨ Возможности

- 🧠 **AI анализ контекста** - анализирует сообщения в группе с помощью OpenRouter.ai
- 💬 **Умные ответы** - генерирует релевантные ответы на основе контекста
- 📊 **Аналитика настроения** - определяет тональность сообщений
- 🎯 **Адаптивная частота** - отвечает раз в 5 сообщений (настраивается)
- 📈 **База данных** - сохраняет историю взаимодействий
- 🔧 **Простая настройка** - конфигурация через .env файл

## 🚀 Быстрый запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка конфигурации

Скопируйте `config.env.example` в `config.env` и заполните:

```bash
cp config.env.example config.env
```

Отредактируйте `config.env`:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=ваш_токен_бота

# OpenAI Configuration (using OpenRouter.ai)
OPENAI_API_KEY=ваш_openrouter_api_ключ

# Bot Settings
RESPONSE_FREQUENCY=5  # Отвечать раз в 5 сообщений
MIN_CONTEXT_MESSAGES=1  # Минимум сообщений для анализа
```

### 3. Запуск бота

**Простой запуск (рекомендуется):**
```bash
python3 start_simple.py
```

**Запуск с проверками:**
```bash
python3 run_all.py
```

**Остановка:**
```bash
python3 stop_all.py
```

## 📁 Структура проекта

```
ai-chat/
├── main_bot.py          # Основной файл бота
├── bot_service.py       # Сервис обработки сообщений
├── ai_service.py        # AI сервис (OpenRouter.ai)
├── config.py            # Конфигурация
├── models.py            # Модели базы данных
├── start_simple.py      # Простой запуск
├── run_all.py          # Запуск с проверками
├── stop_all.py         # Остановка всех процессов
├── config.env          # Конфигурация (создать из .example)
├── requirements.txt    # Зависимости Python
└── smart_bot.log      # Логи работы
```

## ⚙️ Конфигурация

### Основные параметры в `config.env`:

- `TELEGRAM_BOT_TOKEN` - токен Telegram бота
- `OPENAI_API_KEY` - API ключ OpenRouter.ai
- `RESPONSE_FREQUENCY` - частота ответов (по умолчанию: 5)
- `MIN_CONTEXT_MESSAGES` - минимум сообщений для анализа (по умолчанию: 1)
- `MAX_CONTEXT_MESSAGES` - максимум сообщений в контексте (по умолчанию: 10)

## 🔧 Команды бота

- `/start` - информация о боте
- `/help` - справка по командам
- `/stats` - статистика чата

## 📊 Мониторинг

Логи сохраняются в файл `smart_bot.log`:

```bash
# Просмотр логов в реальном времени
tail -f smart_bot.log

# Поиск ошибок
grep "ERROR" smart_bot.log
```

## 🛠️ Разработка

### Архитектура

1. **main_bot.py** - точка входа, обработчики Telegram
2. **bot_service.py** - бизнес-логика, буфер сообщений
3. **ai_service.py** - интеграция с OpenRouter.ai
4. **models.py** - работа с базой данных SQLite

### Добавление новых функций

1. Обработчики команд добавляйте в `main_bot.py`
2. Бизнес-логику размещайте в `bot_service.py`
3. AI функции добавляйте в `ai_service.py`

## 🐛 Устранение неполадок

### Бот не отвечает
- Проверьте токен в `config.env`
- Убедитесь что бот добавлен в группу как администратор
- Проверьте логи: `tail -f smart_bot.log`

### Ошибки API
- Проверьте API ключ OpenRouter.ai
- Убедитесь в наличии квоты на API

### Конфликт процессов
```bash
python3 stop_all.py  # Остановить все процессы
python3 start_simple.py  # Запустить заново
```

## 📝 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

## 🤝 Поддержка

Если у вас есть вопросы или предложения, создайте Issue в репозитории.

---

**Статус:** ✅ Активная разработка  
**Версия:** 2.0  
**Python:** 3.8+ 