#!/usr/bin/env python3
"""
Automated Test Suite for CI/CD
Comprehensive tests that can run in automated environments
"""

import pytest
import sys
import os
import json
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from refresh_bot import SystemAnalyzer, URLManager, HackerEffects, SiteAnalyzer
from config_manager import ConfigManager
from vapt_analyzer import VAPTAnalyzer

class TestSystemAnalyzer:
    """Test SystemAnalyzer functionality"""
    
    def test_get_system_info(self):
        """Test system information retrieval"""
        info = SystemAnalyzer.get_system_info()
        assert 'cpu_percent' in info
        assert 'memory_percent' in info
        assert 'disk_usage' in info
        assert 'network_connections' in info
        assert isinstance(info['cpu_percent'], (int, float))
        assert isinstance(info['memory_percent'], (int, float))
        assert isinstance(info['disk_usage'], (int, float))
        assert isinstance(info['network_connections'], int)
    
    def test_generate_session_id(self):
        """Test session ID generation"""
        session_id = SystemAnalyzer.generate_session_id()
        assert isinstance(session_id, str)
        assert len(session_id) == 8
        
        # Test uniqueness
        id1 = SystemAnalyzer.generate_session_id()
        time.sleep(0.01)
        id2 = SystemAnalyzer.generate_session_id()
        assert id1 != id2

class TestURLManager:
    """Test URL management functionality"""
    
    def test_load_saved_urls(self):
        """Test loading saved URLs"""
        urls = URLManager.load_saved_urls()
        assert isinstance(urls, list)
    
    def test_add_url(self):
        """Test adding a URL"""
        initial_urls = URLManager.load_saved_urls()
        initial_count = len(initial_urls)
        
        test_url = f"https://test-{int(time.time())}.example.com"
        count = URLManager.add_url(test_url, "Test URL")
        
        assert count > initial_count
        
        # Verify it was added
        urls = URLManager.load_saved_urls()
        assert len(urls) == count
        
        # Clean up
        URLManager.remove_url(len(urls) - 1)
    
    def test_remove_url(self):
        """Test removing a URL"""
        # Add a test URL
        test_url = f"https://test-remove-{int(time.time())}.example.com"
        URLManager.add_url(test_url, "Test Remove")
        
        urls = URLManager.load_saved_urls()
        initial_count = len(urls)
        
        # Remove it
        removed = URLManager.remove_url(initial_count - 1)
        assert removed is not None
        
        # Verify it was removed
        urls_after = URLManager.load_saved_urls()
        assert len(urls_after) == initial_count - 1

class TestConfigManager:
    """Test configuration management"""
    
    def test_load_config(self):
        """Test loading default configuration"""
        config = ConfigManager.load_config()
        assert isinstance(config, dict)
        
        # Check required keys
        required_keys = [
            'url', 'refresh_count', 'delay', 'headless',
            'stealth', 'vapt_enabled', 'mode'
        ]
        for key in required_keys:
            assert key in config, f"Missing key: {key}"
    
    def test_config_values(self):
        """Test configuration value types"""
        config = ConfigManager.load_config()
        assert isinstance(config['url'], str)
        assert isinstance(config['refresh_count'], int)
        assert isinstance(config['delay'], (int, float))
        assert isinstance(config['headless'], bool)
        assert isinstance(config['stealth'], bool)
        assert isinstance(config['vapt_enabled'], bool)
        assert isinstance(config['mode'], str)

class TestVAPTAnalyzer:
    """Test VAPT security analysis functionality"""
    
    def test_vapt_methods_exist(self):
        """Test that all VAPT methods are available"""
        methods = [
            'check_security_headers',
            'check_sensitive_files',
            'test_sql_injection',
            'test_xss',
            'test_xss_vulnerabilities',
            'check_cors_policy'
        ]
        
        for method in methods:
            assert hasattr(VAPTAnalyzer, method), f"Missing method: {method}"
            assert callable(getattr(VAPTAnalyzer, method))
    
    def test_check_security_headers(self):
        """Test security header checking (without network call)"""
        # Just verify the method exists and is callable
        assert callable(VAPTAnalyzer.check_security_headers)
    
    def test_check_cors_policy(self):
        """Test CORS policy checking method exists"""
        assert callable(VAPTAnalyzer.check_cors_policy)

class TestHackerEffects:
    """Test UI effects functionality"""
    
    def test_glitch_text(self):
        """Test glitch text effect"""
        original = "TEST MESSAGE"
        glitched = HackerEffects.glitch_text(original, intensity=0)
        assert glitched == original
        
        glitched = HackerEffects.glitch_text(original, intensity=10)
        assert len(glitched) == len(original)
    
    def test_matrix_rain_no_crash(self):
        """Test that matrix rain doesn't crash"""
        try:
            # Should not raise exception even if terminal not available
            HackerEffects.matrix_rain(duration=0)
        except Exception as e:
            pytest.fail(f"matrix_rain raised exception: {e}")

class TestSiteAnalyzer:
    """Test site analysis functionality"""
    
    def test_analyze_site_structure(self):
        """Test that analyze_site returns proper structure"""
        # We can't test with real driver in CI, but we can verify the method exists
        assert hasattr(SiteAnalyzer, 'analyze_site')
        assert callable(SiteAnalyzer.analyze_site)
    
    def test_display_analysis(self):
        """Test analysis display method"""
        assert hasattr(SiteAnalyzer, 'display_analysis')
        assert callable(SiteAnalyzer.display_analysis)
    
    def test_save_analysis(self):
        """Test analysis saving"""
        assert hasattr(SiteAnalyzer, 'save_analysis')
        assert callable(SiteAnalyzer.save_analysis)

class TestFileOperations:
    """Test file operations and permissions"""
    
    def test_directory_creation(self):
        """Test that required directories can be created"""
        test_dir = "test_temp_dir"
        os.makedirs(test_dir, exist_ok=True)
        assert os.path.exists(test_dir)
        os.rmdir(test_dir)
    
    def test_json_read_write(self):
        """Test JSON file operations"""
        test_file = "test_temp.json"
        test_data = {"test": "data", "value": 123}
        
        # Write
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        # Read
        with open(test_file, 'r') as f:
            loaded = json.load(f)
        
        assert loaded == test_data
        
        # Clean up
        os.remove(test_file)
    
    def test_required_directories(self):
        """Test that all required directories exist or can be created"""
        required_dirs = ['screenshots', 'history', 'reports', 'saved_urls']
        
        for directory in required_dirs:
            os.makedirs(directory, exist_ok=True)
            assert os.path.exists(directory)

class TestModuleImports:
    """Test that all modules can be imported"""
    
    def test_refresh_bot_import(self):
        """Test refresh_bot module import"""
        from refresh_bot import SystemAnalyzer, URLManager, HackerEffects
        assert SystemAnalyzer is not None
        assert URLManager is not None
        assert HackerEffects is not None
    
    def test_config_manager_import(self):
        """Test config_manager module import"""
        from config_manager import ConfigManager
        assert ConfigManager is not None
    
    def test_vapt_analyzer_import(self):
        """Test vapt_analyzer module import"""
        from vapt_analyzer import VAPTAnalyzer
        assert VAPTAnalyzer is not None
    
    def test_ui_components_import(self):
        """Test ui_components module import"""
        from ui_components import clear_screen, print_banner, loading_animation
        assert clear_screen is not None
        assert print_banner is not None
        assert loading_animation is not None

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
