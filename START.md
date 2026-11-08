# cKey API Gateway - Инструкция по запуску

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск API сервера

Откройте терминал и запустите:

```bash
python ckey_api.py
```

Сервер будет запущен на `http://localhost:8000`

### 3. Доступ к API

После запуска у вас есть несколько способов использовать API:

---

## 🔌 Способы использования

### 🌐 Веб интерфейс

Откройте браузер и перейдите:

```
file:///D:/PycharmProjects/pycharmlicense/api_test.html
```

Это интерактивный веб-интерфейс для генерации лицензий.

### 📊 Swagger документация

Откройте в браузере:

```
http://localhost:8000/docs
```

Автоматически сгенерированная документация с интерактивными эндпоинтами.

### 🔧 Python скрипт (CLI)

```bash
python <script_name>
```

Где `<script_name>` один из:
- `check_status.py` - проверить статус API
- `test_api.py` - запустить полный тест
- `ckey_cli.py` - CLI инструмент для работы с API

#### Примеры использования CLI:

```bash
# Список всех продуктов
python ckey_cli.py list

# Получить PyCharm лицензию
python ckey_cli.py fire pycharm --name "My License"

# Получить IntelliJ IDEA лицензию
python ckey_cli.py fire idea --name "My License"

# С кастомной датой окончания
python ckey_cli.py fire idea --name "ProjectName" --expiry "2025-12-31"
```

### 🧪 Python код

```python
import requests

# Простое использование
response = requests.get("http://localhost:8000/api/license/pycharm")

if response.status_code == 200:
    data = response.json()
    if data.get("success"):
        license_key = data["data"]
        print(f"Получен ключ: {license_key}")
```

### 💻 cURL запросы

```bash
# PyCharm лицензия
curl "http://localhost:8000/api/license/pycharm"

# IntelliJ IDEA лицензия
curl "http://localhost:8000/api/license/idea"

# С кастомными параметрами
curl "http://localhost:8000/api/license?product=PC&name=MyLicense&expiry=2099-12-31"
```

---

## 📚 API Эндпоинты

### Основные эндпоинты

| Эндпоинт | Описание |
|----------|----------|
| `GET /api/products` | Список всех продуктов |
| `GET /api/license` | Генерация лицензии (параметры через query) |
| `GET /api/license/pycharm` | PyCharm лицензия |
| `GET /api/license/idea` | IntelliJ IDEA лицензия |
| `GET /api/license/goland` | GoLand лицензия |
| `GET /api/license/phpstorm` | PhpStorm лицензия |
| `GET /api/license/clion` | CLion лицензия |
| `GET /api/license/webstorm` | WebStorm лицензия |
| `GET /api/license/rider` | Rider лицензия |
| `GET /api/license/datagrip` | DataGrip лицензия |
| `GET /api/license/rubymine` | RubyMine лицензия |
| `GET /api/license/appcode` | AppCode лицензия |
| `GET /api/license/dataspell` | DataSpell лицензия |
| `GET /api/license/rustrover` | RustRover лицензия |
| `GET /api/download/ja-netfilter.jar` | Скачать ja-netfilter.jar |

### Параметры запроса

К общим параметрам для всех эндпоинтов генерации лицензии:

- `product` (required) - код продукта
- `name` (optional) - название лицензии (по умолчанию: ckey.run)
- `expiry` (optional) - дата окончания (по умолчанию: 2099-12-31)
- `assignee` (optional) - имя пользователя

### Коды продуктов

| Код | Продукт |
|-----|---------|
| II | IntelliJ IDEA |
| PC | PyCharm / PyTorch |
| GO | GoLand |
| PS | PhpStorm |
| CL | CLion |
| WS | WebStorm |
| RD | Rider |
| DB | DataGrip |
| RM | RubyMine |
| AC | AppCode |
| DS | DataSpell |
| RR | RustRover |

---

## 📁 Структура проекта

```
pycharmlicense/
├── ckey_api.py          # API сервер (FastAPI)
├── ckey_cli.py          # CLI инструмент
├── test_api.py          # Тесты API
├── check_status.py      # Проверка статуса
├── api_test.html        # Веб интерфейс для тестов
├── requirements.txt     # Зависимости Python
└── README_API.md        # Документация API
```

---

## ⚙️ Устранение неполадок

### Проблема: Сервер не стартует

**Решение**: Убедитесь, что в системе установлен Python 3.8+ и все зависимости:

```bash
pip install -r requirements.txt
```

Проверьте версию Python:

```bash
python --version
```

### Проблема: Соединение не устанавливается

**Решение**:
1. Проверьте, что сервер запущен
2. Убедитесь, что к нему нет брандмауэров
3. Попробуйте перезапустить сервер

```bash
# Ctrl+C - остановить
python ckey_api.py    # перезапустить
```

### Проблема: Плохой интернет или慢ты API

**Решение**: Добавьте таймаут в запросах или используйте локальный кэш

---

## 💡 Дополнительно

### Создание собственного сервиса

API готов к интеграции с любым приложением. Просто делайте HTTP GET/POST запросы к портам port 8000.

### API в Docker

Ожидаю, что можно создать Dockerfile:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "ckey_api.py"]
```

---

## 🔒 Логирование

API автоматически пишет логи в консоль:
- Возможно перенаправить в файл: `> api.log 2>&1`
- Включить DEBUG режим при запуске

---

## 📝 Лицензионные условия

Используйте этот API на свой страх и риск. Лицензии генерируются через ckey.run.

---

## 📬 Поддержка

Документация доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json
