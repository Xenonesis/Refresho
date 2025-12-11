# 🔌 Plugin Development Guide - REFRESHO v5.0+

## Introduction

The REFRESHO plugin system allows you to extend functionality with custom code. Plugins can hook into various events during mission execution.

---

## Plugin Architecture

### Plugin Lifecycle

```
Plugin Loading
    ↓
on_init()
    ↓
on_mission_start()
    ↓
on_refresh() (repeated)
    ↓
on_mission_complete() / on_error()
    ↓
on_shutdown()
```

### Available Hooks

| Hook | When Called | Parameters |
|------|-------------|------------|
| `on_init()` | Plugin is loaded | None |
| `on_mission_start(config)` | Mission starts | `config: Dict` |
| `on_refresh(num, total)` | Each refresh | `num: int, total: int` |
| `on_mission_complete(results)` | Mission completes | `results: Dict` |
| `on_error(error)` | Error occurs | `error: Exception` |
| `on_shutdown()` | Plugin is unloaded | None |

---

## Creating Your First Plugin

### Step 1: Create Plugin File

Create a new Python file in the `plugins/` directory:

```python
# plugins/hello_world.py

from plugin_system import Plugin

class HelloWorldPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = "HelloWorld"
        self.version = "1.0.0"
        self.author = "Your Name"
        self.description = "A simple hello world plugin"
    
    def on_init(self):
        print("🎉 Hello World plugin initialized!")
    
    def on_mission_start(self, config):
        print(f"🚀 Mission starting for: {config['url']}")
    
    def on_mission_complete(self, results):
        print(f"✅ Mission complete! Status: {results['status']}")
```

### Step 2: Load the Plugin

```python
from plugin_system import PluginManager

manager = PluginManager()
manager.load_plugin('plugins/hello_world.py')
```

---

## Advanced Plugin Examples

### 1. Notification Plugin

Send notifications via email, SMS, or other services:

```python
from plugin_system import Plugin
import smtplib
from email.mime.text import MIMEText

class EmailNotificationPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = "EmailNotifier"
        self.version = "1.0.0"
        self.description = "Send email notifications"
        
        # Configuration
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "your-email@gmail.com"
        self.sender_password = "your-app-password"
        self.recipient_email = "recipient@example.com"
    
    def send_email(self, subject, body):
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
                
            print("📧 Email sent successfully")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
    
    def on_mission_complete(self, results):
        subject = f"REFRESHO Mission Complete - {results['status']}"
        body = f"""
Mission Completed

URL: {results.get('url', 'N/A')}
Refreshes: {results.get('refresh_count', 0)}
Duration: {results.get('execution_time', 0):.2f}s
Status: {results['status']}
"""
        self.send_email(subject, body)
    
    def on_error(self, error):
        subject = "REFRESHO Mission Error"
        body = f"An error occurred during mission execution:\n\n{error}"
        self.send_email(subject, body)
```

### 2. Database Logger Plugin

Log mission data to a database:

```python
from plugin_system import Plugin
import sqlite3
from datetime import datetime

class DatabaseLoggerPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = "DatabaseLogger"
        self.version = "1.0.0"
        self.description = "Log missions to SQLite database"
        self.db_path = "logs/missions.db"
        
        self._init_database()
    
    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS missions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                url TEXT,
                refresh_count INTEGER,
                execution_time REAL,
                status TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def on_mission_complete(self, results):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO missions (timestamp, url, refresh_count, execution_time, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            results.get('url', 'N/A'),
            results.get('refresh_count', 0),
            results.get('execution_time', 0),
            results['status']
        ))
        
        conn.commit()
        conn.close()
        print("💾 Mission logged to database")
```

### 3. Screenshot Manager Plugin

Automatically organize and manage screenshots:

```python
from plugin_system import Plugin
import os
import shutil
from datetime import datetime

class ScreenshotManagerPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = "ScreenshotManager"
        self.version = "1.0.0"
        self.description = "Organize screenshots by date and mission"
        self.base_dir = "screenshots"
    
    def on_mission_complete(self, results):
        # Create organized directory structure
        date_str = datetime.now().strftime("%Y-%m-%d")
        mission_id = results.get('mission_id', 'unknown')
        
        target_dir = os.path.join(self.base_dir, date_str, mission_id)
        os.makedirs(target_dir, exist_ok=True)
        
        # Move screenshots to organized location
        for file in os.listdir(self.base_dir):
            if file.endswith('.png') and file.startswith('screenshot_'):
                src = os.path.join(self.base_dir, file)
                dst = os.path.join(target_dir, file)
                shutil.move(src, dst)
        
        print(f"📁 Screenshots organized in {target_dir}")
```

### 4. Performance Tracker Plugin

Track and analyze performance trends:

```python
from plugin_system import Plugin
import json
import statistics
from datetime import datetime

class PerformanceTrackerPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = "PerformanceTracker"
        self.version = "1.0.0"
        self.description = "Track performance trends over time"
        self.history_file = "logs/performance_history.json"
        self.history = self._load_history()
    
    def _load_history(self):
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def _save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def on_mission_complete(self, results):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'url': results.get('url', 'N/A'),
            'execution_time': results.get('execution_time', 0),
            'refresh_count': results.get('refresh_count', 0),
            'rate': results.get('rate', 0)
        }
        
        self.history.append(entry)
        self._save_history()
        
        # Analyze trends
        if len(self.history) >= 5:
            recent_times = [h['execution_time'] for h in self.history[-10:]]
            avg_time = statistics.mean(recent_times)
            
            print(f"📊 Performance Trend: Avg execution time (last 10): {avg_time:.2f}s")
```

---

## Plugin Best Practices

### 1. Error Handling

Always wrap your plugin code in try-except blocks:

```python
def on_mission_complete(self, results):
    try:
        # Your code here
        pass
    except Exception as e:
        print(f"[{self.name}] Error: {e}")
```

### 2. Configuration

Use external configuration files:

```python
def __init__(self):
    super().__init__()
    self.config = self._load_config()

def _load_config(self):
    try:
        with open('plugins/my_plugin_config.json', 'r') as f:
            return json.load(f)
    except:
        return {}  # Default config
```

### 3. Resource Cleanup

Clean up resources in `on_shutdown()`:

```python
def on_shutdown(self):
    # Close database connections
    if hasattr(self, 'db_conn'):
        self.db_conn.close()
    
    # Save any pending data
    self._save_state()
```

### 4. Performance

Don't block mission execution:

```python
import threading

def on_refresh(self, num, total):
    # Run expensive operations in background
    thread = threading.Thread(target=self._process_data, args=(num,))
    thread.daemon = True
    thread.start()
```

---

## Plugin API Reference

### Plugin Base Class

```python
class Plugin:
    name: str              # Plugin name
    version: str           # Plugin version
    author: str           # Plugin author
    description: str      # Plugin description
    enabled: bool         # Is plugin enabled
```

### Hook Methods

```python
def on_init():
    """Called when plugin is loaded"""

def on_mission_start(config: Dict):
    """Called when mission starts
    
    Args:
        config: Mission configuration dictionary
    """

def on_refresh(refresh_num: int, total: int):
    """Called on each refresh
    
    Args:
        refresh_num: Current refresh number
        total: Total number of refreshes
    """

def on_mission_complete(results: Dict):
    """Called when mission completes successfully
    
    Args:
        results: Mission results dictionary
    """

def on_error(error: Exception):
    """Called when an error occurs
    
    Args:
        error: The exception that occurred
    """

def on_shutdown():
    """Called when plugin is unloaded"""
```

---

## Testing Your Plugin

Create a test script:

```python
# test_my_plugin.py

from plugin_system import PluginManager

# Initialize
manager = PluginManager()
manager.load_plugin('plugins/my_plugin.py')

# Simulate mission lifecycle
config = {'url': 'https://example.com', 'refresh_count': 10}
manager.trigger_hook('on_mission_start', config)

for i in range(1, 11):
    manager.trigger_hook('on_refresh', i, 10)

results = {
    'url': 'https://example.com',
    'refresh_count': 10,
    'execution_time': 5.23,
    'status': 'SUCCESS'
}
manager.trigger_hook('on_mission_complete', results)

manager.trigger_hook('on_shutdown')
```

---

## Distribution

### Package Your Plugin

Create a plugin package:

```
my_plugin/
├── __init__.py
├── my_plugin.py
├── config.json
├── README.md
└── requirements.txt
```

### Share Your Plugin

1. Upload to GitHub
2. Create a release
3. Share with the community

---

## Community Plugins

Check the [Plugin Repository](https://github.com/Xenonesis/Refresho-Plugins) for community-created plugins.

---

**Happy Plugin Development! 🚀**
