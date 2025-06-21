# 🔍 REFRESHO v2.0 - Site Intelligence Feature

## 🎯 New Feature Added: Comprehensive Site Analysis

Your REFRESHO v3.0 now includes a powerful **Site Intelligence System** that analyzes every target website and provides detailed reconnaissance reports.

## 🚀 What It Does

### 📊 **Comprehensive Analysis**
When REFRESHO visits any site, it automatically:
- ✅ Analyzes page performance (load time, size)
- ✅ Counts all page elements (links, images, forms, scripts)
- ✅ Detects technologies (jQuery, React, Vue.js, Bootstrap, etc.)
- ✅ Evaluates security (HTTPS, cookies, headers)
- ✅ Extracts SEO data (title, description, keywords)
- ✅ Displays real-time intelligence in terminal
- ✅ Saves detailed JSON reports to `history/` folder

### 🖥️ **Terminal Display Example**
```
+==============================================================+
|                    SITE INTELLIGENCE REPORT                 |
+==============================================================+
[TARGET] https://www.google.com
[TITLE] Google
[DOMAIN] www.google.com
[TIMESTAMP] 2025-06-21 04:30:00

[PERFORMANCE METRICS]
  Load Time: 0.11s
  Page Size: 194,915 bytes
  Security: HTTPS

[CONTENT ANALYSIS]
  Links: 26
  Images: 10
  Forms: 1
  Scripts: 12
  Stylesheets: 2
  Cookies: 2

[TECHNOLOGIES DETECTED]
  • Vue.js
```

### 📁 **Automatic History Saving**
Each analysis is saved as a JSON file in the `history/` folder:
- **Filename Format**: `domain_YYYYMMDD_HHMMSS.json`
- **Example**: `www_google_com_20250621_043000.json`
- **Content**: Complete analysis data in structured JSON format

## 🛠️ How to Use

### 1. **Enable During Configuration**
When running REFRESHO, you'll see:
```
[ADVANCED] Enable advanced features?
[>] Enable site intelligence analysis? (Y/n):
```
- Press ENTER or 'Y' to enable (default: enabled)
- Type 'n' to disable

### 2. **View Analysis Reports**
Use the included history viewer:
```bash
python view_history.py
```

### 3. **Access Raw Data**
JSON files in `history/` folder contain complete analysis data for integration with other tools.

## 📋 Analysis Data Structure

Each report contains:
```json
{
  "timestamp": "2025-06-21 04:30:00",
  "url": "https://example.com",
  "domain": "example.com",
  "title": "Page Title",
  "description": "Meta description",
  "keywords": "meta keywords",
  "load_time": 0.85,
  "page_size": 194915,
  "technologies": ["jQuery", "Bootstrap"],
  "links": {"total": 26},
  "images": 10,
  "forms": 1,
  "scripts": 12,
  "stylesheets": 2,
  "cookies": [{"name": "session", "domain": ".example.com"}],
  "security": {
    "https": true,
    "has_forms": true,
    "cookie_count": 2
  }
}
```

## 🎯 Use Cases

### 🔍 **Reconnaissance**
- Analyze target websites before testing
- Identify technologies and frameworks
- Assess security posture

### 📊 **Monitoring**
- Track website changes over time
- Monitor performance metrics
- Detect technology updates

### 🔬 **Research**
- Gather intelligence on web technologies
- Analyze site structures
- Study security implementations

### 🛡️ **Security Assessment**
- Check HTTPS implementation
- Analyze cookie configurations
- Identify potential vulnerabilities

## 🎉 Benefits

- **🚀 Zero Configuration** - Works automatically
- **📱 Real-time Display** - See results immediately
- **💾 Persistent Storage** - All data saved for later analysis
- **🔄 Historical Tracking** - Compare changes over time
- **🔧 Integration Ready** - Standard JSON format
- **⚡ Fast Analysis** - Minimal impact on refresh performance

## 🎮 Quick Test

Test the feature:
```bash
python test_site_analysis.py
```

View saved reports:
```bash
python view_history.py
```

---

**🔥 Your REFRESHO v3.0 is now a complete web intelligence platform!**

*Feature developed by Amazon Q Developer*  
*Original tool by Addy@Xenonesis*