#!/usr/bin/env python3
"""
Plugin System for REFRESHO v5.0+
Extensible architecture for custom functionality
"""

import os
import sys
import importlib.util
from typing import Dict, List, Callable, Optional
from datetime import datetime

class Plugin:
    """Base class for REFRESHO plugins"""
    
    def __init__(self):
        self.name = "BasePlugin"
        self.version = "1.0.0"
        self.author = "Unknown"
        self.description = "Base plugin class"
        self.enabled = True
    
    def on_init(self):
        """Called when plugin is loaded"""
        pass
    
    def on_mission_start(self, config: Dict):
        """Called when mission starts"""
        pass
    
    def on_refresh(self, refresh_num: int, total: int):
        """Called on each refresh"""
        pass
    
    def on_mission_complete(self, results: Dict):
        """Called when mission completes"""
        pass
    
    def on_error(self, error: Exception):
        """Called when error occurs"""
        pass
    
    def on_shutdown(self):
        """Called when plugin is unloaded"""
        pass

class PluginManager:
    """Manage REFRESHO plugins"""
    
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, Plugin] = {}
        self.hooks: Dict[str, List[Callable]] = {
            'on_init': [],
            'on_mission_start': [],
            'on_refresh': [],
            'on_mission_complete': [],
            'on_error': [],
            'on_shutdown': []
        }
        
        # Create plugin directory if it doesn't exist
        os.makedirs(plugin_dir, exist_ok=True)
    
    def load_plugin(self, plugin_path: str) -> bool:
        """Load a plugin from file"""
        try:
            # Import the plugin module
            spec = importlib.util.spec_from_file_location("plugin", plugin_path)
            if spec is None or spec.loader is None:
                return False
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find plugin class
            plugin_class = None
            for item in dir(module):
                obj = getattr(module, item)
                if isinstance(obj, type) and issubclass(obj, Plugin) and obj != Plugin:
                    plugin_class = obj
                    break
            
            if plugin_class is None:
                print(f"\033[91m[PLUGIN] No plugin class found in {plugin_path}\033[0m")
                return False
            
            # Instantiate plugin
            plugin = plugin_class()
            self.plugins[plugin.name] = plugin
            
            # Register hooks
            for hook_name in self.hooks.keys():
                method = getattr(plugin, hook_name, None)
                if method and callable(method):
                    self.hooks[hook_name].append(method)
            
            # Call init
            plugin.on_init()
            
            print(f"\033[92m[PLUGIN] Loaded: {plugin.name} v{plugin.version}\033[0m")
            return True
            
        except Exception as e:
            print(f"\033[91m[PLUGIN ERROR] Failed to load {plugin_path}: {e}\033[0m")
            return False
    
    def load_all_plugins(self):
        """Load all plugins from plugin directory"""
        print(f"\033[96m[PLUGIN] Loading plugins from {self.plugin_dir}/\033[0m")
        
        if not os.path.exists(self.plugin_dir):
            print(f"\033[93m[PLUGIN] Plugin directory not found\033[0m")
            return
        
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                plugin_path = os.path.join(self.plugin_dir, filename)
                self.load_plugin(plugin_path)
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin"""
        if plugin_name not in self.plugins:
            return False
        
        plugin = self.plugins[plugin_name]
        plugin.on_shutdown()
        
        # Remove hooks
        for hook_list in self.hooks.values():
            hook_list[:] = [h for h in hook_list if not hasattr(h, '__self__') or h.__self__ != plugin]
        
        del self.plugins[plugin_name]
        print(f"\033[93m[PLUGIN] Unloaded: {plugin_name}\033[0m")
        return True
    
    def trigger_hook(self, hook_name: str, *args, **kwargs):
        """Trigger a hook for all plugins"""
        if hook_name not in self.hooks:
            return
        
        for hook in self.hooks[hook_name]:
            try:
                hook(*args, **kwargs)
            except Exception as e:
                print(f"\033[91m[PLUGIN ERROR] Hook {hook_name}: {e}\033[0m")
    
    def list_plugins(self):
        """List all loaded plugins"""
        print("\033[96m[PLUGIN] Loaded Plugins:\033[0m")
        if not self.plugins:
            print("\033[93m  No plugins loaded\033[0m")
            return
        
        for name, plugin in self.plugins.items():
            status = "✅" if plugin.enabled else "❌"
            print(f"  {status} {name} v{plugin.version} - {plugin.description}")

# Example plugins

class LoggerPlugin(Plugin):
    """Example plugin that logs all events"""
    
    def __init__(self):
        super().__init__()
        self.name = "Logger"
        self.version = "1.0.0"
        self.author = "REFRESHO Team"
        self.description = "Logs all mission events to file"
        self.log_file = "logs/plugin_events.log"
        
        os.makedirs("logs", exist_ok=True)
    
    def _log(self, message: str):
        """Write to log file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")
    
    def on_init(self):
        self._log("Logger plugin initialized")
    
    def on_mission_start(self, config: Dict):
        self._log(f"Mission started: {config.get('url', 'N/A')}")
    
    def on_refresh(self, refresh_num: int, total: int):
        self._log(f"Refresh {refresh_num}/{total}")
    
    def on_mission_complete(self, results: Dict):
        self._log(f"Mission complete: {results.get('status', 'UNKNOWN')}")
    
    def on_error(self, error: Exception):
        self._log(f"Error occurred: {error}")
    
    def on_shutdown(self):
        self._log("Logger plugin shutdown")

class StatisticsPlugin(Plugin):
    """Example plugin that tracks statistics"""
    
    def __init__(self):
        super().__init__()
        self.name = "Statistics"
        self.version = "1.0.0"
        self.author = "REFRESHO Team"
        self.description = "Track mission statistics"
        self.stats = {
            'total_missions': 0,
            'total_refreshes': 0,
            'total_errors': 0
        }
    
    def on_mission_start(self, config: Dict):
        self.stats['total_missions'] += 1
    
    def on_refresh(self, refresh_num: int, total: int):
        self.stats['total_refreshes'] += 1
    
    def on_error(self, error: Exception):
        self.stats['total_errors'] += 1
    
    def on_mission_complete(self, results: Dict):
        print(f"\033[96m[STATS] Missions: {self.stats['total_missions']} | "
              f"Refreshes: {self.stats['total_refreshes']} | "
              f"Errors: {self.stats['total_errors']}\033[0m")

if __name__ == "__main__":
    print("Plugin System Module - REFRESHO v5.0+")
