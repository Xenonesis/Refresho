#!/usr/bin/env python3
"""
REFRESHO v2.0 - URL Management Utility
Standalone tool to manage saved URLs
"""
import sys
sys.path.append('.')
from refresh_bot import URLManager

def main():
    print("REFRESHO v2.0 - URL Management Utility")
    print("=" * 50)
    
    while True:
        saved_urls = URLManager.load_saved_urls()
        
        print(f"\n[SAVED URLS] ({len(saved_urls)} total)")
        if saved_urls:
            for i, url_data in enumerate(saved_urls, 1):
                print(f"  [{i}] {url_data['name']}: {url_data['url']}")
        else:
            print("  No saved URLs found")
        
        print("\n[OPTIONS]")
        print("  [A] Add new URL")
        if saved_urls:
            print("  [D] Delete URL")
        print("  [Q] Quit")
        
        choice = input("\n[>] Select option: ").strip().lower()
        
        if choice == 'a':
            url = input("[>] Enter URL: ").strip()
            if url:
                name = input("[>] Enter name: ").strip()
                URLManager.add_url(url, name)
                print(f"[OK] Added: {name}")
            else:
                print("[ERROR] URL cannot be empty")
        
        elif choice == 'd' and saved_urls:
            try:
                index = int(input("[>] Enter URL number to delete: ")) - 1
                removed = URLManager.remove_url(index)
                if removed:
                    print(f"[OK] Deleted: {removed['name']}")
                else:
                    print("[ERROR] Invalid URL number")
            except ValueError:
                print("[ERROR] Please enter a valid number")
        
        elif choice == 'q':
            print("[EXIT] Goodbye!")
            break
        
        else:
            print("[ERROR] Invalid option")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[EXIT] Goodbye!")
        sys.exit(0)