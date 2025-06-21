#!/usr/bin/env python3
"""
Demo of the new URL selection system
"""
import sys
sys.path.append('.')
from refresh_bot import URLManager

def demo_url_selection():
    print("REFRESHO v3.0 - URL Selection Demo")
    print("=" * 50)
    
    # Show current saved URLs
    saved_urls = URLManager.load_saved_urls()
    
    print("[TARGET] Enter target URL or select preset:")
    print("[1] Default: https://github.com/Xenonesis")
    
    option_num = 2
    for i, url_data in enumerate(saved_urls):
        print(f"[{option_num}] {url_data['name']}: {url_data['url']}")
        option_num += 1
    
    print(f"[{option_num}] Custom URL")
    print(f"[{option_num + 1}] Manage saved URLs")
    
    print("\n" + "=" * 50)
    print("Features:")
    print("✓ Google preset removed")
    print("✓ Dynamic saved URLs displayed")
    print("✓ Add/remove URLs on the fly")
    print("✓ URLs persist between sessions")
    print("✓ Custom naming for easy identification")

if __name__ == "__main__":
    demo_url_selection()