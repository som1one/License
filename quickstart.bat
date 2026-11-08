@echo off
REM Quick Start Script for CKey API Service

echo =====================================
echo CKey API Gateway Service
echo =====================================
echo.
REM Activate virtual environment if exists

REM Install dependencies if needed
echo Checking dependencies...
pip show fastapi >nul 2>&1
if %errorLevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting service...
echo Port: 8000
echo Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop
echo =====================================
echo.

python ckey_service_manager.py start

echo.
echo Service started. Run test command.
echo.
pause
