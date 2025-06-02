# 🔍 Мониторинг SmartGroupBot

Комплексное руководство по мониторингу, логированию и диагностике SmartGroupBot.

## 📋 Обзор мониторинга

SmartGroupBot предоставляет многоуровневую систему мониторинга:
- 📊 **Логирование** - Детальные логи всех операций
- 📈 **Метрики** - Производительность и статистика
- 🚨 **Алерты** - Уведомления о проблемах
- 📱 **Дашборд** - Визуальный мониторинг
- 🔧 **Диагностика** - Инструменты для отладки

## 📊 Система логирования

### 🔧 Конфигурация логов

```python
# config.py - настройки логирования
LOG_LEVEL = "INFO"                    # DEBUG, INFO, WARNING, ERROR
LOG_FILE_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_FILE_BACKUP_COUNT = 5             # Количество backup файлов
LOG_FORMAT = "detailed"               # simple, detailed, json
```

### 📝 Структура логов

```
logs/
├── smart_bot.log           # Основные логи
├── smart_bot.log.1         # Архив логов
├── smart_bot.log.2
├── error.log              # Только ошибки
├── telegram_api.log       # Логи Telegram API
├── database.log           # Логи базы данных
└── web_dashboard.log      # Логи веб-панели
```

### 🎯 Уровни логирования

#### DEBUG - Детальная отладка
```python
2025-01-15 14:30:15.123 | DEBUG    | ai_service:analyze_context:45 - 
🧠 Анализируем 5 сообщений: ['Привет', 'Как дела?', ...]

2025-01-15 14:30:15.124 | DEBUG    | ai_service:_get_fallback_response:78 - 
💡 Детекция приветствия: last_message='привет всем!'

2025-01-15 14:30:15.125 | DEBUG    | bot_service:add_message_to_context:156 - 
📝 Добавлено в буфер чата -1001234567890: "Привет всем!" (размер буфера: 6)
```

#### INFO - Общая информация
```python
2025-01-15 14:30:15.126 | INFO     | main_bot:handle_message:89 - 
📨 Получено сообщение в чате "Тестовая группа" (-1001234567890)

2025-01-15 14:30:15.140 | INFO     | ai_service:analyze_context_and_generate_response:123 - 
✅ AI результат: {'detected_topic': 'приветствие', 'sentiment': 0.8, 'should_respond': True}

2025-01-15 14:30:15.145 | INFO     | telegram_bot:send_message:67 - 
📤 Отправлено сообщение в чат -1001234567890: "Привет! Как дела? 👋"
```

#### WARNING - Предупреждения
```python
2025-01-15 14:30:15.200 | WARNING  | ai_service:analyze_context_and_generate_response:98 - 
⚠️ Не удалось распарсить JSON от OpenAI, используем fallback

2025-01-15 14:30:15.201 | WARNING  | telegram_bot:send_message:75 - 
⚠️ Rate limit warning: слишком много запросов, ждём 1 секунду

2025-01-15 14:30:15.202 | WARNING  | models:save_interaction:234 - 
⚠️ Большой размер контекста (15 сообщений), обрезаем до 10
```

#### ERROR - Ошибки
```python
2025-01-15 14:30:15.300 | ERROR    | ai_service:analyze_context_and_generate_response:104 - 
❌ Ошибка OpenAI API: RateLimitError('Rate limit exceeded')

2025-01-15 14:30:15.301 | ERROR    | telegram_bot:send_message:82 - 
❌ Ошибка отправки сообщения: HTTPError('Chat not found')

2025-01-15 14:30:15.302 | ERROR    | models:save_interaction:245 - 
❌ Ошибка сохранения в БД: IntegrityError('UNIQUE constraint failed')
```

## 📊 Метрики и аналитика

### 🎯 Ключевые метрики (KPI)

#### Производительность
```python
# Время ответа системы
response_time_metrics = {
    "ai_analysis_time": "среднее время анализа AI",
    "db_save_time": "время сохранения в БД", 
    "telegram_api_time": "время API Telegram",
    "total_processing_time": "общее время обработки"
}

# Пример логирования метрик
2025-01-15 14:30:15.400 | INFO | metrics:track_performance:12 - 
📊 Метрики производительности: ai_analysis=0.15s, db_save=0.02s, telegram_api=0.08s, total=0.25s
```

#### Использование ресурсов
```python
# Мониторинг памяти и CPU
system_metrics = {
    "memory_usage": "текущее использование памяти",
    "memory_peak": "пиковое использование памяти",
    "cpu_usage": "загрузка процессора",
    "open_connections": "количество открытых соединений"
}

# Пример
2025-01-15 14:30:15.500 | INFO | metrics:system_stats:25 - 
🖥️ Система: память=142MB/512MB (27.7%), CPU=15%, соединения=3
```

#### Бизнес метрики
```python
business_metrics = {
    "messages_processed": "обработано сообщений",
    "responses_generated": "сгенерировано ответов", 
    "response_rate": "процент ответов",
    "active_chats": "активных чатов",
    "avg_sentiment": "средний sentiment",
    "popular_topics": "популярные темы"
}

# Пример
2025-01-15 14:30:15.600 | INFO | metrics:business_stats:38 - 
📈 Бизнес метрики: сообщений=1247, ответов=183 (14.7%), чатов=12, sentiment=0.65
```

### 📈 Сбор метрик

#### Автоматический сбор
```python
# metrics.py
import time
import psutil
from functools import wraps
from loguru import logger

class MetricsCollector:
    def __init__(self):
        self.metrics = {}
        self.start_time = time.time()
    
    def track_performance(self, operation_name):
        """Декоратор для отслеживания производительности"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    end_time = time.time()
                    
                    # Записываем метрику
                    duration = end_time - start_time
                    self.record_metric(f"{operation_name}_time", duration)
                    
                    if duration > 1.0:  # Медленная операция
                        logger.warning(f"⏱️ Медленная операция {operation_name}: {duration:.2f}s")
                    
                    return result
                except Exception as e:
                    # Записываем ошибку
                    self.record_metric(f"{operation_name}_errors", 1)
                    logger.error(f"❌ Ошибка в {operation_name}: {e}")
                    raise
            return wrapper
        return decorator
    
    def record_metric(self, name, value):
        """Записать метрику"""
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append({
            "timestamp": time.time(),
            "value": value
        })
        
        # Ограничиваем размер истории
        if len(self.metrics[name]) > 1000:
            self.metrics[name] = self.metrics[name][-500:]
    
    def get_system_stats(self):
        """Получить системную статистику"""
        process = psutil.Process()
        
        stats = {
            "memory_mb": process.memory_info().rss / 1024 / 1024,
            "cpu_percent": process.cpu_percent(),
            "uptime_hours": (time.time() - self.start_time) / 3600,
            "threads": process.num_threads(),
            "open_files": len(process.open_files())
        }
        
        logger.info(f"🖥️ Системная статистика: {stats}")
        return stats

# Глобальный экземпляр
metrics = MetricsCollector()

# Использование декоратора
@metrics.track_performance("ai_analysis")
async def analyze_context_and_generate_response(self, context_messages):
    # Код анализа...
    pass
```

#### Ручной сбор метрик
```python
# В коде приложения
from metrics import metrics

# Увеличение счётчика
metrics.record_metric("messages_received", 1)

# Запись времени
start_time = time.time()
# ... операция ...
metrics.record_metric("operation_duration", time.time() - start_time)

# Запись значения
metrics.record_metric("chat_participants", participants_count)
```

## 🚨 Система алертов

### ⚠️ Настройка алертов

```python
# alerts.py
import asyncio
from loguru import logger
from typing import Dict, List, Callable

class AlertManager:
    def __init__(self):
        self.alerts = []
        self.handlers = []
    
    def add_alert(self, name: str, condition: Callable, severity: str = "warning"):
        """Добавить алерт"""
        alert = {
            "name": name,
            "condition": condition,
            "severity": severity,  # info, warning, error, critical
            "last_triggered": None,
            "count": 0
        }
        self.alerts.append(alert)
        logger.info(f"🚨 Добавлен алерт: {name} ({severity})")
    
    def add_handler(self, handler: Callable):
        """Добавить обработчик алертов"""
        self.handlers.append(handler)
    
    async def check_alerts(self):
        """Проверить все алерты"""
        for alert in self.alerts:
            try:
                if alert["condition"]():
                    await self._trigger_alert(alert)
            except Exception as e:
                logger.error(f"❌ Ошибка проверки алерта {alert['name']}: {e}")
    
    async def _trigger_alert(self, alert):
        """Сработал алерт"""
        alert["count"] += 1
        alert["last_triggered"] = time.time()
        
        message = f"🚨 АЛЕРТ: {alert['name']} (серьёзность: {alert['severity']})"
        logger.warning(message)
        
        # Отправляем уведомления
        for handler in self.handlers:
            try:
                await handler(alert, message)
            except Exception as e:
                logger.error(f"❌ Ошибка отправки алерта: {e}")

# Настройка алертов
alert_manager = AlertManager()

# Алерт на высокое использование памяти
alert_manager.add_alert(
    "high_memory_usage",
    lambda: psutil.Process().memory_info().rss > 500 * 1024 * 1024,  # 500MB
    "warning"
)

# Алерт на ошибки API
alert_manager.add_alert(
    "openai_api_errors",
    lambda: metrics.get_metric_count("openai_errors", last_minutes=5) > 10,
    "error"
)

# Алерт на отсутствие активности
alert_manager.add_alert(
    "no_activity",
    lambda: metrics.get_metric_age("messages_received") > 3600,  # 1 час
    "warning"
)
```

### 📧 Обработчики алертов

#### Telegram уведомления
```python
async def telegram_alert_handler(alert, message):
    """Отправка алертов в Telegram"""
    admin_chat_id = config.admin_chat_id
    if admin_chat_id:
        await telegram_bot.send_message(
            chat_id=admin_chat_id,
            text=f"🚨 {message}\n\nВремя: {datetime.now()}\nСчётчик: {alert['count']}"
        )

alert_manager.add_handler(telegram_alert_handler)
```

#### Email уведомления
```python
import smtplib
from email.mime.text import MIMEText

async def email_alert_handler(alert, message):
    """Отправка алертов по email"""
    if alert["severity"] in ["error", "critical"]:
        msg = MIMEText(f"{message}\n\nДетали:\n{json.dumps(alert, indent=2)}")
        msg["Subject"] = f"SmartGroupBot Alert: {alert['name']}"
        msg["From"] = config.alert_email_from
        msg["To"] = config.alert_email_to
        
        with smtplib.SMTP(config.smtp_server) as server:
            server.send_message(msg)

alert_manager.add_handler(email_alert_handler)
```

#### Webhook уведомления
```python
import httpx

async def webhook_alert_handler(alert, message):
    """Отправка алертов через webhook"""
    payload = {
        "alert": alert["name"],
        "severity": alert["severity"],
        "message": message,
        "timestamp": time.time(),
        "count": alert["count"]
    }
    
    async with httpx.AsyncClient() as client:
        await client.post(config.alert_webhook_url, json=payload)

alert_manager.add_handler(webhook_alert_handler)
```

## 📱 Веб-дашборд мониторинга

### 🖥️ Real-time дашборд

```html
<!-- templates/monitoring.html -->
<!DOCTYPE html>
<html>
<head>
    <title>SmartGroupBot Monitoring</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>
</head>
<body>
    <div class="monitoring-dashboard">
        <h1>🔍 SmartGroupBot Monitoring</h1>
        
        <!-- Статус системы -->
        <div class="status-panel">
            <div class="status-card" id="bot-status">
                <h3>🤖 Bot Status</h3>
                <div class="status-indicator" id="bot-indicator">🟢 Online</div>
                <div class="uptime" id="uptime">Uptime: 2d 15h 30m</div>
            </div>
            
            <div class="status-card" id="api-status">
                <h3>🔌 API Status</h3>
                <div id="telegram-api">Telegram: 🟢 OK</div>
                <div id="openai-api">OpenAI: 🟡 Fallback</div>
                <div id="database-status">Database: 🟢 OK</div>
            </div>
            
            <div class="status-card" id="performance">
                <h3>⚡ Performance</h3>
                <div id="memory-usage">Memory: 142MB / 512MB</div>
                <div id="cpu-usage">CPU: 15%</div>
                <div id="response-time">Avg Response: 0.25s</div>
            </div>
        </div>
        
        <!-- Графики -->
        <div class="charts-panel">
            <div class="chart-container">
                <canvas id="messagesChart"></canvas>
            </div>
            <div class="chart-container">
                <canvas id="performanceChart"></canvas>
            </div>
            <div class="chart-container">
                <canvas id="errorsChart"></canvas>
            </div>
        </div>
        
        <!-- Логи в реальном времени -->
        <div class="logs-panel">
            <h3>📊 Real-time Logs</h3>
            <div class="log-filters">
                <button onclick="filterLogs('all')" class="active">All</button>
                <button onclick="filterLogs('error')">Errors</button>
                <button onclick="filterLogs('warning')">Warnings</button>
                <button onclick="filterLogs('info')">Info</button>
            </div>
            <div id="logs-container" class="logs-container"></div>
        </div>
        
        <!-- Алерты -->
        <div class="alerts-panel">
            <h3>🚨 Active Alerts</h3>
            <div id="alerts-container"></div>
        </div>
    </div>

    <script>
        // WebSocket соединение для real-time обновлений
        const socket = io();
        
        // Обновление статуса
        socket.on('status_update', function(data) {
            updateStatus(data);
        });
        
        // Новые логи
        socket.on('new_log', function(log) {
            addLogEntry(log);
        });
        
        // Новые метрики
        socket.on('metrics_update', function(metrics) {
            updateCharts(metrics);
        });
        
        // Алерты
        socket.on('alert_triggered', function(alert) {
            showAlert(alert);
        });
        
        // График сообщений
        const messagesChart = new Chart(document.getElementById('messagesChart'), {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Messages per minute',
                    data: [],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Messages Activity'
                    }
                }
            }
        });
        
        // График производительности
        const performanceChart = new Chart(document.getElementById('performanceChart'), {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Response Time (ms)',
                        data: [],
                        borderColor: 'rgb(255, 99, 132)',
                        yAxisID: 'y'
                    },
                    {
                        label: 'Memory Usage (MB)',
                        data: [],
                        borderColor: 'rgb(54, 162, 235)',
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left'
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>
```

### 🔄 WebSocket для real-time обновлений

```python
# web_dashboard.py - добавление WebSocket поддержки
from flask_socketio import SocketIO, emit
import json

socketio = SocketIO(app, cors_allowed_origins="*")

class RealtimeLogger:
    def __init__(self, socketio):
        self.socketio = socketio
        self.setup_log_handler()
    
    def setup_log_handler(self):
        """Настройка обработчика логов для real-time отправки"""
        class SocketIOHandler(logging.Handler):
            def __init__(self, socketio):
                super().__init__()
                self.socketio = socketio
            
            def emit(self, record):
                log_entry = {
                    "timestamp": record.created,
                    "level": record.levelname,
                    "module": record.module,
                    "message": record.getMessage(),
                    "formatted": self.format(record)
                }
                self.socketio.emit('new_log', log_entry)
        
        # Добавляем handler к loguru
        logger.add(SocketIOHandler(self.socketio), level="INFO")

# Инициализация real-time логгера
realtime_logger = RealtimeLogger(socketio)

@socketio.on('connect')
def handle_connect():
    """Клиент подключился"""
    emit('status_update', {
        "bot_status": "online",
        "uptime": get_uptime(),
        "memory_usage": get_memory_usage(),
        "active_chats": get_active_chats_count()
    })

@socketio.on('request_metrics')
def handle_metrics_request():
    """Запрос метрик от клиента"""
    emit('metrics_update', {
        "messages_per_minute": get_messages_per_minute(),
        "response_times": get_response_times(),
        "error_rates": get_error_rates()
    })
```

## 🔧 Диагностические инструменты

### 🩺 Health Check endpoints

```python
# web_dashboard.py - endpoints для мониторинга
@app.route('/health')
def health_check():
    """Базовая проверка здоровья"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.route('/health/detailed')
def detailed_health_check():
    """Детальная проверка всех компонентов"""
    checks = {}
    
    # Проверка бота
    try:
        # Попытка получить информацию о боте
        bot_info = asyncio.run(telegram_bot.get_me())
        checks["telegram_bot"] = {
            "status": "healthy",
            "bot_username": bot_info.get("username"),
            "last_check": datetime.now().isoformat()
        }
    except Exception as e:
        checks["telegram_bot"] = {
            "status": "unhealthy",
            "error": str(e),
            "last_check": datetime.now().isoformat()
        }
    
    # Проверка базы данных
    try:
        db_stats = asyncio.run(database.get_stats())
        checks["database"] = {
            "status": "healthy",
            "connection_count": db_stats.get("connections"),
            "last_check": datetime.now().isoformat()
        }
    except Exception as e:
        checks["database"] = {
            "status": "unhealthy",
            "error": str(e),
            "last_check": datetime.now().isoformat()
        }
    
    # Проверка OpenAI
    try:
        # Быстрый тест OpenAI API
        test_result = asyncio.run(ai_service.test_connection())
        checks["openai_api"] = {
            "status": "healthy" if test_result else "degraded",
            "mode": "openai" if test_result else "fallback",
            "last_check": datetime.now().isoformat()
        }
    except Exception as e:
        checks["openai_api"] = {
            "status": "unhealthy",
            "error": str(e),
            "last_check": datetime.now().isoformat()
        }
    
    # Общий статус
    overall_status = "healthy"
    if any(check["status"] == "unhealthy" for check in checks.values()):
        overall_status = "unhealthy"
    elif any(check["status"] == "degraded" for check in checks.values()):
        overall_status = "degraded"
    
    return {
        "overall_status": overall_status,
        "checks": checks,
        "timestamp": datetime.now().isoformat()
    }

@app.route('/metrics')
def prometheus_metrics():
    """Метрики в формате Prometheus"""
    metrics_text = []
    
    # Счётчики
    metrics_text.append(f"smartbot_messages_total {metrics.get_total('messages_received')}")
    metrics_text.append(f"smartbot_responses_total {metrics.get_total('responses_sent')}")
    metrics_text.append(f"smartbot_errors_total {metrics.get_total('errors')}")
    
    # Гистограммы
    response_times = metrics.get_recent_values("response_time", minutes=5)
    if response_times:
        avg_response_time = sum(response_times) / len(response_times)
        metrics_text.append(f"smartbot_response_time_seconds {avg_response_time}")
    
    # Gauges
    metrics_text.append(f"smartbot_active_chats {get_active_chats_count()}")
    metrics_text.append(f"smartbot_memory_bytes {psutil.Process().memory_info().rss}")
    
    return "\n".join(metrics_text), 200, {"Content-Type": "text/plain"}
```

### 🐛 Debug endpoints

```python
@app.route('/debug/context/<chat_id>')
def debug_context(chat_id):
    """Отладка контекста чата"""
    context = bot_service.get_context_messages(chat_id)
    buffer_info = bot_service.get_buffer_info(chat_id)
    
    return {
        "chat_id": chat_id,
        "context_messages": context,
        "buffer_size": len(context),
        "buffer_info": buffer_info,
        "last_activity": buffer_info.get("last_message_time")
    }

@app.route('/debug/ai/test')
def debug_ai_test():
    """Тестирование AI сервиса"""
    test_messages = ["Привет всем!", "Как дела?", "Что нового?"]
    
    result = asyncio.run(
        ai_service.analyze_context_and_generate_response(test_messages)
    )
    
    return {
        "test_input": test_messages,
        "ai_result": result,
        "mode": "openai" if "openai" in str(result) else "fallback",
        "timestamp": datetime.now().isoformat()
    }

@app.route('/debug/database/stats')
def debug_database_stats():
    """Статистика базы данных"""
    stats = asyncio.run(database.get_detailed_stats())
    
    return {
        "total_interactions": stats.get("total_interactions"),
        "interactions_today": stats.get("interactions_today"),
        "unique_chats": stats.get("unique_chats"),
        "database_size_mb": stats.get("database_size_mb"),
        "index_usage": stats.get("index_usage"),
        "slow_queries": stats.get("slow_queries", [])
    }
```

## 📊 Grafana интеграция

### 📈 Настройка Grafana дашборда

```json
{
  "dashboard": {
    "title": "SmartGroupBot Monitoring",
    "panels": [
      {
        "title": "Messages Activity",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(smartbot_messages_total[5m])",
            "legendFormat": "Messages per second"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph", 
        "targets": [
          {
            "expr": "smartbot_response_time_seconds",
            "legendFormat": "Avg Response Time"
          }
        ]
      },
      {
        "title": "Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "smartbot_memory_bytes / 1024 / 1024",
            "legendFormat": "Memory MB"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(smartbot_errors_total[5m])",
            "legendFormat": "Errors per second"
          }
        ]
      }
    ]
  }
}
```

## 🔍 Логи анализ

### 📊 Парсинг и анализ логов

```python
# log_analyzer.py
import re
from collections import defaultdict, Counter
from datetime import datetime, timedelta

class LogAnalyzer:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.log_pattern = re.compile(
            r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \| (\w+)\s+\| ([^:]+):([^:]+):(\d+) - (.+)'
        )
    
    def parse_logs(self, hours=24):
        """Парсинг логов за последние N часов"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        logs = []
        
        with open(self.log_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = self.log_pattern.match(line.strip())
                if match:
                    timestamp_str, level, module, function, line_num, message = match.groups()
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
                    
                    if timestamp >= cutoff_time:
                        logs.append({
                            'timestamp': timestamp,
                            'level': level,
                            'module': module,
                            'function': function,
                            'line': int(line_num),
                            'message': message
                        })
        
        return logs
    
    def analyze_errors(self, logs=None):
        """Анализ ошибок"""
        if logs is None:
            logs = self.parse_logs()
        
        error_logs = [log for log in logs if log['level'] in ['ERROR', 'WARNING']]
        
        analysis = {
            'total_errors': len(error_logs),
            'errors_by_module': Counter(log['module'] for log in error_logs),
            'errors_by_hour': defaultdict(int),
            'common_errors': Counter(),
            'error_timeline': []
        }
        
        for log in error_logs:
            hour_key = log['timestamp'].strftime('%Y-%m-%d %H:00')
            analysis['errors_by_hour'][hour_key] += 1
            
            # Извлекаем тип ошибки
            message = log['message']
            if 'OpenAI API' in message:
                analysis['common_errors']['OpenAI API errors'] += 1
            elif 'Rate limit' in message:
                analysis['common_errors']['Rate limit errors'] += 1
            elif 'Database' in message or 'БД' in message:
                analysis['common_errors']['Database errors'] += 1
            elif 'Telegram' in message:
                analysis['common_errors']['Telegram API errors'] += 1
            
            analysis['error_timeline'].append({
                'timestamp': log['timestamp'].isoformat(),
                'level': log['level'],
                'message': message[:100] + '...' if len(message) > 100 else message
            })
        
        return analysis
    
    def analyze_performance(self, logs=None):
        """Анализ производительности"""
        if logs is None:
            logs = self.parse_logs()
        
        performance_logs = [
            log for log in logs 
            if 'метрики производительности' in log['message'].lower()
        ]
        
        response_times = []
        for log in performance_logs:
            message = log['message']
            # Извлекаем время total=X.XXs
            match = re.search(r'total=(\d+\.\d+)s', message)
            if match:
                response_times.append(float(match.group(1)))
        
        if response_times:
            return {
                'avg_response_time': sum(response_times) / len(response_times),
                'min_response_time': min(response_times),
                'max_response_time': max(response_times),
                'samples_count': len(response_times),
                'slow_responses': len([t for t in response_times if t > 1.0])
            }
        
        return {'error': 'No performance data found'}
    
    def generate_report(self):
        """Генерация полного отчёта"""
        logs = self.parse_logs(24)  # За последние 24 часа
        
        report = {
            'report_time': datetime.now().isoformat(),
            'total_logs': len(logs),
            'logs_by_level': Counter(log['level'] for log in logs),
            'most_active_modules': Counter(log['module'] for log in logs).most_common(10),
            'error_analysis': self.analyze_errors(logs),
            'performance_analysis': self.analyze_performance(logs)
        }
        
        return report

# Использование
if __name__ == "__main__":
    analyzer = LogAnalyzer('smart_bot.log')
    report = analyzer.generate_report()
    
    print(f"📊 Отчёт по логам за последние 24 часа:")
    print(f"Всего записей: {report['total_logs']}")
    print(f"Ошибок: {report['error_analysis']['total_errors']}")
    print(f"Среднее время ответа: {report['performance_analysis'].get('avg_response_time', 'N/A')}s")
```

## 🚀 Continuous Monitoring

### 📱 Мониторинг в production

```bash
#!/bin/bash
# monitoring_check.sh - скрипт проверки системы

echo "🔍 Проверка SmartGroupBot..."

# Проверка процесса
if pgrep -f "python.*main_bot.py" > /dev/null; then
    echo "✅ Процесс бота запущен"
else
    echo "❌ Процесс бота не найден!"
    exit 1
fi

# Проверка health endpoint
health_status=$(curl -s http://localhost:5001/health | jq -r '.status' 2>/dev/null)
if [ "$health_status" = "healthy" ]; then
    echo "✅ Health check пройден"
else
    echo "❌ Health check провален: $health_status"
    exit 1
fi

# Проверка размера логов
log_size=$(du -sh smart_bot.log | cut -f1)
echo "📊 Размер логов: $log_size"

# Проверка использования памяти
memory_usage=$(ps aux | grep "main_bot.py" | grep -v grep | awk '{print $6}')
if [ ! -z "$memory_usage" ]; then
    memory_mb=$((memory_usage / 1024))
    echo "🖥️ Использование памяти: ${memory_mb}MB"
    
    if [ $memory_mb -gt 500 ]; then
        echo "⚠️ Высокое использование памяти!"
    fi
fi

# Проверка свободного места
disk_usage=$(df -h . | awk 'NR==2 {print $5}' | sed 's/%//')
echo "💾 Использование диска: ${disk_usage}%"

if [ $disk_usage -gt 80 ]; then
    echo "⚠️ Мало свободного места на диске!"
fi

echo "✅ Проверка завершена"
```

### ⏰ Cron задачи для мониторинга

```bash
# crontab -e
# Проверка каждые 5 минут
*/5 * * * * /path/to/monitoring_check.sh >> /var/log/smartbot_monitoring.log 2>&1

# Отчёт по логам каждые 6 часов
0 */6 * * * cd /path/to/smartbot && python log_analyzer.py > /tmp/log_report.txt && mail -s "SmartBot Log Report" admin@example.com < /tmp/log_report.txt

# Очистка старых логов раз в неделю
0 2 * * 0 find /path/to/smartbot/logs -name "*.log.*" -mtime +7 -delete

# Backup базы данных ежедневно
0 3 * * * cp /path/to/smartbot/bot_database.db /backups/bot_database_$(date +\%Y\%m\%d).db
```

---

**🎯 Эффективный мониторинг обеспечивает стабильную работу SmartGroupBot!**

**📚 Дополнительные инструменты:**
- [Grafana](https://grafana.com/) - Визуализация метрик
- [Prometheus](https://prometheus.io/) - Сбор метрик
- [ELK Stack](https://www.elastic.co/elk-stack) - Анализ логов
- [Sentry](https://sentry.io/) - Отслеживание ошибок 