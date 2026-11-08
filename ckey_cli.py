#!/usr/bin/env python
"""
Упрощенный интерфейс для работы с cKey API
Использование:
    python ckey_cli.py [COMMAND] [OPTIONS]
"""

import requests
import json
import argparse
import sys


class CKeyAPI:
    """Клиент для работы с cKey API"""

    BASE_URL = "http://localhost:8000/api"

    def __init__(self):
        try:
            response = requests.get(f"{self.BASE_URL}/products", timeout=5)
            response.raise_for_status()
            self.available_products = response.json()
            self.connected = True
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка подключения к API: {str(e)}", file=sys.stderr)
            print("Убедитесь, что сервер запущен (python ckey_api.py)")
            sys.exit(1)

    def get_license(self, product_code, name="ckey.run", expiry="2099-12-31", assignee=""):
        """Получить лицензию для продукта"""
        url = f"{self.BASE_URL}/license"
        params = {
            "product": product_code,
            "name": name,
            "expiry": expiry,
            "assignee": assignee
        }

        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "product_code": data["product_code"],
                    "license_name": data["license_name"],
                    "expiry_date": data.get("expiry_date"),
                    "key": data["data"]
                }
            else:
                return {"success": False, "error": data.get("detail", "Unknown error")}
        else:
            return {"success": False, "error": f"Status code: {response.status_code}"}

    def get_idea_license(self, name="ckey.run", expiry="2099-12-31", assignee=""):
        """Получить лицензию IntelliJ IDEA"""
        url = f"{self.BASE_URL}/license/idea"
        params = {"name": name, "expiry": expiry, "assignee": assignee}
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "product_code": data["product_code"],
                    "license_name": data["license_name"],
                    "expiry_date": data.get("expiry_date"),
                    "key": data["data"]
                }
            else:
                return {"success": False, "error": data.get("detail", "Unknown error")}
        else:
            return {"success": False, "error": f"Status code: {response.status_code}"}

    def get_pycharm_license(self, name="ckey.run", expiry="2099-12-31", assignee=""):
        """Получить лицензию PyCharm"""
        url = f"{self.BASE_URL}/license/pycharm"
        params = {"name": name, "expiry": expiry, "assignee": assignee}
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "product_code": data["product_code"],
                    "license_name": data["license_name"],
                    "expiry_date": data.get("expiry_date"),
                    "key": data["data"]
                }
            else:
                return {"success": False, "error": data.get("detail", "Unknown error")}
        else:
            return {"success": False, "error": f"Status code: {response.status_code}"}

    def list_products(self):
        """Показать список доступных продуктов"""
        return self.available_products


def format_key(key, max_length=80):
    """Форматирование ключа для красивого отображения"""
    if len(key) > max_length:
        return key[:max_length] + "..."
    return key


def print_license_success(license_data, product_name=""):
    """Печать успешной лицензии"""
    print(f"\n{'=' * 60}")
    print(f"✅ Лицензия получена!")
    print(f"{'=' * 60}")
    print(f"Продукт: {license_data['product_code']} ({product_name})")
    print(f"Лицензия: {license_data['license_name']}")
    print(f"Дата окончания: {license_data['expiry_date']}")
    print(f"Длина ключа: {len(license_data['key'])} символов")
    print(f"\nКлюч лицензии:")
    print(f"{format_key(license_data['key'])}\n")
    print(f"{'=' * 60}\n")


def main():
    """Главная функция CLI"""
    parser = argparse.ArgumentParser(
        description="Управление лицензиями через cKey API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %s fire pycharm --name "MyProd"
  %s fire idea --name "MyProd"
  %s list
  %s list
        """ % (sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0])
    )

    subparsers = parser.add_subparsers(dest="command", help="Команды")

    # Команда list
    subparsers.add_parser("list", help="Список доступных продуктов")

    # Команда fire (для PyCharm)
    pycharm_parser = subparsers.add_parser("fire", help="Получить PyCharm лицензию")
    pycharm_parser.add_argument("platform", choices=["pycharm", "pytorch"], help="Платформа")
    pycharm_parser.add_argument("--name", default="ckey.run", help="Название лицензии")
    pycharm_parser.add_argument("--expiry", default="2099-12-31", help="Дата окончания (yyyy-MM-dd)")
    pycharm_parser.add_argument("--assignee", default="", help="Имя пользователя")

    # Команда fire (для IntelliJ IDEA)
    idea_parser = subparsers.add_parser("fire", help="Получить IntelliJ IDEA лицензию")
    idea_parser.add_argument("platform", choices=["idea"], help="Платформа")
    idea_parser.add_argument("--name", default="ckey.run", help="Название лицензии")
    idea_parser.add_argument("--expiry", default="2099-12-31", help="Дата окончания (yyyy-MM-dd)")
    idea_parser.add_argument("--assignee", default="", help="Имя пользователя")

    args = parser.parse_args()

    # Создание клиента
    client = CKeyAPI()

    # Обработка команды list
    if args.command == "list":
        products = client.list_products()
        print(f"\n{'=' * 50}")
        print(f"Доступные продукты: {len(products)}")
        print(f"{'=' * 50}\n")

        for code, name in sorted(products.items()):
            print(f"  {code:2s} - {name}")

        print(f"\n{'=' * 50}\n")
        return

    # Обработка команды fire
    if args.command == "fire":
        if args.platform == "pycharm" or args.platform == "pytorch":
            license_data = client.get_pycharm_license(
                name=args.name,
                expiry=args.expiry,
                assignee=args.assignee
            )
            name = "PyCharm / PyTorch"

            if license_data["success"]:
                print_license_success(license_data, name)
                with open("pycharm_license.key", "w") as f:
                    f.write(license_data["key"])
                print("✅ Ключ сохранен в файл: pycharm_license.key\n")
            else:
                print(f"❌ Ошибка: {license_data['error']}\n")

        elif args.platform == "idea":
            license_data = client.get_idea_license(
                name=args.name,
                expiry=args.expiry,
                assignee=args.assignee
            )
            name = "IntelliJ IDEA"

            if license_data["success"]:
                print_license_success(license_data, name)
                with open("idea_license.key", "w") as f:
                    f.write(license_data["key"])
                print("✅ Ключ сохранен в файл: idea_license.key\n")
            else:
                print(f"❌ Ошибка: {license_data['error']}\n")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
