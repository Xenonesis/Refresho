@echo off
echo Installing REFRESHO v4.0 Dependencies...
echo.

echo [1/3] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [2/3] Installing required packages...
pip install -r requirements.txt

echo.
echo.
echo Installation complete! You can now run refresh_bot.py
pause