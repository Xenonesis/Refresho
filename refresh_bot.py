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

# Fix Windows encoding issues
if os.name == 'nt':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8')

class HackerEffects:
    @staticmethod
    def matrix_rain(duration=2):
        chars = "01" + string.ascii_letters + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        width = os.get_terminal_size().columns if hasattr(os, 'get_terminal_size') else 80
        for _ in range(duration * 15):
            line = ''.join(random.choice(chars) for _ in range(width))
            print(f"\033[92m{line}\033[0m")
            time.sleep(0.05)
    
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
            if os.path.exists('saved_urls.json'):
                with open('saved_urls.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    @staticmethod
    def save_urls(urls):
        """Save URLs to file"""
        try:
            with open('saved_urls.json', 'w', encoding='utf-8') as f:
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

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """
\033[92m
██████╗ ███████╗███████╗██████╗ ███████╗███████╗██╗  ██╗ ██████╗ 
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██║  ██║██╔═══██╗
██████╔╝█████╗  █████╗  ██████╔╝█████╗  ███████╗███████║██║   ██║
██╔══██╗██╔══╝  ██╔══╝  ██╔══██╗██╔══╝  ╚════██║██╔══██║██║   ██║
██║  ██║███████╗██║     ██║  ██║███████╗███████║██║  ██║╚██████╔╝
╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ 
\033[0m
\033[96m+==============================================================+\033[0m
\033[96m|              ADVANCED WEB REFRESHER TOOL v2.0              |\033[0m
\033[96m|                 Developed by Addy@Xenonesis                |\033[0m
\033[96m+==============================================================+\033[0m
"""
    print(banner)
    
    # System info display
    sys_info = SystemAnalyzer.get_system_info()
    session_id = SystemAnalyzer.generate_session_id()
    
    print(f"\033[93m[SYSTEM] CPU: {sys_info['cpu_percent']}% | RAM: {sys_info['memory_percent']}% | DISK: {sys_info['disk_usage']}%\033[0m")
    print(f"\033[95m[SESSION] ID: {session_id} | CONNECTIONS: {sys_info['network_connections']} | BOOT: {sys_info['boot_time']}\033[0m")
    print(f"\033[91m[STATUS] INITIALIZING HACKER MODE...\033[0m")
    
    # Matrix effect
    HackerEffects.matrix_rain(1)

def loading_animation():
    phases = [
        "SCANNING NETWORK INTERFACES",
        "BYPASSING SECURITY PROTOCOLS", 
        "INJECTING PAYLOAD MODULES",
        "ESTABLISHING SECURE TUNNEL",
        "ACTIVATING STEALTH MODE",
        "LOADING EXPLOIT FRAMEWORK"
    ]
    
    for phase in phases:
        for i in range(10):
            chars = "/-\\|"
            sys.stdout.write(f"\r\033[92m[{chars[i % 4]}] {phase}{'.' * (i % 4)}\033[0m")
            sys.stdout.flush()
            time.sleep(0.1)
        print(f"\r\033[92m[✓] {phase} COMPLETE\033[0m" + " " * 20)
    
    print("\033[92m[>>>] ALL SYSTEMS OPERATIONAL [<<<]\033[0m")

def get_advanced_config():
    config = {}
    
    print("\n\033[96m+==============================================================+\033[0m")
    print("\033[96m|                    MISSION CONFIGURATION                     |\033[0m")
    print("\033[96m+==============================================================+\033[0m")
    
    # URL Configuration
    HackerEffects.typing_effect("\033[96m[TARGET] Enter target URL or select preset:\033[0m")
    print("\033[93m[1] Default: https://github.com/Xenonesis\033[0m")
    
    # Load and display saved URLs
    saved_urls = URLManager.load_saved_urls()
    option_num = 2
    for i, url_data in enumerate(saved_urls):
        print(f"\033[93m[{option_num}] {url_data['name']}: {url_data['url']}\033[0m")
        option_num += 1
    
    print(f"\033[93m[{option_num}] Custom URL\033[0m")
    print(f"\033[93m[{option_num + 1}] Manage saved URLs\033[0m")
    
    max_option = option_num + 1
    
    while True:
        choice = input(f"\033[92m[>] Select option (1-{max_option}): \033[0m").strip()
        
        if choice == '1' or choice == '':
            config['url'] = "https://github.com/Xenonesis"
            break
        elif choice.isdigit():
            choice_num = int(choice)
            if 2 <= choice_num <= len(saved_urls) + 1:
                # Saved URL selected
                url_index = choice_num - 2
                config['url'] = saved_urls[url_index]['url']
                break
            elif choice_num == option_num:
                # Custom URL
                url = input("\033[92m[>] Enter custom URL: \033[0m").strip()
                if url:
                    config['url'] = url
                    # Ask to save
                    save_choice = input("\033[92m[>] Save this URL for future use? (y/N): \033[0m").lower()
                    if save_choice == 'y':
                        name = input("\033[92m[>] Enter name for this URL: \033[0m").strip()
                        URLManager.add_url(url, name)
                        print("\033[92m[✓] URL saved successfully\033[0m")
                else:
                    config['url'] = "https://github.com/Xenonesis"
                break
            elif choice_num == max_option:
                # Manage URLs
                manage_urls()
                return get_advanced_config()  # Restart configuration
        
        print(f"\033[91m[!] Invalid option. Please select 1-{max_option}.\033[0m")
    
    print(f"\033[92m[✓] TARGET LOCKED: {config['url']}\033[0m")
    
    # Attack Mode Selection
    print("\n\033[96m[ATTACK] Select refresh mode:\033[0m")
    print("\033[93m[1] Stealth Mode (1-1000 refreshes)\033[0m")
    print("\033[93m[2] Assault Mode (1001-10000 refreshes)\033[0m")
    print("\033[93m[3] Nuclear Mode (10001-9999999 refreshes)\033[0m")
    
    while True:
        mode = input("\033[92m[>] Select mode (1-3): \033[0m").strip()
        if mode in ['1', '2', '3']:
            if mode == '1':
                max_count = 1000
                config['mode'] = "STEALTH"
            elif mode == '2':
                max_count = 10000
                config['mode'] = "ASSAULT"
            else:
                max_count = 9999999
                config['mode'] = "NUCLEAR"
            break
        else:
            print("\033[91m[!] Invalid mode. Please select 1-3.\033[0m")
    
    # Refresh count
    while True:
        try:
            count = input(f"\033[92m[>] Refresh count (1-{max_count:,}): \033[0m").strip()
            if not count:
                print("\033[91m[!] Please enter a valid number\033[0m")
                continue
            
            refresh_count = int(count)
            if refresh_count <= 0 or refresh_count > max_count:
                print(f"\033[91m[!] Count must be between 1 and {max_count:,}\033[0m")
                continue
            
            config['refresh_count'] = refresh_count
            break
        except ValueError:
            print("\033[91m[!] Please enter a valid number\033[0m")
    
    # Intelligent delay calculation
    if config['mode'] == "STEALTH":
        config['delay'] = max(1.0, 5.0 / refresh_count)
    elif config['mode'] == "ASSAULT":
        config['delay'] = max(0.5, 2.0 / refresh_count)
    else:
        config['delay'] = max(0.1, 1.0 / refresh_count)
    
    # Browser configuration
    print(f"\n\033[96m[BROWSER] Select browser configuration:\033[0m")
    print("\033[93m[1] Ghost Mode (Headless + Stealth)\033[0m")
    print("\033[93m[2] Phantom Mode (Headless + Fast)\033[0m")
    print("\033[93m[3] Visible Mode (GUI + Debug)\033[0m")
    
    while True:
        browser_mode = input("\033[92m[>] Select mode (1-3): \033[0m").strip()
        if browser_mode == '1':
            config['headless'] = True
            config['stealth'] = True
            break
        elif browser_mode == '2':
            config['headless'] = True
            config['stealth'] = False
            break
        elif browser_mode == '3':
            config['headless'] = False
            config['stealth'] = False
            break
        else:
            print("\033[91m[!] Invalid mode. Please select 1-3.\033[0m")
    
    # Advanced features
    print(f"\n\033[96m[ADVANCED] Enable advanced features?\033[0m")
    config['proxy_rotation'] = input("\033[92m[>] Enable proxy rotation? (y/N): \033[0m").lower() == 'y'
    config['user_agent_rotation'] = input("\033[92m[>] Enable user agent rotation? (y/N): \033[0m").lower() == 'y'
    config['screenshot_capture'] = input("\033[92m[>] Capture screenshots? (y/N): \033[0m").lower() == 'y'
    config['site_analysis'] = input("\033[92m[>] Enable site intelligence analysis? (Y/n): \033[0m").lower() != 'n'
    
    return config

def manage_urls():
    """URL management interface"""
    while True:
        clear_screen()
        print("\033[96m+==============================================================+\033[0m")
        print("\033[96m|                    URL MANAGEMENT SYSTEM                     |\033[0m")
        print("\033[96m+==============================================================+\033[0m")
        
        saved_urls = URLManager.load_saved_urls()
        
        if saved_urls:
            print("\033[93m[SAVED URLS]\033[0m")
            for i, url_data in enumerate(saved_urls):
                print(f"\033[92m[{i + 1}] {url_data['name']}: {url_data['url']}\033[0m")
        else:
            print("\033[93m[INFO] No saved URLs found\033[0m")
        
        print("\n\033[96m[OPTIONS]\033[0m")
        print("\033[93m[A] Add new URL\033[0m")
        if saved_urls:
            print("\033[93m[D] Delete URL\033[0m")
        print("\033[93m[B] Back to main menu\033[0m")
        
        choice = input("\033[92m[>] Select option: \033[0m").strip().lower()
        
        if choice == 'a':
            url = input("\033[92m[>] Enter URL: \033[0m").strip()
            if url:
                name = input("\033[92m[>] Enter name: \033[0m").strip()
                URLManager.add_url(url, name)
                print("\033[92m[✓] URL added successfully\033[0m")
                input("\033[96m[>] Press ENTER to continue...\033[0m")
        
        elif choice == 'd' and saved_urls:
            try:
                index = int(input("\033[92m[>] Enter URL number to delete: \033[0m")) - 1
                removed = URLManager.remove_url(index)
                if removed:
                    print(f"\033[92m[✓] Deleted: {removed['name']}\033[0m")
                else:
                    print("\033[91m[!] Invalid URL number\033[0m")
                input("\033[96m[>] Press ENTER to continue...\033[0m")
            except ValueError:
                print("\033[91m[!] Please enter a valid number\033[0m")
                input("\033[96m[>] Press ENTER to continue...\033[0m")
        
        elif choice == 'b':
            break
        
        else:
            print("\033[91m[!] Invalid option\033[0m")
            input("\033[96m[>] Press ENTER to continue...\033[0m")

def success_animation(execution_time, refresh_count, config):
    clear_screen()
    
    # Epic success banner
    success_banner = """
\033[92m
███████╗██╗   ██╗ ██████╗ ██████╗███████╗███████╗███████╗
██╔════╝██║   ██║██╔════╝██╔════╝██╔════╝██╔════╝██╔════╝
███████╗██║   ██║██║     ██║     █████╗  ███████╗███████╗
╚════██║██║   ██║██║     ██║     ██╔══╝  ╚════██║╚════██║
███████║╚██████╔╝╚██████╗╚██████╗███████╗███████║███████║
╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝╚══════╝╚══════╝╚══════╝
\033[0m"""
    
    print(success_banner)
    
    # Mission stats
    stats = f"""
\033[96m+==============================================================+\033[0m
\033[96m|                      MISSION COMPLETE                        |\033[0m
\033[96m+==============================================================+\033[0m
\033[96m| Target: {config['url']:<49} |\033[0m
\033[96m| Mode: {config['mode']:<51} |\033[0m
\033[96m| Refreshes: {refresh_count:<44,} |\033[0m
\033[96m| Execution Time: {execution_time:.2f}s{'':<37} |\033[0m
\033[96m| Average Speed: {execution_time/refresh_count:.3f}s per refresh{'':<25} |\033[0m
\033[96m| Performance: {(refresh_count/execution_time):.1f} refreshes/second{'':<26} |\033[0m
\033[96m+==============================================================+\033[0m
"""
    
    print(stats)
    
    # Animated completion
    for i in range(5):
        print(f"\033[92m[>>>] MISSION STATUS: {'COMPLETED' if i % 2 == 0 else 'SUCCESS'} [<<<]\033[0m")
        time.sleep(0.5)
        if i < 4:
            print("\033[2A\033[K", end="")
    
    print(f"\033[91m[SIGNATURE] Operation executed by Addy@Xenonesis\033[0m")
    
    # Matrix celebration
    HackerEffects.matrix_rain(1)

def refresho_beast(config):
    clear_screen()
    print_banner()
    loading_animation()
    
    start_time = time.time()
    
    # Advanced Chrome configuration
    chrome_options = Options()
    
    if config['headless']:
        chrome_options.add_argument("--headless")
    
    # Stealth configuration
    if config.get('stealth', False):
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Performance optimization
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    
    # User agent rotation
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    
    if config.get('user_agent_rotation', False):
        chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
    else:
        chrome_options.add_argument(f"--user-agent={user_agents[0]}")
    
    # ChromeDriver service with automatic management
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
    except ImportError:
        # Fallback to system ChromeDriver
        service = Service()
    
    mode_text = f"{config['mode']} MODE"
    print(f"\n\033[96m[INITIALIZING] {mode_text} BROWSER ENGINE...\033[0m")
    
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print(f"\033[92m[✓] {mode_text} ENGINE ONLINE\033[0m")
        
        # Execute JavaScript to remove webdriver property
        if config.get('stealth', False):
            try:
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            except Exception:
                pass  # Ignore stealth script errors
            
    except WebDriverException as e:
        print(f"\033[91m[✗] ENGINE INITIALIZATION FAILED\033[0m")
        print(f"\033[91m[ERROR] {str(e)}\033[0m")
        print(f"\033[93m[SOLUTION] Try installing/updating Chrome and ChromeDriver:\033[0m")
        print(f"\033[93m  pip install --upgrade webdriver-manager\033[0m")
        return
    except Exception as e:
        print(f"\033[91m[✗] UNEXPECTED ERROR: {str(e)}\033[0m")
        return
    
    success_count = 0
    error_count = 0
    
    try:
        # Target acquisition
        print(f"\033[93m[TARGETING] Acquiring target: {config['url']}\033[0m")
        driver.get(config['url'])
        print(f"\033[92m[✓] TARGET ACQUIRED AND LOCKED\033[0m")
        
        # Site intelligence analysis
        if config.get('site_analysis', True):
            print(f"\033[96m[ANALYZING] Conducting site intelligence scan...\033[0m")
            analysis = SiteAnalyzer.analyze_site(driver, config['url'])
            SiteAnalyzer.display_analysis(analysis)
            SiteAnalyzer.save_analysis(analysis)
        
        # Screenshot if enabled
        if config.get('screenshot_capture', False):
            timestamp = int(time.time())
            screenshot_file = f"target_screenshot_{timestamp}.png"
            driver.save_screenshot(screenshot_file)
            print(f"\033[95m[INTEL] Screenshot captured: {screenshot_file}\033[0m")
        
        print(f"\n\033[96m[EXECUTING] {config['mode']} ATTACK WITH {config['refresh_count']:,} REFRESHES\033[0m")
        refresh_start = time.time()
        
        for i in range(config['refresh_count']):
            time.sleep(config['delay'])
            
            try:
                # User agent rotation during execution
                if config.get('user_agent_rotation', False) and i % 100 == 0:
                    try:
                        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                            "userAgent": random.choice(user_agents)
                        })
                    except Exception:
                        pass  # Ignore user agent rotation errors
                
                driver.refresh()
                success_count += 1
                
                # Dynamic progress display
                progress = "█" * (success_count * 30 // config['refresh_count'])
                remaining = "░" * (30 - len(progress))
                percentage = (success_count * 100) // config['refresh_count']
                elapsed = time.time() - refresh_start
                eta = (elapsed / success_count) * (config['refresh_count'] - success_count) if success_count > 0 else 0
                speed = success_count / elapsed if elapsed > 0 else 0
                
                status_line = f"\r\033[92m[{progress}{remaining}] {percentage}% | #{success_count:,}/{config['refresh_count']:,} | Speed: {speed:.1f}/s | ETA: {eta:.1f}s\033[0m"
                print(status_line, end="")
                sys.stdout.flush()
                
            except Exception as e:
                error_count += 1
                if error_count > 10:  # Stop if too many errors
                    print(f"\n\033[91m[ABORT] Too many errors encountered. Mission aborted.\033[0m")
                    break
                continue
        
        print(f"\n\033[92m[COMPLETE] Mission executed successfully\033[0m")
        
    except Exception as e:
        print(f"\n\033[91m[ERROR] Mission failed: {e}\033[0m")
    
    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        
        driver.quit()
        print(f"\033[93m[CLEANUP] Browser engine terminated\033[0m")
        
        if success_count == config['refresh_count']:
            success_animation(execution_time, success_count, config)
        else:
            print(f"\033[91m[PARTIAL] Mission partially completed: {success_count:,}/{config['refresh_count']:,} refreshes\033[0m")
            print(f"\033[93m[STATS] Execution time: {execution_time:.2f}s | Errors: {error_count}\033[0m")

def main():
    try:
        clear_screen()
        
        # Welcome sequence
        HackerEffects.typing_effect("\033[96m[SYSTEM] Initializing REFRESHO v2.0...\033[0m", 0.05)
        time.sleep(1)
        
        config = get_advanced_config()
        
        # Mission briefing
        print(f"\n\033[95m+==============================================================+\033[0m")
        print(f"\033[95m|                     MISSION BRIEFING                        |\033[0m")
        print(f"\033[95m+==============================================================+\033[0m")
        print(f"\033[95m| Target: {config['url']:<49} |\033[0m")
        print(f"\033[95m| Mode: {config['mode']:<51} |\033[0m")
        print(f"\033[95m| Refreshes: {config['refresh_count']:<44,} |\033[0m")
        print(f"\033[95m| Delay: {config['delay']:.3f}s{'':<46} |\033[0m")
        print(f"\033[95m| Browser: {'Headless' if config['headless'] else 'Visible':<47} |\033[0m")
        print(f"\033[95m| Site Analysis: {'Enabled' if config.get('site_analysis', True) else 'Disabled':<42} |\033[0m")
        print(f"\033[95m+==============================================================+\033[0m")
        
        input(f"\n\033[96m[STANDBY] Press ENTER to execute mission...\033[0m")
        
        refresho_beast(config)
        
    except KeyboardInterrupt:
        print(f"\n\033[91m[ABORT] Mission terminated by operator\033[0m")
        sys.exit(0)

if __name__ == "__main__":
    main()