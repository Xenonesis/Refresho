import os
import sys
import time
import json
from datetime import datetime

class MissionController:
    """Mission controller class"""
    
    @staticmethod
    def run_mission(config):
        """Run mission with given configuration (wrapper)"""
        return refresho_beast(config)
    
    @staticmethod
    def display_success_animation(execution_time, refresh_count, config):
        """Display success animation (wrapper)"""
        return success_animation(execution_time, refresh_count, config)

def refresho_beast(config):
    """Main refresh engine with enhanced features"""
    try:
        # Import here to avoid circular imports
        try:
            from .ui_components import clear_screen, print_banner, loading_animation
            from .browser_controller import create_chrome_driver
            from .refresh_bot import HackerEffects, SiteAnalyzer
            from .vapt_analyzer import VAPTAnalyzer
        except ImportError:
            from ui_components import clear_screen, print_banner, loading_animation
            from browser_controller import create_chrome_driver
            from refresh_bot import HackerEffects, SiteAnalyzer
            from vapt_analyzer import VAPTAnalyzer
        
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
                if config.get('screenshot_capture', False) and (i + 1) % 10 == 0:
                    try:
                        screenshot_name = f"screenshots/refresh_{i+1:04d}.png"
                        os.makedirs('screenshots', exist_ok=True)
                        success = driver.save_screenshot(screenshot_name)
                        if success and os.path.exists(screenshot_name):
                            file_size = os.path.getsize(screenshot_name)
                            print(f"\n\033[95m[SCREENSHOT] Saved: {screenshot_name} ({file_size} bytes)\033[0m")
                        else:
                            print(f"\n\033[91m[ERROR] Screenshot failed: {screenshot_name}\033[0m")
                    except Exception as e:
                        print(f"\n\033[91m[ERROR] Screenshot error: {e}\033[0m")
                
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
    # Import here to avoid circular imports
    try:
        from .ui_components import clear_screen
        from .refresh_bot import HackerEffects
    except ImportError:
        from ui_components import clear_screen
        from refresh_bot import HackerEffects
    
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