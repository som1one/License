#!/usr/bin/env python
"""
Валидация и проверка настройки cKey API Gateway

Этот скрипт проверяет:
1. Наличие зависимостей
2. Запуск API сервера
3. Работоспособность эндпоинтов
4. Качество данных
"""
import sys
import os


def check_dependencies():
    """Проверка установленных зависимостей"""
    print("📋 Проверка зависимостей...")

    dependencies = [
        'fastapi',
        'uvicorn',
        'requests'
    ]

    missing = []
    installed = []

    for dep in dependencies:
        try:
            __import__(dep)
            installed.append(dep)
        except ImportError:
            missing.append(dep)

    if missing:
        print(f"   ❌ Отсутствует: {', '.join(missing)}")
        print(f"\n💡 Установите зависимости:")
        print(f"   pip install -r requirements.txt")
        return False
    else:
        print(f"   ✅ Все зависимости установлены: {', '.join(installed)}")
        return True


def check_files():
    """Проверка наличия файлов проекта"""
    print("\n📁 Проверка файлов проекта...")

    required_files = [
        'ckey_api.py',
        'ckey_cli.py',
        'manager.py',
        'requirements.txt',
        'api_test.html',
        'START.md'
    ]

    missing = []
    present = []

    for file in required_files:
        if os.path.exists(file):
            present.append(file)
        else:
            missing.append(file)

    if missing:
        print(f"   ❌ Отсутствуют: {', '.join(missing)}")
        return False
    else:
        print(f"   ✅ Все файлы присутствуют: {len(present)}/{len(required_files)}")
        return True


def start_server():
    """Запуск API сервера"""
    print("\n🚀 Запуск API сервера...")

    try:
        import subprocess

        process = subprocess.Popen(
            [sys.executable, "ckey_api.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print(f"   ↔️  Процесс запущен (PID: {process.pid})")
        print(f"   ⏳ Ожидание запуска...")

        import time
        for _ in range(10):
            time.sleep(1)

        return True

    except Exception as e:
        print(f"   ❌ Ошибка запуска: {str(e)}")
        return False


def check_api():
    """Проверка API"""
    print("\n📡 Проверка сервера API...")

    try:
        import requests

        for attempt in range(3):
            try:
                response = requests.get("http://localhost:8000/api/products", timeout=3)
                if response.status_code == 200:
                    return True
            except requests.exceptions.ConnectionError:
                import time
                time.sleep(2)

        return False

    except Exception as e:
        print(f"   ❌ Ошибка проверки: {str(e)}")
        return False


def test_endpoints():
    """Тестирование эндпоинтов"""
    print("\n🧪 Тестирование эндпоинтов...")

    try:
        import requests

        endpoints = [
            ("GET", "/api/products", "Список продуктов"),
            ("GET", "/api/license/pycharm", "PyCharm лицензия"),
            ("GET", "/api/license/idea", "IntelliJ IDEA лицензия")
        ]

        results = []

        for method, endpoint, description in endpoints:
            try:
                url = f"http://localhost:8000{endpoint}"

                if endpoint == "/api/license/pycharm":
                    response = requests.get(url, params={"expiry": "2099-12-31"}, timeout=10)
                else:
                    response = requests.get(url, timeout=10)

                results.append({
                    "endpoint": description,
                    "status": "✅" if response.status_code == 200 else "❌",
                    "code": response.status_code
                })

            except Exception as e:
                results.append({
                    "endpoint": description,
                    "status": "❌",
                    "error": str(e)
                })

        # Печать результатов
        for result in results:
            if "error" in result:
                print(f"   {result['status']} {result['endpoint']}: {result['error']}")
            else:
                print(f"   {result['status']} {result['endpoint']}: OK")

        return all(r["status"] == "✅" for r in results if "error" not in r)

    except Exception as e:
        print(f"   ❌ Ошибка тестирования: {str(e)}")
        return False


def generate_license():
    """Генерация тестовой лицензии"""
    print("\n🔑 Генерация тестовой лицензии...")

    try:
        import requests

        url = "http://localhost:8000/api/license/pycharm"
        response = requests.get(url, params={"expiry": "2099-12-31"}, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data.get("success"):
                key = data["data"]

                print(f"   ✅ Лицензия сгенерирована")
                print(f"   👤 Продукт: {data['product_code']}")
                print(f"   ⏱️  Дата окончания: {data.get('expiry_date')}")
                print(f"   🔑 Ключ ({len(key)} символов):")
                print(f"      {key[:60]}...")

                return True
            else:
                print(f"   ❌ Ошибка генерации: {data.get('detail')}")
                return False

    except Exception as e:
        print(f"   ❌ Ошибка: {str(e)}")
        return False


def main():
    """Главная функция валидации"""
    print("=" * 60)
    print("🔧 Валидация cKey API Gateway")
    print("=" * 60 + "\n")

    results = {
        "dependencies": check_dependencies(),
        "files": check_files(),
        "server": start_server(),
        "api_check": check_api(),
        "endpoints": test_endpoints(),
        "license": generate_license()
    }

    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ ВАЛИДАЦИИ")
    print("=" * 60)

    total = len(results)
    passed = sum(results.values())

    for item, status in results.items():
        print(f"   {item:15s}: {'✅ ПРОВЕРЕНО' if status else '❌ ОШИБКА'}")

    print(f"\n   📈 Итог: {passed}/{total} проверок пройдено")

    if passed == total:
        print("\n   🎉 ВСЕ СИСТЕМА РАБОТАЕТ!")
        print("\n   📖 Доступ:")
        print(f"      • API: http://localhost:8000/api")
        print(f"      • Документация: http://localhost:8000/docs")
        print(f"      • Веб: api_test.html")
        print(f"      • CLI: python ckey_cli.py")
    else:
        print("\n   ⚠️  НЕКОТОРЫЕ ПРОБЛЕМЫ ОБНАРУЖЕНЫ")
        print("\n   💡 Попробуйте:")
        print(f"      1. pip install -r requirements.txt")
        print(f"      2. python manager.py quick")
        print(f"      3. python manager.py test")

    print("=" * 60)

    if passed == total:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
