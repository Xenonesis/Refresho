#!/usr/bin/env python3
"""
Webhook Notification System for REFRESHO v5.0+
Send notifications to Discord, Slack, Teams, or custom webhooks
"""

import requests
import json
from datetime import datetime
from typing import Dict, Optional

class WebhookNotifier:
    """Send notifications via webhooks"""
    
    @staticmethod
    def send_discord_notification(webhook_url: str, title: str, message: str, 
                                   color: int = 5814783, success: bool = True) -> bool:
        """Send notification to Discord webhook"""
        try:
            embed = {
                "title": title,
                "description": message,
                "color": color if success else 15548997,  # Green or Red
                "timestamp": datetime.utcnow().isoformat(),
                "footer": {
                    "text": "REFRESHO v5.0"
                }
            }
            
            data = {
                "embeds": [embed],
                "username": "REFRESHO Bot"
            }
            
            response = requests.post(webhook_url, json=data, timeout=10)
            return response.status_code == 204
            
        except Exception as e:
            print(f"\033[91m[WEBHOOK ERROR] Discord: {e}\033[0m")
            return False
    
    @staticmethod
    def send_slack_notification(webhook_url: str, title: str, message: str, 
                                success: bool = True) -> bool:
        """Send notification to Slack webhook"""
        try:
            data = {
                "text": f"*{title}*",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": title
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": message
                        }
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": f"✅ Success" if success else "❌ Failed"
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(webhook_url, json=data, timeout=10)
            return response.status_code == 200
            
        except Exception as e:
            print(f"\033[91m[WEBHOOK ERROR] Slack: {e}\033[0m")
            return False
    
    @staticmethod
    def send_teams_notification(webhook_url: str, title: str, message: str,
                                success: bool = True) -> bool:
        """Send notification to Microsoft Teams webhook"""
        try:
            data = {
                "@type": "MessageCard",
                "@context": "https://schema.org/extensions",
                "summary": title,
                "themeColor": "00FF00" if success else "FF0000",
                "title": title,
                "sections": [
                    {
                        "activityTitle": "REFRESHO v5.0",
                        "activitySubtitle": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "text": message
                    }
                ]
            }
            
            response = requests.post(webhook_url, json=data, timeout=10)
            return response.status_code == 200
            
        except Exception as e:
            print(f"\033[91m[WEBHOOK ERROR] Teams: {e}\033[0m")
            return False
    
    @staticmethod
    def send_custom_webhook(webhook_url: str, data: Dict, 
                           method: str = 'POST') -> bool:
        """Send custom webhook notification"""
        try:
            if method == 'POST':
                response = requests.post(webhook_url, json=data, timeout=10)
            elif method == 'PUT':
                response = requests.put(webhook_url, json=data, timeout=10)
            else:
                return False
            
            return response.status_code in [200, 201, 204]
            
        except Exception as e:
            print(f"\033[91m[WEBHOOK ERROR] Custom: {e}\033[0m")
            return False
    
    @staticmethod
    def send_mission_complete(webhook_url: str, webhook_type: str,
                              mission_data: Dict) -> bool:
        """Send mission completion notification"""
        title = "✅ Mission Complete"
        message = (
            f"**Target:** {mission_data.get('url', 'N/A')}\n"
            f"**Refreshes:** {mission_data.get('refresh_count', 0)}\n"
            f"**Duration:** {mission_data.get('execution_time', 0):.2f}s\n"
            f"**Rate:** {mission_data.get('rate', 0):.2f} req/s\n"
            f"**Status:** {mission_data.get('status', 'UNKNOWN')}"
        )
        
        if webhook_type.lower() == 'discord':
            return WebhookNotifier.send_discord_notification(
                webhook_url, title, message, success=True
            )
        elif webhook_type.lower() == 'slack':
            return WebhookNotifier.send_slack_notification(
                webhook_url, title, message, success=True
            )
        elif webhook_type.lower() == 'teams':
            return WebhookNotifier.send_teams_notification(
                webhook_url, title, message, success=True
            )
        else:
            return WebhookNotifier.send_custom_webhook(
                webhook_url, mission_data
            )

class ReportExporter:
    """Export reports in various formats"""
    
    @staticmethod
    def export_json(data: Dict, filename: str) -> bool:
        """Export report as JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"\033[91m[EXPORT ERROR] JSON: {e}\033[0m")
            return False
    
    @staticmethod
    def export_csv(data: Dict, filename: str) -> bool:
        """Export report as CSV"""
        try:
            import csv
            
            # Flatten the data for CSV
            rows = []
            if isinstance(data, dict):
                rows.append(data)
            elif isinstance(data, list):
                rows = data
            
            if not rows:
                return False
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            
            return True
        except Exception as e:
            print(f"\033[91m[EXPORT ERROR] CSV: {e}\033[0m")
            return False
    
    @staticmethod
    def export_html(data: Dict, filename: str, title: str = "REFRESHO Report") -> bool:
        """Export report as HTML"""
        try:
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: #0d1117;
            color: #c9d1d9;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: #161b22;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(0,255,0,0.1);
        }}
        h1 {{
            color: #58a6ff;
            text-align: center;
            border-bottom: 2px solid #30363d;
            padding-bottom: 10px;
        }}
        .metric {{
            background: #0d1117;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #238636;
            border-radius: 4px;
        }}
        .metric-label {{
            color: #8b949e;
            font-size: 12px;
            text-transform: uppercase;
        }}
        .metric-value {{
            color: #58a6ff;
            font-size: 24px;
            font-weight: bold;
        }}
        .success {{
            color: #3fb950;
        }}
        .error {{
            color: #f85149;
        }}
        pre {{
            background: #0d1117;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 {title}</h1>
        <div class="metric">
            <div class="metric-label">Report Generated</div>
            <div class="metric-value">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        <pre>{json.dumps(data, indent=2)}</pre>
    </div>
</body>
</html>
"""
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return True
        except Exception as e:
            print(f"\033[91m[EXPORT ERROR] HTML: {e}\033[0m")
            return False
    
    @staticmethod
    def export_markdown(data: Dict, filename: str, title: str = "REFRESHO Report") -> bool:
        """Export report as Markdown"""
        try:
            md_content = f"""# {title}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Summary

"""
            # Add key-value pairs
            for key, value in data.items():
                if isinstance(value, dict):
                    md_content += f"\n### {key}\n\n"
                    for k, v in value.items():
                        md_content += f"- **{k}:** {v}\n"
                else:
                    md_content += f"- **{key}:** {value}\n"
            
            md_content += "\n---\n\n*Generated by REFRESHO v5.0*\n"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            return True
        except Exception as e:
            print(f"\033[91m[EXPORT ERROR] Markdown: {e}\033[0m")
            return False

if __name__ == "__main__":
    print("Webhook Notifier Module - REFRESHO v5.0+")
