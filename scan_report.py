#!/usr/bin/env python
"""
Группировка всех файлов проекта и проверка готовности

Этот скрипт:
1. Собирает все файлы
2. Ищет возможные проблемы
3. Показывает структуру проекта
4. Подсказывает, как начать работу
"""

import os
import sys
from pathlib import Path


def list_project_files(root_dir="."):
    """Список всех файлов в проекте"""
    files = []
    directories = []

    with os.scandir(root_dir) as entries:
        for entry in entries:
            if entry.is_file():
                files.append({
                    "path": entry.path,
                    "name": entry.name,
                    "type": "script" if entry.name.endswith(".py") else
                           "html" if entry.name.endswith(".html") else
                           "text" if entry.name.endswith((".md", ".txt")) else
                           "binary"
                })
            elif entry.is_dir():
                directories.append({
                    "path": entry.path,
                    "name": entry.name
                })

    return sorted(files, key=lambda x: x["name"]), sorted(directories, key=lambda x: x["name"])


def categorize_files(files):
    """Классификация файлов"""
    categories = {
        "API Server": [],
        "CLI Tools": [],
        "Web Interfaces": [],
        "Documentation": [],
        "Testing": [],
        "Installation Files": [],
        "Other": []
    }

    scripts = ["pycharmlicense"]
    api_scripts = "api"

    for file in files:
        name = file["name"].lower()

        if name.endswith(".py"):
            if "api" in name:
                categories["API Server"].append(file)
            elif "cli" in name or "manager" in name or "test" in name:
                categories["CLI Tools"].append(file)
            else:
                categories["API Server"].append(file)

        elif name.endswith(".html"):
            categories["Web Interfaces"].append(file)

        elif name.endswith(".md"):
            categories["Documentation"].append(file)

        elif name.endswith(".txt"):
            categories["Installation Files"].append(file)

        else:
            categories["Other"].append(file)

    return categories


def check_reads(proj_path, file_path, pattern):
    """Проверка, есть ли чтение нужного фрагмента"""
    try:
        with open(os.path.join(proj_path, file_path), 'r', encoding='utf-8') as f:
            content = f.read()

        pattern = pattern.lower()
        return pattern in content.lower()

    except Exception:
        return False


def display_status(interface, section, status, items):
    """Отображение статуса секции"""
    icon = "✅" if status else "❌"

    print(f"\n{icon} {interface} {section}:")
    print(f"   Присутствуют файлы: {', '.join(items)}")

    return status


def analyze_project():
    """Анализ проекта"""
    files, dirs = list_project_files(".")

    total_files = len(files)
    total_dirs = len(dirs)

    print("=" * 70)
    print(" 📊 АНАЛИЗ ПРОЕКТА cKey API Gateway")
    print("=" * 70)

    print(f"\n📁 Общая структура: {len(files)} файлов, {len(dirs)} директорий")

    # Классификация
    categories = categorize_files(files)

    print("\n📁 КЛАССИФИКАЦИЯ ФАЙЛОВ")
    print("=" * 70)

    status_all = True

    for category, items in categories.items():
        if items:
            print(f"\n{items[0]['name'].upper()} ({len(items)}):")
            for item in items:
                print(f"   • {item['name']}")

    print("\n" + "=" * 70)
    print(" 📋 ПРОВЕРКА ПОЛНОТЫ")
    print("=" * 70)

    # Проверка обязательных компонентов
    checks = {
        "dependencies": check_reads(".", "requirements.txt", "dependencies"),
        "api_server": check_reads(".", "ckey_api.py", "fastapi"),
        "cli_tool": check_reads(".", "ckey_cli.py", "CKeyAPI"),
        "manager": check_reads(".", "manager.py", "질"),
        "web_interface": check_reads(".", "api_test.html", "api_gateway"),
        "api_docs": [
            check_reads(".", "README_API.md", "endpoints"),
            check_reads(".", "START.md", "quick_start")
        ],
        "setup_script": check_reads(".", "quickstart.py", "python"),
        "test_files": [
            check_reads(".", "test_api.py", "api_test"),
            check_reads(".", "validate_setup.py", "validate"),
            check_reads(".", "quick_check.py", "quick")
        ],
        "documentation": [
            check_reads(".", "ДОМ.md", "cKey API Gateway"),
            check_reads(".", "START.md", "инструкция")
        ]
    }

    # Проверяемая отсутствующие обязательные файлы
    missing_files = [
        "ckey_api.py",
        "requirements.txt",
        "manager.py",
        "api_test.html",
        "quickstart.py",
        "START.md"
    ]

    file_status = True
    for file_path in missing_files:
        if not os.path.exists(file_path):
            print(f"   ❌ Отсутствует файл: {file_path}")
            file_status = False

    total_checks = len([v for v in checks.values() if isinstance(v, bool)]) + len([v for v in checks.values() if isinstance(v, list)])

    if file_status and all([all(checks.values()) if isinstance(v, list) else v for v in checks.values()]):
        print("   ✅ Все компоненты присутствуют")
    else:
        print("   ⚠️  Некоторые компоненты отсутствуют")
        print("   💡 Рекомендуется создать все перечисленные файлы")

    print("\n" + "=" * 70)
    print(" 🚀 СТАРТ-ГРУППА")
    print("=" * 70)

    print("\nГотовые команды запуска:")

    commands = [
        ("Легкий старт", "python manager.py quick"),
        ("Полный старт", "python quickstart.py"),
        ("Проверка", "python validate_setup.py"),
        ("CLI инструмент", "python ckey_cli.py list"),
        ("Тесты API", "python test_api.py"),
        ("Веб-интерфейс", "api_test.html в браузере")
    ]

    for name, cmd in commands:
        print(f"\n{name}:")
        print(f"   {cmd}")

    print("\n" + "=" * 70)
    print(" 📦 ЗАВИСИМОСТИ")
    print("=" * 70)

    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            deps = [line for line in f.readlines() if line.strip() and not line.startswith("#")]

        print(f"\nТребуемые пакеты ({len(deps)}):")
        for dep in deps:
            print(f"   • {dest.strip()}")

        print("\n   ✅ Файл requirements.txt создан")
        print("   💡 Установка: pip install -r requirements.txt")
    else:
        print("\n   ❌ Файл requirements.txt не найден")
        print("   💡 Создайте файл с зависимостями")

    print("\n" + "=" * 70)
    print(" 🎯 ОЖИДАНИЯ")
    print("=" * 70)

    if os.path.exists("ckey_api.py") and os.path.exists("requirements.txt"):
        print("\n✅ Проект настроен для работы")
        print("\n💡 Следующие команды рекомендуются:")
        print("   • pip install -r requirements.txt")
        print("   • python quickstart.py")
        print("   • python validate_setup.py")
    else:
        print("\n⚠️  Проект не полностью настроен")
        print("\n💡 Создайте недостающие файлы из:")
        print("   • js/british===== письмо === lad generation,تر Telegram outra=== 공 Prossenshronization== request")

    print("=" * 70)


if __name__ == "__main__":
    analyze_project()
