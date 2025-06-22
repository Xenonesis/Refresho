#!/usr/bin/env python3
"""
REFRESHO v4.0 - Comprehensive Test Suite
Combined test file for all refresh_bot functionality including VAPT, WebDriver, and core features
"""

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
from refresh_bot import HackerEffects, SystemAnalyzer, SiteAnalyzer, URLManager, VAPTAnalyzer

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

        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install())
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
        self.assertTrue(True)

class TestURLManager(unittest.TestCase):
    """Test suite for the URL management system."""

    def setUp(self):
        """Set up for URLManager tests, ensuring a clean state with mocked file ops."""
        self.mock_file_content = []
        self.mock_file_exists = False

        self.patcher_open = patch('builtins.open', MagicMock())
        self.patcher_json_load = patch('json.load')
        self.patcher_json_dump = patch('json.dump')
        self.patcher_os_path_exists = patch('os.path.exists')

        self.mock_open = self.patcher_open.start()
        self.mock_json_load = self.patcher_json_load.start()
        self.mock_json_dump = self.patcher_json_dump.start()
        self.mock_os_path_exists = self.patcher_os_path_exists.start()

        self.mock_os_path_exists.side_effect = lambda path: self.mock_file_exists
        self.mock_json_load.side_effect = lambda fp: self.mock_file_content

        def _mock_dump_json(data, fp, indent=None, ensure_ascii=True):
            self.mock_file_content[:] = data
            self.mock_file_exists = True
        self.mock_json_dump.side_effect = _mock_dump_json

        self.mock_file_handle = MagicMock()
        self.mock_open.return_value.__enter__.return_value = self.mock_file_handle

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

class TestVAPTFunctionality(unittest.TestCase):
    """Test suite for VAPT (Vulnerability Assessment) functionality"""

    def setUp(self):
        """Set up test configuration for VAPT tests"""
        self.test_url = "https://httpbin.org"

    @patch('requests.head')
    def test_security_headers_check(self, mock_head):
        """Test security headers checking functionality"""
        print("\n🛡️  Testing Security Headers Check...")
        
        # Mock response with some security headers
        mock_response = MagicMock()
        mock_response.headers = {
            'Strict-Transport-Security': 'max-age=31536000',
            'Content-Security-Policy': 'default-src \'self\'',
            'X-Frame-Options': 'DENY'
        }
        mock_head.return_value = mock_response
        
        headers = VAPTAnalyzer.check_security_headers(self.test_url)
        
        self.assertIsInstance(headers, dict)
        self.assertIn('Strict-Transport-Security', headers)
        self.assertEqual(headers['Strict-Transport-Security'], 'max-age=31536000')
        print(f"✅ Security headers check completed: {len(headers)} headers found")

    @patch('requests.get')
    def test_sensitive_files_check(self, mock_get):
        """Test sensitive files detection functionality"""
        print("\n📁 Testing Sensitive Files Check...")
        
        # Mock response for files not found
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response
        
        files = VAPTAnalyzer.check_sensitive_files(self.test_url)
        
        self.assertIsInstance(files, list)
        self.assertEqual(len(files), 0)  # No files should be found with 404 responses
        print(f"✅ Sensitive files check completed: {len(files)} files found")

    @patch('socket.socket')
    def test_port_scan(self, mock_socket):
        """Test basic port scanning functionality"""
        print("\n🔌 Testing Port Scan...")
        
        # Mock socket to simulate closed ports
        mock_sock = MagicMock()
        mock_sock.connect_ex.return_value = 1  # Connection refused
        mock_socket.return_value = mock_sock
        
        ports = VAPTAnalyzer.scan_ports(self.test_url, [80, 443])
        
        self.assertIsInstance(ports, list)
        print(f"✅ Port scan completed: {len(ports)} open ports found")

    def test_class_structure_validation(self):
        """Test that all required VAPT methods exist"""
        print("\n🏗️  Testing VAPT Class Structure...")
        
        # Check VAPTAnalyzer methods
        self.assertTrue(hasattr(VAPTAnalyzer, 'check_security_headers'))
        self.assertTrue(hasattr(VAPTAnalyzer, 'check_sensitive_files'))
        self.assertTrue(hasattr(VAPTAnalyzer, 'scan_ports'))
        self.assertTrue(hasattr(VAPTAnalyzer, 'perform_vapt_checks'))
        self.assertTrue(hasattr(VAPTAnalyzer, 'display_vapt_results'))
        self.assertTrue(hasattr(VAPTAnalyzer, 'save_vapt_results'))
        
        # Check SiteAnalyzer methods
        self.assertTrue(hasattr(SiteAnalyzer, 'analyze_site'))
        self.assertTrue(hasattr(SiteAnalyzer, 'display_analysis'))
        self.assertTrue(hasattr(SiteAnalyzer, 'save_analysis'))
        
        print("✅ All required VAPT methods found")

    @patch('refresh_bot.VAPTAnalyzer.check_security_headers')
    @patch('refresh_bot.VAPTAnalyzer.check_sensitive_files')
    @patch('refresh_bot.VAPTAnalyzer.scan_ports')
    def test_perform_vapt_checks(self, mock_scan, mock_files, mock_headers):
        """Test the main VAPT checks integration"""
        print("\n🎯 Testing Complete VAPT Checks...")
        
        # Mock return values
        mock_headers.return_value = {'Content-Security-Policy': 'default-src \'self\''}
        mock_files.return_value = []
        mock_scan.return_value = [80, 443]
        
        mock_driver = MagicMock()
        results = VAPTAnalyzer.perform_vapt_checks(self.test_url, mock_driver)
        
        self.assertIsInstance(results, dict)
        self.assertIn('security_headers', results)
        self.assertIn('sensitive_files', results)
        self.assertIn('open_ports', results)
        
        print("✅ Complete VAPT checks integration successful")

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

def run_vapt_functionality_test():
    """Standalone VAPT functionality test (without browser)"""
    print("\n" + "="*80)
    print("🔍 STANDALONE VAPT FUNCTIONALITY TEST")
    print("="*80)
    
    test_url = "https://httpbin.org"
    print(f"\n📡 Testing URL: {test_url}")
    
    # Test 1: Security Headers Check
    print("\n🛡️  Testing Security Headers Check...")
    try:
        headers = VAPTAnalyzer.check_security_headers(test_url)
        print(f"✅ Security headers check completed: {len(headers)} headers found")
        if headers:
            for header, value in headers.items():
                print(f"   • {header}: {value[:50]}{'...' if len(str(value)) > 50 else ''}")
        else:
            print("   • No security headers found")
    except Exception as e:
        print(f"❌ Security headers check failed: {e}")
    
    # Test 2: Sensitive Files Check
    print("\n📁 Testing Sensitive Files Check...")
    try:
        files = VAPTAnalyzer.check_sensitive_files(test_url)
        print(f"✅ Sensitive files check completed: {len(files)} files found")
        if files:
            for file_path in files:
                print(f"   • {file_path}")
        else:
            print("   • No sensitive files found")
    except Exception as e:
        print(f"❌ Sensitive files check failed: {e}")
    
    # Test 3: Port Scan (limited to common web ports)
    print("\n🔌 Testing Port Scan...")
    try:
        web_ports = [80, 443]
        ports = VAPTAnalyzer.scan_ports(test_url, web_ports)
        print(f"✅ Port scan completed: {len(ports)} open ports found")
        if ports:
            for port in ports:
                print(f"   • Port {port} is open")
        else:
            print("   • No ports found open (or scan skipped)")
    except Exception as e:
        print(f"❌ Port scan failed: {e}")
    
    # Test 4: Class Structure Validation
    print("\n🏗️  Testing Class Structure...")
    try:
        required_methods = [
            (SiteAnalyzer, 'display_analysis'),
            (SiteAnalyzer, 'save_analysis'),
            (VAPTAnalyzer, 'perform_vapt_checks'),
            (VAPTAnalyzer, 'display_vapt_results'),
            (VAPTAnalyzer, 'save_vapt_results')
        ]
        
        for cls, method in required_methods:
            if hasattr(cls, method):
                print(f"✅ {cls.__name__}.{method} method found")
            else:
                print(f"❌ {cls.__name__}.{method} method missing!")
                
    except Exception as e:
        print(f"❌ Class structure test failed: {e}")
    
    print("\n🎯 VAPT functionality test completed!")
    print("=" * 80)

if __name__ == '__main__':
    print("🚀 REFRESHO v4.0 - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    
    # First run standalone VAPT test
    run_vapt_functionality_test()
    
    # Then run full unit test suite
    print("\n🧪 RUNNING UNIT TEST SUITE...")
    print("=" * 80)
    
    # Create test suite with all test classes
    test_classes = [
        TestWebDriverFix,
        TestHackerEffects,
        TestSystemAnalyzer, 
        TestRefreshoBeast,
        TestUtilityFunctions,
        TestSiteAnalysis,
        TestURLManager,
        TestVAPTFunctionality,
        TestErrorHandling,
        TestIntegration
    ]
    
    suite = unittest.TestSuite()
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print(f"\n{'='*80}")
    print(f"🎯 REFRESHO v4.0 COMPREHENSIVE TEST SUITE COMPLETE")
    print(f"{'='*80}")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"Success Rate: {success_rate:.1f}%")
    print(f"{'='*80}")
    
    if len(result.failures) == 0 and len(result.errors) == 0:
        print("🎉 ALL TESTS PASSED - REFRESHO v4.0 IS READY FOR DEPLOYMENT!")
    else:
        print("⚠️  SOME TESTS FAILED - CHECK OUTPUT ABOVE FOR DETAILS")