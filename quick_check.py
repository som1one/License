#!/usr/bin/env python
"""Quick test check"""

import requests
import json

try:
    response = requests.get("http://localhost:8000/api/products", timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ API работает!")
        print(f"Доступно продуктов: {len(data)}")
        
        print("\nПродукты:")
        for code, name in sorted(data.items()):
            print(f"  {code}: {name}")
    else:
        print(f"❌ Ошибка API: статус {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ API не запущен")
    print("Запустите: python manager.py test")
except Exception as e:
    print(f"❌ Ошибка: {e}")
