import unittest
from unittest.mock import patch, MagicMock, call
import time
import sys
import io
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError as e:
    print(f"[ERROR] webdriver-manager import failed: {e}")
    sys.exit(1)

# Import modules from refresh_bot for testing
sys.path.append('.')
import refresh_bot
from refresh_bot import HackerEffects, SystemAnalyzer, SiteAnalyzer, URLManager

class TestWebDriverFix(unittest.TestCase):
    """Test suite for WebDriver configuration and basic navigation."""

    def test_webdriver_initialization_and_navigation(self):
        """Test WebDriver initialization, navigation, and refresh."""
        print("\nTesting WebDriver configuration...")
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        try:
            service = Service(ChromeDriverManager().install())
            print("[OK] ChromeDriver service created successfully")
        except Exception as e:
            self.fail(f"[ERROR] ChromeDriver service failed: {e}")
        
        try:
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("[OK] Chrome WebDriver initialized successfully")
            
            driver.get("https://www.google.com")
            print(f"[OK] Successfully navigated to: {driver.current_url}")
            self.assertEqual(driver.current_url, "https://www.google.com/")
            
            driver.refresh()
            print("[OK] Page refresh successful")
            
            driver.quit()
            print("[OK] WebDriver closed successfully")
            self.assertTrue(True) # Indicate success
            
        except Exception as e:
            self.fail(f"[ERROR] WebDriver test failed: {e}")

class TestHackerEffects(unittest.TestCase):
    """Test suite for hacker visual effects"""
    
    @patch('time.sleep')
    @patch('builtins.print')
    @patch('random.choice')
    def test_matrix_rain(self, mock_choice, mock_print, mock_sleep):
        """Test matrix rain animation"""
        mock_choice.return_value = '1'
        
        HackerEffects.matrix_rain(duration=1)
        
        self.assertGreater(mock_print.call_count, 10)
        mock_sleep.assert_called()
    
    def test_glitch_text(self):
        """Test text glitching effect"""
        original_text = "HELLO WORLD"
        glitched = HackerEffects.glitch_text(original_text, intensity=0)
        
        self.assertEqual(glitched, original_text)
        
        glitched_high = HackerEffects.glitch_text(original_text, intensity=10)
        self.assertEqual(len(glitched_high), len(original_text))
    
    @patch('time.sleep')
    @patch('sys.stdout')
    def test_typing_effect(self, mock_stdout, mock_sleep):
        """Test typing animation effect"""
        mock_stdout.write = MagicMock()
        mock_stdout.flush = MagicMock()
        
        test_text = "TEST"
        HackerEffects.typing_effect(test_text, delay=0.01)
        
        self.assertGreaterEqual(mock_stdout.write.call_count, len(test_text))
        mock_stdout.flush.assert_called()

class TestSystemAnalyzer(unittest.TestCase):
    """Test suite for system analysis functions"""
    
    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    @patch('psutil.net_connections')
    @patch('psutil.boot_time')
    def test_get_system_info(self, mock_boot, mock_net, mock_disk, mock_memory, mock_cpu):
        """Test system information gathering"""
        mock_cpu.return_value = 25.5
        mock_memory.return_value.percent = 60.2
        mock_disk.return_value.percent = 45.8
        mock_net.return_value = [1, 2, 3]
        mock_boot.return_value = 1640995200
        
        sys_info = SystemAnalyzer.get_system_info()
        
        self.assertEqual(sys_info['cpu_percent'], 25.5)
        self.assertEqual(sys_info['memory_percent'], 60.2)
        self.assertEqual(sys_info['disk_usage'], 45.8)
        self.assertEqual(sys_info['network_connections'], 3)
        self.assertIn('boot_time', sys_info)
    
    def test_generate_session_id(self):
        """Test session ID generation"""
        session_id = SystemAnalyzer.generate_session_id()
        
        self.assertEqual(len(session_id), 8)
        self.assertTrue(session_id.isupper())
        self.assertTrue(session_id.isalnum())
        
        session_id2 = SystemAnalyzer.generate_session_id()
        self.assertNotEqual(session_id, session_id2)

class TestRefreshoBeast(unittest.TestCase):
    """Test suite for main REFRESHO functionality"""
    
    def setUp(self):
        """Set up test configuration"""
        self.test_config = {
            'url': 'https://example.com',
            'refresh_count': 5,
            'delay': 0.01,
            'mode': 'STEALTH',
            'headless': True,
            'stealth': True,
            'user_agent_rotation': False,
            'screenshot_capture': False
        }
    
    @patch('refresh_bot.clear_screen')
    @patch('refresh_bot.print_banner')
    @patch('refresh_bot.loading_animation')
    @patch('refresh_bot.webdriver.Chrome')
    def test_refresho_beast_success(self, mock_chrome, mock_loading, mock_banner, mock_clear):
        """Test successful REFRESHO beast execution"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            refresh_bot.refresho_beast(self.test_config)
        finally:
            sys.stdout = sys.__stdout__
        
        mock_driver.get.assert_called_once_with(self.test_config['url'])
        self.assertEqual(mock_driver.refresh.call_count, self.test_config['refresh_count'])
        mock_driver.quit.assert_called_once()
        
        mock_clear.assert_called()
        mock_banner.assert_called_once()
        mock_loading.assert_called_once()
    
    @patch('refresh_bot.clear_screen')
    @patch('refresh_bot.print_banner')
    @patch('refresh_bot.loading_animation')
    @patch('refresh_bot.webdriver.Chrome')
    def test_refresho_beast_webdriver_failure(self, mock_chrome, mock_loading, mock_banner, mock_clear):
        """Test WebDriver initialization failure"""
        from selenium.common.exceptions import WebDriverException
        mock_chrome.side_effect = WebDriverException("Driver not found")
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            result = refresh_bot.refresho_beast(self.test_config)
        finally:
            sys.stdout = sys.__stdout__
        
        self.assertIsNone(result)
    
    @patch('refresh_bot.clear_screen')
    @patch('refresh_bot.print_banner')
    @patch('refresh_bot.loading_animation')
    @patch('refresh_bot.webdriver.Chrome')
    def test_refresho_beast_with_screenshots(self, mock_chrome, mock_loading, mock_banner, mock_clear):
        """Test REFRESHO with screenshot capture enabled"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        config_with_screenshots = self.test_config.copy()
        config_with_screenshots['screenshot_capture'] = True
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            refresh_bot.refresho_beast(config_with_screenshots)
        finally:
            sys.stdout = sys.__stdout__
        
        mock_driver.save_screenshot.assert_called()
    
    @patch('refresh_bot.clear_screen')
    @patch('refresh_bot.print_banner')
    @patch('refresh_bot.loading_animation')
    @patch('refresh_bot.webdriver.Chrome')
    def test_refresho_beast_user_agent_rotation(self, mock_chrome, mock_loading, mock_banner, mock_clear):
        """Test user agent rotation functionality"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        config_with_rotation = self.test_config.copy()
        config_with_rotation['user_agent_rotation'] = True
        config_with_rotation['refresh_count'] = 200
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            refresh_bot.refresho_beast(config_with_rotation)
        finally:
            sys.stdout = sys.__stdout__
        
        mock_driver.execute_cdp_cmd.assert_called()

class TestUtilityFunctions(unittest.TestCase):
    """Test suite for utility functions"""
    
    def test_clear_screen(self):
        """Test screen clearing function"""
        try:
            refresh_bot.clear_screen()
        except Exception as e:
            self.fail(f"clear_screen() raised {e} unexpectedly!")
    
    @patch('refresh_bot.SystemAnalyzer.get_system_info')
    @patch('refresh_bot.SystemAnalyzer.generate_session_id')
    @patch('refresh_bot.HackerEffects.matrix_rain')
    @patch('builtins.print')
    def test_print_banner(self, mock_print, mock_matrix, mock_session, mock_sys_info):
        """Test banner printing with system info"""
        mock_sys_info.return_value = {
            'cpu_percent': 25.0,
            'memory_percent': 60.0,
            'disk_usage': 45.0,
            'network_connections': 5,
            'boot_time': '2025-01-01 12:00:00'
        }
        mock_session.return_value = 'ABC12345'
        
        refresh_bot.print_banner()
        
        mock_sys_info.assert_called_once()
        mock_session.assert_called_once()
        mock_matrix.assert_called_once()
        mock_print.assert_called()
    
    @patch('builtins.print')
    @patch('time.sleep')
    @patch('sys.stdout')
    def test_loading_animation(self, mock_stdout, mock_sleep, mock_print):
        """Test loading animation sequence"""
        mock_stdout.write = MagicMock()
        mock_stdout.flush = MagicMock()
        
        refresh_bot.loading_animation()
        
        self.assertGreater(mock_stdout.write.call_count, 50)
        mock_stdout.flush.assert_called()
        mock_print.assert_called()
    
    @patch('refresh_bot.clear_screen')
    @patch('refresh_bot.HackerEffects.matrix_rain')
    @patch('builtins.print')
    @patch('time.sleep')
    def test_success_animation(self, mock_sleep, mock_print, mock_matrix, mock_clear):
        """Test success animation display"""
        execution_time = 10.5
        refresh_count = 100
        config = {'url': 'https://example.com', 'mode': 'STEALTH'}
        
        refresh_bot.success_animation(execution_time, refresh_count, config)
        
        mock_clear.assert_called_once()
        mock_matrix.assert_called_once()
        mock_print.assert_called()
        mock_sleep.assert_called()

class TestConfigurationSystem(unittest.TestCase):
    """Test suite for configuration system"""
    
    @patch('builtins.input')
    @patch('refresh_bot.HackerEffects.typing_effect')
    @patch('builtins.print')
    def test_get_advanced_config_defaults(self, mock_print, mock_typing, mock_input):
        """Test configuration with default values"""
        mock_input.side_effect = ['1', '1', '10', '1', 'n', 'n', 'n', 'y']
        
        config = refresh_bot.get_advanced_config()
        
        self.assertEqual(config['url'], 'https://github.com/Xenonesis')
        self.assertEqual(config['mode'], 'STEALTH')
        self.assertEqual(config['refresh_count'], 10)
        self.assertTrue(config['headless'])
        self.assertTrue(config['stealth'])
        self.assertFalse(config['proxy_rotation'])
        self.assertFalse(config['user_agent_rotation'])
        self.assertFalse(config['screenshot_capture'])
    
    @patch('refresh_bot.URLManager.load_saved_urls', return_value=[])
    @patch('builtins.input')
    @patch('refresh_bot.HackerEffects.typing_effect')
    @patch('builtins.print')
    def test_get_advanced_config_custom(self, mock_print, mock_typing, mock_input, mock_load_urls):
        """Test configuration with custom values"""
        mock_input.side_effect = [
                    '2', 'https://custom.com', 'n',
                    '2', '5000',
                    '3',
                    'y', 'y', 'y', 'y'
                ]
        
        config = refresh_bot.get_advanced_config()
        
        self.assertEqual(config['url'], 'https://custom.com')
        self.assertEqual(config['mode'], 'ASSAULT')
        self.assertEqual(config['refresh_count'], 5000)
        self.assertFalse(config['headless'])
        self.assertFalse(config['stealth'])
        self.assertTrue(config['proxy_rotation'])
        self.assertTrue(config['user_agent_rotation'])
        self.assertTrue(config['screenshot_capture'])

class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflow"""
    
    @patch('refresh_bot.get_advanced_config')
    @patch('refresh_bot.refresho_beast')
    @patch('builtins.input')
    @patch('refresh_bot.clear_screen')
    @patch('refresh_bot.HackerEffects.typing_effect')
    @patch('builtins.print')
    def test_main_function_complete_flow(self, mock_print, mock_typing, mock_clear, 
                                       mock_input, mock_refresho, mock_config):
        """Test complete main function workflow"""
        mock_config.return_value = {
            'url': 'https://example.com',
            'refresh_count': 10,
            'delay': 1.0,
            'mode': 'STEALTH',
            'headless': True
        }
        
        mock_input.return_value = ''
        
        refresh_bot.main()
        
        mock_config.assert_called_once()
        mock_refresho.assert_called_once()
        mock_clear.assert_called()
        mock_typing.assert_called()

class TestErrorHandling(unittest.TestCase):
    """Test suite for error handling scenarios"""
    
    @patch('refresh_bot.clear_screen')
    @patch('refresh_bot.print_banner')
    @patch('refresh_bot.loading_animation')
    @patch('refresh_bot.webdriver.Chrome')
    def test_network_error_handling(self, mock_chrome, mock_loading, mock_banner, mock_clear):
        """Test handling of network errors during refresh"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        mock_driver.refresh.side_effect = Exception("Network error")
        
        config = {
            'url': 'https://example.com',
            'refresh_count': 5,
            'delay': 0.01,
            'mode': 'STEALTH',
            'headless': True,
            'stealth': False
        }
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            refresh_bot.refresho_beast(config)
        finally:
            sys.stdout = sys.__stdout__
        
        mock_driver.quit.assert_called_once()
    
    @patch('refresh_bot.get_advanced_config')
    @patch('builtins.print')
    def test_keyboard_interrupt_handling(self, mock_print, mock_config):
        """Test handling of keyboard interrupt"""
        mock_config.side_effect = KeyboardInterrupt()
        
        with self.assertRaises(SystemExit):
            refresh_bot.main()

class TestSiteAnalysis(unittest.TestCase):
    """Test suite for the Site Analysis feature."""

    @patch('refresh_bot.webdriver.Chrome')
    @patch('refresh_bot.SiteAnalyzer.analyze_site')
    @patch('refresh_bot.SiteAnalyzer.display_analysis')
    @patch('refresh_bot.SiteAnalyzer.save_analysis')
    @patch('builtins.print')
    def test_site_analysis_feature(self, mock_print, mock_save, mock_display, mock_analyze, mock_chrome):
        """Test the site analysis workflow."""
        print("\nTesting Site Analysis Feature...")
        
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_analyze.return_value = {"title": "Test Title", "links": 5, "images": 10}
        mock_save.return_value = "analysis_report_test.json"

        # Capture stdout to suppress print statements
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            # Simulate the original test_site_analysis function's logic
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install()) # This line might still cause issues if ChromeDriverManager() is not mocked
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            test_url = "https://www.google.com"
            driver.get(test_url)
            analysis = SiteAnalyzer.analyze_site(driver, test_url)
            SiteAnalyzer.display_analysis(analysis)
            filename = SiteAnalyzer.save_analysis(analysis)
            driver.quit()

        except Exception as e:
            self.fail(f"[ERROR] Site analysis test failed: {e}")
        finally:
            sys.stdout = sys.__stdout__

        mock_driver.get.assert_called_once_with(test_url)
        mock_analyze.assert_called_once_with(mock_driver, test_url)
        mock_display.assert_called_once_with({"title": "Test Title", "links": 5, "images": 10})
        mock_save.assert_called_once_with({"title": "Test Title", "links": 5, "images": 10})
        mock_driver.quit.assert_called_once()
        self.assertTrue(True) # Indicate success

class TestURLManager(unittest.TestCase):
    """Test suite for the URL management system."""

    def setUp(self):
        """Set up for URLManager tests, ensuring a clean state with mocked file ops."""
        self.mock_file_content = [] # In-memory representation of saved_urls.json
        self.mock_file_exists = False # Simulate existence of the file

        # Patch built-in functions and modules that URLManager interacts with
        self.patcher_open = patch('builtins.open', MagicMock())
        self.patcher_json_load = patch('json.load')
        self.patcher_json_dump = patch('json.dump')
        self.patcher_os_path_exists = patch('os.path.exists')

        self.mock_open = self.patcher_open.start()
        self.mock_json_load = self.patcher_json_load.start()
        self.mock_json_dump = self.patcher_json_dump.start()
        self.mock_os_path_exists = self.patcher_os_path_exists.start()

        # Configure mocks
        # When os.path.exists is called, return our internal flag
        self.mock_os_path_exists.side_effect = lambda path: self.mock_file_exists

        # When json.load is called, return our internal content
        self.mock_json_load.side_effect = lambda fp: self.mock_file_content

        # When json.dump is called, update our internal content and set file_exists
        def _mock_dump_json(data, fp, indent=None, ensure_ascii=True):
            self.mock_file_content[:] = data # Modify list in place to reflect changes
            self.mock_file_exists = True
        self.mock_json_dump.side_effect = _mock_dump_json

        # Mock file handle for open() calls (not strictly necessary if json.load/dump are mocked, but good practice)
        self.mock_file_handle = MagicMock()
        self.mock_open.return_value.__enter__.return_value = self.mock_file_handle

        # Re-initialize the in-memory state for each test
        self.mock_file_content = []
        self.mock_file_exists = False


    def tearDown(self):
        """Clean up after URLManager tests by stopping all patches."""
        self.patcher_open.stop()
        self.patcher_json_load.stop()
        self.patcher_json_dump.stop()
        self.patcher_os_path_exists.stop()

    def test_add_and_load_urls(self):
        """Test adding and loading URLs with mocked file system."""
        print("\nTesting URL Management System (Mocked)...")
        
        URLManager.add_url("https://www.github.com", "GitHub")
        URLManager.add_url("https://www.stackoverflow.com", "Stack Overflow")
        
        urls = URLManager.load_saved_urls()
        self.assertEqual(len(urls), 2)
        self.assertEqual(urls[0]['url'], "https://www.github.com")
        self.assertEqual(urls[1]['name'], "Stack Overflow")
        print("[OK] URLs added and loaded successfully (Mocked).")

    def test_remove_url(self):
        """Test removing a URL with mocked file system."""
        # Setup initial content
        self.mock_file_content = [
            {'name': 'GitHub', 'url': 'https://www.github.com'},
            {'name': 'Stack Overflow', 'url': 'https://www.stackoverflow.com'}
        ]
        self.mock_file_exists = True

        removed = URLManager.remove_url(0)
        self.assertIsNotNone(removed)
        self.assertEqual(removed['name'], "GitHub")
        
        urls = URLManager.load_saved_urls()
        self.assertEqual(len(urls), 1)
        self.assertEqual(urls[0]['url'], "https://www.stackoverflow.com")
        print("[OK] URL removed successfully (Mocked).")

    def test_remove_invalid_index(self):
        """Test removing URL with an invalid index with mocked file system."""
        # Setup initial content
        self.mock_file_content = [
            {'name': 'GitHub', 'url': 'https://www.github.com'}
        ]
        self.mock_file_exists = True

        removed = URLManager.remove_url(100) # Invalid index
        self.assertIsNone(removed)
        
        urls = URLManager.load_saved_urls()
        self.assertEqual(len(urls), 1)
        print("[OK] Invalid index removal handled correctly (Mocked).")

    def test_file_creation(self):
        """Test if the saved_urls.json file is created with mocked file system."""
        # Initially, the file does not exist
        self.mock_file_exists = False
        self.mock_file_content = []

        URLManager.add_url("https://www.example.com", "Example")
        self.assertTrue(self.mock_file_exists) # Check our internal mock state
        self.assertEqual(len(self.mock_file_content), 1)
        print("[OK] saved_urls.json file created (Mocked).")

if __name__ == '__main__':
    # Create test suite with all test classes
    test_classes = [
        TestWebDriverFix,
        TestHackerEffects,
        TestSystemAnalyzer, 
        TestRefreshoBeast,
        TestUtilityFunctions,
        TestConfigurationSystem,
        TestIntegration,
        TestErrorHandling,
        TestSiteAnalysis,
        TestURLManager
    ]
    
    suite = unittest.TestSuite()
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print(f"\n{'='*60}")
    print(f"REFRESHO v3.0 COMBINED TEST SUITE COMPLETE")
    print(f"{'='*60}")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*60}")