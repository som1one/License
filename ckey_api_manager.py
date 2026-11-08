#!/usr/bin/env python
"""
Standalone cKey API Manager для ckey_api_fixed.py
Управляет запуском и закрытием API сервера
"""
import subprocess
import sys
import time
import requests
from threading import Thread
import socket

class CKeyAPIServerFixed:
    """Управление API сервером"""

    def __init__(self, host="127.0.0.1", port=8000):
        self.host = host
        self.port = port
        self.process = None
        self.is_running = False

    def start(self):
        """Запуск API сервера"""
        if self.is_running:
            print("✅ API уже запущен")
            return

        print(f"🚀 Запуск API сервера на {self.host}:{self.port}...")

        # Запуск сервера в отдельном потоке
        self.process = subprocess.Popen(
            [sys.executable, "ckey_api_fixed.py"],
            cwd=".",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
        )

        # Ожидание запуска
        print("⏳ Ожидание запуска сервера...")
        max_retries = 30
        retry_count = 0

        while retry_count < max_retries:
            try:
                response = requests.get(f"http://{self.host}:{self.port}/api/products", timeout=2)
                if response.status_code == 200:
                    self.is_running = True
                    print(f"✅ API запущен успешно!")
                    print(f"📊 URL: http://{self.host}:{self.port}")
                    print(f"📖 Документация: http://{self.host}:{self.port}/docs\n")
                    return True
            except (requests.exceptions.RequestException, ConnectionRefusedError, socket.error):
                retry_count += 1
                time.sleep(1)
                print(f"⏳ Ожидание ({retry_count}/{max_retries})...")

        print(f"❌ Не удалось запустить API сервер")
        return False

    def stop(self):
        """Остановка API сервера"""
        if not self.process:
            print("⚠️ API сервер не запущен")
            return

        print("🛑 Остановка API сервера...")
        self.process.terminate()
        self.process.wait(timeout=5)
        self.is_running = False
        print("✅ API сервер остановлен")

    def restart(self):
        """Перезапуск API сервера"""
        self.stop()
        time.sleep(2)
        return self.start()


def interactive_menu():
    """Интерактивное меню"""
    server = CKeyAPIServerFixed()

    while True:
        print("\n" + "=" * 50)
        print("cKey API Gateway Manager")
        print("=" * 50)

        if server.is_running:
            print("✅ API: ВКЛЮЧЕН")
            print(f"📍 URL: http://localhost:{server.port}")
            print(f"📖 Документация: http://localhost:{server.port}/docs")
        else:
            print("❌ API: ОТКЛЮЧЕН")

        print("\nМеню:")
        if server.is_running:
            print("1. Перезезапустить API")
            print("2. Отключить API")
            print("3. Открыть веб-интерфейс")
            print("4. Показать команду для браузера")
            print("5. Выход")
        else:
            print("1. Включить API")
            print("2. Выход")

        choice = input("\nВыберите действие: ")

        if choice == "1":
            if server.is_running:
                server.restart()
            else:
                server.start()
        elif choice == "2":
            if server.is_running:
                server.stop()
            else:
                print("API уже отключен")
        elif choice == "3":
            print("Открывается веб-интерфейс...")
            # Запуск quickstart.py в браузере
            import webbrowser
            webbrowser.open(f"file://{os.path.abspath('api_test.html')}")
        elif choice == "4":
            print(f"URL для браузера: http://localhost:{server.port}/docs")
        elif choice == "5":
            server.stop()
            break
        else:
            print("Неверный выбор")


if __name__ == "__main__":
    import os
    interactive_menu()
