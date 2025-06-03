#!/usr/bin/env python3
"""
Простой запуск SmartGroupBot без веб-дашборда
Используется для стабильной работы бота
"""

import asyncio
import logging
import sys
from pathlib import Path

# Добавляем путь к проекту
sys.path.insert(0, str(Path(__file__).parent))

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('smart_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Основная функция запуска"""
    try:
        logger.info("🚀 Запуск SmartGroupBot (простой режим)")
        
        # Проверяем конфигурацию
        try:
            from config import config
            logger.info("✅ Конфигурация загружена")
        except Exception as e:
            logger.error(f"❌ Ошибка конфигурации: {e}")
            return
        
        # Запускаем бота
        from main_bot import SmartGroupBot
        bot = SmartGroupBot()
        
        logger.info("🤖 Запуск бота...")
        await bot.start()
        
    except KeyboardInterrupt:
        logger.info("🛑 Остановка по Ctrl+C")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main()) 