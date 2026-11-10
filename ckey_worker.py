#!/usr/bin/env python3
"""
cKey Worker - Selenium воркер для получения ключей через ckey.run
Открывает страницу, кликает по продукту, заполняет диалог, перехватывает ключ
"""
import os
import sys
import time
import re
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


PRODUCT_XPATHS = {
    "PC": '//article[@data-product="PyCharm"]//button[contains(@class, "license-copy")]',
    "II": '//article[@data-product="IntelliJ IDEA"]//button[contains(@class, "license-copy")]',
    "A":  '//article[@data-product="Android Studio"]//button[contains(@class, "license-copy")]',
    "CL": '//article[@data-product="CLion"]//button[contains(@class, "license-copy")]',
    "J":  '//article[@data-product="Rider"]//button[contains(@class, "license-copy")]',
}


class CKeyWorker:
    def __init__(self, timeout: int = 30):
        self.driver = None
        self.timeout = timeout

    def start(self) -> bool:
        try:
            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1280,800")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_argument(
                "user-agent=Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )

            self.driver = webdriver.Chrome(options=options)

            # Hide webdriver + intercept clipboard before page load
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                window.__ckey_key = null;
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                navigator.clipboard.writeText = async (text) => {
                    window.__ckey_key = text;
                };
                """
            })
            return True
        except Exception as e:
            print(f"[WORKER] Failed to start browser: {e}", file=sys.stderr)
            return False

    def get_key(self, product_code: str, name: str = "ckey.run") -> Optional[str]:
        if product_code not in PRODUCT_XPATHS:
            print(f"[WORKER] Unknown product: {product_code}", file=sys.stderr)
            return None

        if not self.driver and not self.start():
            return None

        try:
            xpath = PRODUCT_XPATHS[product_code]
            self.driver.get("https://ckey.run")

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-grid"))
            )
            print(f"[WORKER] Page loaded: {self.driver.title}", file=sys.stderr)

            btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            print(f"[WORKER] Found button for {product_code}", file=sys.stderr)

            # Re-override clipboard (runtime safety)
            self.driver.execute_script("""
            window.__ckey_key = null;
            navigator.clipboard.writeText = async (text) => {
                window.__ckey_key = text;
            };
            """)

            # Click → opens license form dialog
            btn.click()

            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.ID, "form"))
            )
            print(f"[WORKER] Dialog opened, submitting...", file=sys.stderr)

            # Submit form → generates key → copies to clipboard
            submit = self.driver.find_element(By.CSS_SELECTOR, "#form .submit[type=submit]")
            submit.click()

            # Wait for key on clipboard
            for _ in range(self.timeout * 2):
                time.sleep(0.5)
                try:
                    k = self.driver.execute_script("return window.__ckey_key || null;")
                    if k and len(k) > 50:
                        print(f"[WORKER] Key obtained ({len(k)} chars)", file=sys.stderr)
                        return k
                except:
                    pass

            # Fallback: scan page text
            body = self.driver.find_element(By.TAG_NAME, "body").text
            matches = re.findall(r'[A-F0-9]{10}-eyJ[A-Za-z0-9_\-=/+]+=+', body)
            for m in matches:
                if len(m) > 200:
                    print(f"[WORKER] Extracted from page text", file=sys.stderr)
                    return m

            print(f"[WORKER] No key found", file=sys.stderr)
            return None

        except Exception as e:
            print(f"[WORKER] Error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return None

    def close(self):
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="cKey Worker")
    parser.add_argument("product", nargs="?", default="PC", help="Product code: PC, II, A, CL, J")
    args = parser.parse_args()

    with CKeyWorker() as w:
        key = w.get_key(args.product.upper())
        if key:
            print(key)
            return 0
        return 1


if __name__ == "__main__":
    sys.exit(main())
