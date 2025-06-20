@echo off
color 0A
title REFRESHO v2.0 - ULTIMATE WEB REFRESHER BEAST by Addy@Xenonesis
mode con: cols=120 lines=40

echo.
echo ████████████████████████████████████████████████████████████████████████████████████████████████████████████████
echo █                                                                                                                █
echo █    ██████╗ ███████╗███████╗██████╗ ███████╗███████╗██╗  ██╗ ██████╗     ██╗   ██╗██████╗     ██████╗         █
echo █    ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██║  ██║██╔═══██╗    ██║   ██║╚════██╗   ██╔═████╗        █
echo █    ██████╔╝█████╗  █████╗  ██████╔╝█████╗  ███████╗███████║██║   ██║    ██║   ██║ █████╔╝   ██║██╔██║        █
echo █    ██╔══██╗██╔══╝  ██╔══╝  ██╔══██╗██╔══╝  ╚════██║██╔══██║██║   ██║    ╚██╗ ██╔╝██╔═══╝    ████╔╝██║        █
echo █    ██║  ██║███████╗██║     ██║  ██║███████╗███████║██║  ██║╚██████╔╝     ╚████╔╝ ███████╗██╗╚██████╔╝        █
echo █    ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝       ╚═══╝  ╚══════╝╚═╝ ╚═════╝         █
echo █                                                                                                                █
echo █                              🔥 ULTIMATE WEB REFRESHER BEAST 🔥                                              █
echo █                                   💀 Developed by Addy@Xenonesis 💀                                          █
echo █                                                                                                                █
echo ████████████████████████████████████████████████████████████████████████████████████████████████████████████████
echo.

REM Display system information
echo [SYSTEM] Analyzing host environment...
systeminfo | findstr /C:"OS Name" /C:"Total Physical Memory" /C:"System Type"
echo.

REM Check Python installation
echo [SCAN] Detecting Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [CRITICAL] Python not detected in system PATH!
    echo [SOLUTION] Install Python 3.7+ from https://python.org
    echo [STATUS] Mission aborted - Python required
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [SUCCESS] Python %PYTHON_VERSION% detected and operational
echo.

REM Check Chrome installation
echo [SCAN] Detecting Chrome browser...
reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version >nul 2>&1
if errorlevel 1 (
    reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Google\Chrome\BLBeacon" /v version >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] Chrome browser not detected
        echo [INFO] Chrome will be auto-downloaded by Selenium if needed
    ) else (
        echo [SUCCESS] Chrome browser detected and ready
    )
) else (
    echo [SUCCESS] Chrome browser detected and ready
)
echo.

REM Virtual environment setup
echo [SETUP] Configuring virtual environment...
if not exist ".venv" (
    echo [CREATE] Building isolated Python environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [CRITICAL] Virtual environment creation failed!
        echo [DEBUG] Check Python installation and permissions
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created successfully
) else (
    echo [SUCCESS] Virtual environment already exists
)

REM Activate virtual environment
echo [ACTIVATE] Entering virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [CRITICAL] Virtual environment activation failed!
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment activated

REM Upgrade pip
echo [UPGRADE] Updating package manager...
python -m pip install --upgrade pip --quiet --no-warn-script-location
echo [SUCCESS] Package manager updated

REM Install dependencies
echo [INSTALL] Installing REFRESHO dependencies...
echo [INFO] Installing: selenium, colorama, psutil, requests, pillow, fake-useragent
pip install -r requirements.txt --quiet --no-warn-script-location
if errorlevel 1 (
    echo [CRITICAL] Dependency installation failed!
    echo [DEBUG] Check internet connection and requirements.txt
    pause
    exit /b 1
)
echo [SUCCESS] All dependencies installed successfully

REM Display pre-launch information
echo.
echo ████████████████████████████████████████████████████████████████████████████████████████████████████████████████
echo █                                        LAUNCH SEQUENCE                                                       █
echo ████████████████████████████████████████████████████████████████████████████████████████████████████████████████
echo.
echo [READY] REFRESHO v2.0 is armed and ready for deployment
echo [MODES] Available: STEALTH ^| ASSAULT ^| NUCLEAR
echo [FEATURES] Matrix effects, System monitoring, Intelligent targeting
echo [CAPABILITIES] Up to 9,999,999 refreshes with advanced evasion
echo.

REM Launch countdown
for /L %%i in (3,-1,1) do (
    echo [COUNTDOWN] Launching in %%i seconds...
    timeout /t 1 /nobreak >nul
)

echo [LAUNCH] Initiating REFRESHO v2.0...
echo.

REM Execute REFRESHO
python refresh_bot.py

REM Post-execution
echo.
echo ████████████████████████████████████████████████████████████████████████████████████████████████████████████████
echo █                                      MISSION COMPLETE                                                        █
echo ████████████████████████████████████████████████████████████████████████████████████████████████████████████████
echo.

REM Ask about testing
set /p run_tests="[OPTION] Execute test suite? (y/N): "
if /i "%run_tests%"=="y" (
    echo [TESTING] Running comprehensive test suite...
    echo.
    python -m unittest test_refresh_bot.py -v
    echo.
    echo [COMPLETE] Test suite execution finished
)

REM Performance report
echo.
echo [REPORT] Session performance summary:
echo [TIME] Execution completed at %date% %time%
echo [STATUS] All systems nominal
echo [CLEANUP] Deactivating virtual environment...

REM Deactivate virtual environment
deactivate

echo.
echo ████████████████████████████████████████████████████████████████████████████████████████████████████████████████
echo █                                                                                                                █
echo █                           🎯 REFRESHO v2.0 SESSION TERMINATED 🎯                                            █
echo █                                                                                                                █
echo █                              💀 Thanks for using REFRESHO! 💀                                               █
echo █                                 🔥 Developed by Addy@Xenonesis 🔥                                           █
echo █                                                                                                                █
echo █                                  #HackTheWeb #RefreshThePlanet                                               █
echo █                                                                                                                █
echo ████████████████████████████████████████████████████████████████████████████████████████████████████████████████
echo.
pause