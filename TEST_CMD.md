# Команды для тестирования API Gateway

## Через npm скрипты (проще всего):

```bash
# Установить зависимости (один раз)
npm install

# Запустить API сервер
npm run dev
```

Затем в этом же терминале запустите тесты:

```bash
# Проверить что сервер работает (вернет список продуктов)
npm run check:alive

# Проверить список продуктов
npm run list:products

# Тест 1: Лицензия PyCharm
npm run test:pycharm

# Тест 2: Лицензия IntelliJ IDEA
npm run test:intellij

# Открыть веб-доку
npm run docs
```

## Прямые Python команды:

```powershell
# Статус API
python -c "import requests; r=requests.get('http://127.0.0.1:8000/api/products'); print(r.json())"

# PyCharm лицензия
python -c "import requests; r=requests.get('http://127.0.0.1:8000/api/license?product=PC&name=Test&expiry=2099-12-31&assignee=User'); print(r.json())"

# IntelliJ IDEA лицензия
python -c "import requests; r=requests.get('http://127.0.0.1:8000/api/license?product=II&name=Test&expiry=2099-12-31&assignee=User'); print(r.json())"

# Список продуктов
python -c "import requests; r=requests.get('http://127.0.0.1:8000/api/products'); print(r.json())"

# Веб-доку
start http://127.0.0.1:8000/docs
```

## Через менеджер:

```powershell
# Запуск API с интерактивным меню
python manager.py

# Интерактивный режим
# В меню выберите: 1 - Включить API
```

## URL-адреса:

- 😊 API Gateway: http://127.0.0.1:8000
- 📖 Документация API: http://127.0.0.1:8000/docs
- 🔧 Веб-интерфейс: `quickstart.py`
- 📦 API сервер: `ckey_api_fixed.py`

## Коды продуктов:

- II - IntelliJ IDEA (In名利图书管)
- PC - PyCharm (天溪径路)
- A - Android Studio (大官开发)
- CL - DataGrip (直大趣兴)
- J - JetBrains Rider (竖帘求写)

## Для остановки:

Выйти из консоли с сервером → Ctrl+C, или запустить `python manager.py` и выбрать остановку.
