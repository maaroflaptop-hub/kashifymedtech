@echo off
title Launching HR ERP System
echo ===================================================
echo             Launching HR ERP System
echo ===================================================
echo.

:: Check if Docker is installed and running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running or not found in the PATH.
    echo Please make sure Docker Desktop is started and running.
    echo.
    pause
    exit /b 1
)

echo [INFO] Docker is running. Building and starting container services...
docker-compose up -d --build

if %errorlevel% neq 0 (
    echo [ERROR] Failed to start Docker containers.
    echo.
    pause
    exit /b 1
)

echo [INFO] Containers started successfully.
echo Waiting 5 seconds for services to initialize...
timeout /t 5 /nobreak >nul

echo Opening browser at http://127.0.0.1:8501...
start http://127.0.0.1:8501

echo.
echo HR ERP system is running in the background.
echo To stop the system, run Stop_HR_ERP.bat
echo.
timeout /t 3 >nul
