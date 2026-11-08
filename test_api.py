"""
Тестовый скрипт для проверки работы cKey API
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_license_generation():
    """Тест генерации лицензии для PyCharm"""
    print("=== Тест: Генерация лицензии PyCharm ===")

    url = f"{BASE_URL}/license"

    params = {
        "product": "PC",
        "name": "Test License",
        "expiry": "2099-12-31",
        "assignee": "test_user"
    }

    print(f"Запрос к: {url}")
    print(f"Параметры: {json.dumps(params, indent=2, ensure_ascii=False)}")

    response = requests.get(url, params=params)

    print(f"\nСтатус: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print("\n✅ Успешный ответ:")

        if data.get("success"):
            license_key = data.get("data", "")
            print(f"Продукт: {data['product_code']}")
            print(f"Лицензия: {data['license_name']}")
            print(f"Дата окончания: {data.get('expiry_date')}")
            print(f"\nКлюч лицензии ({len(license_key)} символов):")
            print(f"{license_key}")
        else:
            print(f"❌ Ошибка: {data.get('detail', 'Unknown error')}")
    else:
        print(f"❌ Ошибка запроса: {response.text}")
    print()


def test_idea_license():
    """Тест генерации лицензии для IntelliJ IDEA"""
    print("=== Тест: Генерация лицензии IntelliJ IDEA ===")

    url = f"{BASE_URL}/license/idea"

    print(f"Запрос к: {url}")

    response = requests.get(url)

    print(f"\nСтатус: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print("\n✅ Успешный ответ:")

        if data.get("success"):
            license_key = data.get("data", "")
            print(f"Продукт: {data['product_code']}")
            print(f"Лицензия: {data['license_name']}")
            print(f"\nКлюч лицензии ({len(license_key)} символов):")
            print(f"{license_key}")
        else:
            print(f"❌ Ошибка: {data.get('detail', 'Unknown error')}")
    else:
        print(f"❌ Ошибка запроса: {response.text}")
    print()


def test_products_list():
    """Тест получения списка продуктов"""
    print("=== Тест: Список доступных продуктов ===")

    url = f"{BASE_URL}/products"

    response = requests.get(url)

    print(f"Запрос к: {url}")
    print(f"\nСтатус: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Доступно продуктов: {len(data)}")
        print("\nСписок продуктов:")
        for code, name in data.items():
            print(f"  - {code}: {name}")
    else:
        print(f"❌ Ошибка запроса: {response.text}")
    print()


def test_custom_expiry_date():
    """Тест со своей датой окончания"""
    print("=== Тест: Лцензия с кастомной датой окончания ===")

    url = f"{BASE_URL}/license/pycharm"

    params = {
        "name": "Custom License",
        "expiry": "2025-12-31"
    }

    response = requests.get(url, params=params)

    print(f"Запрос к: {url}")
    print(f"Параметры: {json.dumps(params, indent=2, ensure_ascii=False)}")
    print(f"\nСтатус: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print("\n✅ Успешный ответ:")

        if data.get("success"):
            license_key = data.get("data", "")
            print(f"Дата окончания: {data.get('expiry_date')}")
            print(f"\nКлюч лицензии ({len(license_key)} символов):")
            print(f"{license_key}")
        else:
            print(f"❌ Ошибка: {data.get('detail', 'Unknown error')}")
    else:
        print(f"❌ Ошибка запроса: {response.text}")
    print()


def test_invalid_product():
    """Тест с некорректным кодом продукта"""
    print("=== Тест: Некорректный код продукта ===")

    url = f"{BASE_URL}/license"

    params = {
        "product": "INVALID",
        "name": "Test License",
        "expiry": "2099-12-31"
    }

    response = requests.get(url, params=params)

    print(f"Запрос к: {url}")
    print(f"Некорректный код продукта: INVALID")
    print(f"\nСтатус: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print("\nРезультат:")
        print(json.dumps(data, indent=2))
    else:
        print(f"✅ Ожидаемая ошибка: {response.status_code}")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("Запуск тестов cKey API")
    print("=" * 60)
    print()

    try:
        test_idea_license()
        test_license_generation()
        test_products_list()
        test_custom_expiry_date()
        test_invalid_product()

        print("=" * 60)
        print("Тесты завершены!")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("\n❌ Ошибка: Не удалось подключиться к API.")
        print("Пожалуйста, убедитесь, что сервер запущен и доступен по адресу:")
        print("  http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {str(e)}")
