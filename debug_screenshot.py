#!/usr/bin/env python3
"""
Debug screenshot functionality
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def test_screenshot_debug():
    """Debug screenshot functionality step by step"""
    print("🔍 DEBUGGING SCREENSHOT FUNCTIONALITY")
    print("=" * 50)
    
    # Step 1: Check directory
    print("Step 1: Checking screenshots directory...")
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
        print("✅ Created screenshots directory")
    else:
        print("✅ Screenshots directory exists")
    
    # Step 2: Test basic screenshot
    print("\nStep 2: Testing basic screenshot...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ WebDriver created successfully")
        
        # Navigate to a simple page
        driver.get("https://httpbin.org")
        print("✅ Navigated to httpbin.org")
        
        # Wait for page load
        time.sleep(2)
        
        # Test screenshot with absolute path
        screenshot_path = os.path.abspath("screenshots/debug_test.png")
        print(f"📸 Attempting screenshot: {screenshot_path}")
        
        success = driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot result: {success}")
        
        # Check if file exists
        if os.path.exists(screenshot_path):
            file_size = os.path.getsize(screenshot_path)
            print(f"✅ Screenshot saved successfully: {file_size} bytes")
        else:
            print("❌ Screenshot file not found!")
        
        # Test with different method
        print("\nStep 3: Testing with get_screenshot_as_file...")
        screenshot_path2 = os.path.abspath("screenshots/debug_test2.png")
        success2 = driver.get_screenshot_as_file(screenshot_path2)
        print(f"📸 get_screenshot_as_file result: {success2}")
        
        if os.path.exists(screenshot_path2):
            file_size2 = os.path.getsize(screenshot_path2)
            print(f"✅ Screenshot 2 saved successfully: {file_size2} bytes")
        else:
            print("❌ Screenshot 2 file not found!")
        
        # Test with PNG data
        print("\nStep 4: Testing with get_screenshot_as_png...")
        png_data = driver.get_screenshot_as_png()
        if png_data:
            screenshot_path3 = os.path.abspath("screenshots/debug_test3.png")
            with open(screenshot_path3, 'wb') as f:
                f.write(png_data)
            print(f"✅ PNG data screenshot saved: {len(png_data)} bytes")
        else:
            print("❌ No PNG data received!")
        
        driver.quit()
        
        # List all files in screenshots directory
        print("\nStep 5: Listing screenshots directory...")
        if os.path.exists('screenshots'):
            files = os.listdir('screenshots')
            print(f"Files in screenshots/: {files}")
            for f in files:
                if f.endswith('.png'):
                    full_path = os.path.join('screenshots', f)
                    size = os.path.getsize(full_path)
                    print(f"  📸 {f}: {size} bytes")
        
        print("\n🎉 Screenshot debug complete!")
        
    except Exception as e:
        print(f"❌ Error during screenshot test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_screenshot_debug()