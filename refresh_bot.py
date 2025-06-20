import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

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
\033[96m[+] Advanced Web Refresher Tool\033[0m
\033[93m[*] Developed by Addy@Xenonesis\033[0m
\033[91m[!] Initializing hacker mode...\033[0m
"""
    print(banner)
    time.sleep(1)

def loading_animation():
    chars = "/-\\|/-\\|"
    for i in range(20):
        sys.stdout.write(f"\r\033[92m[*] Loading {chars[i % len(chars)]}\033[0m")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\r\033[92m[✓] Ready to hack!\033[0m" + " " * 10)

def get_user_config():
    config = {}
    
    # Get URL
    print("\n\033[96m[?] Enter target URL (or press Enter for default):\033[0m")
    print("\033[93m[*] Default: https://github.com/Xenonesis\033[0m")
    url = input("\033[92m[>] URL: \033[0m").strip()
    config['url'] = url if url else "https://github.com/Xenonesis"
    print(f"\033[92m[✓] Target URL: {config['url']}\033[0m")
    
    # Get refresh count
    while True:
        try:
            print("\n\033[96m[?] How many times do you want to refresh?\033[0m")
            print("\033[93m[*] Maximum limit: 9,999,999\033[0m")
            count = input("\033[92m[>] Count: \033[0m").strip()
            
            if not count:
                print("\033[91m[!] Please enter a valid number\033[0m")
                continue
                
            refresh_count = int(count)
            
            if refresh_count <= 0:
                print("\033[91m[!] Count must be greater than 0\033[0m")
                continue
            elif refresh_count > 9999999:
                print("\033[91m[!] Maximum limit exceeded (9,999,999)\033[0m")
                continue
            else:
                config['refresh_count'] = refresh_count
                print(f"\033[92m[✓] Refresh count: {refresh_count:,}\033[0m")
                break
                
        except ValueError:
            print("\033[91m[!] Please enter a valid number\033[0m")
        except KeyboardInterrupt:
            print("\n\033[91m[!] Operation cancelled by user\033[0m")
            sys.exit(0)
    
    # Get delay
    while True:
        try:
            print("\n\033[96m[?] Delay between refreshes (seconds)?\033[0m")
            print("\033[93m[*] Default: 1 second (press Enter)\033[0m")
            delay_input = input("\033[92m[>] Delay: \033[0m").strip()
            
            if not delay_input:
                config['delay'] = 1
                break
            
            delay = float(delay_input)
            if delay < 0:
                print("\033[91m[!] Delay cannot be negative\033[0m")
                continue
            
            config['delay'] = delay
            break
            
        except ValueError:
            print("\033[91m[!] Please enter a valid number\033[0m")
        except KeyboardInterrupt:
            print("\n\033[91m[!] Operation cancelled by user\033[0m")
            sys.exit(0)
    
    print(f"\033[92m[✓] Delay: {config['delay']} seconds\033[0m")
    
    # Get browser mode
    print("\n\033[96m[?] Browser mode:\033[0m")
    print("\033[93m[1] Headless (invisible, faster)\033[0m")
    print("\033[93m[2] Visible (show browser window)\033[0m")
    
    while True:
        try:
            mode = input("\033[92m[>] Choose mode (1/2): \033[0m").strip()
            if mode == '1' or mode == '':
                config['headless'] = True
                print("\033[92m[✓] Headless mode selected\033[0m")
                break
            elif mode == '2':
                config['headless'] = False
                print("\033[92m[✓] Visible mode selected\033[0m")
                break
            else:
                print("\033[91m[!] Please enter 1 or 2\033[0m")
        except KeyboardInterrupt:
            print("\n\033[91m[!] Operation cancelled by user\033[0m")
            sys.exit(0)
    
    return config

def success_animation(execution_time, refresh_count):
    print("\n\033[92m" + "="*60)
    print("\033[92m" + " " * 20 + "MISSION ACCOMPLISHED")
    print("\033[92m" + "="*60 + "\033[0m")
    
    # Matrix-style success animation
    success_art = f"""
\033[92m
    ███████╗██╗   ██╗ ██████╗ ██████╗███████╗███████╗███████╗
    ██╔════╝██║   ██║██╔════╝██╔════╝██╔════╝██╔════╝██╔════╝
    ███████╗██║   ██║██║     ██║     █████╗  ███████╗███████╗
    ╚════██║██║   ██║██║     ██║     ██╔══╝  ╚════██║╚════██║
    ███████║╚██████╔╝╚██████╗╚██████╗███████╗███████║███████║
    ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝╚══════╝╚══════╝╚══════╝
\033[0m
\033[96m[+] Target successfully refreshed {refresh_count:,} times!\033[0m
\033[93m[*] Execution time: {execution_time:.2f} seconds\033[0m
\033[95m[*] Average time per refresh: {execution_time/refresh_count:.3f}s\033[0m
\033[91m[!] Hack complete - Addy@Xenonesis\033[0m
"""
    
    for line in success_art.split('\n'):
        print(line)
        time.sleep(0.1)
    
    # Blinking effect
    for _ in range(3):
        print("\033[92m[>>>] REFRESHO TERMINATED SUCCESSFULLY [<<<]\033[0m")
        time.sleep(0.3)
        print("\033[2A\033[K", end="")
        time.sleep(0.3)
    print("\033[92m[>>>] REFRESHO TERMINATED SUCCESSFULLY [<<<]\033[0m")

def refresho(url, refresh_count, delay=1, headless=True):
    clear_screen()
    print_banner()
    loading_animation()
    
    start_time = time.time()
    
    # Set up Chrome options
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    service = Service()
    
    mode_text = "stealth" if headless else "visible"
    print(f"\n\033[96m[*] Initializing {mode_text} browser...\033[0m")

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print(f"\033[92m[✓] {mode_text.title()} browser initialized\033[0m")
    except WebDriverException as e:
        print("\033[91m[✗] Error initializing Chrome WebDriver\033[0m")
        print(f"\033[91m[!] {str(e)}\033[0m")
        return

    success_count = 0
    try:
        try:
            print(f"\033[93m[*] Targeting: {url}\033[0m")
            driver.get(url)
            print("\033[92m[✓] Target acquired\033[0m")
        except Exception as e:
            print(f"\033[91m[✗] Target acquisition failed: {e}\033[0m")
            return

        print(f"\033[96m[*] Initiating refresh sequence for {refresh_count:,} refreshes...\033[0m")
        refresh_start = time.time()
        
        for i in range(refresh_count):
            time.sleep(delay)
            try:
                driver.refresh()
                success_count += 1
                progress = "█" * (success_count * 20 // refresh_count)
                remaining = "░" * (20 - len(progress))
                percentage = (success_count * 100) // refresh_count
                elapsed = time.time() - refresh_start
                eta = (elapsed / success_count) * (refresh_count - success_count) if success_count > 0 else 0
                print(f"\r\033[92m[{progress}{remaining}] {percentage}% | #{success_count:,} | ETA: {eta:.1f}s\033[0m", end="")
                sys.stdout.flush()
            except Exception as e:
                print(f"\n\033[91m[✗] Refresh failed: {e}\033[0m")
                break

    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        
        driver.quit()
        print(f"\n\033[93m[*] {mode_text.title()} browser terminated\033[0m")
        print(f"\033[96m[*] Total execution time: {execution_time:.2f} seconds\033[0m")
        
        if success_count == refresh_count:
            success_animation(execution_time, refresh_count)
        else:
            print(f"\033[91m[!] Mission partially completed: {success_count:,}/{refresh_count:,} refreshes\033[0m")
            print(f"\033[93m[*] Partial execution time: {execution_time:.2f} seconds\033[0m")

def main():
    try:
        config = get_user_config()
        print("\n\033[95m[*] Configuration Summary:\033[0m")
        print(f"\033[95m    URL: {config['url']}\033[0m")
        print(f"\033[95m    Refreshes: {config['refresh_count']:,}\033[0m")
        print(f"\033[95m    Delay: {config['delay']}s\033[0m")
        print(f"\033[95m    Mode: {'Headless' if config['headless'] else 'Visible'}\033[0m")
        
        input("\n\033[96m[*] Press Enter to start the mission...\033[0m")
        
        refresho(
            config['url'], 
            config['refresh_count'], 
            config['delay'], 
            config['headless']
        )
    except KeyboardInterrupt:
        print("\n\033[91m[!] Program terminated by user\033[0m")
        sys.exit(0)

if __name__ == "__main__":
    main()
