"""
Модели базы данных
"""
from datetime import datetime
from typing import Dict, List, Any
import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import config

Base = declarative_base()


class ChatInteraction(Base):
    """Модель для хранения взаимодействий в чатах"""
    
    __tablename__ = "chat_interactions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    chat_id = Column(String(50), nullable=False, index=True)
    chat_title = Column(String(255), nullable=True)
    context_messages = Column(JSON, nullable=False)  # Список последних сообщений
    detected_topic = Column(String(255), nullable=True)
    sentiment = Column(String(20), nullable=True)  # positive, neutral, negative
    bot_response = Column(Text, nullable=True)
    response_generated = Column(Boolean, default=False, nullable=False)
    participants_count = Column(Integer, default=0, nullable=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект в словарь"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'chat_id': self.chat_id,
            'chat_title': self.chat_title,
            'context_messages': self.context_messages,
            'detected_topic': self.detected_topic,
            'sentiment': self.sentiment,
            'bot_response': self.bot_response,
            'response_generated': self.response_generated,
            'participants_count': self.participants_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatInteraction':
        """Создает объект из словаря"""
        return cls(
            chat_id=data['chat_id'],
            chat_title=data.get('chat_title'),
            context_messages=data['context_messages'],
            detected_topic=data.get('detected_topic'),
            sentiment=data.get('sentiment'),
            bot_response=data.get('bot_response'),
            response_generated=data.get('response_generated', False),
            participants_count=data.get('participants_count', 0)
        )


class DatabaseManager:
    """Менеджер для работы с базой данных"""
    
    def __init__(self, database_url: str = None):
        self.database_url = database_url or config.database_url
        self.engine = create_engine(self.database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Создаем таблицы
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Получает сессию базы данных"""
        return self.SessionLocal()
    
    def save_interaction(self, interaction_data: Dict[str, Any]) -> ChatInteraction:
        """Сохраняет взаимодействие в базу данных"""
        session = self.get_session()
        try:
            interaction = ChatInteraction.from_dict(interaction_data)
            session.add(interaction)
            session.commit()
            session.refresh(interaction)
            return interaction
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_chat_history(self, chat_id: str, limit: int = 50) -> List[ChatInteraction]:
        """Получает историю чата"""
        session = self.get_session()
        try:
            interactions = session.query(ChatInteraction)\
                .filter(ChatInteraction.chat_id == chat_id)\
                .order_by(ChatInteraction.timestamp.desc())\
                .limit(limit)\
                .all()
            return interactions
        finally:
            session.close()
    
    def get_total_interactions(self) -> int:
        """Получает общее количество взаимодействий"""
        session = self.get_session()
        try:
            return session.query(ChatInteraction).count()
        finally:
            session.close()


# Глобальный экземпляр менеджера базы данных
db_manager = DatabaseManager() 