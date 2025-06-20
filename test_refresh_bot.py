import unittest
from unittest.mock import patch, MagicMock
import time
import sys
import io
import refresh_bot

class TestRefreshBot(unittest.TestCase):

    @patch('refresh_bot.webdriver.Chrome')
    @patch('refresh_bot.clear_screen')
    @patch('refresh_bot.print_banner')
    @patch('refresh_bot.loading_animation')
    def test_refresho_success(self, mock_loading, mock_banner, mock_clear, mock_chrome):
        """Test successful refresh operation"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        url = "https://github.com/Xenonesis"
        refresh_count = 3
        delay = 0.01
        headless = True

        # Capture stdout to suppress print statements during testing
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            refresh_bot.refresho(url, refresh_count, delay, headless)
        finally:
            sys.stdout = sys.__stdout__

        # Verify WebDriver interactions
        mock_driver.get.assert_called_once_with(url)
        self.assertEqual(mock_driver.refresh.call_count, refresh_count)
        mock_driver.quit.assert_called_once()

        # Verify UI functions were called
        mock_clear.assert_called_once()
        mock_banner.assert_called_once()
        mock_loading.assert_called_once()

    @patch('refresh_bot.webdriver.Chrome')
    @patch('refresh_bot.clear_screen')
    @patch('refresh_bot.print_banner')
    @patch('refresh_bot.loading_animation')
    def test_refresho_webdriver_exception(self, mock_loading, mock_banner, mock_clear, mock_chrome):
        """Test WebDriver initialization failure"""
        from selenium.common.exceptions import WebDriverException
        mock_chrome.side_effect = WebDriverException("Driver not found")

        url = "https://github.com/Xenonesis"
        refresh_count = 1
        delay = 0
        headless = True

        # Capture stdout to suppress print statements during testing
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            result = refresh_bot.refresho(url, refresh_count, delay, headless)
        finally:
            sys.stdout = sys.__stdout__

        # Should return None when WebDriver fails to initialize
        self.assertIsNone(result)

    @patch('refresh_bot.webdriver.Chrome')
    @patch('refresh_bot.clear_screen')
    @patch('refresh_bot.print_banner')
    @patch('refresh_bot.loading_animation')
    def test_refresho_invalid_url(self, mock_loading, mock_banner, mock_clear, mock_chrome):
        """Test handling of invalid URL"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_driver.get.side_effect = Exception("Invalid URL")

        url = "invalid_url"
        refresh_count = 1
        delay = 0
        headless = True

        # Capture stdout to suppress print statements during testing
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            refresh_bot.refresho(url, refresh_count, delay, headless)
        finally:
            sys.stdout = sys.__stdout__

        mock_driver.get.assert_called_once_with(url)
        mock_driver.quit.assert_called_once()

    @patch('refresh_bot.webdriver.Chrome')
    @patch('refresh_bot.clear_screen')
    @patch('refresh_bot.print_banner')
    @patch('refresh_bot.loading_animation')
    def test_refresho_refresh_failure(self, mock_loading, mock_banner, mock_clear, mock_chrome):
        """Test handling of refresh failures"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_driver.refresh.side_effect = Exception("Refresh failed")

        url = "https://github.com/Xenonesis"
        refresh_count = 2
        delay = 0
        headless = True

        # Capture stdout to suppress print statements during testing
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            refresh_bot.refresho(url, refresh_count, delay, headless)
        finally:
            sys.stdout = sys.__stdout__

        mock_driver.get.assert_called_once_with(url)
        mock_driver.refresh.assert_called_once()  # Should fail on first attempt
        mock_driver.quit.assert_called_once()

    def test_clear_screen(self):
        """Test clear_screen function"""
        # This function calls os.system, so we just test it doesn't crash
        try:
            refresh_bot.clear_screen()
        except Exception as e:
            self.fail(f"clear_screen() raised {e} unexpectedly!")

    @patch('builtins.print')
    @patch('time.sleep')
    def test_print_banner(self, mock_sleep, mock_print):
        """Test banner printing function"""
        refresh_bot.print_banner()
        mock_print.assert_called()
        mock_sleep.assert_called_with(1)

    @patch('sys.stdout')
    @patch('time.sleep')
    def test_loading_animation(self, mock_sleep, mock_stdout):
        """Test loading animation function"""
        mock_stdout.write = MagicMock()
        mock_stdout.flush = MagicMock()
        
        refresh_bot.loading_animation()
        
        # Should have multiple write calls for animation
        self.assertGreater(mock_stdout.write.call_count, 1)
        mock_stdout.flush.assert_called()

    @patch('builtins.print')
    @patch('time.sleep')
    def test_success_animation(self, mock_sleep, mock_print):
        """Test success animation function"""
        execution_time = 10.5
        refresh_count = 100
        
        refresh_bot.success_animation(execution_time, refresh_count)
        
        # Should print multiple times for animation
        self.assertGreater(mock_print.call_count, 5)
        mock_sleep.assert_called()

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow"""
    
    @patch('refresh_bot.get_user_config')
    @patch('refresh_bot.refresho')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_function(self, mock_print, mock_input, mock_refresho, mock_config):
        """Test main function workflow"""
        # Mock user configuration
        mock_config.return_value = {
            'url': 'https://example.com',
            'refresh_count': 10,
            'delay': 1.0,
            'headless': True
        }
        
        # Mock user pressing Enter to start
        mock_input.return_value = ''
        
        refresh_bot.main()
        
        # Verify configuration was requested
        mock_config.assert_called_once()
        
        # Verify refresho was called with correct parameters
        mock_refresho.assert_called_once_with(
            'https://example.com', 10, 1.0, True
        )

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
