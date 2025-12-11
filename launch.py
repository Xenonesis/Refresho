#!/usr/bin/env python3
"""
REFRESHO v5.0 - Simple Launcher
"""

import os
import sys

def main():
    print("🔥 REFRESHO v5.0 - LAUNCHER")
    print("=" * 40)
    print("1. Run Demo (Safe)")
    print("2. Run Full REFRESHO")
    print("3. Run Tests")
    print("4. Exit")
    print("=" * 40)
    
    choice = input("Select option (1-4): ").strip()
    
    if choice == '1':
        print("\n🚀 Running Demo...")
        os.system("python demo.py")
    elif choice == '2':
        print("\n🚀 Launching REFRESHO v5.0...")
        print("Note: Use Ctrl+C to exit if needed")
        os.system("python src/refresh_bot.py")
    elif choice == '3':
        print("\n🧪 Running Tests...")
        os.system("python tests/test_features.py")
    elif choice == '4':
        print("👋 Goodbye!")
        sys.exit(0)
    else:
        print("❌ Invalid option!")
        main()

if __name__ == "__main__":
    main()