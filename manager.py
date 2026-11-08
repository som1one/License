#!/usr/bin/env python
import sys
sys.path.insert(0, '.')
from ckey_api_manager import interactive_menu

if __name__ == "__main__":
    try:
        interactive_menu()
    except KeyboardInterrupt:
        print("\n👋 Пока!")
