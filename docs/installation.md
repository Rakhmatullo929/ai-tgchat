# 📦 Руководство по установке SmartGroupBot

## 📋 Системные требования

- **Python:** 3.10 или выше
- **ОС:** Linux, macOS, Windows
- **RAM:** минимум 512MB, рекомендуется 1GB+
- **Дисковое пространство:** 100MB для проекта + данные базы
- **Интернет:** постоянное соединение для Telegram и OpenAI API

## 🛠️ Подготовка окружения

### Windows

```powershell
# Установка Python (если не установлен)
# Скачайте с https://python.org и установите

# Проверка версии
python --version

# Установка Git (если не установлен)
# Скачайте с https://git-scm.com
```

### macOS

```bash
# Установка Homebrew (если не установлен)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Установка Python
brew install python@3.10

# Установка Git
brew install git
```

### Ubuntu/Debian

```bash
# Обновление пакетов
sudo apt update

# Установка Python и pip
sudo apt install python3.10 python3.10-venv python3-pip git

# Установка дополнительных зависимостей
sudo apt install build-essential libssl-dev libffi-dev
```

### CentOS/RHEL

```bash
# Установка EPEL репозитория
sudo yum install epel-release

# Установка Python и Git
sudo yum install python3 python3-pip git

# Установка компилятора
sudo yum groupinstall "Development Tools"
```

## 🔧 Установка проекта

### 1. Клонирование репозитория

```bash
# Клонирование из GitHub
git clone https://github.com/your-username/smartgroupbot.git
cd smartgroupbot

# Или скачивание архива
curl -L https://github.com/your-username/smartgroupbot/archive/main.zip -o smartgroupbot.zip
unzip smartgroupbot.zip
cd smartgroupbot-main
```

### 2. Создание виртуального окружения

```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация (Linux/Mac)
source venv/bin/activate

# Активация (Windows)
venv\Scripts\activate

# Проверка активации
which python  # должен показать путь к venv/bin/python
```

### 3. Установка зависимостей

```bash
# Обновление pip
pip install --upgrade pip

# Установка зависимостей
pip install -r requirements.txt

# Проверка установки
pip list
```

## 🔑 Получение API ключей

### Telegram Bot Token

1. **Открыть Telegram** и найти [@BotFather](https://t.me/botfather)

2. **Создать нового бота:**
   ```
   /newbot
   ```

3. **Следовать инструкциям:**
   - Введите имя бота (например: "My Smart Group Bot")
   - Введите username (например: "mysmartgroupbot")

4. **Получить токен:**
   ```
   Use this token to access the HTTP API:
   1234567890:ABCdefGhIjKlMnOpQrStUvWxYz
   ```

5. **Настроить права бота:**
   ```
   /mybots → [Ваш бот] → Bot Settings → Group Privacy → Turn OFF
   ```

### OpenAI API Key (опционально)

1. **Зарегистрироваться** на [OpenAI](https://platform.openai.com)

2. **Создать API ключ:**
   - Перейти в [API Keys](https://platform.openai.com/api-keys)
   - Нажать "Create new secret key"
   - Скопировать ключ (показывается только один раз!)

3. **Пополнить баланс** (минимум $5)

## ⚙️ Конфигурация

### 1. Создание конфигурационного файла

```bash
# Копирование примера
cp config.env.example config.env

# Редактирование конфигурации
nano config.env  # или ваш любимый редактор
```

### 2. Заполнение конфигурации

```env
# =================================
# TELEGRAM BOT CONFIGURATION
# =================================
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGhIjKlMnOpQrStUvWxYz
BOT_NAME=SmartGroupBot
BOT_PERSONALITY=Дружелюбный и умный помощник в групповых чатах

# =================================
# OPENAI CONFIGURATION (OPTIONAL)
# =================================
OPENAI_API_KEY=sk-1234567890abcdef...
OPENAI_MODEL=gpt-3.5-turbo
MAX_RESPONSE_TOKENS=150

# =================================
# BOT BEHAVIOR SETTINGS
# =================================
RESPONSE_FREQUENCY=5           # Отвечать раз в N сообщений
MIN_CONTEXT_MESSAGES=5         # Минимум сообщений для анализа
MAX_CONTEXT_MESSAGES=10        # Максимум сообщений в контексте

# =================================
# DATABASE CONFIGURATION
# =================================
DATABASE_URL=sqlite:///bot_database.db

# =================================
# WEB DASHBOARD SETTINGS
# =================================
WEB_HOST=0.0.0.0
WEB_PORT=5001
WEB_DEBUG=false

# =================================
# LOGGING CONFIGURATION
# =================================
LOG_LEVEL=INFO
LOG_FILE_MAX_SIZE=10485760     # 10MB
LOG_FILE_BACKUP_COUNT=5
```

### 3. Инициализация базы данных

```bash
# Создание таблиц
python models.py

# Проверка создания базы
ls -la *.db  # должен появиться bot_database.db
```

## 🚀 Первый запуск

### 1. Запуск бота

```bash
# Активация виртуального окружения (если не активно)
source venv/bin/activate

# Запуск основного бота
python main_bot.py
```

**Ожидаемый вывод:**
```
2025-01-15 10:30:00 | INFO | SmartGroupBot инициализирован
2025-01-15 10:30:01 | INFO | 🤖 === ЗАПУСК SMARTGROUPBOT ===
2025-01-15 10:30:01 | INFO | 🤖 Бот @yourbotname готов!
2025-01-15 10:30:01 | INFO | 📖 Может читать все сообщения в группах: True
2025-01-15 10:30:01 | INFO | 🤖 === SMARTGROUPBOT АКТИВЕН ===
```

### 2. Запуск веб-панели (опционально)

В **новом терминале**:

```bash
# Переход в директорию проекта
cd smartgroupbot

# Активация виртуального окружения
source venv/bin/activate

# Запуск веб-панели
python web_dashboard.py
```

**Ожидаемый вывод:**
```
 * Running on http://0.0.0.0:5001
 * Debug mode: off
```

### 3. Проверка работы

1. **Найти бота в Telegram** по username
2. **Отправить команду** `/start`
3. **Получить ответ** от бота
4. **Добавить в группу** и протестировать
5. **Открыть веб-панель** http://localhost:5001

## 🔍 Диагностика проблем

### Проблема: "ModuleNotFoundError"

```bash
# Проверка активации виртуального окружения
which python
pip list

# Переустановка зависимостей
pip install -r requirements.txt --force-reinstall
```

### Проблема: "Unauthorized" при запуске бота

```bash
# Проверка токена
echo $TELEGRAM_BOT_TOKEN

# Проверка файла конфигурации
cat config.env | grep TELEGRAM_BOT_TOKEN

# Тест токена через curl
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"
```

### Проблема: "Permission denied" для базы данных

```bash
# Проверка прав доступа
ls -la *.db

# Установка правильных прав
chmod 644 bot_database.db
```

### Проблема: Веб-панель не открывается

```bash
# Проверка занятости порта
netstat -tlnp | grep 5001

# Использование другого порта
export WEB_PORT=5002
python web_dashboard.py
```

### Проблема: Бот не отвечает в группах

1. **Проверить права бота:**
   - `/mybots` → ваш бот → `Bot Settings` → `Group Privacy` → `Turn OFF`

2. **Проверить логи:**
   ```bash
   tail -f smart_bot.log
   ```

3. **Отправить несколько сообщений подряд** (минимум 5)

## 📦 Установка в production

### С помощью systemd (Linux)

1. **Создать сервисный файл:**
```bash
sudo nano /etc/systemd/system/smartgroupbot.service
```

```ini
[Unit]
Description=SmartGroupBot Telegram Bot
After=network.target

[Service]
Type=simple
User=bot
Group=bot
WorkingDirectory=/opt/smartgroupbot
ExecStart=/opt/smartgroupbot/venv/bin/python main_bot.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=/opt/smartgroupbot
EnvironmentFile=/opt/smartgroupbot/config.env

[Install]
WantedBy=multi-user.target
```

2. **Настроить и запустить:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable smartgroupbot
sudo systemctl start smartgroupbot
sudo systemctl status smartgroupbot
```

### С помощью supervisor

1. **Установить supervisor:**
```bash
sudo apt install supervisor
```

2. **Создать конфигурацию:**
```bash
sudo nano /etc/supervisor/conf.d/smartgroupbot.conf
```

```ini
[program:smartgroupbot]
command=/opt/smartgroupbot/venv/bin/python main_bot.py
directory=/opt/smartgroupbot
user=bot
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/smartgroupbot.log
```

3. **Перезапустить supervisor:**
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start smartgroupbot
```

## 🐳 Docker установка

### Быстрый старт

```bash
# Клонирование репозитория
git clone https://github.com/your-username/smartgroupbot.git
cd smartgroupbot

# Настройка переменных окружения
cp config.env.example .env
nano .env  # заполнить токены

# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f bot
```

### Ручная сборка

```bash
# Сборка образа
docker build -t smartgroupbot .

# Запуск контейнера
docker run -d \
  --name smartgroupbot \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  smartgroupbot
```

## 🔄 Обновление

### Из Git репозитория

```bash
# Остановка бота
sudo systemctl stop smartgroupbot

# Обновление кода
git pull origin main

# Установка новых зависимостей
source venv/bin/activate
pip install -r requirements.txt

# Обновление базы данных (если есть миграции)
python models.py

# Запуск бота
sudo systemctl start smartgroupbot
```

### Docker обновление

```bash
# Остановка и удаление контейнеров
docker-compose down

# Обновление образов
docker-compose pull

# Запуск обновленной версии
docker-compose up -d
```

## 🆘 Получение помощи

При возникновении проблем:

1. **Проверить логи:**
   ```bash
   tail -f smart_bot.log
   journalctl -u smartgroupbot -f
   ```

2. **Проверить статус:**
   ```bash
   systemctl status smartgroupbot
   docker-compose ps
   ```

3. **Обратиться за помощью:**
   - [GitHub Issues](https://github.com/your-username/smartgroupbot/issues)
   - [Telegram поддержка](https://t.me/smartgroupbot_support)
   - [Discord сервер](https://discord.gg/smartgroupbot)

---

✅ **Поздравляем! SmartGroupBot успешно установлен и готов к работе!** 