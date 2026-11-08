from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import requests

app = FastAPI(
    title="cKey Run API Gateway",
    description="API прослойка для получения ключей от ckey.run",
    version="1.0.0"
)

ckey_base_url = "https://ckey.run"
license_url = f"{ckey_base_url}/generateLicense/file"


def fetch_license_sync(
    product_code: str,
    license_name: str = "ckey.run",
    expiry_date: str = "2099-12-31",
    assignee_name: str = ""
) -> Dict[str, Any]:
    """
    Получение лицензии через ckey.run API
    """
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "assigneeName": assignee_name,
        "expiryDate": expiry_date,
        "licenseName": license_name,
        "productCode": product_code
    }

    try:
        response = requests.post(license_url, json=payload, headers=headers, timeout=30)

        if response.status_code == 200:
            return {
                "success": True,
                "data": response.text,
                "product_code": product_code,
                "license_name": license_name,
                "expiry_date": expiry_date,
                "assignee_name": assignee_name
            }
        else:
            return {
                "success": False,
                "error": f"API возвратил статус {response.status_code}",
                "detail": response.text
            }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Ошибка запроса: {str(e)}",
            "detail": str(e)
        }


@app.get("/")
def root():
    """Корневой endpoint"""
    return {
        "message": "cKey API Gateway is running",
        "version": "1.0.0",
        "endpoints": {
            "products": "/api/products",
            "license": "/api/license",
            "ideaplus": "/api/ideaplus",
            "generic": "/api/generic",
            "docs": "/docs"
        }
    }


@app.get("/api/products")
def get_products():
    """Получение списка доступных продуктов"""
    return {
        "II": "IntelliJ IDEA",
        "PC": "PyCharm",
        "A": "Android Studio",
        "CL": "DataGrip",
        "J": "JetBrains Rider"
    }


@app.get("/api/license")
def license_generation(
    product: str = Query(..., description="Код продукта (II, PC, A, CL, J)"),
    name: str = Query("ckey.run", description="Название лицензии"),
    expiry: str = Query("2099-12-31", description="Дата окончания"),
    assignee: str = Query("", description="Имя получателя")
):
    """
    Генерация стандартной лицензии
    """
    result = fetch_license_sync(product, name, expiry, assignee)

    if result["success"]:
        return JSONResponse(content=result)
    else:
        raise HTTPException(status_code=500, detail=result["error"])


@app.get("/api/generic")
def generic_license(
    product: str = Query(..., description="Код продукта"),
    name: str = Query("ckey.run", description="Название лицензии"),
    expiry: str = Query("2099-12-31", description="Дата окончания"),
    assignee: str = Query("", description="Имя получателя")
):
    """
    Общий метод генерации лицензии
    """
    if not product:
        raise HTTPException(status_code=400, detail="Не указан код продукта")

    result = fetch_license_sync(product, name, expiry, assignee)

    if result["success"]:
        return JSONResponse(content=result)
    else:
        raise HTTPException(status_code=500, detail=result["error"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
