from fastapi import APIRouter, Form, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from app.models.contact import ContactResponse
from app.services.contact_service import ContactService
from config.settings import get_settings

router = APIRouter(prefix="/api/v1/contact", tags=["Contact"])


def get_contact_service() -> ContactService:
    """Dependency для получения сервиса контактов"""
    return ContactService()


@router.post("/send", response_model=ContactResponse)
async def send_message(
    request: Request,
    telegram: str = Form(...),
    message: str = Form(...),
    contact_service: ContactService = Depends(get_contact_service)
):
    """
    Отправить контактное сообщение
    
    Args:
        telegram: Telegram username
        message: Текст сообщения
        
    Returns:
        ContactResponse с результатом отправки
    """
    try:
        # Получаем информацию о клиенте
        client_ip = request.client.host if request.client else None
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
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка обработки сообщения: {str(e)}"
        )


@router.get("/messages")
async def get_messages(
    limit: int = 50,
    offset: int = 0,
    contact_service: ContactService = Depends(get_contact_service)
):
    """
    Получить список сообщений (для админки)
    
    Args:
        limit: Количество сообщений
        offset: Смещение
        
    Returns:
        Dict с сообщениями
    """
    try:
        result = await contact_service.get_messages(limit=limit, offset=offset)
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Неизвестная ошибка")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка получения сообщений: {str(e)}"
        )


@router.get("/messages/{message_id}")
async def get_message(
    message_id: int,
    contact_service: ContactService = Depends(get_contact_service)
):
    """
    Получить сообщение по ID
    
    Args:
        message_id: ID сообщения
        
    Returns:
        ContactMessage
    """
    try:
        message = await contact_service.get_message_by_id(message_id)
        
        if not message:
            raise HTTPException(
                status_code=404,
                detail=f"Сообщение с ID {message_id} не найдено"
            )
        
        return message
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка получения сообщения: {str(e)}"
        )
