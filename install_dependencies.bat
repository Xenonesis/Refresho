@echo off
echo Installing REFRESHO v3.0 Dependencies...
echo.

echo [1/3] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [2/3] Installing required packages...
pip install -r requirements.txt

echo.
echo [3/3] Installing/updating ChromeDriver...
python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"

echo.
echo Installation complete! You can now run refresh_bot.py
pause