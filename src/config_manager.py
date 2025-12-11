from urllib.parse import urlparse
try:
    from .ui_components import clear_screen
except ImportError:
    from ui_components import clear_screen

class ConfigManager:
    """Configuration management class"""
    
    @staticmethod
    def load_config():
        """Load default configuration"""
        return {
            'url': 'https://github.com/Xenonesis',
            'refresh_count': 10,
            'delay': 1.0,
            'headless': True,
            'stealth': False,
            'vapt_enabled': False,
            'proxy_rotation': False,
            'user_agent_rotation': False,
            'screenshot_capture': False,
            'site_intelligence': False,
            'mode': 'STEALTH'
        }
    
    @staticmethod
    def get_advanced_config():
        """Get user configuration for the mission (wrapper)"""
        return get_advanced_config()

def get_advanced_config():
    """Get user configuration for the mission"""
    config = {}
    
    print("\n\033[96m+==============================================================+\033[0m")
    print("\033[96m|                    MISSION CONFIGURATION                     |\033[0m")
    print("\033[96m+==============================================================+\033[0m")
    
    # Import here to avoid circular imports
    try:
        from .refresh_bot import HackerEffects, URLManager
    except ImportError:
        from refresh_bot import HackerEffects, URLManager
    
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
    # Import here to avoid circular imports
    try:
        from .refresh_bot import URLManager
    except ImportError:
        from refresh_bot import URLManager
    
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