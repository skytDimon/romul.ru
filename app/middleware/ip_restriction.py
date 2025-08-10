import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import List
import ipaddress

logger = logging.getLogger(__name__)


class IPRestrictionMiddleware(BaseHTTPMiddleware):
    """
    Middleware для ограничения доступа к административным эндпоинтам по IP-адресам
    """
    
    def __init__(self, app, admin_ips: List[str], restricted_paths: List[str] = None):
        super().__init__(app)
        self.admin_ips = admin_ips
        self.restricted_paths = restricted_paths or ["/docs", "/redoc", "/openapi.json", "/health"]
        
        # Преобразуем IP-адреса в объекты для более эффективной проверки
        self.admin_networks = []
        for ip in admin_ips:
            try:
                # Поддерживаем как отдельные IP, так и сети (CIDR)
                self.admin_networks.append(ipaddress.ip_network(ip, strict=False))
            except ValueError:
                logger.warning(f"Некорректный IP-адрес в настройках: {ip}")
    
    async def dispatch(self, request: Request, call_next):
        """
        Проверяем доступ к административным эндпоинтам
        """
        path = request.url.path
        
        # Проверяем, является ли путь административным
        if any(path.startswith(restricted_path) for restricted_path in self.restricted_paths):
            client_ip = self._get_client_ip(request)
            
            if not self._is_admin_ip(client_ip):
                logger.warning(f"Попытка доступа к {path} с неразрешенного IP: {client_ip}")
                return JSONResponse(
                    status_code=403,
                    content={
                        "detail": "Access forbidden: Administrative endpoint",
                        "message": "У вас нет доступа к этому ресурсу"
                    }
                )
        
        response = await call_next(request)
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """
        Получаем реальный IP-адрес клиента с учетом прокси
        """
        # Проверяем заголовки прокси в порядке приоритета
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # X-Forwarded-For может содержать несколько IP через запятую
            # Берем первый (оригинальный клиент)
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()
        
        forwarded = request.headers.get("Forwarded")
        if forwarded:
            # Парсим заголовок Forwarded (RFC 7239)
            for part in forwarded.split(";"):
                if part.strip().startswith("for="):
                    ip = part.split("=")[1].strip().strip('"')
                    # Убираем порт если есть
                    if ":" in ip and not ip.startswith("["):
                        ip = ip.split(":")[0]
                    return ip
        
        # Если прокси заголовков нет, используем прямое соединение
        return request.client.host if request.client else "unknown"
    
    def _is_admin_ip(self, client_ip: str) -> bool:
        """
        Проверяем, находится ли IP-адрес в списке разрешенных
        """
        if client_ip == "unknown":
            return False
        
        try:
            client_addr = ipaddress.ip_address(client_ip)
            
            for network in self.admin_networks:
                if client_addr in network:
                    return True
            
            return False
            
        except ValueError:
            logger.warning(f"Некорректный IP-адрес клиента: {client_ip}")
            return False
