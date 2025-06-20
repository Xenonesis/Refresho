#!/usr/bin/env python3
"""
Test the new site analysis feature
"""
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Import the SiteAnalyzer from refresh_bot
sys.path.append('.')
from refresh_bot import SiteAnalyzer

def test_site_analysis():
    print("Testing Site Analysis Feature...")
    print("=" * 50)
    
    # Setup Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("[OK] WebDriver initialized")
        
        # Test with Google
        test_url = "https://www.google.com"
        print(f"[TEST] Analyzing: {test_url}")
        
        driver.get(test_url)
        analysis = SiteAnalyzer.analyze_site(driver, test_url)
        
        # Display analysis
        SiteAnalyzer.display_analysis(analysis)
        
        # Save analysis
        filename = SiteAnalyzer.save_analysis(analysis)
        
        driver.quit()
        print("\n[SUCCESS] Site analysis test completed!")
        print(f"[INFO] Report saved to: {filename}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        return False

if __name__ == "__main__":
    test_site_analysis()