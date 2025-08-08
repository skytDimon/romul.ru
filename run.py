#!/usr/bin/env python3
"""
Скрипт для запуска приложения Romulus et Remus
"""

import uvicorn
import sys
import os
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import get_settings


def main():
    """Основная функция запуска"""
    settings = get_settings()
    
    print(f"🚀 Запуск {settings.APP_NAME}")
    print(f"📊 Режим: {settings.ENVIRONMENT}")
    print(f"🌐 Адрес: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"🔍 Health Check: http://{settings.HOST}:{settings.PORT}/health")
    print("-" * 50)
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )


if __name__ == "__main__":
    main()
