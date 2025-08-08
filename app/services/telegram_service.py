import httpx
import logging
from typing import Optional, Dict, Any
from config.settings import get_settings

logger = logging.getLogger(__name__)


class TelegramService:
    """Сервис для работы с Telegram Bot API"""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_url = f"https://api.telegram.org/bot{self.settings.TELEGRAM_BOT_TOKEN}"
    
    async def send_message(
        self, 
        chat_id: int, 
        text: str, 
        parse_mode: str = "HTML",
        disable_web_page_preview: bool = True
    ) -> Dict[str, Any]:
        """
        Отправить сообщение в Telegram
        
        Args:
            chat_id: ID чата
            text: Текст сообщения
            parse_mode: Режим парсинга (HTML/Markdown)
            disable_web_page_preview: Отключить превью ссылок
            
        Returns:
            Dict с результатом отправки
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": text,
                        "parse_mode": parse_mode,
                        "disable_web_page_preview": disable_web_page_preview
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Сообщение отправлено в Telegram: {result.get('result', {}).get('message_id')}")
                    return {
                        "success": True,
                        "message_id": result.get("result", {}).get("message_id"),
                        "response": result
                    }
                else:
                    logger.error(f"Ошибка отправки в Telegram: {response.status_code} - {response.text}")
                    return {
                        "success": False,
                        "error": f"HTTP {response.status_code}",
                        "details": response.text
                    }
                    
        except httpx.TimeoutException:
            logger.error("Таймаут при отправке в Telegram")
            return {"success": False, "error": "Timeout"}
        except Exception as e:
            logger.error(f"Ошибка при отправке в Telegram: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def send_contact_form(
        self, 
        telegram: str, 
        message: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Отправить форму контакта в Telegram
        
        Args:
            telegram: Telegram username
            message: Текст сообщения
            ip_address: IP адрес пользователя
            user_agent: User-Agent браузера
            
        Returns:
            Dict с результатом отправки
        """
        # Формируем текст сообщения
        text = f"📨 <b>Новая заявка с сайта</b>\n\n"
        text += f"👤 <b>Telegram:</b> {telegram}\n"
        text += f"💬 <b>Сообщение:</b>\n{message}\n\n"
        
        if ip_address:
            text += f"🌐 <b>IP:</b> {ip_address}\n"
        if user_agent:
            text += f"🔍 <b>User-Agent:</b> {user_agent[:100]}...\n"
        
        text += f"⏰ <b>Время:</b> {self._get_current_time()}"
        
        return await self.send_message(
            chat_id=self.settings.TELEGRAM_CHAT_ID,
            text=text
        )
    
    def _get_current_time(self) -> str:
        """Получить текущее время в читаемом формате"""
        from datetime import datetime
        return datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    async def get_bot_info(self) -> Dict[str, Any]:
        """Получить информацию о боте"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/getMe")
                if response.status_code == 200:
                    return {"success": True, "data": response.json()}
                else:
                    return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
