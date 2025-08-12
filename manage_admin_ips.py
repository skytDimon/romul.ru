#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Утилита для управления административными IP-адресами
"""

import os
import sys
from typing import List

def safe_print(text):
    """Безопасный вывод текста с обработкой кодировки"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Если не удается вывести Unicode, заменяем проблемные символы
        print(text.encode('ascii', 'replace').decode('ascii'))

def get_current_ips() -> List[str]:
    """Получить текущие IP-адреса из переменной окружения или настроек по умолчанию"""
    admin_ips_env = os.getenv("ADMIN_IPS", "")
    if admin_ips_env:
        return [ip.strip() for ip in admin_ips_env.split(",") if ip.strip()]
    
    # IP по умолчанию
    return [
        "127.0.0.1",        # Локальный IPv4
        "::1",              # Локальный IPv6
        # Добавьте ваши IP-адреса здесь (раскомментируйте нужные):
        "192.168.1.100",    # Пример домашнего IP
        # "203.0.113.50",   # Пример внешнего IP
        # "10.0.0.0/8",     # Пример подсети
    ]

def set_admin_ips(ips: List[str]):
    """Установить IP-адреса через переменную окружения"""
    os.environ["ADMIN_IPS"] = ",".join(ips)
    safe_print(f"[OK] Установлены административные IP-адреса: {', '.join(ips)}")

def add_ip(ip: str):
    """Добавить IP-адрес к списку"""
    current_ips = get_current_ips()
    if ip not in current_ips:
        current_ips.append(ip)
        set_admin_ips(current_ips)
        safe_print(f"[OK] IP-адрес {ip} добавлен")
    else:
        safe_print(f"[WARNING] IP-адрес {ip} уже в списке")

def remove_ip(ip: str):
    """Удалить IP-адрес из списка"""
    current_ips = get_current_ips()
    if ip in current_ips:
        current_ips.remove(ip)
        set_admin_ips(current_ips)
        safe_print(f"[OK] IP-адрес {ip} удален")
    else:
        safe_print(f"[WARNING] IP-адрес {ip} не найден в списке")

def list_ips():
    """Показать текущие IP-адреса"""
    current_ips = get_current_ips()
    safe_print("[INFO] Текущие административные IP-адреса:")
    for i, ip in enumerate(current_ips, 1):
        safe_print(f"  {i}. {ip}")

def get_my_ip():
    """Показать текущий внешний IP-адрес"""
    try:
        import requests
        response = requests.get("https://httpbin.org/ip", timeout=5)
        ip = response.json()["origin"]
        safe_print(f"[INFO] Ваш текущий внешний IP-адрес: {ip}")
        return ip
    except Exception as e:
        safe_print(f"[ERROR] Не удалось получить внешний IP: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        safe_print("[INFO] Управление административными IP-адресами")
        safe_print("\nИспользование:")
        safe_print("  python manage_admin_ips.py list                    # Показать текущие IP")
        safe_print("  python manage_admin_ips.py add <IP>               # Добавить IP")
        safe_print("  python manage_admin_ips.py remove <IP>            # Удалить IP")
        safe_print("  python manage_admin_ips.py myip                   # Показать мой IP")
        safe_print("  python manage_admin_ips.py add-my-ip              # Добавить мой IP")
        safe_print("\nПримеры:")
        safe_print("  python manage_admin_ips.py add 192.168.1.100")
        safe_print("  python manage_admin_ips.py add 203.0.113.0/24     # Добавить подсеть")
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
        safe_print("[ERROR] Неизвестная команда или недостаточно параметров")

if __name__ == "__main__":
    main()
