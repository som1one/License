#!/usr/bin/env python
"""Запуск API сервера ckey_api_fixed.py"""
import subprocess
import sys

if __name__ == "__main__":
    server = subprocess.Popen(
        [sys.executable, "ckey_api_fixed.py"],
        cwd=".",
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    print(f"Server started with PID: {server.pid}")
    print("Docs: http://localhost:8000/docs")
    print("Stop server: Ctrl+C in console or use manager.py")
