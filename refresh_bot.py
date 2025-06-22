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

class VAPTAnalyzer:
    @staticmethod
    def check_security_headers(url):
        """Check for common security headers"""
        headers = {}
        try:
            response = requests.head(url, timeout=10) # Use HEAD request for efficiency
            headers = response.headers
        except requests.exceptions.RequestException as e:
            print(f"\033[91m[VAPT ERROR] Failed to get headers for {url}: {e}\033[0m")
            return {}

        security_headers = {
            'Strict-Transport-Security': headers.get('Strict-Transport-Security'),
            'Content-Security-Policy': headers.get('Content-Security-Policy'),
            'X-Content-Type-Options': headers.get('X-Content-Type-Options'),
            'X-Frame-Options': headers.get('X-Frame-Options'),
            'Referrer-Policy': headers.get('Referrer-Policy'),
            'Permissions-Policy': headers.get('Permissions-Policy'),
            'Cross-Origin-Embedder-Policy': headers.get('Cross-Origin-Embedder-Policy'),
            'Cross-Origin-Opener-Policy': headers.get('Cross-Origin-Opener-Policy'),
            'Cross-Origin-Resource-Policy': headers.get('Cross-Origin-Resource-Policy'),
            'Feature-Policy': headers.get('Feature-Policy') # Older name for Permissions-Policy
        }
        # Filter out None values
        return {k: v for k, v in security_headers.items() if v is not None}

    @staticmethod
    def check_sensitive_files(url):
        """Check for common sensitive files/directories"""
        sensitive_paths = [
            '/robots.txt',
            '/.env',
            '/.git/config',
            '/wp-config.php', # Common WordPress file
            '/admin/', # Common admin directory
            '/backup/', # Common backup directory
            '/temp/', # Common temp directory
            '/tmp/' # Common temp directory
        ]
        found_files = []
        base_url = urlparse(url).scheme + "://" + urlparse(url).netloc

        for path in sensitive_paths:
            target_url = base_url + path
            try:
                # Use a short timeout and check status code
                response = requests.get(target_url, timeout=5)
                # Consider 200 OK as potentially found, but also check for common "Not Found" content
                # This is a basic check, a real VAPT tool would be more sophisticated
                if response.status_code == 200:
                     # Simple check to avoid reporting generic 404 pages that return 200
                    if "not found" not in response.text.lower() and "page not found" not in response.text.lower():
                         found_files.append(target_url)
            except requests.exceptions.RequestException:
                # Ignore connection errors, timeouts, etc.
                pass
        return found_files

    @staticmethod
    def scan_ports(url, ports=[80, 443, 22, 21, 23, 25, 110, 143, 3306, 5432, 6379, 27017]):
        """Basic port scan for common ports"""
        open_ports = []
        domain = urlparse(url).netloc
        # Remove port if present in domain
        if ':' in domain:
            domain = domain.split(':')[0]

        # Avoid scanning IP addresses that might be internal
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain):
             print(f"\033[93m[VAPT INFO] Skipping port scan for IP address: {domain}\033[0m")
             return []

        print(f"\033[96m[VAPT] Starting basic port scan for {domain}...\033[0m")
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1) # Short timeout
            try:
                result = sock.connect_ex((domain, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"\033[92m[VAPT] Port {port} is OPEN\033[0m")
                # else:
                    # print(f"\033[93m[VAPT] Port {port} is closed or filtered ({result})\033[0m") # Too noisy
                sock.close()
            except socket.gaierror:
                print(f"\033[91m[VAPT ERROR] Hostname could not be resolved: {domain}\033[0m")
                return []
            except socket.error as e:
                 # print(f"\033[91m[VAPT ERROR] Socket error on port {port}: {e}\033[0m") # Too noisy
                 pass # Ignore other socket errors
            except Exception as e:
                 print(f"\033[91m[VAPT ERROR] Unexpected error during port scan on port {port}: {e}\033[0m")
                 pass # Catch any other exceptions
        print(f"\033[96m[VAPT] Basic port scan finished.\033[0m")
        return open_ports

    @staticmethod
    def perform_vapt_checks(url, driver):
        """Perform all VAPT checks"""
        vapt_results = {}
        print(f"\n\033[96m[VAPT] Starting VAPT analysis for {url}...\033[0m")

        # Security Headers
        print(f"\033[96m[VAPT] Checking security headers...\033[0m")
        vapt_results['security_headers'] = VAPTAnalyzer.check_security_headers(url)
        print(f"\033[92m[VAPT] Security headers check complete.\033[0m")

        # Sensitive Files
        print(f"\033[96m[VAPT] Checking for sensitive files...\033[0m")
        vapt_results['sensitive_files'] = VAPTAnalyzer.check_sensitive_files(url)
        print(f"\033[92m[VAPT] Sensitive files check complete.\033[0m")

        # Port Scan
        # Note: Port scan doesn't require the selenium driver, only the URL
        print(f"\033[96m[VAPT] Performing basic port scan...\033[0m")
        vapt_results['open_ports'] = VAPTAnalyzer.scan_ports(url)
        print(f"\033[92m[VAPT] Basic port scan complete.\033[0m")

        print(f"\033[96m[VAPT] VAPT analysis finished.\033[0m")
        return vapt_results

    @staticmethod
    def display_vapt_results(vapt_results):
        """Display VAPT results in terminal"""
        print(f"\n\033[96m+==============================================================+\033[0m")
        print(f"\033[96m|                      VAPT ANALYSIS REPORT                    |\033[0m")
        print(f"\033[96m+==============================================================+\033[0m")

        # Security Headers
        print(f"\033[96m[SECURITY HEADERS]\033[0m")
        if vapt_results.get('security_headers'):
            for header, value in vapt_results['security_headers'].items():
                print(f"\033[92m  • {header}: {value}\033[0m")
        else:
            print(f"\033[93m  No specific security headers found or could not retrieve.\033[0m")

        # Sensitive Files
        print(f"\n\033[96m[SENSITIVE FILES/DIRECTORIES]\033[0m")
        if vapt_results.get('sensitive_files'):
            for file_path in vapt_results['sensitive_files']:
                print(f"\033[91m  [!] Potentially found: {file_path}\033[0m")
        else:
            print(f"\033[92m  No common sensitive files/directories found.\033[0m")

        # Open Ports
        print(f"\n\033[96m[OPEN PORTS (BASIC SCAN)]\033[0m")
        if vapt_results.get('open_ports'):
            for port in vapt_results['open_ports']:
                print(f"\033[91m  [!] Port {port} is OPEN\033[0m")
        else:
            print(f"\033[92m  No common ports found open or scan skipped.\033[0m")

        print(f"\033[96m+==============================================================+\033[0m")


    @staticmethod
    def save_vapt_results(vapt_results, analysis_filename):
        """Append VAPT results to the saved analysis file"""
        if not analysis_filename:
            print(f"\033[91m[VAPT ERROR] Cannot save VAPT results, analysis filename is missing.\033[0m")
            return

        try:
            with open(analysis_filename, 'r+', encoding='utf-8') as f:
                analysis_data = json.load(f)
                analysis_data['vapt_results'] = vapt_results # Add VAPT results
                f.seek(0) # Rewind to the beginning
                json.dump(analysis_data, f, indent=2, ensure_ascii=False)
                f.truncate() # Truncate the rest of the file
            print(f"\033[95m[INTEL] VAPT results appended to: {analysis_filename}\033[0m")
        except FileNotFoundError:
            print(f"\033[91m[VAPT ERROR] Analysis file not found: {analysis_filename}\033[0m")
        except json.JSONDecodeError:
            print(f"\033[91m[VAPT ERROR] Failed to decode JSON from analysis file: {analysis_filename}\033[0m")
        except Exception as e:
            print(f"\033[91m[VAPT ERROR] Failed to save VAPT results: {e}\033[0m")
        

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
\033[0m"""
    banner += """
\033[96m+==============================================================+\033[0m
\033[96m|              ADVANCED WEB REFRESHER TOOL v4.0              |\033[0m
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
# Enable/disable VAPT mode
    print(f"\n\033[96m[SECURITY] Enable VAPT (Vulnerability Assessment) mode?\033[0m")
    print("\033[93m[1] Yes - Include security analysis\033[0m")
    print("\033[93m[2] No - Standard refresh only\033[0m")
    
    while True:
        vapt_choice = input("\033[92m[>] Enable VAPT? (1-2): \033[0m").strip()
        if vapt_choice == '1':
            config['vapt_enabled'] = True
            break
        elif vapt_choice == '2':
            config['vapt_enabled'] = False
            break
        else:
            print("\033[91m[!] Invalid choice. Please select 1 or 2.\033[0m")
    
    # Advanced features
    print(f"\n\033[96m[ADVANCED] Configure advanced features:\033[0m")
    
    config['proxy_rotation'] = input("\033[92m[>] Enable proxy rotation? (y/N): \033[0m").lower() == 'y'
    config['user_agent_rotation'] = input("\033[92m[>] Enable user agent rotation? (y/N): \033[0m").lower() == 'y'
    config['screenshot_capture'] = input("\033[92m[>] Capture screenshots? (y/N): \033[0m").lower() == 'y'
    
    # Site Intelligence 
    config['site_intelligence'] = input("\033[92m[>] Enable site intelligence analysis? (Y/n): \033[0m").lower() != 'n'
    
    return config

def manage_urls():
    """URL management interface"""
    while True:
        clear_screen()
        print("\033[96m+==============================================================+\033[0m")
        print("\033[96m|                    URL MANAGEMENT SYSTEM                     |\033[0m")
        print("\033[96m+==============================================================+\033[0m")
        
        saved_urls = URLManager.load_saved_urls()
        
        print(f"\n\033[93m[SAVED URLS] ({len(saved_urls)} total)\033[0m")
        if saved_urls:
            for i, url_data in enumerate(saved_urls):
                print(f"\033[92m  [{i+1}] {url_data['name']}: {url_data['url']}\033[0m")
        else:
            print("\033[91m  No saved URLs found\033[0m")
        
        print(f"\n\033[96m[OPTIONS]\033[0m")
        print("\033[93m  [A] Add new URL\033[0m")
        if saved_urls:
            print("\033[93m  [D] Delete URL\033[0m")
        print("\033[93m  [R] Return to main menu\033[0m")
        
        choice = input(f"\n\033[92m[>] Select option: \033[0m").strip().lower()
        
        if choice == 'a':
            url = input("\033[92m[>] Enter URL: \033[0m").strip()
            if url:
                name = input("\033[92m[>] Enter name for this URL: \033[0m").strip()
                if not name:
                    name = urlparse(url).netloc or url
                URLManager.add_url(url, name)
                print(f"\033[92m[✓] Added: {name}\033[0m")
                input("\033[92m[>] Press Enter to continue...\033[0m")
            else:
                print("\033[91m[!] URL cannot be empty\033[0m")
                input("\033[92m[>] Press Enter to continue...\033[0m")
        
        elif choice == 'd' and saved_urls:
            try:
                index = int(input("\033[92m[>] Enter URL number to delete: \033[0m")) - 1
                removed = URLManager.remove_url(index)
                if removed:
                    print(f"\033[92m[✓] Deleted: {removed['name']}\033[0m")
                else:
                    print("\033[91m[!] Invalid URL number\033[0m")
                input("\033[92m[>] Press Enter to continue...\033[0m")
            except ValueError:
                print("\033[91m[!] Please enter a valid number\033[0m")
                input("\033[92m[>] Press Enter to continue...\033[0m")
        
        elif choice == 'r':
            break
        
        else:
            print("\033[91m[!] Invalid option\033[0m")
            input("\033[92m[>] Press Enter to continue...\033[0m")

def create_chrome_driver(config):
    """Create Chrome WebDriver with proper configuration"""
    chrome_options = Options()
    
    # Essential options
    if config['headless']:
        chrome_options.add_argument("--headless")
    
    # Core stability options
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    
    # Stealth options
    if config.get('stealth', False):
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # User agent
    if config.get('user_agent_rotation', False):
        try:
            from fake_useragent import UserAgent
            ua = UserAgent()
            chrome_options.add_argument(f"--user-agent={ua.random}")
        except ImportError:
            print("\033[93m[WARNING] fake-useragent not available, using default user agent\033[0m")
    
    # Create service with webdriver-manager
    try:
        service = Service(ChromeDriverManager().install())
        print("\033[92m[✓] ChromeDriver auto-configured\033[0m")
    except Exception as e:
        print(f"\033[91m[ERROR] ChromeDriver setup failed: {e}\033[0m")
        print("\033[93m[INFO] Falling back to system ChromeDriver\033[0m")
        service = Service()
    
    # Create driver
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Additional stealth setup
        if config.get('stealth', False):
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    except Exception as e:
        print(f"\033[91m[ERROR] Failed to create Chrome driver: {e}\033[0m")
        print("\033[93m[TROUBLESHOOT] Please ensure Chrome browser is installed\033[0m")
        print("\033[93m[TROUBLESHOOT] Run: pip install --upgrade selenium webdriver-manager\033[0m")
        raise

def refresho_beast(config):
    """Main refresh engine with enhanced features"""
    try:
        clear_screen()
        print_banner()
        loading_animation()
        
        print(f"\n\033[96m+==============================================================+\033[0m")
        print(f"\033[96m|                    MISSION PARAMETERS                        |\033[0m")
        print(f"\033[96m+==============================================================+\033[0m")
        print(f"\033[93m[TARGET] {config['url']}\033[0m")
        print(f"\033[92m[MODE] {config['mode']}\033[0m")
        print(f"\033[95m[COUNT] {config['refresh_count']:,} refreshes\033[0m")
        print(f"\033[94m[DELAY] {config['delay']:.2f}s per refresh\033[0m")
        print(f"\033[91m[BROWSER] {'Headless' if config['headless'] else 'Visible'} {'+ Stealth' if config.get('stealth') else ''}\033[0m")
        print(f"\033[96m+==============================================================+\033[0m")
        
        HackerEffects.typing_effect("\033[92m[DEPLOYING] Initializing web driver...\033[0m")
        
        # Create driver
        driver = create_chrome_driver(config)
        
        print(f"\033[92m[✓] WebDriver initialized successfully\033[0m")
        print(f"\033[92m[✓] Target locked: {config['url']}\033[0m")
        
        # Navigate to target
        HackerEffects.typing_effect("\033[96m[INFILTRATING] Establishing connection to target...\033[0m")
        driver.get(config['url'])
        print(f"\033[92m[✓] Connection established\033[0m")
        
        # Site Intelligence Analysis
        analysis_filename = None
        if config.get('site_intelligence', False):
            print(f"\n\033[96m[INTEL] Gathering site intelligence...\033[0m")
            analysis = SiteAnalyzer.analyze_site(driver, config['url'])
            SiteAnalyzer.display_analysis(analysis)
            analysis_filename = SiteAnalyzer.save_analysis(analysis)
            
            # VAPT Analysis
            if config.get('vapt_enabled', False):
                vapt_results = VAPTAnalyzer.perform_vapt_checks(config['url'], driver)
                VAPTAnalyzer.display_vapt_results(vapt_results)
                VAPTAnalyzer.save_vapt_results(vapt_results, analysis_filename)
        
        # Refresh loop
        print(f"\n\033[91m[EXECUTING] Commencing refresh assault...\033[0m")
        
        start_time = time.time()
        failed_refreshes = 0
        
        for i in range(config['refresh_count']):
            try:
                # Progress indicator
                progress = (i + 1) / config['refresh_count'] * 100
                bar_length = 30
                filled_length = int(bar_length * (i + 1) // config['refresh_count'])
                bar = '█' * filled_length + '-' * (bar_length - filled_length)
                
                refresh_status = f"\033[92m[{i+1:,}/{config['refresh_count']:,}]\033[0m"
                progress_bar = f"\033[96m[{bar}]\033[0m"
                percentage = f"\033[93m{progress:.1f}%\033[0m"
                
                sys.stdout.write(f"\r{refresh_status} {progress_bar} {percentage}")
                sys.stdout.flush()
                
                # Perform refresh
                driver.refresh()
                
                # Screenshot capture
                if config.get('screenshot_capture', False) and (i + 1) % 50 == 0:
                    screenshot_name = f"screenshots/refresh_{i+1:04d}.png"
                    os.makedirs('screenshots', exist_ok=True)
                    driver.save_screenshot(screenshot_name)
                
                # User agent rotation
                if config.get('user_agent_rotation', False) and (i + 1) % 100 == 0:
                    try:
                        from fake_useragent import UserAgent
                        ua = UserAgent()
                        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                            "userAgent": ua.random
                        })
                    except ImportError:
                        pass
                
                # Delay
                time.sleep(config['delay'])
                
            except Exception as e:
                failed_refreshes += 1
                if failed_refreshes > 10:
                    print(f"\n\033[91m[ERROR] Too many failures, aborting mission\033[0m")
                    break
        
        execution_time = time.time() - start_time
        
        print(f"\n\033[92m[✓] MISSION ACCOMPLISHED\033[0m")
        print(f"\033[95m[STATS] {config['refresh_count']:,} refreshes in {execution_time:.2f}s\033[0m")
        print(f"\033[94m[RATE] {config['refresh_count']/execution_time:.2f} refreshes/second\033[0m")
        if failed_refreshes > 0:
            print(f"\033[93m[WARNING] {failed_refreshes} failed refreshes\033[0m")
        
        driver.quit()
        
        # Success animation
        success_animation(execution_time, config['refresh_count'], config)
        
        return True
        
    except KeyboardInterrupt:
        print(f"\n\033[93m[ABORTED] Mission terminated by user\033[0m")
        try:
            driver.quit()
        except:
            pass
        return False
        
    except Exception as e:
        print(f"\n\033[91m[CRITICAL ERROR] {e}\033[0m")
        print(f"\033[93m[TROUBLESHOOT] Check your internet connection and try again\033[0m")
        try:
            driver.quit()
        except:
            pass
        return False

def success_animation(execution_time, refresh_count, config):
    """Display success animation and stats"""
    clear_screen()
    
    # Matrix celebration
    HackerEffects.matrix_rain(2)
    
    success_banner = """
\033[92m
███╗   ███╗██╗███████╗███████╗██╗ ██████╗ ███╗   ██╗
████╗ ████║██║██╔════╝██╔════╝██║██╔═══██╗████╗  ██║
██╔████╔██║██║███████╗███████╗██║██║   ██║██╔██╗ ██║
██║╚██╔╝██║██║╚════██║╚════██║██║██║   ██║██║╚██╗██║
██║ ╚═╝ ██║██║███████║███████║██║╚██████╔╝██║ ╚████║
╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
 ██████╗ ██████╗ ███╗   ███╗██████╗ ██╗     ███████╗████████╗███████╗
██╔════╝██╔═══██╗████╗ ████║██╔══██╗██║     ██╔════╝╚══██╔══╝██╔════╝
██║     ██║   ██║██╔████╔██║██████╔╝██║     █████╗     ██║   █████╗  
██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝     ██║   ██╔══╝  
╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ███████╗███████╗   ██║   ███████╗
 ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝   ╚═╝   ╚══════╝
\033[0m"""
    
    print(success_banner)
    
    print(f"\033[96m+==============================================================+\033[0m")
    print(f"\033[96m|                    MISSION REPORT                            |\033[0m")
    print(f"\033[96m+==============================================================+\033[0m")
    print(f"\033[92m[TARGET] {config['url']}\033[0m")
    print(f"\033[95m[MODE] {config['mode']} MODE\033[0m")
    print(f"\033[93m[REFRESHES] {refresh_count:,} successful operations\033[0m")
    print(f"\033[94m[TIME] {execution_time:.2f} seconds\033[0m")
    print(f"\033[91m[RATE] {refresh_count/execution_time:.2f} ops/second\033[0m")
    print(f"\033[96m+==============================================================+\033[0m")
    
    # Generate mission report
    report = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'target': config['url'],
        'mode': config['mode'],
        'refresh_count': refresh_count,
        'execution_time': execution_time,
        'rate': refresh_count/execution_time,
        'config': config
    }
    
    # Save mission report
    try:
        if not os.path.exists('reports'):
            os.makedirs('reports')
        
        report_file = f"reports/mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\033[95m[INTEL] Mission report saved: {report_file}\033[0m")
    except Exception as e:
        print(f"\033[91m[ERROR] Failed to save report: {e}\033[0m")
    
    HackerEffects.typing_effect("\033[92m[STATUS] All systems nominal. Ready for next mission.\033[0m")
    time.sleep(2)

def main():
    """Main application entry point"""
    try:
        clear_screen()
        print_banner()
        
        HackerEffects.typing_effect("\033[96m[SYSTEM] Welcome to REFRESHO v4.0 - Advanced Web Refresher\033[0m")
        
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
        
        HackerEffects.typing_effect("\033[96m[SHUTDOWN] REFRESHO v4.0 terminating. Thank you for using our services.\033[0m")
        
    except KeyboardInterrupt:
        print(f"\n\033[93m[EXIT] REFRESHO v4.0 terminated by user\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\n\033[91m[CRITICAL ERROR] {e}\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    main()