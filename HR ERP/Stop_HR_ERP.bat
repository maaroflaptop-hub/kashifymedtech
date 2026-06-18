@echo off
title Stopping HR ERP System
echo ===================================================
echo             Stopping HR ERP System
echo ===================================================
echo.

docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Docker is not running or not found. Cannot stop containers.
    pause
    exit /b 1
)

echo [INFO] Stopping and removing containers...
docker-compose down

if %errorlevel% neq 0 (
    echo [ERROR] Failed to stop Docker containers.
    pause
    exit /b 1
)

echo.
echo HR ERP system containers have been stopped successfully.
echo.
timeout /t 3 >nul
