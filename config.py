"""
Конфигурация приложения
"""
import os
from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import field_validator

# Загружаем переменные окружения
load_dotenv()


class Config(BaseSettings):
    """Настройки приложения"""
    
    # Telegram Bot
    telegram_bot_token: str
    
    # OpenAI
    openai_api_key: str
    
    # Database
    database_url: str = "sqlite:///bot_database.db"
    
    # Bot Settings
    bot_name: str = "SmartGroupBot"
    bot_personality: str = "Дружелюбный и умный помощник в групповых чатах"
    response_frequency: int = 2
    min_context_messages: int = 2
    max_context_messages: int = 10
    
    # Logging
    log_level: str = "INFO"
    
    @field_validator('telegram_bot_token')
    @classmethod
    def validate_telegram_token(cls, v):
        if not v or v == "your_telegram_bot_token_here":
            raise ValueError("TELEGRAM_BOT_TOKEN must be set")
        return v
    
    @field_validator('openai_api_key')
    @classmethod
    def validate_openai_key(cls, v):
        if not v or v == "your_openai_api_key_here":
            raise ValueError("OPENAI_API_KEY must be set")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Создаем экземпляр конфигурации
try:
    config = Config()
except Exception as e:
    print(f"❌ Ошибка конфигурации: {e}")
    print("Пожалуйста, создайте .env файл на основе config.env.example")
    exit(1) 