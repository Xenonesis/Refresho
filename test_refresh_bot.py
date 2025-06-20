import unittest
from unittest.mock import patch, MagicMock, call
import time
import sys
import io
import os
import refresh_bot
from refresh_bot import HackerEffects, SystemAnalyzer

class TestHackerEffects(unittest.TestCase):
    """Test suite for hacker visual effects"""
    
    @patch('time.sleep')
    @patch('builtins.print')
    @patch('random.choice')
    def test_matrix_rain(self, mock_choice, mock_print, mock_sleep):
        """Test matrix rain animation"""
        mock_choice.return_value = '1'
        
        HackerEffects.matrix_rain(duration=1)
        
        # Should print multiple lines
        self.assertGreater(mock_print.call_count, 10)
        mock_sleep.assert_called()
    
    def test_glitch_text(self):
        """Test text glitching effect"""
        original_text = "HELLO WORLD"
        glitched = HackerEffects.glitch_text(original_text, intensity=0)
        
        # With 0 intensity, text should remain unchanged
        self.assertEqual(glitched, original_text)
        
        # With high intensity, text should be different
        glitched_high = HackerEffects.glitch_text(original_text, intensity=10)
        # Length should remain the same
        self.assertEqual(len(glitched_high), len(original_text))
    
    @patch('time.sleep')
    @patch('sys.stdout')
    def test_typing_effect(self, mock_stdout, mock_sleep):
        """Test typing animation effect"""
        mock_stdout.write = MagicMock()
        mock_stdout.flush = MagicMock()
        
        test_text = "TEST"
        HackerEffects.typing_effect(test_text, delay=0.01)
        
        # Should write each character
        self.assertEqual(mock_stdout.write.call_count, len(test_text))
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
        # Mock system values
        mock_cpu.return_value = 25.5
        mock_memory.return_value.percent = 60.2
        mock_disk.return_value.percent = 45.8
        mock_net.return_value = [1, 2, 3]  # 3 connections
        mock_boot.return_value = 1640995200  # Fixed timestamp
        
        sys_info = SystemAnalyzer.get_system_info()
        
        self.assertEqual(sys_info['cpu_percent'], 25.5)
        self.assertEqual(sys_info['memory_percent'], 60.2)
        self.assertEqual(sys_info['disk_usage'], 45.8)
        self.assertEqual(sys_info['network_connections'], 3)
        self.assertIn('boot_time', sys_info)
    
    def test_generate_session_id(self):
        """Test session ID generation"""
        session_id = SystemAnalyzer.generate_session_id()
        
        # Should be 8 characters long and uppercase
        self.assertEqual(len(session_id), 8)
        self.assertTrue(session_id.isupper())
        self.assertTrue(session_id.isalnum())
        
        # Should generate different IDs
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
        
        # Capture stdout to suppress print statements
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            refresh_bot.refresho_beast(self.test_config)
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify WebDriver interactions
        mock_driver.get.assert_called_once_with(self.test_config['url'])
        self.assertEqual(mock_driver.refresh.call_count, self.test_config['refresh_count'])
        mock_driver.quit.assert_called_once()
        
        # Verify UI functions were called
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
        
        # Capture stdout to suppress print statements
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            result = refresh_bot.refresho_beast(self.test_config)
        finally:
            sys.stdout = sys.__stdout__
        
        # Should return None when WebDriver fails
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
        
        # Capture stdout to suppress print statements
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            refresh_bot.refresho_beast(config_with_screenshots)
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify screenshot was attempted
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
        config_with_rotation['refresh_count'] = 200  # Ensure rotation triggers
        
        # Capture stdout to suppress print statements
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            refresh_bot.refresho_beast(config_with_rotation)
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify CDP command was called for user agent rotation
        mock_driver.execute_cdp_cmd.assert_called()

class TestUtilityFunctions(unittest.TestCase):
    """Test suite for utility functions"""
    
    def test_clear_screen(self):
        """Test screen clearing function"""
        # This function calls os.system, so we just test it doesn't crash
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
            'boot_time': '2024-01-01 12:00:00'
        }
        mock_session.return_value = 'ABC12345'
        
        refresh_bot.print_banner()
        
        # Verify system info and matrix effect were called
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
        
        # Should have multiple write calls for animation phases
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
        
        # Verify components were called
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
        # Simulate user selecting all defaults
        mock_input.side_effect = ['1', '1', '10', '1', 'n', 'n', 'n']
        
        config = refresh_bot.get_advanced_config()
        
        # Verify default configuration
        self.assertEqual(config['url'], 'https://github.com/Xenonesis')
        self.assertEqual(config['mode'], 'STEALTH')
        self.assertEqual(config['refresh_count'], 10)
        self.assertTrue(config['headless'])
        self.assertTrue(config['stealth'])
        self.assertFalse(config['proxy_rotation'])
        self.assertFalse(config['user_agent_rotation'])
        self.assertFalse(config['screenshot_capture'])
    
    @patch('builtins.input')
    @patch('refresh_bot.HackerEffects.typing_effect')
    @patch('builtins.print')
    def test_get_advanced_config_custom(self, mock_print, mock_typing, mock_input):
        """Test configuration with custom values"""
        # Simulate user selecting custom options
        mock_input.side_effect = [
            '3', 'https://custom.com',  # Custom URL
            '2', '5000',               # Assault mode, 5000 refreshes
            '3',                       # Visible browser
            'y', 'y', 'y'             # Enable all advanced features
        ]
        
        config = refresh_bot.get_advanced_config()
        
        # Verify custom configuration
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
        # Mock configuration
        mock_config.return_value = {
            'url': 'https://example.com',
            'refresh_count': 10,
            'delay': 1.0,
            'mode': 'STEALTH',
            'headless': True
        }
        
        # Mock user pressing Enter to start
        mock_input.return_value = ''
        
        refresh_bot.main()
        
        # Verify workflow
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
        
        # Simulate network error on refresh
        mock_driver.refresh.side_effect = Exception("Network error")
        
        config = {
            'url': 'https://example.com',
            'refresh_count': 5,
            'delay': 0.01,
            'mode': 'STEALTH',
            'headless': True,
            'stealth': False
        }
        
        # Capture stdout to suppress print statements
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            refresh_bot.refresho_beast(config)
        finally:
            sys.stdout = sys.__stdout__
        
        # Should still quit driver even with errors
        mock_driver.quit.assert_called_once()
    
    @patch('refresh_bot.get_advanced_config')
    @patch('builtins.print')
    def test_keyboard_interrupt_handling(self, mock_print, mock_config):
        """Test handling of keyboard interrupt"""
        mock_config.side_effect = KeyboardInterrupt()
        
        with self.assertRaises(SystemExit):
            refresh_bot.main()

if __name__ == '__main__':
    # Create test suite with all test classes
    test_classes = [
        TestHackerEffects,
        TestSystemAnalyzer, 
        TestRefreshoBeast,
        TestUtilityFunctions,
        TestConfigurationSystem,
        TestIntegration,
        TestErrorHandling
    ]
    
    suite = unittest.TestSuite()
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests with high verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"REFRESHO v2.0 TEST SUITE COMPLETE")
    print(f"{'='*60}")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*60}")