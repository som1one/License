# CKey API Gateway Service

Упрощенный и надежный сервис для получения лицензий.

## Быстрый старт

### 1. Установить зависимости
```bash
pip install -r requirements.txt
```

### 2. Запустить сервис
```bash
python ckey_service_manager.py start
```

### 3. Проверить работу
```bash
python ckey_service_manager.py test
```

### 4. Проверить статус
```bash
python ckey_service_manager.py status
```

## Управление

```bash
# Старт
python ckey_service_manager.py start

# Стоп
python ckey_service_manager.py stop

# Перезапуск
python ckey_service_manager.py restart

# Статус
python ckey_service_manager.py status

# Быстрая проверка API
python ckey_service_manager.py test
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info |
| `/status` | GET | Status check |
| `/products` | GET | List of products |
| `/license` | POST | Generate license |
| `/license/generate` | POST | Alternate license endpoint |

### Products
- **II** - IntelliJ IDEA
- **PC** - PyCharm
- **A** - Android Studio
- **CL** - DataGrip
- **J** - JetBrains Rider

### Examples

**Get products:**
```bash
curl http://localhost:8000/api/products
```

**Generate PyCharm license:**
```bash
curl -X POST http://localhost:8000/api/license \
  -H "Content-Type: application/json" \
  -d '{"product":"PC","name":"Test","expiry":"2099-12-31"}'
```

## Установка как Windows Service

```bash
# Запустить от имени администратора
install_service.bat
```

Управление службой:
```cmd
net start CKeyAPI      # Start
net stop CKeyAPI       # Stop
sc query CKeyAPI       # Status
sc delete CKeyAPI      # Uninstall
```

## Docker

```bash
# Build
docker build -t ckey-api:latest .

# Run
docker run -d -p 8000:8000 ckey-api:latest
```

## Production

Идеально для:
- Микросервисы
- Cron jobs
- Docker контейнеры
- Windows Service

Время инициализации: <500ms
Memory footprint: ~50MB
