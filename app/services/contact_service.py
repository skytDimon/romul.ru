import logging
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.contact import ContactMessage, ContactResponse
from app.services.telegram_service import TelegramService
from config.settings import get_settings

logger = logging.getLogger(__name__)


class ContactService:
    """Сервис для обработки контактных сообщений"""
    
    def __init__(self):
        self.settings = get_settings()
        self.telegram_service = TelegramService()
        # В будущем здесь будет подключение к базе данных
        self._messages = []  # Временное хранилище в памяти
    
    async def process_contact_message(
        self,
        telegram: str,
        message: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> ContactResponse:
        """
        Обработать контактное сообщение
        
        Args:
            telegram: Telegram username
            message: Текст сообщения
            ip_address: IP адрес пользователя
            user_agent: User-Agent браузера
            
        Returns:
            ContactResponse с результатом обработки
        """
        try:
            # Создаем объект сообщения
            contact_message = ContactMessage(
                telegram=telegram,
                message=message,
                ip_address=ip_address,
                user_agent=user_agent,
                created_at=datetime.now()
            )
            
            # Сохраняем в "базу данных" (пока в память)
            contact_message.id = len(self._messages) + 1
            self._messages.append(contact_message)
            
            # Отправляем в Telegram
            telegram_result = await self.telegram_service.send_contact_form(
                telegram=telegram,
                message=message,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            if telegram_result["success"]:
                contact_message.status = "sent"
                logger.info(f"Сообщение {contact_message.id} успешно отправлено в Telegram")
                return ContactResponse(
                    success=True,
                    message="Сообщение отправлено!",
                    message_id=contact_message.id
                )
            else:
                contact_message.status = "failed"
                logger.error(f"Ошибка отправки сообщения {contact_message.id}: {telegram_result.get('error')}")
                return ContactResponse(
                    success=False,
                    message=f"Ошибка отправки: {telegram_result.get('error', 'Неизвестная ошибка')}"
                )
                
        except Exception as e:
            logger.error(f"Ошибка обработки контактного сообщения: {str(e)}")
            return ContactResponse(
                success=False,
                message=f"Ошибка обработки: {str(e)}"
            )
    
    async def get_messages(
        self, 
        limit: int = 50, 
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Получить список сообщений (для админки)
        
        Args:
            limit: Количество сообщений
            offset: Смещение
            
        Returns:
            Dict с сообщениями и метаданными
        """
        try:
            messages = self._messages[offset:offset + limit]
            return {
                "success": True,
                "messages": [msg.dict() for msg in messages],
                "total": len(self._messages),
                "limit": limit,
                "offset": offset
            }
        except Exception as e:
            logger.error(f"Ошибка получения сообщений: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_message_by_id(self, message_id: int) -> Optional[ContactMessage]:
        """
        Получить сообщение по ID
        
        Args:
            message_id: ID сообщения
            
        Returns:
            ContactMessage или None
        """
        try:
            for message in self._messages:
                if message.id == message_id:
                    return message
            return None
        except Exception as e:
            logger.error(f"Ошибка получения сообщения {message_id}: {str(e)}")
            return None
