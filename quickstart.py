#!/usr/bin/env python
"""
Quickstart script для автоматического запуска и проверки cKey API Gateway

Быстрое начало работы:
1. Проверка зависимостей
2. Проверка файлов
3. Запуск сервера
4. Открытие веб-интерфейса

Использование:
    python quickstart.py

Опциональные флаги:
    --no-server    - не запускать сервер
    --no-check     - пропустить проверки
    --browser      - открыть браузер автоматически
"""
import sys
import os
import subprocess
import time
import requests
from typing import Optional


class QuickStart:
    """Автоматический запуск и проверка"""

    def __init__(self, check=True, server=True, browser_prompt=True):
        self.check = check
        self.start_server = server
        self.browser_prompt = browser_prompt
        self.api_url = "http://localhost:8000"
        self.is_server_running = False

    def check_dependencies(self) -> bool:
        """Проверка Python зависимостей"""
        print("🔍 Проверка зависимостей Python...")

        dependencies = ['fastapi', 'uvicorn', 'requests']

        for dep in dependencies:
            try:
                __import__(dep)
            except ImportError:
                print(f"   ❌ Недоступен: {dep}")
                return False

        print("   ✅ Все зависимости установлены")
        return True

    def install_dependencies(self) -> bool:
        """Установка зависимостей"""
        print("📦 Установка зависимостей...")

        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                print("   ✅ Зависимости установлены")
                return True
            else:
                print(f"   ❌ Ошибка установки: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print("   ❌ Превышено время ожидания")
            return False
        except Exception as e:
            print(f"   ❌ Ошибка: {str(e)}")
            return False

    def check_files(self) -> bool:
        """Проверка наличия файлов проекта"""
        print("\n📁 Проверка файлов проекта...")

        required = [
        'ckey_api.py',
        'ckey_cli.py',
        'manager.py',
        'quickstart.py',
        'validate_setup.py',
        'test_api.py',
        'check_status.py',
        'quick_check.py',
        'scan_report.py',
        'api_test.html',
        'START.md',
        'README_API.md',
        'requirements.txt',
        'ckey_home.html'
    ]

    missing = [f for f in required if not os.path.exists(f)]

    if missing:
        print(f"   ❌ Отсутствуют: {', '.join(missing)}")
        return False

    print(f"   ✅ Все файлы присутствуют ({len(required)} файлов)")
    return True

    def start_server_process(self) -> bool:
        """Запуск API сервера в фоновом процессе"""
        print("\n🚀 Запуск API сервера...")

        try:
            self.server_process = subprocess.Popen(
                [sys.executable, "ckey_api.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            self.is_server_running = True
            time.sleep(2)

            return True

        except Exception as e:
            print(f"   ❌ Ошибка запуска: {str(e)}")
            return False

    def check_server_health(self) -> bool:
        """Проверка работоспособности сервера"""
        print("\n📡 Проверка работоспособности сервера...")

        if not self.is_server_running:
            return False

        max_retries = 10
        retries = 0

        while retries < max_retries:
            try:
                response = requests.get(f"{self.api_url}/api/products", timeout=3)
                if response.status_code == 200:
                    print("   ✅ API сервер работает!")
                    return True
            except requests.exceptions.ConnectionError:
                time.sleep(1)
                retries += 1

        print("   ⚠️  Сервер не отвечает (может запуститься позже)")
        return False

    def display_info(self):
        """Отображение информации о проекте"""
        print("\n" + "=" * 65)
        print(" 🎉 cKey API Gateway запущен!")
        print("=" * 65)

        print("\n📍 АДРЕСА:")
        print(f"   • API:           {self.api_url}/api")
        print(f"   • Документация:  {self.api_url}/docs")
        print(f"   • Веб-интерфейс: file://{os.path.abspath('api_test.html')}")

        print("\n📝 КОМАНДЫ:")
        print("   • Python:       python test_api.py")
        print("   • CLI:          python ckey_cli.py")
        print("   • Менеджер:     python manager.py")
        print("   • Проверка:     python validate_setup.py")

        print("\n📚 ДОКУМЕНТАЦИЯ:")
        print("   • README:        START.md")
        print("   • ИНСТРУКЦИИ:   Подробное руководство в START.md")
        print("   • СТРУКТУРА ИНФОРМАЦИИ: ДОМ.md")

        print("\n💡 ПОЛЕЗНЫЕ СОВЕТЫ:")
        print("   • Используйте Swagger UI для тестирования")
        print("   • CLI инструмент удобно использовать в скриптах")
        print("   • Веб-интерфейс подходит для тестов в браузере")
        print("   • Проверяйте сервер с python validate_setup.py")

        print("\n" + "=" * 65)

    def open_browser(self, browser_prompt=True):
        """Открытие браузера"""
        if not browser_prompt:
            print("\n🌐 Открытие Swagger документации...")
            import webbrowser
            webbrowser.open(f"{self.api_url}/docs")
            return

        answer = input("\n🌐 Открыть Swagger документацию в браузере? (y/n): ")

        if answer.lower() == 'y':
            import webbrowser
            webbrowser.open(f"{self.api_url}/docs")
        else:
            print("\n💡 Для открытия выполните: http://localhost:8000/docs")


def main():
    """Главная функция"""
    import argparse

    parser = argparse.ArgumentParser(
        description="cKey API Gateway - Автоматический запуск",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="" """
Функции:
  • Проверка зависимостей Python
  • Проверка файлов проекта
  • Автоматическая установка (если надо)
  • Запуск API сервера
  • Проверка работоспособности
  • Вывод информации

Примеры:
  python quickstart.py                  # Полный запуск с проверками
  python quickstart.py --no-server       # Только проверки
  python quickstart.py --browser         # С открытием браузера

Настройка:
  • Все файлы находятся в текущей директории
  • Проверка: python validate_setup.py
  • Документация: START.md
        """
    )

    parser.add_argument(
        "--no-server",
        action="store_true",
        help="Пропустить запуск сервера"
    )

    parser.add_argument(
        "--no-check",
        action="store_true",
        help="Пропустить проверку зависимостей и файлов"
    )

    parser.add_argument(
        "--browser",
        action="store_true",
        help="Автоматически открыть браузер"
    )

    args = parser.parse_args()

    starter = QuickStart(
        check=not args.no_check,
        server=not args.no_server,
        browser_prompt=not args.browser
    )

    # Запуск процесса
    if starter.check and not args.no_check:
        print("🚀 cKey API Gateway - Быстрый старт")
        print("=" * 65 + "\n")

        if not starter.check_dependencies():
            if not starter.install_dependencies():
                print("\n❌ Не удалось установить зависимости")
                return 1

        if not starter.check_files():
            print("\n❌ Недостаточно файлов проекта")
            return 1

    if not starter.check:
        print("🚀 cKey API Gateway")
        print("\nManually запущено (пропускаются проверки)")

    if starter.start_server and not args.no_server:
        if not starter.start_server_process():
            print("❌ Не удалось запустить сервер")
            return 1

        time.sleep(3)

        if not starter.check_server_health():
            print("\n⚠️  Сервер может запуститься позже, проверьте консоль")
            print("   Иногда требуется несколько секунд")
            return 1

    # Вывод информации
    if not args.no_server:
        starter.display_info()
        if starter.browser_prompt:
            starter.open_browser()

    print("\n✅ Проект готов к работе!\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
