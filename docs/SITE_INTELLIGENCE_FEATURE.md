# �� REFRESHO v4.0 - Site Intelligence & VAPT Feature

## �� Enhanced Features: Comprehensive Site Analysis & Security Assessment

Your REFRESHO v4.0 now includes a powerful **Site Intelligence System** and integrated **VAPT (Vulnerability Assessment & Penetration Testing)** capabilities to provide detailed reconnaissance and security reports for every target website.

## �� What It Does

### �� **Comprehensive Analysis**
When REFRESHO visits any site, it automatically:
- ✅ Analyzes page performance (load time, size)
- ✅ Counts all page elements (links, images, forms, scripts)
- ✅ Detects technologies (jQuery, React, Vue.js, Bootstrap, etc.)
- ✅ Evaluates security (HTTPS, cookies, headers)
- ✅ Extracts SEO data (title, description, keywords)
- ✅ **Performs VAPT checks** (Security Headers, Sensitive Files, Basic Port Scan)
- ✅ Displays real-time intelligence in terminal
- ✅ Saves detailed JSON reports to `history/` folder, **including VAPT results**

### ���️ **Terminal Display Example**
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

+==============================================================+
|                      VAPT ANALYSIS REPORT                    |
+==============================================================+

[SECURITY HEADERS]
  • Strict-Transport-Security: max-age=31536000
  • Content-Security-Policy: default-src 'self'
  • X-Frame-Options: DENY

[SENSITIVE FILES/DIRECTORIES]
  No common sensitive files/directories found.

[OPEN PORTS (BASIC SCAN)]
  • Port 80 is OPEN
  • Port 443 is OPEN

+==============================================================+
```

### �� **Automatic History Saving**
Each analysis is saved as a JSON file in the `history/` folder:
- **Filename Format**: `domain_YYYYMMDD_HHMMSS.json`
- **Example**: `www_google_com_20250621_043000.json`
- **Content**: Complete analysis data in structured JSON format, **now including a `vapt_results` section**.

## ���️ How to Use

### 1. **Enable During Configuration**
When running REFRESHO, you'll be prompted to enable Site Intelligence and VAPT:
```
[ADVANCED] Configure advanced features:
[>] Enable site intelligence analysis? (Y/n): 
...
[SECURITY] Enable VAPT (Vulnerability Assessment) mode?
[1] Yes - Include security analysis
[2] No - Standard refresh only
[>] Enable VAPT? (1-2): 
```
- Press ENTER or 'Y' for Site Intelligence (default: enabled)
- Select '1' for VAPT (default: disabled)

### 2. **View Analysis Reports**
Use the included history viewer:
```bash
python src/view_history.py
```
This viewer has been updated to display the VAPT results alongside the site intelligence data.

### 3. **Access Raw Data**
JSON files in `history/` folder contain complete analysis data for integration with other tools.

## �� Analysis Data Structure

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
  },
  "vapt_results": {  # New section
    "security_headers": {
      "Strict-Transport-Security": "max-age=31536000",
      "Content-Security-Policy": "default-src 'self'"
    },
    "sensitive_files": [],
    "open_ports": [80, 443]
  }
}
```

## �� Use Cases

### �� **Reconnaissance**
- Analyze target websites before testing
- Identify technologies and frameworks
- Assess security posture

### �� **Monitoring**
- Track website changes over time
- Monitor performance metrics
- Detect technology updates

### �� **Research**
- Gather intelligence on web technologies
- Analyze site structures
- Study security implementations

### ���️ **Security Assessment**
- Check HTTPS implementation
- Analyze cookie configurations
- Identify potential vulnerabilities
- **Perform basic vulnerability checks**

## �� Benefits

- **�� Zero Configuration** - Works automatically
- **�� Real-time Display** - See results immediately
- **�� Persistent Storage** - All data saved for later analysis
- **�� Historical Tracking** - Compare changes over time
- **�� Integration Ready** - Standard JSON format
- **�� Fast Analysis** - Minimal impact on refresh performance
- **���️ Integrated Security** - VAPT results included in reports

## �� Quick Test

Run the comprehensive test suite:
```bash
python -m unittest test_refresh_bot.py -v
```

View saved reports:
```bash
python src/view_history.py
```

---

**🔥 Your REFRESHO v4.0 is now a complete web intelligence and security assessment platform!**

*Feature developed by Amazon Q Developer & Roo (Claude Sonnet 4)*
*Original tool by Addy@Xenonesis*