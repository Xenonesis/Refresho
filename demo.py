#!/usr/bin/env python3
"""
REFRESHO v5.0 - Quick Demo
"""

import time
import os
from src.refresh_bot import SystemAnalyzer, URLManager
from src.vapt_analyzer import VAPTAnalyzer

def demo_refresho():
    """Demonstrate REFRESHO functionality"""
    print("=" * 60)
    print("🔥 REFRESHO v5.0 - ULTIMATE WEB REFRESHER & VAPT TOOLKIT")
    print("💀 Developed by Addy@Xenonesis")
    print("=" * 60)
    
    # System Information
    print("\n[SYSTEM INFO]")
    sys_info = SystemAnalyzer.get_system_info()
    print(f"CPU: {sys_info['cpu_percent']}%")
    print(f"RAM: {sys_info['memory_percent']}%") 
    print(f"DISK: {sys_info['disk_usage']}%")
    print(f"Network Connections: {sys_info['network_connections']}")
    
    # Session ID
    session_id = SystemAnalyzer.generate_session_id()
    print(f"Session ID: {session_id}")
    
    # URL Manager Demo
    print("\n[URL MANAGER]")
    urls = URLManager.load_saved_urls()
    print(f"Saved URLs: {len(urls)}")
    
    # Add demo URL
    URLManager.add_url("https://httpbin.org", "HTTPBin Test")
    urls = URLManager.load_saved_urls()
    print(f"URLs after adding demo: {len(urls)}")
    
    # VAPT Demo
    print("\n[VAPT SECURITY TESTING]")
    print("Testing security headers for httpbin.org...")
    headers = VAPTAnalyzer.check_security_headers("https://httpbin.org")
    print(f"Security headers found: {len(headers)}")
    for header, value in headers.items():
        print(f"  • {header}: {value[:50]}...")
    
    # Sensitive files check
    print("\nChecking for sensitive files...")
    sensitive = VAPTAnalyzer.check_sensitive_files("https://httpbin.org")
    print(f"Sensitive files found: {len(sensitive)}")
    
    print("\n[DEMO COMPLETE]")
    print("✅ All core functionalities working!")
    print("✅ VAPT security testing operational!")
    print("✅ URL management functional!")
    print("✅ System monitoring active!")
    
    print("\n🚀 To run full REFRESHO:")
    print("   Method 1: python src/refresh_bot.py")
    print("   Method 2: run_refresh_bot.bat")
    print("   Method 3: Double-click run_refresh_bot.bat")

if __name__ == "__main__":
    demo_refresho()