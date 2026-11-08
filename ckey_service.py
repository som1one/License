import uvicorn
import sys
import os
import signal
import atexit

class CKeyAPIService:
    def __init__(self, host='127.0.0.1', port=8000):
        self.host = host
        self.port = port
        self.process = None
        self.pid_file = 'ckey_api.pid'
        self.log_file = 'ckey_api.log'

    def _write_pid(self):
        with open(self.pid_file, 'w') as f:
            f.write(str(os.getpid()))

    def _remove_pid(self):
        if os.path.exists(self.pid_file):
            os.remove(self.pid_file)

    def start(self):
        """Запуск API в фоне"""
        if self.is_running():
            print(f"API already running on {self.host}:{self.port}")
            return True

        self._write_pid()
        self.process = uvicorn.run(
            'ckey_api:app',
            host=self.host,
            port=self.port,
            workers=1,
            log_level="info",
            access_log=False,
            use_colors=False
        )
        return True

    def stop(self):
        """Остановка API"""
        pid = self._get_pid()
        if pid:
            try:
                import subprocess
                subprocess.run(['taskkill', '/PID', str(pid)], capture_output=True)
                time.sleep(1)
                self._remove_pid()
                return True
            except Exception:
                return False
        return False

    def restart(self):
        """Перезапуск"""
        self.stop()
        time.sleep(1)
        return self.start()

    def is_running(self):
        """Проверка статуса"""
        pid = self._get_pid()
        if not pid:
            return False
        try:
            import psutil
            p = psutil.Process(pid)
            return p.is_running()
        except:
            return False

    def _get_pid(self):
        try:
            with open(self.pid_file, 'r') as f:
                return int(f.read().strip())
        except:
            return None

if __name__ == '__main__':
    import argparse
    import time

    parser = argparse.ArgumentParser(description='CKey API Service')
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'status', 'logs'])
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8000)

    args = parser.parse_args()

    service = CKeyAPIService(host=args.host, port=args.port)

    if args.action == 'start':
        service.start()
    elif args.action == 'stop':
        service.stop()
    elif args.action == 'restart':
        service.restart()
    elif args.action == 'status':
        print(f"Status: {'RUNNING' if service.is_running() else 'STOPPED'}")
        print(f"PID: {service._get_pid() or 'N/A'}")
        print(f"URL: http://{service.host}:{service.port}")
    elif args.action == 'logs':
        if service._get_pid():
            time.sleep(1)
            with open(service.log_file, 'r') as f:
                # Read last 50 lines
                lines = f.readlines()
                for line in lines[-50:]:
                    print(line.strip())
        else:
            print("No logs - service not running")
