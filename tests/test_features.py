#!/usr/bin/env python3
"""
REFRESHO v4.0 - Feature Test Script
Test all features to ensure they work correctly
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def test_screenshot_functionality():
    """Test screenshot capture functionality"""
    print("\n[SCREENSHOT] Testing Screenshot Functionality...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Navigate to test page
        driver.get("https://httpbin.org")
        
        # Create screenshots directory
        os.makedirs('screenshots', exist_ok=True)
        
        # Test screenshot capture
        screenshot_path = "screenshots/test_screenshot.png"
        success = driver.save_screenshot(screenshot_path)
        
        if success and os.path.exists(screenshot_path):
            file_size = os.path.getsize(screenshot_path)
            print(f"[OK] Screenshot saved: {screenshot_path} ({file_size} bytes)")
            return True
        else:
            print("[ERROR] Screenshot failed to save")
            return False
            
    except Exception as e:
        print(f"[ERROR] Screenshot test failed: {e}")
        return False
    finally:
        try:
            driver.quit()
        except:
            pass

def test_directory_creation():
    """Test directory creation functionality"""
    print("\n[DIRS] Testing Directory Creation...")
    
    test_dirs = ['screenshots', 'history', 'reports', 'saved_urls']
    
    for dir_name in test_dirs:
        try:
            os.makedirs(dir_name, exist_ok=True)
            if os.path.exists(dir_name):
                print(f"[OK] Directory created: {dir_name}")
            else:
                print(f"[ERROR] Failed to create: {dir_name}")
                return False
        except Exception as e:
            print(f"[ERROR] Directory creation failed for {dir_name}: {e}")
            return False
    
    return True

def test_file_operations():
    """Test file read/write operations"""
    print("\n[FILES] Testing File Operations...")
    
    try:
        # Test JSON file operations
        import json
        test_data = {"test": "data", "timestamp": time.time()}
        
        with open("test_file.json", "w") as f:
            json.dump(test_data, f)
        
        with open("test_file.json", "r") as f:
            loaded_data = json.load(f)
        
        if loaded_data == test_data:
            print("[OK] JSON file operations working")
            os.remove("test_file.json")
            return True
        else:
            print("[ERROR] JSON file operations failed")
            return False
            
    except Exception as e:
        print(f"[ERROR] File operations test failed: {e}")
        return False

def test_imports():
    """Test all required imports"""
    print("\n[IMPORTS] Testing Imports...")
    
    required_modules = [
        'selenium', 'requests', 'psutil', 'json', 'time', 
        'os', 'sys', 'random', 'hashlib', 'socket', 're'
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"[OK] {module} imported successfully")
        except ImportError as e:
            print(f"[ERROR] Failed to import {module}: {e}")
            return False
    
    return True

def test_webdriver_setup():
    """Test WebDriver setup and basic functionality"""
    print("\n[WEBDRIVER] Testing WebDriver Setup...")
    
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Test navigation
        driver.get("https://httpbin.org")
        title = driver.title
        
        if title:
            print(f"[OK] WebDriver working - Page title: {title}")
            driver.quit()
            return True
        else:
            print("[ERROR] WebDriver failed - No page title")
            driver.quit()
            return False
            
    except Exception as e:
        print(f"[ERROR] WebDriver test failed: {e}")
        return False

def main():
    """Run all feature tests"""
    print("REFRESHO v5.0 - FEATURE TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Directory Creation", test_directory_creation),
        ("File Operations", test_file_operations),
        ("WebDriver Setup", test_webdriver_setup),
        ("Screenshot Functionality", test_screenshot_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n[TEST] Running {test_name} test...")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("[SUCCESS] ALL TESTS PASSED - REFRESHO is ready!")
    else:
        print("[WARNING] SOME TESTS FAILED - Check issues above")
    
    return passed == len(tests)

if __name__ == "__main__":
    main()