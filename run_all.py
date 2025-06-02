"""
Скрипт для запуска всех компонентов SmartGroupBot
"""
import asyncio
import threading
import time
import sys
from loguru import logger

from main import main as run_bot
from web_dashboard import app


def run_web_dashboard():
    """Запускает веб-панель в отдельном потоке"""
    try:
        logger.info("🌐 Запуск веб-панели на http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        logger.error(f"❌ Ошибка веб-панели: {e}")


async def run_bot_async():
    """Запускает бота асинхронно"""
    try:
        await run_bot()
    except Exception as e:
        logger.error(f"❌ Ошибка бота: {e}")


def main():
    """Главная функция для запуска всех компонентов"""
    try:
        print("🚀 SmartGroupBot - Запуск всех компонентов")
        print("=" * 50)
        
        # Запускаем веб-панель в отдельном потоке
        web_thread = threading.Thread(target=run_web_dashboard, daemon=True)
        web_thread.start()
        
        # Даем время веб-серверу запуститься
        time.sleep(2)
        
        print("✅ Веб-панель: http://localhost:5000")
        print("🤖 Запуск Telegram бота...")
        print("=" * 50)
        
        # Запускаем бота
        asyncio.run(run_bot_async())
        
    except KeyboardInterrupt:
        print("\n🛑 Остановка по Ctrl+C")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 