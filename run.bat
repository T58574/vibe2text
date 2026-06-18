@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH. Please install Python.
    pause
    exit /b 1
)

if not exist .venv (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

if not exist .env (
    echo [INFO] Creating .env from .env.example...
    copy .env.example .env >nul
)

echo [INFO] Installing/updating requirements...
.venv\Scripts\python -m pip install --upgrade pip >nul
.venv\Scripts\python -m pip install -r requirements.txt >nul
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo [INFO] Starting STT Vidjet...
start "" ".venv\Scripts\pythonw.exe" main.py
echo [INFO] App launched successfully in background.
