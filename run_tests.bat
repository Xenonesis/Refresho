@echo off
REM Run automated tests for REFRESHO v5.0

echo ============================================
echo REFRESHO v5.0 - Test Suite Runner
echo ============================================
echo.

REM Check if pytest is installed
python -m pytest --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pytest not installed. Installing...
    pip install pytest pytest-cov pytest-timeout
    echo.
)

echo [1/3] Running unit tests...
python -m pytest tests/test_automated.py -v
echo.

echo [2/3] Running integration tests...
python tests/test_features.py
echo.

echo [3/3] Running demo test...
python demo.py
echo.

echo ============================================
echo Test suite completed!
echo ============================================
pause
