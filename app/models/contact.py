from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ContactMessage(BaseModel):
    """Модель контактного сообщения"""
    
    id: Optional[int] = None
    telegram: str = Field(..., description="Telegram username")
    message: str = Field(..., description="Текст сообщения")
    created_at: datetime = Field(default_factory=datetime.now)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    status: str = Field(default="pending", description="Статус обработки")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ContactResponse(BaseModel):
    """Ответ на отправку сообщения"""
    
    success: bool
    message: str
    message_id: Optional[int] = None
