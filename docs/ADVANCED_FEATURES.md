# 🚀 Advanced Features - REFRESHO v5.0+

## Table of Contents
- [Performance Monitoring](#performance-monitoring)
- [API Testing](#api-testing)
- [Load Testing](#load-testing)
- [Webhook Notifications](#webhook-notifications)
- [Report Export](#report-export)
- [Plugin System](#plugin-system)
- [Scheduled Testing](#scheduled-testing)

---

## Performance Monitoring

Track and analyze performance metrics for your web testing missions.

### Features
- Load time tracking
- Response time analysis
- Refresh time monitoring
- Statistical analysis (min, max, mean, median, std dev)
- Error tracking

### Usage

```python
from advanced_features import PerformanceMonitor

# Initialize monitor
monitor = PerformanceMonitor()

# Record metrics
monitor.record_load_time(2.34)
monitor.record_response_time(0.45)
monitor.record_refresh_time(0.89)

# Get statistics
stats = monitor.get_statistics()
print(stats)

# Print formatted report
monitor.print_report()
```

### Example Output
```
[LOAD TIMES]
  Count:   10
  Min:     1.234s
  Max:     3.456s
  Mean:    2.145s
  Median:  2.100s
  Std Dev: 0.543s
```

---

## API Testing

Test REST API endpoints with comprehensive reporting.

### Features
- Support for GET, POST, PUT, DELETE methods
- Custom headers and data
- Response time measurement
- Status code checking
- Multiple endpoint testing
- Success rate calculation

### Usage

```python
from advanced_features import APITester

# Test single endpoint
result = APITester.test_endpoint(
    url='https://api.example.com/users',
    method='GET',
    headers={'Authorization': 'Bearer token123'}
)

# Test multiple endpoints
endpoints = [
    {'url': 'https://api.example.com/users', 'method': 'GET'},
    {'url': 'https://api.example.com/posts', 'method': 'GET'},
    {'url': 'https://api.example.com/login', 'method': 'POST', 
     'data': {'username': 'test', 'password': 'test123'}}
]

results = APITester.test_multiple_endpoints(endpoints)

# Generate report
report = APITester.generate_report(results)
print(f"Success Rate: {report['success_rate']}%")
```

---

## Load Testing

Perform load testing to measure website performance under stress.

### Features
- Configurable number of requests
- Concurrent or sequential execution
- Response time tracking
- Success rate calculation
- Requests per second measurement

### Usage

```python
from advanced_features import LoadTester

# Run load test
report = LoadTester.run_load_test(
    url='https://example.com',
    num_requests=100,
    delay=0.5
)

# Print report
LoadTester.print_load_test_report(report)
```

### Example Output
```
[LOAD TEST REPORT]
[TARGET] https://example.com
[REQUESTS] Total: 100 | Success: 98 | Failed: 2
[SUCCESS RATE] 98.0%
[TOTAL TIME] 52.34s
[REQUESTS/SEC] 1.91

[RESPONSE TIMES]
  Average: 0.523s
  Min:     0.234s
  Max:     1.456s
```

---

## Webhook Notifications

Send notifications to Discord, Slack, Teams, or custom webhooks.

### Supported Platforms
- ✅ Discord
- ✅ Slack
- ✅ Microsoft Teams
- ✅ Custom Webhooks

### Usage

```python
from webhook_notifier import WebhookNotifier

# Discord notification
WebhookNotifier.send_discord_notification(
    webhook_url='https://discord.com/api/webhooks/...',
    title='Mission Complete',
    message='Successfully completed 1000 refreshes!',
    success=True
)

# Slack notification
WebhookNotifier.send_slack_notification(
    webhook_url='https://hooks.slack.com/services/...',
    title='Mission Complete',
    message='Target: example.com\nRefreshes: 1000',
    success=True
)

# Mission completion notification
mission_data = {
    'url': 'https://example.com',
    'refresh_count': 1000,
    'execution_time': 125.5,
    'rate': 7.97,
    'status': 'SUCCESS'
}

WebhookNotifier.send_mission_complete(
    webhook_url='your_webhook_url',
    webhook_type='discord',
    mission_data=mission_data
)
```

---

## Report Export

Export reports in multiple formats for analysis and sharing.

### Supported Formats
- ✅ JSON
- ✅ CSV
- ✅ HTML
- ✅ Markdown

### Usage

```python
from webhook_notifier import ReportExporter

report_data = {
    'mission_id': 'MSN-12345',
    'timestamp': '2025-12-11 23:00:00',
    'url': 'https://example.com',
    'refreshes': 1000,
    'status': 'SUCCESS'
}

# Export as JSON
ReportExporter.export_json(report_data, 'reports/mission.json')

# Export as HTML
ReportExporter.export_html(report_data, 'reports/mission.html', 
                          title='Mission Report')

# Export as Markdown
ReportExporter.export_markdown(report_data, 'reports/mission.md')

# Export as CSV
ReportExporter.export_csv([report_data], 'reports/mission.csv')
```

---

## Plugin System

Extend REFRESHO functionality with custom plugins.

### Creating a Plugin

```python
from plugin_system import Plugin

class MyCustomPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = "MyCustomPlugin"
        self.version = "1.0.0"
        self.author = "Your Name"
        self.description = "Does something awesome"
    
    def on_init(self):
        print("Plugin initialized!")
    
    def on_mission_start(self, config):
        print(f"Mission starting: {config['url']}")
    
    def on_refresh(self, refresh_num, total):
        print(f"Refresh {refresh_num}/{total}")
    
    def on_mission_complete(self, results):
        print(f"Mission complete: {results['status']}")
    
    def on_error(self, error):
        print(f"Error occurred: {error}")
    
    def on_shutdown(self):
        print("Plugin shutting down")
```

### Using Plugins

```python
from plugin_system import PluginManager

# Initialize plugin manager
manager = PluginManager(plugin_dir='plugins')

# Load all plugins
manager.load_all_plugins()

# Load specific plugin
manager.load_plugin('plugins/my_plugin.py')

# List loaded plugins
manager.list_plugins()

# Trigger hooks
manager.trigger_hook('on_mission_start', config={'url': 'https://example.com'})
manager.trigger_hook('on_refresh', 1, 10)
manager.trigger_hook('on_mission_complete', {'status': 'SUCCESS'})

# Unload plugin
manager.unload_plugin('MyCustomPlugin')
```

### Built-in Plugins

#### Logger Plugin
Logs all events to file.

```python
from plugin_system import LoggerPlugin

# Events logged:
# - Plugin initialization
# - Mission start
# - Each refresh
# - Mission completion
# - Errors
# - Plugin shutdown
```

#### Statistics Plugin
Tracks mission statistics.

```python
from plugin_system import StatisticsPlugin

# Tracks:
# - Total missions
# - Total refreshes
# - Total errors
```

---

## Scheduled Testing

Run tests on a schedule for continuous monitoring.

### Usage

```python
from advanced_features import ScheduledTester

# Initialize scheduler
scheduler = ScheduledTester()

# Add scheduled tests
scheduler.add_test(
    url='https://example.com',
    interval=300,  # 5 minutes
    max_runs=100
)

scheduler.add_test(
    url='https://api.example.com/health',
    interval=60,  # 1 minute
    max_runs=None  # Unlimited
)

# Run scheduled tests
scheduler.run_scheduled_tests()
```

---

## Configuration File

Use `config.json` for persistent configuration.

### Example Configuration

```json
{
  "webhooks": {
    "enabled": true,
    "notify_on_complete": true,
    "discord_webhook": "https://discord.com/api/webhooks/..."
  },
  "performance": {
    "enable_monitoring": true,
    "track_load_times": true,
    "generate_performance_report": true
  },
  "plugins": {
    "enabled": true,
    "plugin_directory": "plugins",
    "enabled_plugins": ["Logger", "Statistics"]
  }
}
```

---

## Integration Example

Combine multiple features for comprehensive testing:

```python
from advanced_features import PerformanceMonitor, LoadTester
from webhook_notifier import WebhookNotifier, ReportExporter
from plugin_system import PluginManager

# Initialize components
monitor = PerformanceMonitor()
plugin_manager = PluginManager()
plugin_manager.load_all_plugins()

# Run load test
report = LoadTester.run_load_test('https://example.com', 100)

# Export report
ReportExporter.export_html(report, 'reports/load_test.html')
ReportExporter.export_json(report, 'reports/load_test.json')

# Send notification
WebhookNotifier.send_discord_notification(
    webhook_url='your_webhook',
    title='Load Test Complete',
    message=f"Success Rate: {report['success_rate']}%",
    success=True
)

# Print performance report
monitor.print_report()
```

---

## Best Practices

1. **Use Performance Monitoring** for all production missions
2. **Set up Webhooks** for real-time notifications
3. **Export Reports** in multiple formats for analysis
4. **Create Custom Plugins** for specific needs
5. **Schedule Regular Tests** for continuous monitoring
6. **Combine Features** for comprehensive testing workflows

---

## API Reference

For detailed API documentation, see:
- [Performance Monitoring API](../src/advanced_features.py)
- [Webhook Notifier API](../src/webhook_notifier.py)
- [Plugin System API](../src/plugin_system.py)

---

**Version:** 5.0+  
**Last Updated:** December 2025  
**Status:** ✅ Stable
