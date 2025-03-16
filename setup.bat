@echo off
setlocal enabledelayedexpansion

:: Color codes
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "NC=[0m"

:: Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo %RED%Python is not installed. Please download from https://www.python.org/downloads/windows/%NC%
    pause
    exit /b 1
)

:: Create virtual environment
if not exist encryption_env (
    echo %YELLOW%Creating virtual environment...%NC%
    python -m venv encryption_env
)

:: Activate virtual environment
call encryption_env\Scripts\activate

:: Install dependencies
echo %YELLOW%Installing dependencies...%NC%
pip install --upgrade pip
pip install cryptography tkinter pyinstaller

:: Menu
:menu
cls
echo %GREEN%🔒 The Goat's Encryption Tool - Setup Script 🔒%NC%
echo.
echo 1. Run Encryption Tool
echo 2. Create Standalone App
echo 3. Exit
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" goto run_app
if "%choice%"=="2" goto create_standalone
if "%choice%"=="3" goto end
echo %RED%Invalid choice. Try again.%NC%
pause
goto menu

:run_app
echo %GREEN%Launching Encryption Tool...%NC%
python "Advanceder Encryption.py"
pause
goto menu

:create_standalone
echo %YELLOW%Creating standalone application...%NC%
pyinstaller --onefile --windowed --name "GoatEncryption" "Advanceder Encryption.py"
echo %GREEN%Standalone app created in 'dist' directory%NC%
pause
goto menu

:end
echo %GREEN%Goodbye!%NC%
endlocal 