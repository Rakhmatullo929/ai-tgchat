# 🤖 SmartGroupBot

**Профессиональный AI-бот для Telegram групп с интеллектуальным анализом контекста и веб-аналитикой**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-Latest-blue.svg)](https://core.telegram.org/bots/api)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-green.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Описание

SmartGroupBot - это интеллектуальный бот для Telegram групп, который использует возможности GPT-3.5 для анализа контекста беседы и генерации релевантных ответов. Бот включает в себя веб-панель аналитики, систему управления базой данных и fallback-режим для работы без OpenAI.

### ✨ Основные возможности

- 🧠 **AI-анализ контекста** - использует GPT-3.5 для понимания темы и настроения беседы
- 📊 **Веб-аналитика** - красивая панель управления с графиками и статистикой
- 💾 **База данных** - SQLAlchemy для хранения истории и аналитики
- 🎯 **Умная частота ответов** - не спамит, отвечает только когда это уместно
- 🔄 **Fallback режим** - работает даже при исчерпании OpenAI квоты
- 🐳 **Docker поддержка** - легкий деплой с помощью Docker Compose
- 📱 **Адаптивный интерфейс** - веб-панель работает на всех устройствах

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.10+
- Telegram Bot Token (получить у [@BotFather](https://t.me/botfather))
- OpenAI API Key (опционально, для AI-режима)

### Установка

1. **Клонирование репозитория**
```bash
git clone https://github.com/your-username/smartgroupbot.git
cd smartgroupbot
```

2. **Создание виртуального окружения**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. **Установка зависимостей**
```bash
pip install -r requirements.txt
```

4. **Настройка конфигурации**
```bash
cp config.env.example config.env
# Отредактируйте config.env своими токенами
```

5. **Инициализация базы данных**
```bash
python models.py
```

6. **Запуск бота**
```bash
python main_bot.py
```

7. **Запуск веб-панели** (в отдельном терминале)
```bash
python web_dashboard.py
```

Откройте http://localhost:5001 для доступа к аналитике.

### 🐳 Запуск с Docker

```bash
# Настройте .env файл
cp config.env.example .env

# Запустите все сервисы
docker-compose up -d

# Просмотр логов
docker-compose logs -f bot
```

## 📖 Документация

### Архитектура системы

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram API  │────│   SmartGroupBot │────│   OpenAI API    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │
                               ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   SQLAlchemy    │────│   Web Dashboard │
                       │    Database     │    │   (Flask)       │
                       └─────────────────┘    └─────────────────┘
```

### Основные компоненты

#### 🤖 main_bot.py
Главный файл бота с обработкой сообщений и командами:
- `/start` - информация о боте
- `/help` - справка по командам
- `/stats` - статистика чата

#### 🧠 ai_service.py
AI-сервис для анализа контекста:
- Интеграция с OpenAI GPT-3.5
- Fallback режим с умными ответами
- Анализ настроения и тем

#### 💼 bot_service.py
Основная бизнес-логика:
- Буферизация сообщений
- Контроль частоты ответов
- Сохранение в базу данных

#### 🗄️ models.py
Модели базы данных:
- Таблица взаимодействий
- Менеджер базы данных
- Миграции

#### 🌐 web_dashboard.py
Веб-интерфейс аналитики:
- Графики Chart.js
- REST API endpoints
- Responsive дизайн

#### ⚙️ config.py
Конфигурация системы:
- Настройки бота
- API ключи
- Параметры базы данных

### Конфигурация

Основные параметры в `config.env`:

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
BOT_NAME=SmartGroupBot

# OpenAI (опционально)
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-3.5-turbo

# Настройки поведения
MIN_CONTEXT_MESSAGES=5         # Минимум сообщений для анализа
RESPONSE_FREQUENCY=5           # Частота ответов (раз в N сообщений)
MAX_CONTEXT_MESSAGES=10        # Максимум сообщений в контексте
MAX_RESPONSE_TOKENS=150        # Максимум токенов в ответе

# База данных
DATABASE_URL=sqlite:///bot_database.db

# Веб-панель
WEB_HOST=0.0.0.0
WEB_PORT=5001
```

## 🎯 Использование

### Добавление бота в группу

1. Найдите вашего бота в Telegram
2. Добавьте его в группу как администратора
3. Убедитесь, что у бота есть права:
   - Чтение сообщений
   - Отправка сообщений
   - Чтение истории

### Настройка приватности

**Важно!** Для работы в группах измените настройки приватности:

1. Напишите [@BotFather](https://t.me/botfather)
2. Выберите `/mybots` → ваш бот
3. `Bot Settings` → `Group Privacy` → `Turn OFF`

### Команды бота

- `/start` - Показать информацию о боте
- `/help` - Справка по использованию
- `/stats` - Статистика текущего чата (только для админов)

### Веб-панель

Откройте http://localhost:5001 для доступа к:

- 📊 **Общая статистика** - количество чатов, сообщений, ответов
- 📈 **Графики активности** - динамика по времени
- 💭 **Анализ настроений** - распределение эмоций
- 🔍 **Популярные темы** - самые обсуждаемые топики
- 💬 **История чатов** - детальная информация по каждому чату

## 🛠️ Разработка

### Структура проекта

```
smartgroupbot/
├── main_bot.py              # Главный файл бота
├── ai_service.py            # AI-сервис
├── bot_service.py           # Бизнес-логика
├── models.py                # Модели БД
├── config.py                # Конфигурация
├── web_dashboard.py         # Веб-панель
├── telegram_bot.py          # Telegram API обертки
├── requirements.txt         # Python зависимости
├── docker-compose.yml       # Docker конфигурация
├── Dockerfile               # Docker образ
├── config.env.example       # Пример конфигурации
├── templates/
│   └── dashboard.html       # HTML шаблон
└── docs/                    # Документация
    ├── installation.md
    ├── configuration.md
    └── api.md
```

### Расширение функциональности

#### Добавление новой команды

```python
async def my_command(self, update, context):
    """Моя новая команда"""
    await update.message.reply_text("Привет!")

# В main_bot.py добавить:
self.application.add_handler(CommandHandler("mycommand", self.my_command))
```

#### Создание нового AI-анализатора

```python
class MyAnalyzer:
    def analyze(self, messages):
        # Ваша логика
        return {"topic": "тема", "sentiment": 0.5}

# В ai_service.py добавить анализатор
```

#### Новые метрики для веб-панели

```python
# В web_dashboard.py добавить endpoint
@app.route('/api/my-metric')
def my_metric():
    # Вычисление метрики
    return jsonify({"value": 42})
```

### Тестирование

```bash
# Запуск тестов
python -m pytest tests/

# Тестирование бота
python main_bot.py  # В отдельном терминале
# Отправьте сообщения боту в Telegram
```

### Деплой

#### Production с Docker

```bash
# Настройка переменных окружения
export TELEGRAM_BOT_TOKEN="your_token"
export OPENAI_API_KEY="your_key"

# Сборка и запуск
docker-compose -f docker-compose.prod.yml up -d
```

#### VPS деплой

```bash
# На сервере
git clone https://github.com/your-username/smartgroupbot.git
cd smartgroupbot
pip install -r requirements.txt

# Настройка systemd service
sudo cp smartgroupbot.service /etc/systemd/system/
sudo systemctl enable smartgroupbot
sudo systemctl start smartgroupbot
```

## 📊 Аналитика и мониторинг

### Метрики

- **Активность чатов** - количество сообщений по времени
- **Частота ответов** - процент сообщений с ответами бота  
- **Анализ настроений** - распределение positive/neutral/negative
- **Популярные темы** - топ обсуждаемых тем
- **Производительность** - время ответа AI, нагрузка на API

### Логирование

Бот ведет детальные логи:
- 📩 Входящие сообщения
- 🧠 AI-анализ
- 📤 Отправленные ответы
- ❌ Ошибки и исключения

### Мониторинг

Веб-панель предоставляет real-time мониторинг:
- Статус бота (онлайн/офлайн)
- Последняя активность
- Использование OpenAI API
- Ошибки и предупреждения

## 🔒 Безопасность

- 🔐 Все токены в переменных окружения
- 🚫 Автоматическая фильтрация спама
- 🛡️ Валидация входных данных
- 📝 Аудит всех действий
- 🔄 Ротация API ключей

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📋 TODO

- [ ] Поддержка множественных языков
- [ ] Интеграция с Grafana для мониторинга
- [ ] Плагинная архитектура
- [ ] Machine Learning для улучшения ответов
- [ ] WebSocket для real-time обновлений
- [ ] Экспорт аналитики в Excel/PDF
- [ ] Интеграция с другими AI провайдерами

## 🐛 Известные проблемы

- При превышении лимита OpenAI API бот переключается на fallback режим
- Веб-панель требует перезагрузки для обновления данных
- Большие группы (1000+ участников) могут вызывать задержки

## 📞 Поддержка

- 📧 Email: support@smartgroupbot.com
- 💬 Telegram: [@smartgroupbot_support](https://t.me/smartgroupbot_support)
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/smartgroupbot/issues)
- 📚 Wiki: [GitHub Wiki](https://github.com/your-username/smartgroupbot/wiki)

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 🎉 Благодарности

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - отличная библиотека для Telegram
- [OpenAI](https://openai.com) - за предоставление GPT API
- [Flask](https://flask.palletsprojects.com/) - для веб-интерфейса
- [Chart.js](https://www.chartjs.org/) - для красивых графиков

---

**⭐ Поставьте звезду проекту, если он вам понравился!**

*Создано с ❤️ для Telegram сообществ* 