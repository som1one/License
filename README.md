# cKey API Gateway Service

Сервис для получения ключей от ckey.run через API gateway.

## Быстрый старт

### Windows

1. **Установить зависимости (один раз):**
```cmd
pip install -r requirements.txt
```

2. **Запустить сервис:**
```cmd
python ckey_service_manager.py start
```

3. **Проверить работу:**
```cmd
python ccheck_service_manager.py test
```

&

## Управление

| Команда | Действие |
|---------|----------|
| `python ccheck_service_manager.py start` | Запустить сервис |
| `python ccheck_service_manager.py stop` | Остановить сервис |
| `python ccheck_service_manager.py restart` | Перезапустить |
| `python ccheck_service_manager.py status` | Статус |
| `python ccheck_service_manager.py test` | Тест API |

## API Endpoints

### Основной эндпоинт для генерации:
```
POST http://localhost:8000/api/license/generate
```

### JSON payload:
```json
{
    "product": "PC",      // II, PC, A, CL, J
    "name": "Test License",
    "expiry": "2099-12-31",
    "assignee": "User Name"
}
```

### Get список продуктов:
```
GET http://localhost:8000/api/products
```

## Доступные продукты

- **II** - IntelliJ IDEA
- **PC** - PyCharm
- **A** - Android Studio
- **CL** - DataGrip
- **J** - JetBrains Rider

## Примеры запросов

### 1. PyCharm license
```bash
curl -X POST http://localhost:8000/api/license/generate \
  -H "Content-Type: application/json" \
  -d "{\"product\":\"PC\",\"name\":\"My License\",\"expiry\":\"2099-12-31\",\"assignee\":\"User\"}"
```

### 2. IntelliJ IDEA license
```bash
curl -X POST http://localhost:8000/api/license/generate \
  -H "Content-Type: application/json" \
  -d "{\"product\":\"II\",\"name\":\"My License\",\"expiry\":\"2099-12-31\",\"assignee\":\"User\"}"
```

### 3. Get products list
```bash
curl http://localhost:8000/api/products
```

## Windows как система

### Установка как Windows Service

```cmd
# Запустить от имени администратора
install_service.bat
```

### Управление службой

```cmd
net start CKeyAPI      # Старт
net stop CKeyAPI       # Стоп
sc query CKeyAPI       # Состояние
sc delete CKeyAPI      # Удалить
```

## Docker

```bash
# Build
docker build -t ckey-api:latest .

# Run
docker run -d -p 8000:8000 ckey-api:latest

# Stop
docker stop $(docker ps -q -f name=ckey-api)
```

## Ресурсы

- 📖 Swagger документация: http://localhost:8000/docs
- 📁 Структура проекта: PROJECT_STRUCTURE.md
- 📘 Документация API: README_API.md

## Технологии

- FastAPI - modern API framework
- Uvicorn - ASGI server
- Python 3.11+
- HTTP requests

## Лицензия

MIT

## Характеристики

- ⚡ Быстрая инициализация (<500ms)
- 💾 Малая нагрузка (~50MB RAM)
- 🚀 Доступно как сервис
- 🐳 Docker support
- 🖥️ Windows support
- 🔐 Защищенная цепочка запросов
- 🔧 Graceful shutdown
- 📊 Production-ready