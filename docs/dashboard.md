# 📈 Веб-панель SmartGroupBot

Подробное руководство по использованию веб-панели SmartGroupBot для мониторинга и управления.

## 🌐 Обзор

Веб-панель SmartGroupBot предоставляет интуитивный интерфейс для:
- 📊 Мониторинга аналитики в реальном времени
- 🎛️ Управления настройками бота
- 📈 Просмотра детальной статистики
- 🔍 Анализа взаимодействий
- 📤 Экспорта данных

**Доступ:** http://localhost:5001 (по умолчанию)

## 🚀 Быстрый старт

### Запуск панели
```bash
# Панель запускается автоматически с ботом
python main_bot.py

# Или отдельно
python web_dashboard.py
```

### Первый вход
1. **Откройте браузер:** http://localhost:5001
2. **Главная страница:** Общая статистика и навигация
3. **Навигация:** Используйте меню для перехода между разделами

## 📱 Интерфейс панели

### 🏠 Главная страница

```
┌─────────────────────────────────────────────────────────┐
│                SmartGroupBot Dashboard                  │
├─────────────────────────────────────────────────────────┤
│  📊 Статистика     🎛️ Настройки     📤 Экспорт        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📈 Активность за 24 часа                             │
│  ┌─────────────────────────────────────────────────┐   │
│  │     📊 График активности                        │   │
│  │                                                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  🏷️ Популярные темы        📭 Настроения              │
│  ┌─────────────────┐      ┌─────────────────────────┐   │
│  │ 1. общение      │      │ 😊 Позитив: 65%       │   │
│  │ 2. работа       │      │ 😐 Нейтрал: 28%       │   │
│  │ 3. погода       │      │ 😔 Негатив: 7%        │   │
│  └─────────────────┘      └─────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Ключевые показатели (KPI)
- **📊 Общие взаимодействия:** Количество обработанных сообщений
- **🤖 Ответы бота:** Количество и процент ответов
- **👥 Активные чаты:** Число активных групп
- **⚡ Среднее время ответа:** Производительность системы

---

## 📊 Раздел аналитики

### 📈 Графики и метрики

#### График активности
```javascript
// Интерактивный график с помощью Chart.js
{
  type: 'line',
  data: {
    labels: ['00:00', '01:00', '02:00', ...],
    datasets: [{
      label: 'Сообщения',
      data: [12, 19, 3, 5, 2, 3],
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1
    }]
  },
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Активность чатов за 24 часа'
      }
    }
  }
}
```

#### Круговая диаграмма настроений
- **😊 Позитивные:** Зелёный цвет
- **😐 Нейтральные:** Жёлтый цвет  
- **😔 Негативные:** Красный цвет

#### Тепловая карта активности
```
      Пн  Вт  Ср  Чт  Пт  Сб  Вс
00-06 ░░  ░░  ░░  ░░  ░░  ░░  ░░
06-12 ██  ██  ██  ██  ██  ░░  ░░
12-18 ███ ███ ███ ███ ███ ██  ██
18-24 ██  ██  ██  ██  ░░  ███ ███
```

### 📋 Детальная статистика

#### По чатам
```
┌─────────────────────────────────────────────────────┐
│ Название чата        │ Сообщений │ Ответов │ Sentiment │
├─────────────────────────────────────────────────────┤
│ 💼 Рабочий чат       │    156    │   24   │   0.68   │
│ 🎮 Игровая группа    │     89    │   15   │   0.75   │
│ 📚 Обучение Python   │     67    │   12   │   0.62   │
│ 🏠 Семейный чат      │     34    │    6   │   0.82   │
└─────────────────────────────────────────────────────┘
```

#### По темам
```
┌─────────────────────────────────────────────────────┐
│ Тема               │ Упоминания │ Sentiment │ Тренд   │
├─────────────────────────────────────────────────────┤
│ 💼 Работа          │     89     │   0.45   │   ↗️    │
│ 🎮 Развлечения     │     67     │   0.82   │   ↗️    │
│ 📚 Образование     │     45     │   0.68   │   →     │
│ 🏠 Быт            │     34     │   0.55   │   ↘️    │
└─────────────────────────────────────────────────────┘
```

---

## 🎛️ Настройки

### ⚙️ Общие настройки бота

```html
<!-- Интерфейс настроек -->
<div class="settings-panel">
  <h3>🤖 Поведение бота</h3>
  
  <div class="setting-item">
    <label>Частота ответов (раз в N сообщений):</label>
    <input type="range" min="1" max="20" value="5" id="frequency">
    <span id="frequency-value">5</span>
  </div>
  
  <div class="setting-item">
    <label>Минимум сообщений для анализа:</label>
    <input type="number" min="2" max="10" value="5" id="min-context">
  </div>
  
  <div class="setting-item">
    <label>Личность бота:</label>
    <select id="personality">
      <option value="friendly">Дружелюбный помощник</option>
      <option value="professional">Профессиональный</option>
      <option value="funny">Весёлый собеседник</option>
      <option value="wise">Мудрый наставник</option>
    </select>
  </div>
  
  <button onclick="saveSettings()" class="btn-primary">
    💾 Сохранить настройки
  </button>
</div>
```

### 🔧 Технические настройки

#### База данных
- **URL подключения:** Изменение database_url
- **Время жизни данных:** Автоочистка старых записей
- **Резервное копирование:** Настройка backup'ов

#### Логирование
- **Уровень логов:** DEBUG, INFO, WARNING, ERROR
- **Ротация файлов:** Размер и количество файлов
- **Фильтры:** По модулям и типам событий

#### API настройки
- **OpenAI ключ:** Безопасное обновление
- **Rate limiting:** Лимиты запросов
- **Timeout'ы:** Время ожидания ответов

---

## 📊 REST API

### 🔌 Основные endpoints

#### Получение статистики
```bash
# Общая статистика
GET /api/stats
{
  "total_interactions": 1247,
  "bot_responses": 183,
  "active_chats": 12,
  "avg_sentiment": 0.65,
  "response_rate": 14.7
}

# Статистика по чатам
GET /api/chats
[
  {
    "chat_id": "-1001234567890",
    "chat_title": "Рабочий чат",
    "messages_count": 156,
    "responses_count": 24,
    "avg_sentiment": 0.68,
    "last_activity": "2025-01-15T14:30:00Z"
  }
]
```

#### Получение взаимодействий
```bash
# Последние взаимодействия
GET /api/interactions?limit=50&offset=0
{
  "total": 1247,
  "interactions": [
    {
      "id": 1247,
      "timestamp": "2025-01-15T14:30:00Z",
      "chat_id": "-1001234567890",
      "chat_title": "Рабочий чат",
      "context_messages": ["Привет всем!", "Как дела?"],
      "detected_topic": "приветствие",
      "sentiment": 0.8,
      "bot_response": "Привет! Как дела? 👋",
      "response_generated": true
    }
  ]
}

# Фильтрация по чату
GET /api/interactions?chat_id=-1001234567890

# Фильтрация по времени
GET /api/interactions?start_date=2025-01-15&end_date=2025-01-16
```

#### Аналитика настроений
```bash
GET /api/analytics/sentiment
{
  "overall": {
    "positive": 0.65,
    "neutral": 0.28,
    "negative": 0.07
  },
  "by_chat": {
    "-1001234567890": {
      "positive": 0.68,
      "neutral": 0.25,
      "negative": 0.07
    }
  },
  "timeline": [
    {
      "date": "2025-01-15",
      "avg_sentiment": 0.65
    }
  ]
}
```

#### Управление ботом
```bash
# Симуляция сообщения
POST /api/chat/-1001234567890/simulate
{
  "message": "Привет всем!",
  "user": "TestUser"
}

# Получение настроек
GET /api/settings
{
  "response_frequency": 5,
  "min_context_messages": 5,
  "bot_personality": "Дружелюбный помощник",
  "ai_mode": "fallback"
}

# Обновление настроек
PUT /api/settings
{
  "response_frequency": 3,
  "min_context_messages": 3
}
```

---

## 📤 Экспорт данных

### 📋 Форматы экспорта

#### JSON Export
```json
{
  "export_info": {
    "timestamp": "2025-01-15T14:30:00Z",
    "total_records": 1247,
    "date_range": {
      "start": "2025-01-01T00:00:00Z",
      "end": "2025-01-15T23:59:59Z"
    }
  },
  "interactions": [
    {
      "id": 1,
      "timestamp": "2025-01-01T10:30:00Z",
      "chat_id": "-1001234567890",
      "chat_title": "Рабочий чат",
      "context_messages": ["Привет!", "Как дела?"],
      "detected_topic": "приветствие",
      "sentiment": 0.8,
      "bot_response": "Привет! 👋",
      "response_generated": true,
      "participants_count": 12
    }
  ],
  "analytics": {
    "total_messages": 1247,
    "bot_responses": 183,
    "avg_sentiment": 0.65,
    "popular_topics": [
      {"topic": "общение", "count": 89},
      {"topic": "работа", "count": 67}
    ]
  }
}
```

#### CSV Export
```csv
id,timestamp,chat_id,chat_title,topic,sentiment,response_generated,bot_response
1,2025-01-01T10:30:00Z,-1001234567890,Рабочий чат,приветствие,0.8,true,"Привет! 👋"
2,2025-01-01T10:35:00Z,-1001234567890,Рабочий чат,работа,0.6,false,
```

#### PDF Report
- 📊 Графики и диаграммы
- 📋 Таблицы с данными
- 📈 Аналитические выводы
- 📅 Временные тренды

### 🎯 Настройки экспорта

```html
<div class="export-settings">
  <h3>📤 Настройки экспорта</h3>
  
  <div class="date-range">
    <label>📅 Период:</label>
    <input type="date" id="start-date">
    <input type="date" id="end-date">
  </div>
  
  <div class="format-selection">
    <label>📄 Формат:</label>
    <select id="export-format">
      <option value="json">JSON (подробный)</option>
      <option value="csv">CSV (таблица)</option>
      <option value="pdf">PDF (отчёт)</option>
    </select>
  </div>
  
  <div class="data-selection">
    <label>📊 Данные:</label>
    <input type="checkbox" id="include-messages" checked>
    <label for="include-messages">Сообщения</label>
    
    <input type="checkbox" id="include-analytics" checked>
    <label for="include-analytics">Аналитика</label>
    
    <input type="checkbox" id="include-settings">
    <label for="include-settings">Настройки</label>
  </div>
  
  <button onclick="exportData()" class="btn-export">
    📤 Экспортировать данные
  </button>
</div>
```

---

## 🔍 Поиск и фильтрация

### 🎯 Фильтры данных

#### По времени
- **Последний час:** Данные за последние 60 минут
- **Сегодня:** Данные с начала дня
- **Неделя:** Последние 7 дней
- **Месяц:** Последние 30 дней
- **Произвольный период:** Выбор дат

#### По чатам
```html
<select id="chat-filter" multiple>
  <option value="-1001234567890">💼 Рабочий чат</option>
  <option value="-1001234567891">🎮 Игровая группа</option>
  <option value="-1001234567892">📚 Обучение Python</option>
</select>
```

#### По темам
- **🏷️ Конкретная тема:** Фильтр по detected_topic
- **📊 Диапазон sentiment:** От негативного до позитивного
- **🤖 Тип ответа:** С ответом бота / без ответа

### 🔍 Поиск

```html
<div class="search-panel">
  <input type="text" 
         placeholder="🔍 Поиск по тексту сообщений..." 
         id="search-input">
  
  <div class="search-filters">
    <select id="search-field">
      <option value="all">Везде</option>
      <option value="messages">В сообщениях</option>
      <option value="responses">В ответах бота</option>
      <option value="topics">В темах</option>
    </select>
    
    <button onclick="search()" class="btn-search">
      🔍 Найти
    </button>
  </div>
</div>
```

---

## 📱 Мобильная версия

### 📱 Адаптивный дизайн

Веб-панель полностью адаптирована для мобильных устройств:

```css
/* Мобильная адаптация */
@media (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-container {
    height: 250px;
  }
  
  .stats-cards {
    flex-direction: column;
  }
}
```

### 🔄 Offline режим

- **Service Worker:** Кэширование для offline доступа
- **Локальное хранение:** Сохранение последних данных
- **Синхронизация:** Обновление при восстановлении связи

---

## ⚡ Производительность

### 🚀 Оптимизации

#### Фронтенд
- **Lazy loading:** Загрузка данных по требованию
- **Виртуализация:** Для больших таблиц
- **Кэширование:** Статических ресурсов
- **Сжатие:** Gzip для API ответов

#### Бэкенд
- **Database indexing:** Оптимизация запросов
- **Connection pooling:** Пул соединений с БД
- **Caching:** Redis для часто запрашиваемых данных
- **Pagination:** Постраничная выгрузка

### 📊 Метрики производительности

```javascript
// Мониторинг производительности
window.performance.mark('dashboard-start');
// ... загрузка данных ...
window.performance.mark('dashboard-end');

window.performance.measure(
  'dashboard-load',
  'dashboard-start',
  'dashboard-end'
);
```

---

## 🔒 Безопасность

### 🛡️ Защита данных

#### Аутентификация
```python
# Middleware для проверки доступа
@app.before_request
def check_access():
    # Проверка IP адреса
    if request.remote_addr not in allowed_ips:
        abort(403)
    
    # Проверка токена (опционально)
    token = request.headers.get('Authorization')
    if not verify_token(token):
        abort(401)
```

#### CORS настройки
```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

#### Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per hour"]
)

@app.route('/api/stats')
@limiter.limit("10 per minute")
def get_stats():
    # ...
```

---

## 🆘 Устранение проблем

### 🔧 Частые проблемы

#### Панель не загружается
```bash
# Проверка статуса веб-сервера
curl http://localhost:5001/health

# Проверка логов
tail -f smart_bot.log | grep "Flask"

# Проверка конфигурации
python -c "from config import config; print(f'Web: {config.web_host}:{config.web_port}')"
```

#### Нет данных в графиках
- **Проверить БД:** `SELECT COUNT(*) FROM chat_interactions;`
- **Проверить фильтры:** Убедиться в корректности временного диапазона
- **Обновить страницу:** Ctrl+F5 для принудительного обновления

#### Медленная загрузка
- **Проверить размер БД:** Большие таблицы замедляют запросы
- **Очистить кэш браузера:** Устаревшие данные
- **Проверить сеть:** Ping до сервера

### 📞 Получение помощи

- **🔧 Техподдержка:** [@smartgroupbot_support](https://t.me/smartgroupbot_support)
- **📚 Документация:** http://localhost:5001/docs
- **🐛 Баг-репорты:** [GitHub Issues](https://github.com/your-username/smartgroupbot/issues)

---

**🔄 Веб-панель обновляется в реальном времени. Последнее обновление: 15.01.2025** 