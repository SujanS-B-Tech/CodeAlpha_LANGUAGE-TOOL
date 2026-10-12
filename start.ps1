# =====================================================================
# LinguaBridge — Language Translation Tool PowerShell Launcher
# =====================================================================

Set-Location -Path $PSScriptRoot

try {
    Write-Host "=====================================================================" -ForegroundColor Cyan
    Write-Host "          LinguaBridge — Language Translation Tool Launcher           " -ForegroundColor Cyan
    Write-Host "=====================================================================" -ForegroundColor Cyan
    Write-Host ""

    # 1. Detect Python command
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCmd) {
        $pythonCmd = Get-Command py -ErrorAction SilentlyContinue
    }

    if (-not $pythonCmd) {
        Write-Host "[ERROR] Python was not found in your system PATH." -ForegroundColor Red
        Write-Host "Please install Python 3.9+ from https://www.python.org/ and ensure 'Add Python to PATH' is checked." -ForegroundColor Yellow
        Read-Host "`nPress Enter to exit..."
        exit 1
    }

    $ver = & $pythonCmd.Source --version 2>&1
    Write-Host "[*] Detected Python: $ver" -ForegroundColor Green

    # 2. Check / Create Virtual Environment
    $venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        Write-Host "[*] Creating virtual environment in .venv..." -ForegroundColor Yellow
        & $pythonCmd.Source -m venv .venv
    }

    if (-not (Test-Path $venvPython)) {
        Write-Host "[WARNING] Could not create .venv. Falling back to global Python." -ForegroundColor Yellow
        $venvPython = $pythonCmd.Source
    } else {
        Write-Host "[OK] Virtual environment ready." -ForegroundColor Green
    }

    # 3. Install requirements
    Write-Host "[*] Checking and installing dependencies..." -ForegroundColor Yellow
    & $venvPython -m pip install -r requirements.txt

    # 4. Copy .env if not exists
    if (-not (Test-Path ".env")) {
        if (Test-Path ".env.example") {
            Copy-Item ".env.example" ".env"
            Write-Host "[*] Initialized .env template." -ForegroundColor Green
        }
    }

    # 5. Launch Streamlit
    Write-Host ""
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host "[OK] Launching LinguaBridge at http://localhost:8501" -ForegroundColor Green
    Write-Host "Press Ctrl+C in this terminal window to stop the server." -ForegroundColor White
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host ""

    & $venvPython -m streamlit run app.py
}
catch {
    Write-Host "`n[ERROR] An error occurred: $_" -ForegroundColor Red
}
finally {
    Write-Host "`nLinguaBridge process ended."
    Read-Host "Press Enter to exit..."
}
