#!/usr/bin/env python
"""
Fast API Testing Tool
Точный и быстрый инструмент для проверки API
"""
import argparse
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("[ERROR] requests not installed. Run: pip install requests")
    sys.exit(1)


PRODUCTS = {
    "II": "IntelliJ IDEA",
    "PC": "PyCharm",
    "A": "Android Studio",
    "CL": "DataGrip",
    "J": "JetBrains Rider"
}


def test_endpoint(url, method="GET", body=None):
    """Test API endpoint"""
    print(f"\n[TEST] {method} {url}...")

    try:
        if method == "GET":
            resp = requests.get(url, timeout=5)
        elif method == "POST":
            resp = requests.post(url, json=body, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")

        print(f"[STATUS] {resp.status_code}")

        if resp.status_code == 200:
            try:
                data = resp.json()
                if "products" in data:
                    print(f"[RESULT] Available products:")
                    for code, name in sorted(data.items()):
                        print(f"  - {code}: {name}")
                    return True
                elif "data" in data:
                    print(f"[RESULT] License generated (first 100 chars)")
                    print(f"  {str(data['data'])[:100]}...")
                    return True
                else:
                    print(f"[RESULT] {data}")
                    return True
            except:
                print(f"[RESULT] Text response ({len(resp.text)} chars)")
                return True
        else:
            print(f"[ERROR] {resp.text[:200]}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Connection refused. Is service running?")
        return False
    except requests.exceptions.Timeout:
        print(f"[ERROR] Request timeout")
        return False
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(description='CKey API Test Tool')
    parser.add_argument('action', choices=['status', 'products', 'pycharm', 'intellij'])
    parser.add_argument('--url', default='http://localhost:8000', help='API URL')

    args = parser.parse_args()

    base_url = f"{args.url}/api"

    print("\n" + "="*50)
    print("CKey API Gateway - Test Tool")
    print("="*50)

    if args.action == 'status':
        success = test_endpoint(f"{base_url}/status")
    elif args.action == 'products':
        success = test_endpoint(f"{base_url}/products")
    elif args.action == 'pycharm':
        success = test_endpoint(
            f"{base_url}/license/generate",
            "POST",
            {"product": "PC", "name": "Test License"}
        )
    elif args.action == 'intellij':
        success = test_endpoint(
            f"{base_url}/license/generate",
            "POST",
            {"product": "II", "name": "Test License"}
        )

    print("\n" + "="*50)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
