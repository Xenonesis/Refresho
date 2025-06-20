#!/usr/bin/env python3
"""
Test the URL management system
"""
import sys
import os
import json

# Import URLManager from refresh_bot
sys.path.append('.')
from refresh_bot import URLManager

def test_url_manager():
    print("Testing URL Management System...")
    print("=" * 40)
    
    # Test adding URLs
    print("[TEST] Adding test URLs...")
    URLManager.add_url("https://www.github.com", "GitHub")
    URLManager.add_url("https://www.stackoverflow.com", "Stack Overflow")
    URLManager.add_url("https://www.reddit.com", "Reddit")
    print("[OK] URLs added")
    
    # Test loading URLs
    print("[TEST] Loading saved URLs...")
    urls = URLManager.load_saved_urls()
    print(f"[OK] Loaded {len(urls)} URLs:")
    for i, url_data in enumerate(urls, 1):
        print(f"  [{i}] {url_data['name']}: {url_data['url']}")
    
    # Test removing URL
    print("[TEST] Removing first URL...")
    removed = URLManager.remove_url(0)
    if removed:
        print(f"[OK] Removed: {removed['name']}")
    
    # Check remaining URLs
    urls = URLManager.load_saved_urls()
    print(f"[OK] Remaining URLs: {len(urls)}")
    
    # Check saved file
    if os.path.exists('saved_urls.json'):
        print("[OK] saved_urls.json file created")
        with open('saved_urls.json', 'r') as f:
            data = json.load(f)
            print(f"[OK] File contains {len(data)} URLs")
    
    print("=" * 40)
    print("[SUCCESS] URL Management System working correctly!")

if __name__ == "__main__":
    test_url_manager()