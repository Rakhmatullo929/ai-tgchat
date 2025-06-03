#!/usr/bin/env python3
"""
Скрипт для запуска всех компонентов SmartGroupBot
"""
import asyncio
import threading
import time
import sys
import os
from pathlib import Path

# Добавляем текущую директорию в путь Python
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

print("🚀 SmartGroupBot - Запуск всех компонентов")
print("=" * 50)

# Настройка логирования
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('smart_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def check_environment():
    """Проверка окружения перед запуском"""
    logger.info("🔍 Проверка окружения...")
    
    # Проверяем основные файлы
    required_files = ['main_bot.py', 'web_dashboard.py', 'config.py', 'models.py']
    missing_files = []
    
    for file in required_files:
        if not (current_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        logger.error(f"❌ Отсутствуют файлы: {missing_files}")
        return False
    
    # Проверяем импорты
    try:
        import config
        logger.info("✅ config модуль загружен")
    except Exception as e:
        logger.error(f"❌ Ошибка загрузки config: {e}")
        return False
    
    try:
        import web_dashboard
        logger.info("✅ web_dashboard модуль загружен")
    except Exception as e:
        logger.error(f"❌ Ошибка загрузки web_dashboard: {e}")
        return False
    
    try:
        import main_bot
        logger.info("✅ main_bot модуль загружен")
    except Exception as e:
        logger.error(f"❌ Ошибка загрузки main_bot: {e}")
        return False
    
    return True

def run_web_dashboard():
    """Запускает веб-панель в отдельном потоке"""
    try:
        from web_dashboard import app
        logger.info("🌐 Запуск веб-панели на http://0.0.0.0:5000")
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        logger.error(f"❌ Ошибка веб-панели: {e}")

async def run_bot_async():
    """Запускает бота асинхронно"""
    try:
        from main_bot import main
        await main()
    except Exception as e:
        logger.error(f"❌ Ошибка бота: {e}")
        raise

def main():
    """Главная функция для запуска всех компонентов"""
    try:
        # Проверяем окружение
        if not check_environment():
            logger.error("❌ Проверка окружения не пройдена")
            sys.exit(1)
        
        logger.info("✅ Проверка окружения пройдена")
        
        # Запускаем веб-панель в отдельном потоке
        logger.info("🌐 Запуск веб-панели...")
        web_thread = threading.Thread(target=run_web_dashboard, daemon=True)
        web_thread.start()
        
        # Даем время веб-серверу запуститься
        time.sleep(3)
        
        logger.info("✅ Веб-панель: http://0.0.0.0:5000")
        logger.info("🤖 Запуск Telegram бота...")
        logger.info("=" * 50)
        
        # Запускаем бота
        asyncio.run(run_bot_async())
        
    except KeyboardInterrupt:
        logger.info("\n🛑 Остановка по Ctrl+C")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 