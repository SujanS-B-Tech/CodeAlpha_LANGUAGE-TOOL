@echo off
cd /d "%~dp0"
title LinguaBridge — Language Translation Tool

echo =====================================================================
echo           LinguaBridge — Language Translation Tool Launcher
echo =====================================================================
echo.

:: 1. Verify Python availability
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        goto NoPython
    ) else (
        set "PY_CMD=py"
    )
) else (
    set "PY_CMD=python"
)

echo [*] Python detected:
%PY_CMD% --version
echo.

:: 2. Check if .venv already exists
if exist ".venv\Scripts\python.exe" goto StartApp

:: 3. Create .venv if not exists
echo [*] Creating virtual environment (.venv)...
%PY_CMD% -m venv .venv
if errorlevel 1 goto VenvFailed

:: 4. Install dependencies
echo [*] Installing dependencies from requirements.txt...
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto PipFailed

:StartApp
:: 5. Initialize .env if missing
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo [*] Initialized .env template.
    )
)

:: 6. Launch Streamlit Application
echo.
echo =====================================================================
echo [OK] Launching LinguaBridge Application...
echo Browser URL: http://localhost:8501
echo To stop the server, press Ctrl+C in this terminal window.
echo =====================================================================
echo.

.venv\Scripts\python.exe -m streamlit run app.py

echo.
echo LinguaBridge process ended.
pause
exit /b 0

:NoPython
echo.
echo =====================================================================
echo [ERROR] Python is not installed or not added to your Windows PATH.
echo =====================================================================
echo 1. Download Python from: https://www.python.org/downloads/
echo 2. During installation, CHECK the box: "Add python.exe to PATH"
echo 3. Restart your terminal or computer and run start.bat again.
echo.
pause
exit /b 1

:VenvFailed
echo.
echo =====================================================================
echo [ERROR] Failed to create virtual environment (.venv).
echo =====================================================================
echo Please ensure Python virtual environment module is installed.
echo.
pause
exit /b 1

:PipFailed
echo.
echo =====================================================================
echo [ERROR] Failed to install dependencies from requirements.txt.
echo =====================================================================
echo Check your internet connection or run manually:
echo   .venv\Scripts\python.exe -m pip install -r requirements.txt
echo.
pause
exit /b 1
