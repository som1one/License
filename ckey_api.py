#!/usr/bin/env python
"""
cKey API Gateway - Production ready version
Упрощенный API без лишних логов
"""
import asyncpg
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="cKey API Gateway",
    description="API для получения лицензий от ckey.run",
    version="2.0.0"
)

CKEY_API = "https://ckey.run/generateLicense/file"
PRODUCTS = {
    "II": "IntelliJ IDEA",
    "PC": "PyCharm",
    "A": "Android Studio",
    "CL": "DataGrip",
    "J": "JetBrains Rider"
}


class LicenseRequest(BaseModel):
    product: str
    name: str = "ckey.run"
    expiry: str = "2099-12-31"
    assignee: str = ""


@app.get("/")
def root():
    return {
        "status": "ok",
        "version": "2.0.0",
        "docs": "/docs"
    }


@app.get("/status")
def status():
    return {"status": "running"}


@app.get("/products")
def get_products():
    return PRODUCTS


@app.post("/license")
def create_license(req: LicenseRequest):
    """Генерация лицензии"""
    if req.product not in PRODUCTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid product code. Available: {list(PRODUCTS.keys())}"
        )

    import requests

    payload = {
        "assigneeName": req.assignee,
        "expiryDate": req.expiry,
        "licenseName": req.name,
        "productCode": req.product
    }

    try:
        response = requests.post(CKEY_API, json=payload, timeout=30)

        if response.status_code == 200:
            return JSONResponse({
                "success": True,
                "data": response.text[:500] + "..." if len(response.text) > 500 else response.text,
                "product": req.product,
                "name": req.name
            })
        else:
            raise HTTPException(
                status_code=500,
                detail=f"API error: {response.status_code} - {response.text[:100]}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Request failed: {str(e)}"
        )


class LicenseRequest2(BaseModel):
    product: str
    name: str = "ckey.run"
    expiry: str = "2099-12-31"
    assignee: str = ""


@app.post("/license/generate")
def generate_license(req: LicenseRequest2):
    """Альтернативный эндпоинт"""
    if req.product not in PRODUCTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid product code. Available: {list(PRODUCTS.keys())}"
        )

    import requests

    payload = {
        "assigneeName": req.assignee,
        "expiryDate": req.expiry,
        "licenseName": req.name,
        "productCode": req.product
    }

    try:
        response = requests.post(CKEY_API, json=payload, timeout=30)

        if response.status_code == 200:
            return JSONResponse({
                "success": True,
                "data": response.text,
                "product": req.product
            })
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    raise HTTPException(
        status_code=500,
        detail="Failed to generate license"
    )


@app.on_event("startup")
async def startup():
    """Startup event"""
    pass


@app.on_event("shutdown")
async def shutdown():
    """Shutdown event"""
    pass
