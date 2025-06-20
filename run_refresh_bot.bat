@echo off
color 0A
title REFRESHO - Advanced Web Refresher Tool by Addy@Xenonesis

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █    ██████╗ ███████╗███████╗██████╗ ███████╗███████╗██╗  ██╗ █
echo █    ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██║  ██║ █
echo █    ██████╔╝█████╗  █████╗  ██████╔╝█████╗  ███████╗███████║ █
echo █    ██╔══██╗██╔══╝  ██╔══╝  ██╔══██╗██╔══╝  ╚════██║██╔══██║ █
echo █    ██║  ██║███████╗██║     ██║  ██║███████╗███████║██║  ██║ █
echo █    ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝ █
echo █                                                              █
echo █              Developed by Addy@Xenonesis                    █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo [*] Initializing REFRESHO environment...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo [INFO] Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo [+] Python detected

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo [*] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [+] Virtual environment created
) else (
    echo [+] Virtual environment found
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)

echo [+] Virtual environment activated

REM Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install dependencies
echo [*] Installing dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    echo [INFO] Please check your internet connection
    pause
    exit /b 1
)

echo [+] Dependencies installed successfully
echo.
echo [*] Launching REFRESHO...
echo.

REM Run the refresh bot script
python refresh_bot.py

echo.
echo [*] REFRESHO session completed
echo.

REM Ask user if they want to run tests
set /p run_tests="[?] Do you want to run tests? (y/N): "
if /i "%run_tests%"=="y" (
    echo [*] Running tests...
    python -m unittest test_refresh_bot.py -v
    echo [+] Tests completed
)

REM Deactivate virtual environment
deactivate

echo.
echo [*] Thanks for using REFRESHO!
echo [*] Developed by Addy@Xenonesis
echo.
pause
