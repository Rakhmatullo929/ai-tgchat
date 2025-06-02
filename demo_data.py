"""
Скрипт для создания демонстрационных данных
"""
from datetime import datetime, timedelta
import random
from models import db_manager, ChatInteraction

def create_demo_data():
    """Создает демонстрационные данные в базе"""
    
    # Демо-чаты
    demo_chats = [
        {"chat_id": "-1001234567890", "chat_title": "Команда разработки"},
        {"chat_id": "-1001234567891", "chat_title": "Общий чат"},
        {"chat_id": "-1001234567892", "chat_title": "Обсуждение проектов"},
        {"chat_id": "-1001234567893", "chat_title": "Геймеры"},
    ]
    
    # Демо-сообщения для разных тем
    demo_topics = {
        "работа": {
            "messages": [
                "Когда дедлайн проекта?",
                "Нужно обсудить архитектуру",
                "Код ревью готов",
                "Встреча в 15:00",
                "Баги исправлены"
            ],
            "responses": [
                "Отличная работа команда! 👏",
                "Может стоит обсудить это подробнее?",
                "Я согласен с предложением",
                "Хорошая идея! 💡",
                "Давайте созвонимся"
            ]
        },
        "технологии": {
            "messages": [
                "Что думаете о новом Python 3.12?",
                "FastAPI или Django?",
                "Кто пробовал Claude API?",
                "Kubernetes сложный?",
                "AI революция началась"
            ],
            "responses": [
                "Интересная технология! 🚀",
                "Пробовал, очень круто!",
                "Есть свои плюсы и минусы",
                "Согласен, перспективно",
                "Нужно изучить подробнее"
            ]
        },
        "общение": {
            "messages": [
                "Как дела?",
                "Хороших выходных!",
                "Погода отличная",
                "Кто в кино?",
                "Встретимся завтра"
            ],
            "responses": [
                "Отлично, спасибо! 😊",
                "И вам хороших!",
                "Да, солнышко радует",
                "С удовольствием!",
                "Договорились! 👍"
            ]
        }
    }
    
    sentiments = ["positive", "neutral", "negative"]
    sentiment_weights = [0.6, 0.3, 0.1]  # Больше позитивных
    
    print("🔄 Создание демонстрационных данных...")
    
    # Создаем данные за последние 7 дней
    for i in range(50):
        # Случайный чат
        chat = random.choice(demo_chats)
        
        # Случайная тема
        topic_name = random.choice(list(demo_topics.keys()))
        topic_data = demo_topics[topic_name]
        
        # Случайное время в последние 7 дней
        days_ago = random.randint(0, 7)
        hours_ago = random.randint(0, 23)
        timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
        
        # Генерируем контекст сообщений
        context_messages = random.sample(topic_data["messages"], k=random.randint(3, 5))
        
        # Решаем, генерировать ли ответ
        response_generated = random.random() < 0.4  # 40% шанс ответа
        bot_response = None
        
        if response_generated:
            bot_response = random.choice(topic_data["responses"])
        
        # Случайное настроение
        sentiment = random.choices(sentiments, weights=sentiment_weights)[0]
        
        # Создаем взаимодействие
        interaction_data = {
            'chat_id': chat["chat_id"],
            'chat_title': chat["chat_title"],
            'context_messages': context_messages,
            'detected_topic': topic_name,
            'sentiment': sentiment,
            'bot_response': bot_response,
            'response_generated': response_generated,
            'participants_count': random.randint(3, 12)
        }
        
        try:
            # Создаем объект с кастомным временем
            interaction = ChatInteraction.from_dict(interaction_data)
            interaction.timestamp = timestamp
            
            session = db_manager.get_session()
            session.add(interaction)
            session.commit()
            session.close()
            
        except Exception as e:
            print(f"❌ Ошибка создания записи: {e}")
    
    print("✅ Демонстрационные данные созданы!")
    print(f"📊 Всего записей в БД: {db_manager.get_total_interactions()}")


if __name__ == "__main__":
    create_demo_data()