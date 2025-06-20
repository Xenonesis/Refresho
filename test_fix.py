#!/usr/bin/env python3
"""
Quick test to verify the WebDriver fix
"""
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

try:
    from webdriver_manager.chrome import ChromeDriverManager
    print("[OK] webdriver-manager imported successfully")
except ImportError as e:
    print(f"[ERROR] webdriver-manager import failed: {e}")
    sys.exit(1)

def test_webdriver():
    print("Testing WebDriver configuration...")
    
    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # Service with automatic ChromeDriver management
    try:
        service = Service(ChromeDriverManager().install())
        print("[OK] ChromeDriver service created successfully")
    except Exception as e:
        print(f"[ERROR] ChromeDriver service failed: {e}")
        return False
    
    # Test WebDriver initialization
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("[OK] Chrome WebDriver initialized successfully")
        
        # Test navigation
        driver.get("https://www.google.com")
        print(f"[OK] Successfully navigated to: {driver.current_url}")
        
        # Test refresh
        driver.refresh()
        print("[OK] Page refresh successful")
        
        driver.quit()
        print("[OK] WebDriver closed successfully")
        return True
        
    except Exception as e:
        print(f"[ERROR] WebDriver test failed: {e}")
        return False

if __name__ == "__main__":
    print("REFRESHO v2.0 - WebDriver Fix Test")
    print("=" * 40)
    
    success = test_webdriver()
    
    print("=" * 40)
    if success:
        print("[SUCCESS] All tests passed! Your REFRESHO is ready to use.")
        print("Run 'python refresh_bot.py' to start the main application.")
    else:
        print("[FAILED] Tests failed. Please check your Chrome installation.")
        print("Make sure Chrome browser is installed and up to date.")