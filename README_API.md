# cKey Run API Gateway

API прослойка для получения ключей лицензий от ckey.run.

## Установка

Установите зависимости:

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python ckey_api.py
```

API будет доступен по адресу: http://localhost:8000

## Документация

Откройте интерфейс документации Swagger UI: http://localhost:8000/docs

## Эндпоинты

### Основной эндпоинт генерации лицензии

```
GET /api/license?product=PC&name=my-license&expiry=2099-12-31&assignee=user
```

Параметры:
- `product` (обязательный): Код продукта (например: II, PC, GO, PS, CL, WS, RD, DB, RM, AC, DS, RR)
- `name`, `expiry`, `assignee` (необязательные) - см. документацию

### Готовые эндпоинты для популярных продуктов

- `/api/license/idea` - IntelliJ IDEA
- `/api/license/pycharm` - PyCharm
- `/api/license/pytorch` - PyTorch (использует PyCharm лицензию)
- `/api/products` - список всех продуктов

## Примеры запросов

### Python:

```python
import requests

# URL
base_url = "http://localhost:8000/api"

# Получить лицензию для PyCharm
response = requests.get(f"{base_url}/license/pycharm?name=My License&expiry=2099-12-31")
data = response.json()

# Проверить успешность и получить ключ
if data.get("success"):
    license_key = data["data"]
    print(f"Лицензия получена: {license_key[:50]}...")
else:
    print(f"Ошибка: {data.get('detail', 'Unknown error')}")
```

### cURL:

```bash
# PyCharm лицензия
curl "http://localhost:8000/api/license/pycharm?name=My License&expiry=2099-12-31"

# IntelliJ IDEA лицензия
curl "http://localhost:8000/api/license/idea"

# Список доступных продуктов
curl "http://localhost:8000/api/products"
```

## Возможные коды продуктов

| Код | Продукт |
|-----|---------|
| II | IntelliJ IDEA |
| PC | PyCharm |
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

## Пример ответа

```json
{
    "success": true,
    "product_code": "PC",
    "license_name": "My License",
    "expiry_date": "2099-12-31",
    "data": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
