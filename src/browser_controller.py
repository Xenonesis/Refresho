from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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