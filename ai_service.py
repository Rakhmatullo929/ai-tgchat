"""
Сервис для работы с AI
"""
from openai import OpenAI
from typing import List, Dict, Any, Optional, Tuple
import json
import re
from config import config
from loguru import logger
import random

# Настраиваем OpenAI клиент
client = OpenAI(api_key=config.openai_api_key)


class AIService:
    """Сервис для работы с искусственным интеллектом"""
    
    def __init__(self):
        self.personality = config.bot_personality
        
        # Простые fallback ответы для случаев без OpenAI
        self.fallback_responses = [
            "Интересная мысль! 🤔",
            "А что вы об этом думаете? 💭",
            "Хорошая тема для обсуждения! 💬", 
            "Согласен, это важно 👍",
            "Понятно, расскажите больше 🗣️",
            "Интересно! А как это работает? 🔍",
            "Да, это стоит обсудить 📝",
            "Хороший вопрос! 🤷‍♂️",
            "Мне тоже интересно это узнать 📚",
            "Давайте разберемся вместе! 🤝"
        ]
        
        logger.info("✅ AIService инициализирован")

    def _get_fallback_response(self, context_messages: List[str], topic: str = None) -> Dict:
        """Fallback ответы когда OpenAI недоступен"""
        
        # Простая логика на основе ключевых слов
        last_message = context_messages[-1].lower() if context_messages else ""
        
        # Определяем тип сообщения
        if any(word in last_message for word in ['привет', 'здравствуй', 'добро', 'утро', 'день', 'вечер']):
            responses = ["Привет! Как дела? 👋", "Здравствуйте! Рад всех видеть! 😊", "Привет! Что нового? 🌟"]
            topic = "приветствие"
            should_respond = True
        elif any(word in last_message for word in ['как дела', 'как ты', 'как жизнь', 'как настроение']):
            responses = ["Всё отлично! А у вас как? 😊", "Хорошо! Работаю, помогаю в чате 🤖", "Замечательно! Спасибо что спросили 💙"]
            topic = "самочувствие"
            should_respond = True
        elif any(word in last_message for word in ['что делаешь', 'чем занят', 'что нового']):
            responses = ["Слежу за интересными разговорами в чате! 👀", "Анализирую контекст беседы 🔍", "Участвую в обсуждении 💬"]
            topic = "деятельность"
            should_respond = True
        elif any(word in last_message for word in ['спасибо', 'благодарю', 'thanks']):
            responses = ["Пожалуйста! 😊", "Всегда рад помочь! 🤝", "Не за что! 💙"]
            topic = "благодарность"
            should_respond = True
        elif any(word in last_message for word in ['хорошо', 'отлично', 'супер', 'класс', 'круто']):
            responses = ["Рад это слышать! 😊", "Здорово! 👍", "Отличные новости! 🎉"]
            topic = "позитив"
            should_respond = True
        elif any(word in last_message for word in ['плохо', 'грустно', 'печально', 'проблем']):
            responses = ["Сочувствую 😔", "Надеюсь, всё наладится! 💪", "Держитесь! 🤗"]
            topic = "поддержка"
            should_respond = True
        elif '?' in last_message:
            responses = ["Интересный вопрос! 🤔", "Хорошо спрашиваете! 💭", "А что вы сами думаете? 🧠"]
            topic = "вопрос"
            should_respond = True
        else:
            # Увеличиваем вероятность ответа до 70% для демонстрации
            should_respond = random.random() < 0.7
            responses = self.fallback_responses
            topic = topic or "общение"
        
        if should_respond:
            response = random.choice(responses)
            sentiment = 0.7  # Позитивный
        else:
            response = None
            sentiment = 0.5  # Нейтральный
        
        return {
            "detected_topic": topic or "общение",
            "sentiment": sentiment,
            "should_respond": should_respond,
            "response": response
        }

    async def analyze_context_and_generate_response(
        self, 
        context_messages: List[str], 
        chat_title: str = None
    ) -> Dict:
        """
        Анализирует контекст и генерирует ответ
        
        Returns:
            Dict с полями: detected_topic, sentiment, should_respond, response
        """
        try:
            logger.info(f"🧠 Анализируем {len(context_messages)} сообщений...")
            
            # Подготавливаем контекст для OpenAI
            context_text = "\n".join([f"- {msg}" for msg in context_messages[-5:]])
            
            system_prompt = f"""
Ты умный помощник в групповом чате "{chat_title or 'Группа'}".

Твоя задача:
1. Проанализировать последние сообщения
2. Определить тему разговора
3. Оценить эмоциональный тон (sentiment от -1 до 1)
4. Решить, стоит ли отвечать (should_respond: true/false)
5. Если да - сгенерировать уместный ответ

Отвечай естественно, как участник беседы. Будь полезным, но не навязчивым.
Отвечай на русском языке.

Верни ответ в JSON формате:
{{
    "detected_topic": "тема разговора",
    "sentiment": число_от_-1_до_1,
    "should_respond": true/false,
    "response": "твой ответ или null"
}}
"""

            user_prompt = f"""
Последние сообщения в чате:
{context_text}

Проанализируй контекст и реши, стоит ли отвечать.
"""

            # Пробуем OpenAI API
            try:
                response = await client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                
                content = response.choices[0].message.content.strip()
                logger.info(f"✅ Получен ответ от OpenAI: {content[:100]}...")
                
                # Парсим JSON ответ
                try:
                    result = json.loads(content)
                    logger.info(f"🎯 AI результат: {result}")
                    return result
                except json.JSONDecodeError:
                    logger.warning("⚠️ Не удалось распарсить JSON от OpenAI, используем fallback")
                    return self._get_fallback_response(context_messages)
                    
            except Exception as openai_error:
                logger.error(f"❌ Ошибка OpenAI API: {openai_error}")
                
                # Если ошибка квоты - используем fallback
                if "429" in str(openai_error) or "quota" in str(openai_error).lower():
                    logger.info("💡 Квота OpenAI исчерпана, используем fallback режим")
                    return self._get_fallback_response(context_messages)
                else:
                    # Для других ошибок тоже fallback
                    logger.info("💡 OpenAI недоступен, используем fallback режим")
                    return self._get_fallback_response(context_messages)
                
        except Exception as e:
            logger.error(f"❌ Ошибка AI сервиса: {e}")
            return self._get_fallback_response(context_messages)
    
    def should_respond_based_on_frequency(
        self, 
        recent_messages_count: int, 
        bot_responses_count: int
    ) -> bool:
        """
        Определяет, стоит ли отвечать на основе частоты ответов
        
        Args:
            recent_messages_count: Количество недавних сообщений
            bot_responses_count: Количество ответов бота
        """
        if recent_messages_count == 0:
            return False
            
        # Если бот не отвечал последние N сообщений - можно ответить
        if bot_responses_count == 0 and recent_messages_count >= config.response_frequency:
            return True
            
        # Соотношение ответов к сообщениям не должно превышать 1:N
        response_ratio = bot_responses_count / recent_messages_count
        target_ratio = 1.0 / config.response_frequency
        
        return response_ratio < target_ratio
    
    def extract_topic_keywords(self, text: str) -> List[str]:
        """Извлекает ключевые слова из текста"""
        # Простая реализация - можно улучшить
        words = re.findall(r'\b\w{4,}\b', text.lower())
        # Фильтруем стоп-слова
        stop_words = {'это', 'того', 'этого', 'такой', 'такая', 'такие', 'очень', 'более', 'самый'}
        keywords = [word for word in words if word not in stop_words]
        return keywords[:5]  # Топ 5 ключевых слов


# Глобальный экземпляр сервиса
ai_service = AIService() 