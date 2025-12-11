# 🔥 REFRESHO v5.0 - ULTIMATE WEB REFRESHER & VAPT TOOLKIT

```
██████╗ ███████╗███████╗██████╗ ███████╗███████╗██╗  ██╗ ██████╗
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██║  ██║██╔═══██╗
██████╔╝█████╗  █████╗  ██████╔╝█████╗  ███████╗███████║██║   ██║
██╔══██╗██╔══╝  ██╔══╝  ██╔══██╗██╔══╝  ╚════██║██╔══██║██║   ██║
██║  ██║███████╗██║     ██║  ██║███████╗███████║██║  ██║╚██████╔╝
╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝
```

**🎯 The Most Advanced Web Refresher & Cybersecurity Assessment Tool v5.0**  
**💀 Developed by Addy@Xenonesis**

---

## 🚀 ENHANCED FEATURES v5.0

### 🔥 **CORE CAPABILITIES**
- **Matrix Rain Animation** - Real-time falling code effect
- **Intelligent Refresh Modes** - Stealth, Assault, and Nuclear modes
- **Advanced Browser Control** - Ghost, Phantom, and Visible configurations
- **Site Intelligence System** - Comprehensive target reconnaissance
- **URL Management** - Dynamic URL storage and organization
- **Performance Analytics** - Real-time metrics and reporting

### 🛡️ **COMPREHENSIVE VAPT TOOLKIT** ⭐ NEW ⭐
- **SQL Injection Testing** - 8 different payload patterns
- **XSS Vulnerability Testing** - Reflected XSS detection
- **Directory Traversal Testing** - Path traversal vulnerability checks
- **SSL/TLS Security Analysis** - Certificate and encryption assessment
- **Subdomain Enumeration** - DNS-based subdomain discovery
- **Cookie Security Analysis** - HttpOnly, Secure, SameSite validation
- **CSRF Protection Testing** - Token implementation verification
- **WAF Detection** - Identifies 8 major Web Application Firewalls
- **HTTP Methods Testing** - Dangerous method identification
- **Security Headers Analysis** - 13 critical security headers

### ⚡ **INTELLIGENT MODES**
- **🥷 STEALTH MODE** - 1-1000 refreshes (Undetectable)
- **💥 ASSAULT MODE** - 1001-10000 refreshes (Balanced)
- **☢️ NUCLEAR MODE** - 10001-9999999 refreshes (Maximum power)

---

## 🎮 QUICK START

### 🚀 **Launch Options**

#### **Option 1: Interactive Launcher (Recommended)**
```bash
python launch.py
```

#### **Option 2: Safe Demo Mode**
```bash
python demo.py
```

#### **Option 3: Full Application**
```bash
python src/refresh_bot.py
```

#### **Option 4: Windows Batch File**
```bash
run_refresh_bot.bat
```

### 📦 **Installation**
```bash
git clone https://github.com/Xenonesis/Refresho.git
cd refresho
pip install -r requirements.txt
python launch.py
```

---

## 🛡️ VAPT ANALYSIS CAPABILITIES

### 🔍 **Comprehensive Security Testing**

#### **SQL Injection Detection**
- Tests 8 different SQL injection payloads
- Checks common parameters: id, user, username, search, q, name, email
- Detects SQL error patterns in responses
- Identifies potential database vulnerabilities

#### **Cross-Site Scripting (XSS)**
- Tests 8 XSS vectors for reflected vulnerabilities
- Payload examples: `<script>alert('XSS')</script>`, `<img src=x onerror=alert('XSS')>`
- Checks parameters: search, q, name, comment, message, input
- Identifies unfiltered user input

#### **Directory Traversal**
- Tests 7 path traversal patterns
- Payloads: `../../etc/passwd`, URL-encoded variants
- Checks parameters: file, page, include, path, doc, document
- Detects file inclusion vulnerabilities

#### **SSL/TLS Analysis**
- Certificate validation and details
- Cipher suite assessment
- Protocol version analysis
- Subject Alternative Names (SAN) verification

#### **Security Headers Assessment**
- Checks 13 critical security headers
- HSTS, CSP, X-Frame-Options validation
- Server information disclosure detection
- Security posture evaluation

### 📊 **VAPT Report Example**
```
+==============================================================+
|                      VAPT ANALYSIS REPORT                    |
+==============================================================+

[SECURITY HEADERS]
  • Strict-Transport-Security: max-age=31536000
  • Content-Security-Policy: default-src 'self'
  • X-Frame-Options: DENY

[SQL INJECTION VULNERABILITIES]
  No SQL injection vulnerabilities detected.

[XSS VULNERABILITIES]
  No XSS vulnerabilities detected.

[COOKIE SECURITY ANALYSIS]
  [!] sessionid: Cookie not marked as Secure
  • auth_token: Secure configuration

[OPEN PORTS (BASIC SCAN)]
  [!] Port 80 (HTTP) is OPEN
  [!] Port 443 (HTTPS) is OPEN
  [!] Port 22 (SSH) is OPEN
+==============================================================+
```

---

## 📁 PROJECT STRUCTURE

```
.
├── src/
│   ├── __init__.py
│   ├── refresh_bot.py          # Main application
│   ├── vapt_analyzer.py        # Security testing module
│   ├── ui_components.py        # User interface elements
│   ├── browser_controller.py   # WebDriver management
│   ├── config_manager.py       # Configuration handling
│   └── mission_controller.py   # Mission execution logic
├── tests/
│   ├── __init__.py
│   ├── test_refresh_bot.py     # Main test suite
│   └── test_features.py        # Feature tests
├── docs/
│   └── VAPT_ENHANCED_FEATURES.md
├── assets/
│   └── rf.png
├── history/                    # Site analysis reports
├── reports/                    # Mission reports
├── saved_urls/                 # URL storage
├── screenshots/                # Captured screenshots
├── launch.py                   # Interactive launcher
├── demo.py                     # Safe demo mode
├── requirements.txt
├── run_refresh_bot.bat
├── .gitignore
└── README.md
```

---

## 🎯 MISSION MODES

### 🥷 **STEALTH MODE**
- **Range:** 1-1000 refreshes
- **Detection:** Nearly impossible
- **Use Case:** Long-term monitoring, VAPT analysis

### 💥 **ASSAULT MODE**
- **Range:** 1001-10000 refreshes
- **Detection:** Low risk
- **Use Case:** Stress testing with security analysis

### ☢️ **NUCLEAR MODE**
- **Range:** 10001-9999999 refreshes
- **Detection:** High intensity
- **Use Case:** Maximum performance testing

---

## 🔧 ADVANCED CONFIGURATION

### 🌐 **Browser Modes**
```
[1] Ghost Mode (Headless + Stealth)
[2] Phantom Mode (Headless + Fast)
[3] Visible Mode (GUI + Debug)
```

### 🛡️ **Security Features**
```
[SECURITY] Enable VAPT (Vulnerability Assessment) mode?
[1] Yes - Include comprehensive security analysis
[2] No - Standard refresh only
```

### 🔧 **Advanced Features**
- ✅ Proxy rotation
- ✅ User agent rotation
- ✅ Screenshot capture
- ✅ Site intelligence analysis
- ✅ VAPT security testing
- ✅ Dynamic URL management
- ✅ History tracking & reporting

---

## 🔍 SITE INTELLIGENCE SYSTEM

### 📊 **Real-Time Analysis**
```
+==============================================================+
|                    SITE INTELLIGENCE REPORT                 |
+==============================================================+
[TARGET] https://example.com
[TITLE] Example Domain
[PERFORMANCE METRICS]
  Load Time: 0.85s
  Page Size: 1,256 bytes
  Security: HTTPS

[CONTENT ANALYSIS]
  Links: 15 | Images: 8 | Forms: 2
  Scripts: 5 | Stylesheets: 3 | Cookies: 4

[TECHNOLOGIES DETECTED]
  • jQuery • Bootstrap • React
```

---

## 🧪 TROUBLESHOOTING

### ⚠️ **Common Issues**

#### **ChromeDriver Problems**
```bash
# Update ChromeDriver
pip install --upgrade selenium webdriver-manager
```

#### **Memory Errors**
- Reduce concurrent operations
- Use headless mode
- Lower refresh count

#### **Network Issues**
- Check internet connection
- Verify proxy settings
- Increase timeout values

#### **VAPT Testing Issues**
- Ensure target URL is accessible
- Check for WAF/security measures
- Verify network connectivity

---

## ⚙️ SYSTEM REQUIREMENTS

### 💻 **Minimum**
- Python 3.9+
- 4GB RAM
- Chrome Browser
- Internet connection

### 🚀 **Recommended**
- Python 3.11+
- 8GB RAM
- SSD Storage
- High-speed Internet

---

## 🚨 ETHICAL USAGE & DISCLAIMER

### ⚖️ **Legal Compliance**
- **ONLY test websites you own or have explicit permission to test**
- Follow responsible disclosure practices
- Comply with local laws and regulations
- Respect website terms of service

### 🛡️ **Security Research Guidelines**
- Use VAPT features for legitimate security assessment only
- Do not attempt to exploit discovered vulnerabilities
- Report security issues responsibly
- Maintain confidentiality of sensitive findings

### 📋 **Intended Use Cases**
- Personal website security testing
- Authorized penetration testing
- Educational cybersecurity research
- Development environment testing

---

## 📫 SUPPORT & CONTACT

- **Email:** itisaddy7@gmail.com
- **Repository:** https://github.com/Xenonesis/Refresho.git
- **Issues:** Create detailed bug reports with system information

---

## 📜 LICENSE

MIT License - Copyright (c) 2025 Addy@Xenonesis

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

---

## 🎉 CREDITS

**🔥 Engineered by Addy@Xenonesis**  
**💀 Enhanced VAPT Features by Roo (Claude Sonnet 4)**  
**⚡ Built for Elite Cybersecurity Professionals**

---

**#HackTheWeb #RefreshThePlanet #VAPTMaster #CyberSecurity**