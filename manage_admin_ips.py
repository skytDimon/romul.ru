#!/usr/bin/env python3
"""
Утилита для управления административными IP-адресами
"""

import os
import sys
from typing import List

def get_current_ips() -> List[str]:
    """Получить текущие IP-адреса из переменной окружения или настроек по умолчанию"""
    admin_ips_env = os.getenv("ADMIN_IPS", "")
    if admin_ips_env:
        return [ip.strip() for ip in admin_ips_env.split(",") if ip.strip()]
    
    # IP по умолчанию
    return ["127.0.0.1", "::1"]

def set_admin_ips(ips: List[str]):
    """Установить IP-адреса через переменную окружения"""
    os.environ["ADMIN_IPS"] = ",".join(ips)
    print(f"✅ Установлены административные IP-адреса: {', '.join(ips)}")

def add_ip(ip: str):
    """Добавить IP-адрес к списку"""
    current_ips = get_current_ips()
    if ip not in current_ips:
        current_ips.append(ip)
        set_admin_ips(current_ips)
        print(f"✅ IP-адрес {ip} добавлен")
    else:
        print(f"⚠️  IP-адрес {ip} уже в списке")

def remove_ip(ip: str):
    """Удалить IP-адрес из списка"""
    current_ips = get_current_ips()
    if ip in current_ips:
        current_ips.remove(ip)
        set_admin_ips(current_ips)
        print(f"✅ IP-адрес {ip} удален")
    else:
        print(f"⚠️  IP-адрес {ip} не найден в списке")

def list_ips():
    """Показать текущие IP-адреса"""
    current_ips = get_current_ips()
    print("📋 Текущие административные IP-адреса:")
    for i, ip in enumerate(current_ips, 1):
        print(f"  {i}. {ip}")

def get_my_ip():
    """Показать текущий внешний IP-адрес"""
    try:
        import requests
        response = requests.get("https://httpbin.org/ip", timeout=5)
        ip = response.json()["origin"]
        print(f"🌐 Ваш текущий внешний IP-адрес: {ip}")
        return ip
    except Exception as e:
        print(f"❌ Не удалось получить внешний IP: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("🔧 Управление административными IP-адресами")
        print("\nИспользование:")
        print("  python manage_admin_ips.py list                    # Показать текущие IP")
        print("  python manage_admin_ips.py add <IP>               # Добавить IP")
        print("  python manage_admin_ips.py remove <IP>            # Удалить IP")
        print("  python manage_admin_ips.py myip                   # Показать мой IP")
        print("  python manage_admin_ips.py add-my-ip              # Добавить мой IP")
        print("\nПримеры:")
        print("  python manage_admin_ips.py add 192.168.1.100")
        print("  python manage_admin_ips.py add 203.0.113.0/24     # Добавить подсеть")
        return

    command = sys.argv[1].lower()
    
    if command == "list":
        list_ips()
    elif command == "add" and len(sys.argv) > 2:
        add_ip(sys.argv[2])
    elif command == "remove" and len(sys.argv) > 2:
        remove_ip(sys.argv[2])
    elif command == "myip":
        get_my_ip()
    elif command == "add-my-ip":
        ip = get_my_ip()
        if ip:
            add_ip(ip)
    else:
        print("❌ Неизвестная команда или недостаточно параметров")

if __name__ == "__main__":
    main()
