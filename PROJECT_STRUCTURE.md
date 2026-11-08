# CKey API Gateway Service - Как собрать аккуратно

## Структура проекта

```
pycharmlicense/
├── ckey_api.py              # Основной API (FastAPI, production-ready)
├── ckey_service.py          # Упрощенный API для фонового запуска
├── ckey_api.py              # Original ckey_api (use for backup)
├── ckey_service_manager.py  # CLI менеджер сервиса
├── test_api_manager.py      # Тестовый инструмент
├── manager.py               # Обертка для testing
├── package.json             # npm scripts
├── Dockerfile              # Docker контейнер
├── install_service.bat     # Windows Service installer
├── quickstart.bat          # Быстрый старт Windows
├── .gitignore              # Git exclude
├── requirements.txt        # Python dependencies
├── README_SERVICE.md       # Документация
└── .venv/                  # Виртуальное окружение (create it)
```

## Быстрый старт

### 1. Установить зависимости
```bash
pip install -r requirements.txt
```

### 2. Запустить сервис
```bash
python ckey_service_manager.py start
```

### 3. Проверить
```bash
python ckey_service_manager.py test
```

## Управление

```bash
start    # Запустить
stop     # Остановить
restart  # Перезапустить
status   # Статус
test     # Проверка API
```

## API Endpoints

- POST `http://localhost:8000/api/license/generate` - генерация
- GET `http://localhost:8000/api/products` - список
- GET `http://localhost:8000/docs` - документация

## Products
- II - IntelliJ IDEA
- PC - PyCharm
- A - Android Studio
- CL - DataGrip
- J - JetBrains Rider

## Windows Service

```cmd
install_service.bat      # Установить службу
net start CKeyAPI         # Старт
net stop CKeyAPI          # Стоп
sc delete CKeyAPI         # Удалить
```

## Docker

```bash
docker build -t ckey-api .
docker run -d -p 8001:8000 ckey-api
```
