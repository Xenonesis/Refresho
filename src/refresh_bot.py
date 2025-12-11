import time
import os
import sys
import random
import string
import threading
import json
import hashlib
import socket
import psutil
import re
from urllib.parse import urlparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
import requests
from webdriver_manager.chrome import ChromeDriverManager

# Fix Windows encoding issues
if os.name == 'nt':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8')

class HackerEffects:
    @staticmethod
    def matrix_rain(duration=2):
        """Display matrix rain effect"""
        try:
            chars = "01" + string.ascii_letters + "!@#$%^&*()_+-=[]{}|;:,.<>?"
            try:
                width = os.get_terminal_size().columns
            except:
                width = 80
            for _ in range(duration * 15):
                line = ''.join(random.choice(chars) for _ in range(width))
                print(f"\033[92m{line}\033[0m")
                time.sleep(0.05)
        except Exception as e:
            # Silently skip if terminal doesn't support it
            pass
    
    @staticmethod
    def glitch_text(text, intensity=3):
        glitch_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        result = ""
        for char in text:
            if random.randint(1, 10) <= intensity:
                result += random.choice(glitch_chars)
            else:
                result += char
        return result
    
    @staticmethod
    def typing_effect(text, delay=0.03):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

class SystemAnalyzer:
    @staticmethod
    def get_system_info():
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:\\').percent,
            'network_connections': len(psutil.net_connections()),
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        }
    
    @staticmethod
    def generate_session_id():
        return hashlib.md5(f"{time.time()}{random.randint(1000,9999)}".encode()).hexdigest()[:8].upper()

class URLManager:
    @staticmethod
    def load_saved_urls():
        """Load saved URLs from file"""
        try:
            if not os.path.exists('saved_urls'):
                os.makedirs('saved_urls')
            if os.path.exists('saved_urls/saved_urls.json'):
                with open('saved_urls/saved_urls.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    @staticmethod
    def save_urls(urls):
        """Save URLs to file"""
        try:
            if not os.path.exists('saved_urls'):
                os.makedirs('saved_urls')
            with open('saved_urls/saved_urls.json', 'w', encoding='utf-8') as f:
                json.dump(urls, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"\033[91m[ERROR] Failed to save URLs: {e}\033[0m")
    
    @staticmethod
    def add_url(url, name=None):
        """Add URL to saved list"""
        urls = URLManager.load_saved_urls()
        if not name:
            name = urlparse(url).netloc or url
        urls.append({'name': name, 'url': url})
        URLManager.save_urls(urls)
        return len(urls)
    
    @staticmethod
    def remove_url(index):
        """Remove URL by index"""
        urls = URLManager.load_saved_urls()
        if 0 <= index < len(urls):
            removed = urls.pop(index)
            URLManager.save_urls(urls)
            return removed
        return None

class SiteAnalyzer:
    @staticmethod
    def analyze_site(driver, url):
        """Comprehensive site analysis"""
        analysis = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'url': url,
            'domain': urlparse(url).netloc,
            'title': '',
            'description': '',
            'keywords': '',
            'status_code': 200,
            'page_size': 0,
            'load_time': 0,
            'technologies': [],
            'links': {'internal': 0, 'external': 0},
            'images': 0,
            'forms': 0,
            'scripts': 0,
            'stylesheets': 0,
            'headers': {},
            'cookies': [],
            'security': {},
            'performance': {}
        }
        
        try:
            start_time = time.time()
            
            # Basic page info
            analysis['title'] = driver.title or 'No Title'
            analysis['current_url'] = driver.current_url
            
            # Meta tags
            try:
                desc_elem = driver.find_element(By.XPATH, "//meta[@name='description']")
                analysis['description'] = desc_elem.get_attribute('content') or 'No Description'
            except: pass
            
            try:
                keywords_elem = driver.find_element(By.XPATH, "//meta[@name='keywords']")
                analysis['keywords'] = keywords_elem.get_attribute('content') or 'No Keywords'
            except: pass
            
            # Page elements count
            analysis['links']['total'] = len(driver.find_elements(By.TAG_NAME, 'a'))
            analysis['images'] = len(driver.find_elements(By.TAG_NAME, 'img'))
            analysis['forms'] = len(driver.find_elements(By.TAG_NAME, 'form'))
            analysis['scripts'] = len(driver.find_elements(By.TAG_NAME, 'script'))
            analysis['stylesheets'] = len(driver.find_elements(By.XPATH, "//link[@rel='stylesheet']"))
            
            # Technology detection
            page_source = driver.page_source.lower()
            techs = []
            if 'jquery' in page_source: techs.append('jQuery')
            if 'react' in page_source: techs.append('React')
            if 'angular' in page_source: techs.append('Angular')
            if 'vue' in page_source: techs.append('Vue.js')
            if 'bootstrap' in page_source: techs.append('Bootstrap')
            if 'wordpress' in page_source: techs.append('WordPress')
            analysis['technologies'] = techs
            
            # Performance metrics
            analysis['load_time'] = round(time.time() - start_time, 2)
            analysis['page_size'] = len(driver.page_source)
            
            # Security headers check
            try:
                logs = driver.get_log('performance')
                for log in logs:
                    if 'Network.responseReceived' in str(log):
                        headers = log.get('message', {}).get('params', {}).get('response', {}).get('headers', {})
                        analysis['headers'].update(headers)
                        break
            except: pass
            
            # Cookies
            try:
                cookies = driver.get_cookies()
                analysis['cookies'] = [{'name': c['name'], 'domain': c['domain'], 'secure': c.get('secure', False)} for c in cookies]
            except: pass
            
            # Security analysis
            analysis['security']['https'] = url.startswith('https')
            analysis['security']['has_forms'] = analysis['forms'] > 0
            analysis['security']['cookie_count'] = len(analysis['cookies'])
            
        except Exception as e:
            analysis['error'] = str(e)
        
        return analysis
    
    @staticmethod
    def display_analysis(analysis):
        """Display site analysis in terminal"""
        print(f"\n\033[96m+==============================================================+\033[0m")
        print(f"\033[96m|                    SITE INTELLIGENCE REPORT                 |\033[0m")
        print(f"\033[96m+==============================================================+\033[0m")
        
        print(f"\033[93m[TARGET] {analysis['url']}\033[0m")
        print(f"\033[92m[TITLE] {analysis['title'][:50]}{'...' if len(analysis['title']) > 50 else ''}\033[0m")
        print(f"\033[95m[DOMAIN] {analysis['domain']}\033[0m")
        print(f"\033[94m[TIMESTAMP] {analysis['timestamp']}\033[0m")
        
        print(f"\n\033[96m[PERFORMANCE METRICS]\033[0m")
        print(f"\033[92m  Load Time: {analysis['load_time']}s\033[0m")
        print(f"\033[92m  Page Size: {analysis['page_size']:,} bytes\033[0m")
        print(f"\033[92m  Security: {'HTTPS' if analysis['security']['https'] else 'HTTP'}\033[0m")
        
        print(f"\n\033[96m[CONTENT ANALYSIS]\033[0m")
        print(f"\033[92m  Links: {analysis['links']['total']}\033[0m")
        print(f"\033[92m  Images: {analysis['images']}\033[0m")
        print(f"\033[92m  Forms: {analysis['forms']}\033[0m")
        print(f"\033[92m  Scripts: {analysis['scripts']}\033[0m")
        print(f"\033[92m  Stylesheets: {analysis['stylesheets']}\033[0m")
        print(f"\033[92m  Cookies: {len(analysis['cookies'])}\033[0m")
        
        if analysis['technologies']:
            print(f"\n\033[96m[TECHNOLOGIES DETECTED]\033[0m")
            for tech in analysis['technologies']:
                print(f"\033[92m  • {tech}\033[0m")
        
        if analysis['description'] and analysis['description'] != 'No Description':
            print(f"\n\033[96m[DESCRIPTION]\033[0m")
            print(f"\033[92m  {analysis['description'][:100]}{'...' if len(analysis['description']) > 100 else ''}\033[0m")
    
    @staticmethod
    def save_analysis(analysis):
        """Save analysis to history folder"""
        try:
            # Create history directory if it doesn't exist
            if not os.path.exists('history'):
                os.makedirs('history')
            
            # Generate filename from domain and timestamp
            domain = analysis['domain'].replace('.', '_').replace(':', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"history/{domain}_{timestamp}.json"
            
            # Save detailed JSON report
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            print(f"\033[95m[INTEL] Analysis saved to: {filename}\033[0m")
            return filename
        except Exception as e:
            print(f"\033[91m[ERROR] Failed to save analysis: {e}\033[0m")
            return None

# Import the rest of the classes from separate files
try:
    from .vapt_analyzer import VAPTAnalyzer
    from .ui_components import clear_screen, print_banner, loading_animation
    from .config_manager import get_advanced_config, manage_urls
    from .browser_controller import create_chrome_driver
    from .mission_controller import refresho_beast, success_animation
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from vapt_analyzer import VAPTAnalyzer
    from ui_components import clear_screen, print_banner, loading_animation
    from config_manager import get_advanced_config, manage_urls
    from browser_controller import create_chrome_driver
    from mission_controller import refresho_beast, success_animation

def main():
    """Main application entry point"""
    try:
        clear_screen()
        print_banner()
        
        HackerEffects.typing_effect("\033[96m[SYSTEM] Welcome to REFRESHO v5.0 - Advanced Web Refresher\033[0m")
        
        while True:
            config = get_advanced_config()
            
            print(f"\n\033[96m[CONFIRM] Ready to execute mission with following parameters:\033[0m")
            print(f"\033[93m  Target: {config['url']}\033[0m")
            print(f"\033[93m  Mode: {config['mode']}\033[0m")
            print(f"\033[93m  Count: {config['refresh_count']:,}\033[0m")
            print(f"\033[93m  VAPT: {'Enabled' if config.get('vapt_enabled') else 'Disabled'}\033[0m")
            
            confirm = input(f"\n\033[92m[>] Execute mission? (Y/n): \033[0m").lower()
            if confirm != 'n':
                success = refresho_beast(config)
                if success:
                    print(f"\n\033[92m[SUCCESS] Mission completed successfully!\033[0m")
                else:
                    print(f"\n\033[91m[FAILED] Mission failed or aborted\033[0m")
            
            repeat = input(f"\n\033[92m[>] Start another mission? (y/N): \033[0m").lower()
            if repeat != 'y':
                break
        
        HackerEffects.typing_effect("\033[96m[SHUTDOWN] REFRESHO v5.0 terminating. Thank you for using our services.\033[0m")
        
    except KeyboardInterrupt:
        print(f"\n\033[93m[EXIT] REFRESHO v5.0 terminated by user\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\n\033[91m[CRITICAL ERROR] {e}\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    main()