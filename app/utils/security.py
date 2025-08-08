import re
from typing import Optional
from fastapi import Request


def get_client_ip(request: Request) -> Optional[str]:
    """
    Получить реальный IP адрес клиента
    
    Args:
        request: FastAPI Request объект
        
    Returns:
        IP адрес или None
    """
    # Проверяем заголовки прокси
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Прямое подключение
    if request.client:
        return request.client.host
    
    return None


def validate_input(text: str, max_length: int = 1000) -> bool:
    """
    Валидация пользовательского ввода
    
    Args:
        text: Текст для валидации
        max_length: Максимальная длина
        
    Returns:
        True если валидно, False иначе
    """
    if not text or not isinstance(text, str):
        return False
    
    if len(text) > max_length:
        return False
    
    # Проверяем на потенциально опасные символы
    dangerous_patterns = [
        r'<script.*?>',  # XSS
        r'javascript:',   # JavaScript injection
        r'data:text/html', # Data URL injection
        r'vbscript:',    # VBScript injection
        r'on\w+\s*=',    # Event handlers
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    
    return True


def sanitize_telegram_username(username: str) -> str:
    """
    Очистка Telegram username
    
    Args:
        username: Исходный username
        
    Returns:
        Очищенный username
    """
    if not username:
        return ""
    
    # Убираем @ в начале если есть
    if username.startswith('@'):
        username = username[1:]
    
    # Оставляем только буквы, цифры и подчеркивания
    username = re.sub(r'[^a-zA-Z0-9_]', '', username)
    
    return username.lower()


def rate_limit_key(request: Request) -> str:
    """
    Генерирует ключ для rate limiting
    
    Args:
        request: FastAPI Request объект
        
    Returns:
        Ключ для rate limiting
    """
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("user-agent", "")
    
    # Простой ключ на основе IP и User-Agent
    return f"{client_ip}:{hash(user_agent) % 1000}"
