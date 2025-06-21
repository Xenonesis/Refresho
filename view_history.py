#!/usr/bin/env python3
"""
REFRESHO v3.0 - History Viewer
View saved site analysis reports
"""
import os
import json
import sys
from datetime import datetime

def list_reports():
    """List all available analysis reports"""
    if not os.path.exists('history'):
        print("[INFO] No history directory found")
        return []
    
    reports = []
    for file in os.listdir('history'):
        if file.endswith('.json'):
            reports.append(file)
    
    return sorted(reports, reverse=True)

def display_report(filename):
    """Display a specific report"""
    try:
        with open(f'history/{filename}', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"\n{'='*60}")
        print(f"SITE ANALYSIS REPORT: {filename}")
        print(f"{'='*60}")
        
        print(f"URL: {data['url']}")
        print(f"Domain: {data['domain']}")
        print(f"Title: {data['title']}")
        print(f"Timestamp: {data['timestamp']}")
        print(f"Load Time: {data['load_time']}s")
        print(f"Page Size: {data['page_size']:,} bytes")
        print(f"Security: {'HTTPS' if data['security']['https'] else 'HTTP'}")
        
        print(f"\nContent Analysis:")
        print(f"  Links: {data['links']['total']}")
        print(f"  Images: {data['images']}")
        print(f"  Forms: {data['forms']}")
        print(f"  Scripts: {data['scripts']}")
        print(f"  Stylesheets: {data['stylesheets']}")
        print(f"  Cookies: {len(data['cookies'])}")
        
        if data['technologies']:
            print(f"\nTechnologies Detected:")
            for tech in data['technologies']:
                print(f"  • {tech}")
        
        if data['description']:
            print(f"\nDescription: {data['description']}")
        
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"[ERROR] Failed to read report: {e}")

def main():
    print("REFRESHO v3.0 - Site Analysis History Viewer")
    print("=" * 50)
    
    reports = list_reports()
    
    if not reports:
        print("[INFO] No analysis reports found")
        print("[TIP] Run refresh_bot.py with site analysis enabled to generate reports")
        return
    
    print(f"[INFO] Found {len(reports)} analysis reports:")
    print()
    
    for i, report in enumerate(reports, 1):
        # Extract info from filename
        parts = report.replace('.json', '').split('_')
        domain = '_'.join(parts[:-2]).replace('_', '.')
        date_part = parts[-2]
        time_part = parts[-1]
        
        # Format timestamp
        try:
            dt = datetime.strptime(f"{date_part}_{time_part}", "%Y%m%d_%H%M%S")
            formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            formatted_time = "Unknown"
        
        print(f"[{i:2d}] {domain:<30} | {formatted_time}")
    
    print()
    
    while True:
        try:
            choice = input("Enter report number to view (or 'q' to quit): ").strip()
            
            if choice.lower() == 'q':
                break
            
            index = int(choice) - 1
            if 0 <= index < len(reports):
                display_report(reports[index])
                input("\nPress ENTER to continue...")
            else:
                print("[ERROR] Invalid report number")
                
        except ValueError:
            print("[ERROR] Please enter a valid number or 'q'")
        except KeyboardInterrupt:
            print("\n[EXIT] Goodbye!")
            break

if __name__ == "__main__":
    main()