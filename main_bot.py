#!/usr/bin/env python3
"""
SmartGroupBot - Финальная рабочая версия с полным функционалом
"""

import asyncio
import logging
import sys
import signal
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

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

class SmartGroupBot:
    """Умный групповой бот с полным функционалом"""
    
    def __init__(self):
        from config import config
        from telegram.ext import Application, MessageHandler, CommandHandler, filters
        from telegram.constants import ChatType
        
        self.config = config
        self.application = None
        self.running = False
        
        logger.info("🤖 SmartGroupBot инициализирован")
        
    async def handle_message(self, update, context):
        """Основной обработчик сообщений"""
        try:
            message = update.message
            chat = update.effective_chat
            user = update.effective_user
            
            # Импортируем ChatType и bot_service
            from telegram.constants import ChatType
            from bot_service import bot_service
            
            logger.info(f"📩 Сообщение: '{message.text}' | Чат: {chat.type} | ID: {chat.id}")
            
            # Работаем только с группами и супергруппами
            if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
                logger.info(f"⏭️ Пропускаем - не групповой чат (тип: {chat.type})")
                return
            
            # Игнорируем сообщения от ботов
            if user and user.is_bot:
                logger.info(f"⏭️ Пропускаем - сообщение от бота")
                return
            
            # Игнорируем команды
            if message.text and message.text.startswith('/'):
                logger.info(f"⏭️ Пропускаем - команда: {message.text}")
                return
            
            logger.info(f"✅ Обрабатываем сообщение от @{user.username if user else 'Unknown'}")
            
            # Обработка через bot_service
            chat_id = str(chat.id)
            chat_title = chat.title or "Без названия"
            message_text = message.text or ""
            user_id = str(user.id) if user else None
            username = user.username if user else None
            
            logger.info(f"🔄 Вызываем bot_service.process_message...")
            bot_response = await bot_service.process_message(
                chat_id=chat_id,
                chat_title=chat_title,
                message_text=message_text,
                user_id=user_id,
                username=username
            )
            
            if bot_response:
                logger.info(f"📤 Отправляем ответ: {bot_response[:100]}...")
                await message.reply_text(bot_response)
                logger.info(f"✅ Ответ отправлен!")
            else:
                logger.info(f"🤐 Бот решил не отвечать")
                
        except Exception as e:
            logger.error(f"❌ Ошибка в handle_message: {e}", exc_info=True)
    
    async def start_command(self, update, context):
        """Команда /start"""
        logger.info(f"🚀 Команда /start")
        welcome_text = """
🤖 SmartGroupBot активирован!

Я умный бот для групповых чатов с возможностями:
• 🧠 Анализ контекста разговора
• 💭 Генерация умных ответов с помощью AI
• 📊 Аналитика настроения
• 🎯 Адаптивная частота ответов

Просто общайтесь в группе, и я буду участвовать в диалоге когда это уместно!
        """
        await update.message.reply_text(welcome_text)
    
    async def help_command(self, update, context):
        """Команда /help"""
        help_text = """
🤖 SmartGroupBot - Справка

🔧 Команды:
/start - информация о боте
/help - эта справка
/stats - статистика чата (только для админов)

⚙️ Настройки:
• Минимум сообщений для анализа: {min_context}
• Частота ответов: раз в {frequency} сообщений
• Максимум контекста: {max_context} сообщений

📊 Аналитика доступна на: http://localhost:5001

Бот автоматически анализирует контекст и участвует в беседе.
        """.format(
            min_context=self.config.min_context_messages,
            frequency=self.config.response_frequency,
            max_context=self.config.max_context_messages
        )
        await update.message.reply_text(help_text)
    
    async def stats_command(self, update, context):
        """Команда /stats для статистики чата"""
        try:
            from database import SessionLocal
            from models import ChatInteraction
            from sqlalchemy import func
            
            chat_id = str(update.effective_chat.id)
            
            with SessionLocal() as db:
                # Получаем статистику для текущего чата
                total_messages = db.query(ChatInteraction).filter(
                    ChatInteraction.chat_id == chat_id
                ).count()
                
                responses_given = db.query(ChatInteraction).filter(
                    ChatInteraction.chat_id == chat_id,
                    ChatInteraction.response_generated == True
                ).count()
                
                avg_sentiment = db.query(func.avg(ChatInteraction.sentiment)).filter(
                    ChatInteraction.chat_id == chat_id,
                    ChatInteraction.sentiment.isnot(None)
                ).scalar()
                
                response_rate = (responses_given / total_messages * 100) if total_messages > 0 else 0
                
                stats_text = f"""
📊 Статистика чата "{update.effective_chat.title}":

📈 Всего обработано сообщений: {total_messages}
🤖 Ответов от бота: {responses_given}
📉 Частота ответов: {response_rate:.1f}%
😊 Средний sentiment: {avg_sentiment:.2f if avg_sentiment else 'н/д'}

🌐 Полная аналитика: http://localhost:5001
                """
                
                await update.message.reply_text(stats_text)
                
        except Exception as e:
            logger.error(f"❌ Ошибка в stats_command: {e}")
            await update.message.reply_text("❌ Ошибка получения статистики")
    
    async def start(self):
        """Запуск бота"""
        try:
            logger.info("🤖 === ЗАПУСК SMARTGROUPBOT ===")
            logger.info(f"📋 Конфигурация:")
            logger.info(f"   • Имя: {self.config.bot_name}")
            logger.info(f"   • Частота ответов: раз в {self.config.response_frequency} сообщений")
            logger.info(f"   • Минимум контекста: {self.config.min_context_messages} сообщений")
            
            # Создаем приложение
            from telegram.ext import Application, MessageHandler, CommandHandler, filters
            self.application = Application.builder().token(self.config.telegram_bot_token).build()
            
            # Добавляем обработчики
            self.application.add_handler(CommandHandler("start", self.start_command))
            self.application.add_handler(CommandHandler("help", self.help_command))
            self.application.add_handler(CommandHandler("stats", self.stats_command))
            self.application.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
            )
            
            logger.info("✅ Обработчики настроены")
            
            # Получаем информацию о боте
            bot_info = await self.application.bot.get_me()
            logger.info(f"🤖 Бот @{bot_info.username} готов!")
            logger.info(f"📖 Может читать все сообщения в группах: {bot_info.can_read_all_group_messages}")
            logger.info(f"👥 Может присоединяться к группам: {bot_info.can_join_groups}")
            
            # Запускаем
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling(
                allowed_updates=["message"],
                drop_pending_updates=True
            )
            
            self.running = True
            logger.info("🤖 === SMARTGROUPBOT АКТИВЕН ===")
            logger.info("💬 Готов к работе в группах!")
            logger.info("🌐 Dashboard: http://localhost:5001")
            
            # Основной цикл
            while self.running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"❌ Ошибка запуска: {e}", exc_info=True)
            raise
    
    async def stop(self):
        """Остановка бота"""
        logger.info("🛑 Остановка SmartGroupBot...")
        self.running = False
        
        if self.application:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            
        logger.info("✅ SmartGroupBot остановлен")

async def main():
    """Основная функция"""
    bot = SmartGroupBot()
    
    # Обработчик сигналов
    def signal_handler(signum, frame):
        logger.info(f"📡 Получен сигнал {signum}")
        asyncio.create_task(bot.stop())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("👋 SmartGroupBot остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)
    finally:
        await bot.stop()

if __name__ == "__main__":
    asyncio.run(main()) 