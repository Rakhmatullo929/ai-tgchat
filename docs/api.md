# 🔌 API Документация SmartGroupBot

## 📊 Web Dashboard API

Веб-панель предоставляет REST API для получения аналитических данных.

**Base URL:** `http://localhost:5001`

### 🔐 Аутентификация

В текущей версии API не требует аутентификации. В production рекомендуется добавить API ключи.

---

## 📈 Endpoints

### GET `/api/stats`

Получить общую статистику по всем чатам.

**Пример запроса:**
```bash
curl http://localhost:5001/api/stats
```

**Ответ:**
```json
{
  "total_chats": 5,
  "total_interactions": 147,
  "total_responses": 23,
  "response_rate": 15.6,
  "avg_sentiment": 0.65,
  "active_chats_today": 3,
  "last_activity": "2025-01-15T14:30:00Z"
}
```

**Поля ответа:**
- `total_chats` - общее количество чатов
- `total_interactions` - общее количество взаимодействий
- `total_responses` - количество ответов бота
- `response_rate` - процент ответов (responses/interactions * 100)
- `avg_sentiment` - средний sentiment (-1 до 1)
- `active_chats_today` - активные чаты сегодня
- `last_activity` - время последней активности

---

### GET `/api/chats`

Получить список всех чатов с базовой информацией.

**Пример запроса:**
```bash
curl http://localhost:5001/api/chats
```

**Ответ:**
```json
{
  "chats": [
    {
      "chat_id": "-1001234567890",
      "chat_title": "Тестовая группа",
      "total_interactions": 45,
      "total_responses": 8,
      "response_rate": 17.8,
      "avg_sentiment": 0.7,
      "last_activity": "2025-01-15T14:25:00Z",
      "participants_count": 12
    }
  ],
  "count": 1
}
```

---

### GET `/api/chat/{chat_id}`

Получить детальную информацию по конкретному чату.

**Параметры:**
- `chat_id` - ID чата (например: `-1001234567890`)

**Пример запроса:**
```bash
curl http://localhost:5001/api/chat/-1001234567890
```

**Ответ:**
```json
{
  "chat_id": "-1001234567890",
  "chat_title": "Тестовая группа",
  "stats": {
    "total_interactions": 45,
    "total_responses": 8,
    "response_rate": 17.8,
    "avg_sentiment": 0.7,
    "participants_count": 12
  },
  "sentiment_distribution": {
    "positive": 25,
    "neutral": 15,
    "negative": 5
  },
  "popular_topics": [
    {"topic": "общение", "count": 15},
    {"topic": "погода", "count": 8},
    {"topic": "работа", "count": 5}
  ],
  "recent_interactions": [
    {
      "timestamp": "2025-01-15T14:25:00Z",
      "detected_topic": "общение",
      "sentiment": 0.8,
      "bot_response": "Привет! Как дела?",
      "response_generated": true
    }
  ]
}
```

---

### GET `/api/interactions`

Получить последние взаимодействия со всех чатов.

**Query параметры:**
- `limit` - количество записей (по умолчанию: 50, максимум: 200)
- `offset` - смещение для пагинации (по умолчанию: 0)
- `chat_id` - фильтр по чату (опционально)

**Пример запроса:**
```bash
curl "http://localhost:5001/api/interactions?limit=10&offset=0"
```

**Ответ:**
```json
{
  "interactions": [
    {
      "id": 123,
      "timestamp": "2025-01-15T14:25:00Z",
      "chat_id": "-1001234567890",
      "chat_title": "Тестовая группа",
      "context_messages": [
        "Привет всем!",
        "Как дела?",
        "Что планируете на выходные?"
      ],
      "detected_topic": "общение",
      "sentiment": 0.8,
      "bot_response": "Привет! У меня все отлично! А у вас как настроение? 😊",
      "response_generated": true,
      "participants_count": 12
    }
  ],
  "total": 147,
  "limit": 10,
  "offset": 0
}
```

---

### GET `/api/analytics/sentiment`

Получить аналитику по sentiment'у за период.

**Query параметры:**
- `period` - период (day, week, month) по умолчанию: week
- `chat_id` - фильтр по чату (опционально)

**Пример запроса:**
```bash
curl "http://localhost:5001/api/analytics/sentiment?period=week"
```

**Ответ:**
```json
{
  "period": "week",
  "data": [
    {
      "date": "2025-01-09",
      "positive": 12,
      "neutral": 8,
      "negative": 2
    },
    {
      "date": "2025-01-10",
      "positive": 15,
      "neutral": 10,
      "negative": 1
    }
  ],
  "summary": {
    "total_positive": 85,
    "total_neutral": 45,
    "total_negative": 12,
    "avg_sentiment": 0.68
  }
}
```

---

### GET `/api/analytics/activity`

Получить аналитику активности по времени.

**Query параметры:**
- `period` - период (hour, day, week) по умолчанию: day
- `chat_id` - фильтр по чату (опционально)

**Пример запроса:**
```bash
curl "http://localhost:5001/api/analytics/activity?period=day"
```

**Ответ:**
```json
{
  "period": "day",
  "data": [
    {
      "time": "2025-01-15T10:00:00Z",
      "interactions": 5,
      "responses": 1
    },
    {
      "time": "2025-01-15T11:00:00Z",
      "interactions": 8,
      "responses": 2
    }
  ],
  "summary": {
    "total_interactions": 147,
    "total_responses": 23,
    "peak_hour": "14:00",
    "peak_interactions": 15
  }
}
```

---

### GET `/api/analytics/topics`

Получить топ популярных тем.

**Query параметры:**
- `limit` - количество тем (по умолчанию: 10)
- `period` - период (week, month, all) по умолчанию: all
- `chat_id` - фильтр по чату (опционально)

**Пример запроса:**
```bash
curl "http://localhost:5001/api/analytics/topics?limit=5"
```

**Ответ:**
```json
{
  "topics": [
    {
      "topic": "общение",
      "count": 45,
      "percentage": 30.6,
      "avg_sentiment": 0.7
    },
    {
      "topic": "работа",
      "count": 23,
      "percentage": 15.6,
      "avg_sentiment": 0.2
    }
  ],
  "total_topics": 25,
  "period": "all"
}
```

---

### POST `/api/chat/{chat_id}/simulate`

Симулировать сообщение в чате (для тестирования).

**Параметры:**
- `chat_id` - ID чата

**Body:**
```json
{
  "message": "Привет, как дела?",
  "username": "testuser"
}
```

**Пример запроса:**
```bash
curl -X POST http://localhost:5001/api/chat/-1001234567890/simulate \
  -H "Content-Type: application/json" \
  -d '{"message": "Привет, как дела?", "username": "testuser"}'
```

**Ответ:**
```json
{
  "success": true,
  "bot_response": "Привет! У меня все отлично! А у тебя как настроение? 😊",
  "analysis": {
    "detected_topic": "приветствие",
    "sentiment": 0.8,
    "should_respond": true
  }
}
```

---

## 🤖 Bot Service API

Внутренние методы для взаимодействия с ботом.

### `BotService.process_message()`

Основной метод обработки сообщений.

**Параметры:**
```python
async def process_message(
    chat_id: str,
    chat_title: str, 
    message_text: str,
    user_id: str = None,
    username: str = None
) -> Optional[str]
```

**Возвращает:**
- `str` - ответ бота (если нужен)
- `None` - если отвечать не нужно

### `AIService.analyze_context_and_generate_response()`

Анализ контекста с помощью AI.

**Параметры:**
```python
async def analyze_context_and_generate_response(
    context_messages: List[str],
    chat_title: str = None
) -> Dict
```

**Возвращает:**
```python
{
    "detected_topic": str,      # Тема разговора
    "sentiment": float,         # Sentiment от -1 до 1
    "should_respond": bool,     # Стоит ли отвечать
    "response": str             # Ответ бота (если should_respond=True)
}
```

---

## 📝 Webhook Integration

Для интеграции с внешними системами можно использовать webhooks.

### Настройка Webhook

Добавьте в `config.env`:
```env
WEBHOOK_URL=https://your-domain.com/webhook
WEBHOOK_SECRET=your_secret_key
```

### Webhook Payload

При каждом взаимодействии отправляется POST запрос:

```json
{
  "event": "interaction",
  "timestamp": "2025-01-15T14:25:00Z",
  "data": {
    "chat_id": "-1001234567890",
    "chat_title": "Тестовая группа",
    "message_text": "Привет всем!",
    "detected_topic": "приветствие",
    "sentiment": 0.8,
    "bot_response": "Привет! Как дела?",
    "response_generated": true
  },
  "signature": "sha256=..."
}
```

---

## 🔧 Custom Extensions

### Создание собственного анализатора

```python
class CustomAnalyzer:
    def __init__(self):
        pass
    
    async def analyze(self, messages: List[str]) -> Dict:
        # Ваша логика анализа
        return {
            "detected_topic": "custom_topic",
            "sentiment": 0.5,
            "should_respond": True,
            "response": "Custom response"
        }

# Регистрация анализатора
from ai_service import ai_service
ai_service.add_analyzer("custom", CustomAnalyzer())
```

### Добавление новой команды

```python
async def custom_command(update, context):
    """Кастомная команда"""
    await update.message.reply_text("Кастомный ответ!")

# В main_bot.py
self.application.add_handler(CommandHandler("custom", custom_command))
```

### Создание middleware

```python
class LoggingMiddleware:
    async def process_message(self, message, next_handler):
        # Логирование до обработки
        print(f"Processing: {message.text}")
        
        # Вызов следующего обработчика
        result = await next_handler(message)
        
        # Логирование после обработки
        print(f"Result: {result}")
        
        return result
```

---

## 🐛 Error Handling

### HTTP Status Codes

- `200` - Успешный запрос
- `400` - Некорректные параметры запроса
- `404` - Ресурс не найден
- `429` - Превышение лимита запросов
- `500` - Внутренняя ошибка сервера

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_CHAT_ID",
    "message": "Chat ID must be a valid string",
    "details": {
      "provided": 123,
      "expected": "string"
    }
  },
  "timestamp": "2025-01-15T14:25:00Z",
  "request_id": "req_123456"
}
```

---

## 📚 SDK Examples

### Python SDK

```python
import requests

class SmartGroupBotAPI:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
    
    def get_stats(self):
        response = requests.get(f"{self.base_url}/api/stats")
        return response.json()
    
    def get_chat_info(self, chat_id):
        response = requests.get(f"{self.base_url}/api/chat/{chat_id}")
        return response.json()
    
    def simulate_message(self, chat_id, message, username):
        data = {"message": message, "username": username}
        response = requests.post(
            f"{self.base_url}/api/chat/{chat_id}/simulate",
            json=data
        )
        return response.json()

# Использование
api = SmartGroupBotAPI()
stats = api.get_stats()
print(f"Total chats: {stats['total_chats']}")
```

### JavaScript SDK

```javascript
class SmartGroupBotAPI {
    constructor(baseUrl = 'http://localhost:5001') {
        this.baseUrl = baseUrl;
    }
    
    async getStats() {
        const response = await fetch(`${this.baseUrl}/api/stats`);
        return response.json();
    }
    
    async getChatInfo(chatId) {
        const response = await fetch(`${this.baseUrl}/api/chat/${chatId}`);
        return response.json();
    }
    
    async simulateMessage(chatId, message, username) {
        const response = await fetch(`${this.baseUrl}/api/chat/${chatId}/simulate`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message, username})
        });
        return response.json();
    }
}

// Использование
const api = new SmartGroupBotAPI();
api.getStats().then(stats => {
    console.log(`Total chats: ${stats.total_chats}`);
});
```

---

## 🔒 Security Best Practices

1. **API Keys**: Используйте API ключи в production
2. **Rate Limiting**: Ограничивайте количество запросов
3. **Input Validation**: Валидируйте все входные данные
4. **HTTPS**: Используйте HTTPS в production
5. **CORS**: Настройте CORS для веб-интерфейса

---

## 📊 Rate Limits

- **Dashboard API**: 100 запросов в минуту
- **Analytics API**: 50 запросов в минуту  
- **Simulation API**: 10 запросов в минуту

При превышении лимита возвращается HTTP 429.

---

## 🔄 Versioning

API использует семантическое версионирование. Текущая версия: `v1.0.0`

Для доступа к конкретной версии используйте:
```
/api/v1/stats
```

---

**📞 Поддержка API:** [api-support@smartgroupbot.com](mailto:api-support@smartgroupbot.com) 