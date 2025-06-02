"""
Telegram бот для участия в групповых чатах
"""
import asyncio
from typing import Optional
from telegram import Update, Chat
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from telegram.constants import ChatType
from loguru import logger

from config import config
from bot_service import bot_service
from models import db_manager


class TelegramBot:
    """Класс Telegram бота"""
    
    def __init__(self):
        self.application = None
        self.bot_username = None
        logger.info("🤖 TelegramBot инициализирован")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        chat = update.effective_chat
        
        if chat.type == ChatType.PRIVATE:
            welcome_message = f"""
🤖 Привет! Я {config.bot_name}!

Я умный бот для групповых чатов. Добавь меня в группу, и я буду:
📝 Анализировать контекст беседы
💬 Генерировать релевантные ответы
📊 Сохранять статистику в базу данных

🎯 Настройки:
• Отвечаю примерно раз в {config.response_frequency} сообщений
• Анализирую последние {config.max_context_messages} сообщений
• Сохраняю всю аналитику в БД

Команды:
/start - это сообщение
/stats - статистика чата (только в группах)
/help - помощь

Добавь меня в группу и начнем! 🚀
"""
        else:
            welcome_message = f"""
🤖 Привет! Я {config.bot_name} готов участвовать в вашем чате!

Просто общайтесь, а я буду умно подключаться к беседе.
Используйте /stats для просмотра статистики.
"""
        
        await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = f"""
🤖 {config.bot_name} - Помощь

🎯 Основные возможности:
• Анализ контекста беседы
• Умные ответы по теме
• Контроль частоты ответов
• Сохранение аналитики

📋 Команды:
/start - приветствие и информация
/stats - статистика чата
/help - эта справка

⚙️ Как я работаю:
1. Анализирую последние {config.max_context_messages} сообщений
2. Определяю тему и тон беседы
3. Генерирую ответ, если есть что добавить
4. Сохраняю все данные в БД для аналитики

🔧 Настройки:
• Частота ответов: ~1 раз в {config.response_frequency} сообщений
• Минимум сообщений для анализа: {config.min_context_messages}

Создан с ❤️ для умного участия в групповых чатах!
"""
        await update.message.reply_text(help_text)
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /stats"""
        chat = update.effective_chat
        
        if chat.type == ChatType.PRIVATE:
            await update.message.reply_text(
                "📊 Статистика доступна только в групповых чатах!"
            )
            return
        
        try:
            stats = bot_service.get_chat_stats(str(chat.id))
            
            if not stats:
                await update.message.reply_text(
                    "📊 Пока нет данных для статистики. Начните общаться!"
                )
                return
            
            # Формируем красивую статистику
            stats_text = f"""
📊 Статистика чата "{chat.title}"

🔢 Общие данные:
• Всего взаимодействий: {stats['total_interactions']}
• Ответов сгенерировано: {stats['responses_generated']}
• Частота ответов: {stats['response_rate']:.1%}

😊 Настроения в чате:
• Позитивные: {stats['sentiment_distribution']['positive']}
• Нейтральные: {stats['sentiment_distribution']['neutral']}
• Негативные: {stats['sentiment_distribution']['negative']}

🏷️ Популярные темы:
"""
            
            for i, (topic, count) in enumerate(stats['popular_topics'][:5], 1):
                stats_text += f"{i}. {topic} ({count} раз)\n"
            
            # Общая статистика по всем чатам
            total_interactions = db_manager.get_total_interactions()
            stats_text += f"\n🌍 Всего взаимодействий во всех чатах: {total_interactions}"
            
            await update.message.reply_text(stats_text)
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения статистики: {e}")
            await update.message.reply_text(
                "❌ Произошла ошибка при получении статистики"
            )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик всех текстовых сообщений"""
        message = update.message
        chat = update.effective_chat
        user = update.effective_user
        
        # Обрабатываем только группы и супергруппы
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            return
        
        # Игнорируем сообщения от ботов
        if user.is_bot:
            return
        
        # Игнорируем команды
        if message.text and message.text.startswith('/'):
            return
        
        try:
            # Получаем информацию о сообщении
            chat_id = str(chat.id)
            chat_title = chat.title or "Без названия"
            message_text = message.text or ""
            user_id = str(user.id) if user else None
            username = user.username if user else None
            
            logger.info(f"📩 Новое сообщение в '{chat_title}' от @{username}: {message_text[:50]}...")
            
            # Обрабатываем сообщение через наш сервис
            bot_response = await bot_service.process_message(
                chat_id=chat_id,
                chat_title=chat_title,
                message_text=message_text,
                user_id=user_id,
                username=username
            )
            
            # Если есть ответ - отправляем его
            if bot_response:
                await message.reply_text(bot_response)
                logger.info(f"✅ Ответ отправлен в '{chat_title}': {bot_response[:50]}...")
            
        except Exception as e:
            logger.error(f"❌ Ошибка обработки сообщения: {e}")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик ошибок"""
        logger.error(f"❌ Ошибка при обновлении: {context.error}")
    
    def setup_handlers(self):
        """Настройка обработчиков команд и сообщений"""
        # Команды
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        
        # Обработчик всех текстовых сообщений
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
        
        # Обработчик ошибок
        self.application.add_error_handler(self.error_handler)
        
        logger.info("✅ Обработчики настроены")
    
    async def start_bot(self):
        """Запуск бота"""
        try:
            logger.info("🚀 Запуск Telegram бота...")
            
            # Создаем приложение
            self.application = Application.builder().token(config.telegram_bot_token).build()
            
            # Настраиваем обработчики
            self.setup_handlers()
            
            # Получаем информацию о боте
            bot_info = await self.application.bot.get_me()
            self.bot_username = bot_info.username
            
            logger.info(f"✅ Бот @{self.bot_username} готов к работе!")
            logger.info(f"🔗 Добавить в группу: https://t.me/{self.bot_username}")
            
            # Запускаем polling
            await self.application.run_polling(
                allowed_updates=["message", "edited_message"],
                drop_pending_updates=True
            )
            
        except Exception as e:
            logger.error(f"❌ Ошибка запуска бота: {e}")
            raise
    
    async def stop_bot(self):
        """Остановка бота"""
        if self.application:
            await self.application.stop()
            logger.info("🛑 Бот остановлен")


# Глобальный экземпляр бота
telegram_bot = TelegramBot()

if __name__ == "__main__":
    """Запуск бота при прямом вызове файла"""
    import asyncio
    
    try:
        asyncio.run(telegram_bot.start_bot())
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Ошибка запуска: {e}") 