import logging
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from config.settings import get_settings
from app.api import contact_router, products_router, health_router
from app.utils.logging import setup_logging
from app.services.contact_service import ContactService
from app.middleware import IPRestrictionMiddleware


# Настройка логирования
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Startup
    logger.info("🚀 Запуск приложения Romulus et Remus")
    logger.info(f"📊 Режим: {get_settings().ENVIRONMENT}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Остановка приложения")


# Создание FastAPI приложения
app = FastAPI(
    title=get_settings().APP_NAME,
    description=get_settings().APP_DESCRIPTION,
    version="1.0.0",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ограничение доступа к административным эндпоинтам по IP
app.add_middleware(
    IPRestrictionMiddleware,
    admin_ips=get_settings().ADMIN_IPS,
    restricted_paths=["/docs", "/redoc", "/openapi.json", "/health"]
)

# Trusted Host middleware для безопасности
if get_settings().ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=get_settings().ALLOWED_HOSTS
    )

# Подключение API роутов
app.include_router(contact_router)
app.include_router(products_router)
app.include_router(health_router)

# Настройка шаблонов
templates = Jinja2Templates(directory=get_settings().TEMPLATES_DIR)

# Подключение статических файлов
app.mount("/static", StaticFiles(directory=get_settings().STATIC_DIR), name="static")


# Web страницы
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Главная страница"""
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        logger.error(f"Ошибка загрузки главной страницы: {str(e)}")
        raise


@app.get("/acne", response_class=HTMLResponse)
async def acne_page(request: Request):
    """Страница Acne Studios"""
    try:
        return templates.TemplateResponse("acne.html", {"request": request})
    except Exception as e:
        logger.error(f"Ошибка загрузки страницы Acne: {str(e)}")
        raise


@app.get("/hphealth", response_class=HTMLResponse)
async def hphealth_page(request: Request):
    """Страница HP Health"""
    try:
        return templates.TemplateResponse("hphealth.html", {"request": request})
    except Exception as e:
        logger.error(f"Ошибка загрузки страницы HP Health: {str(e)}")
        raise


@app.get("/zip", response_class=HTMLResponse)
async def zip_page(request: Request):
    """Страница Zip Hoodie"""
    try:
        return templates.TemplateResponse("zip.html", {"request": request})
    except Exception as e:
        logger.error(f"Ошибка загрузки страницы Zip: {str(e)}")
        raise


@app.get("/poizon", response_class=HTMLResponse)
async def poizon_page(request: Request):
    """Страница Poizon"""
    try:
        return templates.TemplateResponse("poizon.html", {"request": request})
    except Exception as e:
        logger.error(f"Ошибка загрузки страницы Poizon: {str(e)}")
        raise


# Legacy endpoint для обратной совместимости
@app.post("/send-message")
async def send_message_legacy(
    request: Request,
    telegram: str = Form(...),
    message: str = Form(...)
):
    """Legacy endpoint для отправки сообщений (для обратной совместимости)"""
    try:
        contact_service = ContactService()
        
        # Получаем информацию о клиенте
        from app.utils.security import get_client_ip
        client_ip = get_client_ip(request)
        user_agent = request.headers.get("user-agent")
        
        # Обрабатываем сообщение
        result = await contact_service.process_contact_message(
            telegram=telegram,
            message=message,
            ip_address=client_ip,
            user_agent=user_agent
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения: {str(e)}")
        return {"success": False, "message": f"Ошибка: {str(e)}"}


# Health check для мониторинга
@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {
        "status": "healthy",
        "service": get_settings().APP_NAME,
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower()
    )
