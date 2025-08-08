# 🏛️ Romulus et Remus - Масштабируемая архитектура

> **Не одежда. Отношение.**

Современное веб-приложение для продажи премиальной одежды с архитектурой, готовой к масштабированию.

## 🚀 Возможности

### ✅ Реализовано
- **Модульная архитектура** - разделение на слои (API, Services, Models)
- **RESTful API** - полный набор эндпоинтов для всех операций
- **Валидация данных** - Pydantic модели для типобезопасности
- **Логирование** - структурированное логирование с настройкой уровней
- **Безопасность** - валидация ввода, защита от XSS
- **Конфигурация** - гибкая система настроек для разных окружений
- **Тестирование** - полный набор unit и integration тестов
- **Документация API** - автоматическая генерация Swagger/OpenAPI
- **Health Checks** - мониторинг состояния сервиса
- **Telegram интеграция** - отправка заявок в Telegram

### 🔮 Планируется
- **База данных** - PostgreSQL с SQLAlchemy и Alembic
- **Кэширование** - Redis для улучшения производительности
- **Аутентификация** - JWT токены для API
- **Rate Limiting** - защита от DDoS
- **Мониторинг** - Prometheus + Grafana
- **Docker** - контейнеризация для деплоя
- **CI/CD** - автоматическое тестирование и деплой

## 📁 Структура проекта

```
romulai/
├── app/                          # Основное приложение
│   ├── api/                      # API роуты
│   │   ├── contact.py           # Контактные сообщения
│   │   ├── products.py          # Продукты и категории
│   │   └── health.py            # Health checks
│   ├── core/                     # Ядро приложения
│   ├── models/                   # Pydantic модели
│   │   ├── contact.py           # Модели сообщений
│   │   └── product.py           # Модели продуктов
│   ├── services/                 # Бизнес-логика
│   │   ├── contact_service.py   # Обработка сообщений
│   │   ├── product_service.py   # Управление продуктами
│   │   └── telegram_service.py  # Telegram API
│   ├── static/                   # Статические файлы
│   │   ├── css/                 # Стили
│   │   ├── js/                  # JavaScript
│   │   └── img/                 # Изображения
│   ├── templates/                # HTML шаблоны
│   ├── utils/                    # Утилиты
│   │   ├── logging.py           # Настройка логирования
│   │   └── security.py          # Безопасность
│   └── main.py                   # Точка входа
├── config/                       # Конфигурация
│   └── settings.py              # Настройки приложения
├── tests/                        # Тесты
│   └── test_api.py              # API тесты
├── requirements.txt              # Зависимости
├── run.py                       # Скрипт запуска
└── README.md                    # Документация
```

## 🛠️ Установка и запуск

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка окружения
Создайте файл `.env` в корне проекта:
```env
ENVIRONMENT=development
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
LOG_LEVEL=INFO
```

### 3. Запуск приложения
```bash
python run.py
```

Или напрямую:
```bash
python -m app.main
```

## 🌐 Доступные URL

### Веб-страницы
- **Главная**: http://localhost:8000/
- **Acne Studios**: http://localhost:8000/acne
- **HP Health**: http://localhost:8000/hphealth
- **Zip Hoodie**: http://localhost:8000/zip
- **Poizon**: http://localhost:8000/poizon

### API Endpoints
- **Документация API**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Детальный Health**: http://localhost:8000/api/v1/health/detailed

### API v1
- **Продукты**: `GET /api/v1/products/`
- **Категории**: `GET /api/v1/products/categories/`
- **Поиск**: `GET /api/v1/products/search/?q=query`
- **Отправка сообщений**: `POST /api/v1/contact/send`

## 🧪 Тестирование

### Запуск тестов
```bash
pytest tests/
```

### Запуск с покрытием
```bash
pytest tests/ --cov=app --cov-report=html
```

## 📊 API Документация

После запуска сервера откройте:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Конфигурация

### Настройки в `config/settings.py`:

```python
# Основные настройки
APP_NAME = "Romulus et Remus"
ENVIRONMENT = "development"  # development/production
DEBUG = False

# Сервер
HOST = "0.0.0.0"
PORT = 8000

# Telegram
TELEGRAM_BOT_TOKEN = "your_token"
TELEGRAM_CHAT_ID = 123456789

# Логирование
LOG_LEVEL = "INFO"
LOG_FILE = "logs/app.log"
```

## 🚀 Масштабирование

### Горизонтальное масштабирование
- **Load Balancer** - распределение нагрузки
- **Микросервисы** - разделение на отдельные сервисы
- **Кэширование** - Redis для сессий и данных
- **CDN** - для статических файлов

### Вертикальное масштабирование
- **База данных** - PostgreSQL с оптимизацией
- **Асинхронность** - FastAPI + async/await
- **Кэширование** - in-memory кэш
- **Оптимизация запросов** - индексы, connection pooling

## 🔒 Безопасность

- ✅ **Валидация ввода** - защита от XSS и инъекций
- ✅ **CORS** - настройка cross-origin запросов
- ✅ **Trusted Hosts** - защита от host header атак
- 🔄 **Rate Limiting** - защита от DDoS (в разработке)
- 🔄 **JWT Auth** - аутентификация API (в разработке)

## 📈 Мониторинг

- ✅ **Health Checks** - проверка состояния сервиса
- ✅ **Структурированное логирование** - для анализа
- 🔄 **Prometheus метрики** - мониторинг производительности
- 🔄 **Grafana дашборды** - визуализация метрик

## 🐳 Docker (планируется)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "run.py"]
```

## 🤝 Разработка

### Code Style
```bash
# Форматирование кода
black app/ tests/

# Сортировка импортов
isort app/ tests/

# Проверка типов
mypy app/

# Линтинг
flake8 app/ tests/
```

### Git Hooks
```bash
# Pre-commit hooks для автоматической проверки
pre-commit install
```

## 📝 Лицензия

MIT License

---

**Romulus et Remus** - Не одежда. Отношение. 🏛️
