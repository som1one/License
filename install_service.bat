@echo off
REM Windows Service Setup Script for CKey API
REM Этот скрипт устанавливает API как службу Windows

set SERVICE_NAME=CKeyAPI
set SERVICE_DISPLAY_NAME="cKey API Gateway"
set SERVICE_BIN=%~dp0ckey_service.py
set SERVICE_DESC=API Gateway для получения лицензий от ckey.run

echo =====================================
echo Установка CKey API как Windows Service
echo =====================================
echo.

:ADMIN_CHECK
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Необходимо запустить от имени администратора!
    pause
    exit /b 1
)

:REMOVE_SERVICE
echo Проверка существующей службы...
sc query %SERVICE_NAME% >nul 2>&1
if %errorLevel% equ 0 (
    echo Удаление существующей службы...
    sc delete %SERVICE_NAME%
    if %errorLevel% neq 0 (
        echo Ошибка при удалении службы!
        pause
        exit /b 1
    )
    echo Служба удалена
)

:ADD_SERVICE
echo Добавление новой службы...
sc create %SERVICE_NAME% `
    binPath= %SERVICE_BIN% `
    start= auto `
    DisplayName= %SERVICE_DISPLAY_NAME% `
    Description= %SERVICE_DESC%

if %errorLevel% neq 0 (
    echo Ошибка при добавлении службы!
    pause
    exit /b 1
)

echo.
echo =====================================
echo Установка завершена!
echo =====================================
echo.
echo Команды управления:
echo   - Старт:   net start %SERVICE_NAME%
echo   - Стоп:    net stop %SERVICE_NAME%
echo   - Состояние: sc query %SERVICE_NAME%
echo   - Удалить: sc delete %SERVICE_NAME%
echo.
pause
