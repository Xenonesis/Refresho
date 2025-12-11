# REFRESHO v5.0 - Usage Guide

## 🚀 Getting Started

### Prerequisites
- Python 3.9+ installed
- Chrome browser installed
- Internet connection
- 4GB+ RAM recommended

### Installation
1. Download/clone REFRESHO v5.0
2. Open terminal in project directory
3. Install dependencies: `pip install -r requirements.txt`

## 🎮 Launch Methods

### Method 1: Interactive Launcher (Recommended)
```bash
python launch.py
```
**Features:**
- Menu-driven interface
- Safe demo mode
- Test runner
- Easy navigation

### Method 2: Demo Mode (Safe Testing)
```bash
python demo.py
```
**Features:**
- No actual web refreshing
- Shows system info
- Tests VAPT functionality
- Demonstrates URL management

### Method 3: Full Application
```bash
python src/refresh_bot.py
```
**Features:**
- Complete REFRESHO experience
- All refresh modes available
- Full VAPT testing
- Advanced configurations

### Method 4: Windows Batch File
```bash
run_refresh_bot.bat
```
**Features:**
- Automatic environment setup
- Dependency installation
- Virtual environment management
- Windows-optimized launcher

## 🎯 Mission Configuration

### Target Selection
1. **Default URL**: https://github.com/Xenonesis
2. **Saved URLs**: Previously stored targets
3. **Custom URL**: Enter any valid URL
4. **URL Management**: Add/remove saved URLs

### Refresh Modes
- **🥷 Stealth Mode**: 1-1000 refreshes (Undetectable)
- **💥 Assault Mode**: 1001-10000 refreshes (Balanced)
- **☢️ Nuclear Mode**: 10001-9999999 refreshes (Maximum power)

### Browser Configuration
- **Ghost Mode**: Headless + Stealth features
- **Phantom Mode**: Headless + Fast execution
- **Visible Mode**: GUI + Debug capabilities

### Advanced Features
- **VAPT Mode**: Enable security vulnerability assessment
- **Screenshot Capture**: Save screenshots every 10 refreshes
- **User Agent Rotation**: Change browser identity
- **Site Intelligence**: Comprehensive target analysis

## 🛡️ VAPT Security Testing

### Enabled Tests
- SQL Injection (8 payload patterns)
- XSS Vulnerabilities (8 vectors)
- Directory Traversal (7 patterns)
- Security Headers (13 headers)
- Sensitive File Detection
- Port Scanning (12 common ports)

### Report Generation
- Real-time terminal output
- JSON reports saved to `history/`
- VAPT results appended to analysis files
- Mission reports in `reports/`

## 📊 Output Files

### Screenshots
- Location: `screenshots/`
- Format: `refresh_XXXX.png`
- Frequency: Every 10 refreshes

### Analysis Reports
- Location: `history/`
- Format: `domain_timestamp.json`
- Contains: Site intelligence + VAPT results

### Mission Reports
- Location: `reports/`
- Format: `mission_timestamp.json`
- Contains: Performance metrics + configuration

### URL Storage
- Location: `saved_urls/saved_urls.json`
- Format: JSON array with name/URL pairs

## 🔧 Troubleshooting

### Common Issues
1. **ChromeDriver Error**: Run `pip install --upgrade selenium webdriver-manager`
2. **Permission Error**: Run as administrator on Windows
3. **Network Timeout**: Check internet connection
4. **Memory Error**: Reduce refresh count or use headless mode

### Debug Mode
- Use Visible Mode for debugging
- Check console output for errors
- Verify target URL accessibility
- Test with demo mode first

## ⚖️ Ethical Usage

### Legal Requirements
- Only test websites you own
- Obtain explicit permission for third-party sites
- Follow responsible disclosure practices
- Comply with local laws and regulations

### Best Practices
- Start with demo mode
- Use stealth mode for legitimate testing
- Respect website terms of service
- Report vulnerabilities responsibly

## 📞 Support

For issues or questions:
- Email: itisaddy7@gmail.com
- Repository: https://github.com/Xenonesis/Refresho.git
- Create detailed bug reports with system information