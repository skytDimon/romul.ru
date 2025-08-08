from fastapi import APIRouter, Depends
from app.services.telegram_service import TelegramService
from config.settings import get_settings

router = APIRouter(prefix="/api/v1/health", tags=["Health"])


def get_telegram_service() -> TelegramService:
    """Dependency для получения сервиса Telegram"""
    return TelegramService()


@router.get("/")
async def health_check():
    """
    Проверка здоровья сервиса
    
    Returns:
        Dict с информацией о состоянии сервиса
    """
    settings = get_settings()
    
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }


@router.get("/telegram")
async def telegram_health(
    telegram_service: TelegramService = Depends(get_telegram_service)
):
    """
    Проверка подключения к Telegram Bot API
    
    Returns:
        Dict с информацией о состоянии Telegram
    """
    try:
        bot_info = await telegram_service.get_bot_info()
        
        if bot_info["success"]:
            return {
                "status": "connected",
                "bot_info": bot_info["data"],
                "message": "Telegram Bot API доступен"
            }
        else:
            return {
                "status": "error",
                "error": bot_info.get("error", "Неизвестная ошибка"),
                "message": "Telegram Bot API недоступен"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Ошибка проверки Telegram Bot API"
        }


@router.get("/detailed")
async def detailed_health_check(
    telegram_service: TelegramService = Depends(get_telegram_service)
):
    """
    Детальная проверка всех компонентов системы
    
    Returns:
        Dict с детальной информацией о состоянии
    """
    settings = get_settings()
    
    # Проверяем Telegram
    telegram_status = await telegram_health(telegram_service)
    
    return {
        "status": "healthy" if telegram_status["status"] == "connected" else "degraded",
        "service": settings.APP_NAME,
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "components": {
            "telegram": telegram_status
        },
        "timestamp": "2024-08-07T23:11:00Z"  # В реальном проекте использовать datetime.now().isoformat()
    }
