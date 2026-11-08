"""
Проверить активность API через интерактивный запрос
"""
import requests
import sys

def check_api_status():
    """Проверка статуса API"""
    try:
        print("Проверка статуса сервера...")
        response = requests.get("http://localhost:8000/api/products", timeout=5)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ API работает!")
            print(f"Получен список продуктов ({len(data)} штук)")

            print("\nДоступные продукты:")
            for code, name in sorted(data.items()):
                print(f"  - {code:2s}: {name}")

            return True
        else:
            print(f"❌ Ошибка сервера: статус {response.status_code}")
            return False

    except requests.exceptions.ConnectionError as e:
        print(f"❌ Не удалось подключиться к серверу")
        print(f"URL: http://localhost:8000")
        print(f"Пожалуйста, убедитесь, что сервер уже запущен!")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        return False


if __name__ == "__main__":
    success = check_api_status()
    sys.exit(0 if success else 1)
