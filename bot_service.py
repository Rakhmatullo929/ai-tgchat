"""
Основной сервис Telegram бота
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
import asyncio
from loguru import logger

from models import db_manager, ChatInteraction
from ai_service import ai_service
from config import config


class MessageBuffer:
    """Буфер для хранения последних сообщений по чатам"""
    
    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.chat_messages = defaultdict(lambda: deque(maxlen=max_messages))
        self.bot_response_counts = defaultdict(int)
        self.last_response_time = defaultdict(lambda: datetime.min)
    
    def add_message(self, chat_id: str, message: str, is_bot: bool = False):
        """Добавляет сообщение в буфер"""
        self.chat_messages[chat_id].append({
            'text': message,
            'timestamp': datetime.now(),
            'is_bot': is_bot
        })
        
        if is_bot:
            self.bot_response_counts[chat_id] += 1
            self.last_response_time[chat_id] = datetime.now()
    
    def get_recent_messages(self, chat_id: str, limit: int = None) -> List[str]:
        """Получает последние сообщения из чата"""
        limit = limit or config.max_context_messages
        messages = list(self.chat_messages[chat_id])[-limit:]
        return [msg['text'] for msg in messages if not msg['is_bot']]
    
    def get_participants_count(self, chat_id: str) -> int:
        """Подсчитывает количество уникальных участников (упрощенная версия)"""
        # В реальной реализации здесь был бы анализ пользователей
        return min(len(self.chat_messages[chat_id]), 10)
    
    def should_respond_by_frequency(self, chat_id: str) -> bool:
        """Проверяет, можно ли отвечать по частоте"""
        recent_messages = len([
            msg for msg in self.chat_messages[chat_id] 
            if not msg['is_bot'] and 
            datetime.now() - msg['timestamp'] < timedelta(minutes=10)
        ])
        
        # Проверяем, не отвечал ли бот недавно
        time_since_last_response = datetime.now() - self.last_response_time[chat_id]
        if time_since_last_response < timedelta(seconds=30):
            return False
        
        # Логика частоты ответов
        bot_responses_recent = len([
            msg for msg in self.chat_messages[chat_id] 
            if msg['is_bot'] and 
            datetime.now() - msg['timestamp'] < timedelta(minutes=10)
        ])
        
        return ai_service.should_respond_based_on_frequency(
            recent_messages, bot_responses_recent
        )


class BotService:
    """Основной сервис бота"""
    
    def __init__(self):
        self.message_buffer = MessageBuffer()
        logger.info("✅ BotService инициализирован")
    
    async def process_message(
        self, 
        chat_id: str, 
        chat_title: str, 
        message_text: str,
        user_id: str = None,
        username: str = None
    ) -> Optional[str]:
        """
        Обрабатывает входящее сообщение и решает, нужно ли отвечать
        """
        try:
            # Валидация входных данных
            if not chat_id or not message_text:
                logger.warning("⚠️ Некорректные данные сообщения")
                return None
                
            # Ограничиваем длину сообщения
            if len(message_text) > 4000:
                message_text = message_text[:4000] + "..."
                logger.info("✂️ Обрезано длинное сообщение")
            
            # Добавляем сообщение в буфер
            self.message_buffer.add_message(chat_id, message_text, is_bot=False)
            
            # Получаем историю сообщений для анализа
            context_messages = self.message_buffer.get_recent_messages(chat_id, config.max_context_messages)
            
            if len(context_messages) < config.min_context_messages:
                logger.debug(f"⏳ Недостаточно контекста для анализа ({len(context_messages)}/{config.min_context_messages})")
                return None
            
            # Проверяем частоту ответов
            if not self.message_buffer.should_respond_by_frequency(chat_id):
                logger.debug("⏭️ Пропуск - частота ответов")
                return None
            
            logger.info(f"🤔 Анализируем контекст в '{chat_title}' ({len(context_messages)} сообщений)")
            
            # Анализируем контекст с таймаутом
            ai_result = None
            try:
                ai_result = await asyncio.wait_for(
                    ai_service.analyze_context_and_generate_response(context_messages, chat_title),
                    timeout=15  # Таймаут 15 секунд
                )
            except asyncio.TimeoutError:
                logger.warning("⏰ Таймаут AI анализа, используем fallback")
                ai_result = {"should_respond": True, "response": None}
            except Exception as e:
                logger.error(f"❌ Ошибка AI анализа: {e}")
                ai_result = {"should_respond": True, "response": None}
            
            # Проверяем результат
            if not ai_result or not isinstance(ai_result, dict):
                logger.warning("⚠️ Некорректный результат AI анализа")
                return None
                
            should_respond = ai_result.get("should_respond", False)
            ai_response = ai_result.get("response", "")
            detected_topic = ai_result.get("topic", "")
            sentiment = ai_result.get("sentiment", "")
            
            logger.info(f"🎯 AI решение: respond={should_respond}, topic={detected_topic}, sentiment={sentiment}")
            
            bot_response = None
            if should_respond and ai_response:
                bot_response = ai_response
                logger.info(f"💬 Генерируем ответ: {bot_response[:100]}...")
            
            # Сохраняем взаимодействие асинхронно
            asyncio.create_task(self._save_interaction(
                chat_id, chat_title, context_messages, 
                detected_topic, sentiment, bot_response, bool(bot_response)
            ))
            
            return bot_response
                
        except Exception as e:
            logger.error(f"❌ Ошибка обработки сообщения: {e}", exc_info=True)
            return None
    
    async def _save_interaction(
        self,
        chat_id: str,
        chat_title: str,
        context_messages: List[str],
        detected_topic: str = None,
        sentiment: str = None,
        bot_response: str = None,
        response_generated: bool = False
    ):
        """Сохраняет взаимодействие в базу данных"""
        try:
            interaction_data = {
                'chat_id': chat_id,
                'chat_title': chat_title,
                'context_messages': context_messages,
                'detected_topic': detected_topic,
                'sentiment': sentiment,
                'bot_response': bot_response,
                'response_generated': response_generated,
                'participants_count': self.message_buffer.get_participants_count(chat_id)
            }
            
            # Сохраняем в фоновом режиме
            await asyncio.get_event_loop().run_in_executor(
                None, db_manager.save_interaction, interaction_data
            )
            
            logger.debug("💾 Взаимодействие сохранено в БД")
            
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения в БД: {e}")
    
    def get_chat_stats(self, chat_id: str) -> Dict[str, Any]:
        """Получает статистику по чату"""
        try:
            history = db_manager.get_chat_history(chat_id, limit=100)
            
            total_interactions = len(history)
            responses_generated = len([h for h in history if h.response_generated])
            
            # Анализ настроений
            sentiments = [h.sentiment for h in history if h.sentiment]
            sentiment_stats = {
                'positive': sentiments.count('positive'),
                'neutral': sentiments.count('neutral'),
                'negative': sentiments.count('negative')
            }
            
            # Популярные темы
            topics = [h.detected_topic for h in history if h.detected_topic]
            topic_counts = {}
            for topic in topics:
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
            
            return {
                'total_interactions': total_interactions,
                'responses_generated': responses_generated,
                'response_rate': responses_generated / max(total_interactions, 1),
                'sentiment_distribution': sentiment_stats,
                'popular_topics': sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            }
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения статистики: {e}")
            return {}


# Глобальный экземпляр сервиса
bot_service = BotService() 