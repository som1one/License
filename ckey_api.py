#!/usr/bin/env python
"""
cKey API Gateway - самодостаточный сервер активации JetBrains
Кеширует ja-netfilter, отдаёт ключи и скрипты активации
"""
import os
import threading
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse, Response
from pydantic import BaseModel
import requests

app = FastAPI(
    title="cKey API Gateway",
    description="Сервер активации JetBrains продуктов",
    version="3.0.0"
)

CKEY_SRC = "https://ckey.run"
CKEY_API = f"{CKEY_SRC}/generateLicense/file"

CACHE_DIR = Path("ja-netfilter-cache")
JA_NETFILTER_DIR = CACHE_DIR / "ja-netfilter"

FILES_TO_CACHE = [
    "ja-netfilter.jar",
    "config/dns.conf",
    "config/env.conf",
    "config/native.conf",
    "config/power.conf",
    "config/url.conf",
    "plugins/dns.jar",
    "plugins/env.jar",
    "plugins/native.jar",
    "plugins/power.jar",
    "plugins/url.jar",
    "plugins/hideme.jar",
    "plugins/privacy.jar",
]

PRODUCTS = {
    "II": "IntelliJ IDEA",
    "PC": "PyCharm",
    "A": "Android Studio",
    "CL": "DataGrip",
    "J": "JetBrains Rider",
}

PRODUCT_CODE_MAP = {
    "II": "II,PCWMP,PSI",
    "PC": "PC,PSI,PCWMP",
    "A": "A,PCWMP,PSI",
    "CL": "CL,PSI,PCWMP",
    "J": "RD,PDB,PSI,PCWMP",
}

PRODUCT_DIR_MAP = {
    "II": "idea",
    "PC": "pycharm",
    "A": "androidstudio",
    "CL": "datagrip",
    "J": "rider",
}


class LicenseRequest(BaseModel):
    product: str
    name: str = "ckey.run"
    expiry: str = "2099-12-31"
    assignee: str = ""


# ---------------------------------------------------------------------------
# Кеширование ja-netfilter
# ---------------------------------------------------------------------------

def cache_file(url: str, dest: Path) -> bool:
    if dest.exists():
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            dest.write_bytes(r.content)
            return True
    except Exception as e:
        print(f"  Failed to cache {url}: {e}")
    return False


def cache_ja_netfilter():
    print("Caching ja-netfilter files...")
    ok = 0
    failed = 0
    for rel_path in FILES_TO_CACHE:
        url = f"{CKEY_SRC}/ja-netfilter/{rel_path}"
        dest = JA_NETFILTER_DIR / rel_path
        if cache_file(url, dest):
            ok += 1
        else:
            failed += 1
    print(f"Cached {ok}/{len(FILES_TO_CACHE)} files" +
          (f" ({failed} failed)" if failed else ""))


@app.on_event("startup")
def on_startup():
    cache_ja_netfilter()


# ---------------------------------------------------------------------------
# Эндпоинты
# ---------------------------------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "ok",
        "version": "3.0.0",
        "docs": "/docs",
        "endpoints": {
            "license": "POST /api/license",
            "license_raw": "POST /api/license/raw",
            "license_v2": "POST /api/license/v2 (ckey.run-совместимый)",
            "license_worker": "POST /api/license/worker",
            "activate": "GET /api/activate/{product}",
            "activate_post": "POST /api/activate",
            "products": "GET /products",
            "ja_netfilter": "GET /ja-netfilter/{path}",
        }
    }


@app.get("/status")
def status():
    return {"status": "running"}


@app.get("/products")
def get_products():
    return PRODUCTS


# ---------------------------------------------------------------------------
# Раздача кешированных файлов ja-netfilter
# ---------------------------------------------------------------------------

@app.get("/ja-netfilter/{path:path}")
def serve_ja_netfilter(path: str):
    file_path = JA_NETFILTER_DIR / path
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(str(file_path))


# ---------------------------------------------------------------------------
# Генерация ключа
# ---------------------------------------------------------------------------

def extract_certificate_key(content: str) -> str | None:
    for tag in ["<certificate-key>", "<Certificate-Key>", "<CERTIFICATE-KEY>"]:
        start = content.find(tag)
        if start != -1:
            return content[start + len(tag):].strip()
    return None


def fetch_key(product: str, name: str = "ckey.run",
              expiry: str = "2099-12-31", assignee: str = "") -> str:
    payload = {
        "assigneeName": assignee,
        "expiryDate": expiry,
        "licenseName": name,
        "productCode": product,
    }
    headers = {"Content-Type": "application/json",
               "User-Agent": "ckey-api-gateway/3.0.0"}
    session = requests.Session()
    session.trust_env = False
    resp = session.post(CKEY_API, json=payload, headers=headers, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"ckey.run returned {resp.status_code}")
    content = resp.text
    key = extract_certificate_key(content)
    if not key:
        raise RuntimeError("No certificate key in response")
    return key


@app.post("/api/license")
def create_license(req: LicenseRequest):
    if req.product not in PRODUCTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid product. Available: {list(PRODUCTS.keys())}",
        )
    try:
        key = fetch_key(req.product, req.name, req.expiry, req.assignee)
        return JSONResponse({
            "success": True,
            "data": key,
            "product": req.product,
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/license/raw")
def create_license_raw(req: LicenseRequest):
    if req.product not in PRODUCTS:
        raise HTTPException(status_code=400, detail=f"Invalid product")
    try:
        key = fetch_key(req.product, req.name, req.expiry, req.assignee)
        return Response(content=key, media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# ckey.run-совместимый endpoint для mentor-organizer
# Принимает те же имена полей, что и ckey.run, отдаёт ключ с <certificate-key>
# ---------------------------------------------------------------------------

class LegacyLicenseRequest(BaseModel):
    productCode: str
    licenseName: str = "LeonovCare"
    expiryDate: str = "2099-12-31"
    assigneeName: str = ""


@app.post("/api/license/v2")
def create_license_v2(req: LegacyLicenseRequest):
    # Нормализуем код продукта — берём первый из набора "PC,PSI,PCWMP" → "PC"
    code = req.productCode.strip().upper().split(",")[0]
    if code not in PRODUCTS:
        raise HTTPException(status_code=400, detail=f"Invalid product: {code}")
    try:
        key = fetch_key(code, req.licenseName, req.expiryDate, req.assigneeName)
        # Возвращаем в формате, который ожидает ckey_client.py
        body = f"<certificate-key>\n{key}"
        return Response(content=body, media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Selenium Worker
# ---------------------------------------------------------------------------

worker_lock = threading.Lock()
_worker_cache = {}


@app.post("/api/license/worker")
def create_license_worker(req: LicenseRequest):
    if req.product not in PRODUCTS:
        raise HTTPException(status_code=400, detail=f"Invalid product")

    from ckey_worker import CKeyWorker

    with worker_lock:
        key = _worker_cache.get(req.product)
        if key:
            return JSONResponse({"success": True, "data": key, "product": req.product, "method": "cache"})

    result = None

    def run_worker(product: str):
        nonlocal result
        try:
            with CKeyWorker(timeout=45) as w:
                k = w.get_key(product)
                if k:
                    _worker_cache[product] = k
                    result = k
        except Exception as e:
            print(f"[WORKER] Background error: {e}", file=sys.stderr)

    t = threading.Thread(target=run_worker, args=(req.product,), daemon=True)
    t.start()
    t.join(timeout=50)

    if result:
        return JSONResponse({"success": True, "data": result, "product": req.product, "method": "worker"})

    cached = _worker_cache.get(req.product)
    if cached:
        return JSONResponse({"success": True, "data": cached, "product": req.product, "method": "cache"})

    raise HTTPException(status_code=504, detail="Worker timed out or failed")


# ---------------------------------------------------------------------------
# Скрипт активации (bash)
# ---------------------------------------------------------------------------

def generate_activate_script(product: str, base_url: str, name: str) -> str:
    product_name = PRODUCTS.get(product, product)
    product_code = PRODUCT_CODE_MAP.get(product, product)
    product_dir = PRODUCT_DIR_MAP.get(product, product.lower())

    return f"""#!/bin/bash

BASE="{base_url}"
PRODUCT_NAME="{product}"
PRODUCT_CODE="{product_code}"

# 1. Рабочая директория (как в ckey.run)
JB_DIR="$HOME/.jb_run"
mkdir -p "$JB_DIR/config" "$JB_DIR/plugins" "$JB_DIR/backups"
CACHE_JB="$HOME/.cache/JetBrains"
CONFIG_JB="$HOME/.config/JetBrains"

# 2. Скачиваем ja-netfilter
echo "Downloading ja-netfilter..."
curl -sL "$BASE/ja-netfilter/ja-netfilter.jar" -o "$JB_DIR/ja-netfilter.jar"
for f in config/dns.conf config/env.conf config/native.conf config/power.conf config/url.conf; do
    curl -sL "$BASE/ja-netfilter/$f" -o "$JB_DIR/$f"
done
for f in plugins/dns.jar plugins/env.jar plugins/native.jar plugins/power.jar plugins/url.jar plugins/hideme.jar plugins/privacy.jar; do
    curl -sL "$BASE/ja-netfilter/$f" -o "$JB_DIR/$f"
done

# 3. Ищем установки IDE через .cache/JetBrains
echo "Looking for {product_name} installation..."
TARGET_DIRS=""
if [ -d "$CACHE_JB" ]; then
    for dir in "$CACHE_JB"/*; do
        [ -d "$dir" ] || continue
        dir_name=$(basename "$dir" | tr '[:upper:]' '[:lower:]')
        if [[ "$dir_name" == *"{product_dir}"* ]] || [[ "$dir_name" == *"$PRODUCT_NAME"* ]]; then
            # Проверяем .home файл
            home_file="$dir/.home"
            if [ -f "$home_file" ]; then
                install_path=$(cat "$home_file")
                if [ -d "$install_path" ]; then
                    echo "  Found: $install_path"
                    TARGET_DIRS="$TARGET_DIRS $dir"
                fi
            fi
        fi
    done
fi

if [ -z "$TARGET_DIRS" ]; then
    # Прямой поиск
    for dir in "$CACHE_JB"/*; do
        [ -d "$dir" ] || continue
        dir_name=$(basename "$dir" | tr '[:upper:]' '[:lower:]')
        if [[ "$dir_name" == *"{product_dir}"* ]]; then
            echo "  Found cache: $dir"
            TARGET_DIRS="$TARGET_DIRS $dir"
        fi
    done
fi

if [ -z "$TARGET_DIRS" ]; then
    echo "Warning: IDE not found under $CACHE_JB"
    echo "Key will still be generated for manual activation."
fi

# 4. Настраиваем .vmoptions и сохраняем ключ
for CACHE_DIR in $TARGET_DIRS; do
    CACHE_NAME=$(basename "$CACHE_DIR")
    CONFIG_DIR="$CONFIG_JB/$CACHE_NAME"
    mkdir -p "$CONFIG_DIR"
    
    # .vmoptions — ищем в config, если нет — создаём
    VM_FILE=""
    for f in "$CONFIG_DIR"/*.vmoptions; do
        [ -f "$f" ] && {{ VM_FILE="$f"; break; }}
    done
    [ -z "$VM_FILE" ] && VM_FILE="$CONFIG_DIR/{product_dir}.vmoptions"
    
    # Резервная копия
    if [ -f "$VM_FILE" ]; then
        cp "$VM_FILE" "$JB_DIR/backups/$(basename "$VM_FILE").bak.$(date +%s)"
    fi
    
    # Добавляем javaagent (как в официальном скрипте)
    AGENT_LINE="-javaagent:$JB_DIR/ja-netfilter.jar=jetbrains"
    if ! grep -qF -- "$AGENT_LINE" "$VM_FILE" 2>/dev/null; then
        echo "$AGENT_LINE" >> "$VM_FILE"
        echo "  Added javaagent to $CACHE_NAME"
    fi
    
    # jetbrains_client.vmoptions
    CLIENT_VM="$CONFIG_DIR/jetbrains_client.vmoptions"
    if [ ! -f "$CLIENT_VM" ]; then
        echo "$AGENT_LINE" > "$CLIENT_VM"
    else
        if ! grep -qF -- "$AGENT_LINE" "$CLIENT_VM" 2>/dev/null; then
            echo "$AGENT_LINE" >> "$CLIENT_VM"
        fi
    fi
    
    # disabled_plugins.txt — удаляем com.intellij.modules.ultimate
    DP_FILE="$CONFIG_DIR/disabled_plugins.txt"
    if [ -f "$DP_FILE" ]; then
        if [[ "$(uname -s)" == "Darwin" ]]; then
            sed -i '' '/^com.intellij.modules.ultimate$/d' "$DP_FILE" 2>/dev/null || true
        else
            sed -i '/^com.intellij.modules.ultimate$/d' "$DP_FILE" 2>/dev/null || true
        fi
    fi
    
    # Скачиваем ключ
    echo "  Downloading license key for $CACHE_NAME..."
    curl -s -X POST "$BASE/api/license/raw" \\
        -H "Content-Type: application/json" \\
        -d '{{"product":"{product}","name":"{name}"}}' \\
        -o "$CONFIG_DIR/{name}.key"
    
    echo "  Key saved to $CONFIG_DIR/{name}.key"
done

echo ""
echo "Done. Restart your IDE to apply changes."
"""


@app.get("/api/activate/{product}")
def activate_script_get(product: str, name: str = "ckey.run"):
    if product not in PRODUCTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid product. Available: {list(PRODUCTS.keys())}",
        )
    host = os.environ.get("HOST", "http://127.0.0.1:8000")
    script = generate_activate_script(product, host, name)
    return Response(content=script, media_type="text/plain",
                    headers={"Content-Disposition": "attachment; filename=activate.sh"})


@app.post("/api/activate")
def activate_script_post(req: LicenseRequest):
    if req.product not in PRODUCTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid product. Available: {list(PRODUCTS.keys())}",
        )
    host = os.environ.get("HOST", "http://127.0.0.1:8000")
    script = generate_activate_script(req.product, host, req.name)
    return Response(content=script, media_type="text/plain",
                    headers={"Content-Disposition": "attachment; filename=activate.sh"})


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run("ckey_api:app", host=host, port=port, log_level="info")
