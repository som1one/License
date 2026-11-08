#!/usr/bin/env python
"""
CKey API Service Manager
Управление службой API с минимальным колоритным выводом
"""
import os
import sys
import time
import subprocess
import signal
import argparse
from pathlib import Path


class ServiceManager:
    def __init__(self):
        self.home = Path(__file__).parent
        self.pid_file = self.home / "ckey_api.pid"
        self.venv_path = self.home / ".venv"

    def check_admin(self):
        """Проверка прав администратора"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def activate_venv(self):
        """Активация виртуального окружения"""
        if self.venv_path.exists():
            venv_bin = self.venv_path / "Scripts" / "python.exe" if sys.platform == "win32" else self.venv_path / "bin" / "python"
            return str(venv_bin)
        return sys.executable

    def is_running(self):
        """Проверка запущен ли сервис"""
        if self.pid_file.exists():
            try:
                pid = int(self.pid_file.read_text().strip())
                return self._check_process(pid)
            except:
                return False
        return False

    def _check_process(self, pid):
        """Проверка процесса"""
        try:
            import psutil
            p = psutil.Process(pid)
            return p.is_running()
        except:
            return False

    def start(self, verbose=False):
        """Запуск сервиса"""
        if self.is_running():
            print("[OK] Service already running")
            return True

        python = self.activate_venv()
        service_path = self.home / "ckey_service.py"

        cmd = [
            python,
            str(service_path),
            "start"
        ]

        result = subprocess.run(
            cmd,
            cwd=self.home,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            time.sleep(1)
            if self.is_running():
                print(f"[OK] Service started on port 8000")
                if verbose:
                    print(f"[INFO] PID: {self.get_pid()}")
                return True
        print(f"[ERROR] Failed to start service")
        return False

    def stop(self):
        """Остановка сервиса"""
        if not self.is_running():
            print("[OK] Service not running")
            return True

        python = self.activate_venv()
        service_path = self.home / "ckey_service.py"

        result = subprocess.run(
            [python, str(service_path), "stop"],
            cwd=self.home,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            print("[OK] Service stopped")
            return True
        print("[ERROR] Failed to stop service")
        return False

    def restart(self):
        """Перезапуск сервиса"""
        print("[INFO] Restarting service...")
        self.stop()
        time.sleep(1)
        return self.start()

    def status(self):
        """Статус сервиса"""
        if self.is_running():
            pid = self.get_pid()
            print(f"[RUNNING] Service is active")
            print(f"[PORT] 8000")
            print(f"[PID] {pid}")
            print(f"[URL] http://localhost:8000")
            return True
        print(f"[STOPPED] Service is not running")
        return False

    def get_pid(self):
        """Получить PID"""
        if self.pid_file.exists():
            try:
                return int(self.pid_file.read_text().strip())
            except:
                return 0
        return 0

    def fast_test(self):
        """Быстрая проверка API"""
        if not self.is_running():
            print("[ERROR] API is not running")
            return False

        import requests
        try:
            resp = requests.get("http://localhost:8000/api/products", timeout=3)
            print(f"[OK] API is responding")
            print(f"[PROD] {resp.json()}")
            return True
        except:
            print("[ERROR] API not responding")
            return False


def main():
    parser = argparse.ArgumentParser(description='CKey API Service Manager')
    parser.add_argument(
        'action',
        choices=['start', 'stop', 'restart', 'status', 'test'],
        help='Action to perform'
    )
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()
    manager = ServiceManager()

    if args.action == 'start':
        manager.start(args.verbose)
    elif args.action == 'stop':
        manager.stop()
    elif args.action == 'restart':
        manager.restart()
    elif args.action == 'status':
        manager.status()
    elif args.action == 'test':
        manager.fast_test()


if __name__ == '__main__':
    main()
