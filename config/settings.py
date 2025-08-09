import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Основные настройки
    APP_NAME: str = "Romulus et Remus"
    APP_DESCRIPTION: str = "Не одежда. Отношение."
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # Сервер
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str = "7936936135:AAENnQtZ_u4C88PEHMYri5aNIyUqVXXKnEA"
    TELEGRAM_CHAT_ID: int = 821740830
    
    # База данных (для будущего расширения)
    DATABASE_URL: Optional[str] = None
    
    # Redis (для кэширования)
    REDIS_URL: Optional[str] = None
    
    # Логирование
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None
    
    # Безопасность
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALLOWED_HOSTS: list = ["*"]
    
    # API
    API_PREFIX: str = "/api/v1"
    
    # Статические файлы
    STATIC_DIR: str = "app/static"
    TEMPLATES_DIR: str = "app/templates"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Создаем экземпляр настроек
settings = Settings()


# Функции для получения настроек
def get_settings() -> Settings:
    """Получить настройки приложения"""
    return settings


def is_development() -> bool:
    """Проверить, что приложение в режиме разработки"""
    return settings.ENVIRONMENT == "development"


def is_production() -> bool:
    """Проверить, что приложение в продакшене"""
    return settings.ENVIRONMENT == "production"
