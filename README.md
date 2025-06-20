# 🚀 REFRESHO - Advanced Web Refresher Tool

```
██████╗ ███████╗███████╗██████╗ ███████╗███████╗██╗  ██╗ ██████╗ 
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██║  ██║██╔═══██╗
██████╔╝█████╗  █████╗  ██████╔╝█████╗  ███████╗███████║██║   ██║
██╔══██╗██╔══╝  ██╔══╝  ██╔══██╗██╔══╝  ╚════██║██╔══██║██║   ██║
██║  ██║███████╗██║     ██║  ██║███████╗███████║██║  ██║╚██████╔╝
╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ 
```

**Developed by Addy@Xenonesis** 🔥

## 🎯 Description
REFRESHO is a powerful, hacker-style web automation tool that refreshes target websites with precision and style. Features a terminal-based interface with real-time progress tracking, execution time analysis, and epic success animations.

## ✨ Features
- 🎨 **Hacker-style ASCII art interface**
- 🎯 **Custom URL targeting**
- 🔢 **Configurable refresh count (up to 9,999,999)**
- ⏱️ **Adjustable delay between refreshes**
- 👁️ **Headless or visible browser modes**
- 📊 **Real-time progress bar with ETA**
- ⚡ **Execution time tracking**
- 🎉 **Epic success animations**
- 🛡️ **Stealth browser configuration**
- 🚨 **Error handling and recovery**

## 🔧 Prerequisites
- Python 3.7 or higher
- Google Chrome browser
- ChromeDriver (auto-managed by Selenium)
- Windows/Linux/macOS support

## 🚀 Quick Start

### Option 1: One-Click Setup (Windows)
```bash
# Double-click run_refresh_bot.bat
# It will automatically set up everything!
```

### Option 2: Manual Setup
```bash
# Clone the repository
git clone <repository-url>
cd refresho

# Install dependencies
pip install -r requirements.txt

# Launch REFRESHO
python refresh_bot.py
```

## 🎮 Usage

1. **Launch the tool:**
   ```bash
   python refresh_bot.py
   ```

2. **Configure your mission:**
   - Enter target URL (or use default)
   - Set refresh count (1 to 9,999,999)
   - Configure delay between refreshes
   - Choose browser mode (headless/visible)

3. **Execute and watch the magic!** ✨

## 📋 Interactive Configuration

```
[?] Enter target URL (or press Enter for default):
[*] Default: https://github.com/Xenonesis
[>] URL: https://example.com

[?] How many times do you want to refresh?
[*] Maximum limit: 9,999,999
[>] Count: 100

[?] Delay between refreshes (seconds)?
[*] Default: 1 second (press Enter)
[>] Delay: 0.5

[?] Browser mode:
[1] Headless (invisible, faster)
[2] Visible (show browser window)
[>] Choose mode (1/2): 1
```

## 🧪 Testing

Run comprehensive tests:
```bash
python -m unittest test_refresh_bot.py -v
```

## 📊 Performance Metrics

- **Real-time progress:** `[████████████████████] 100% | #1,000 | ETA: 0.0s`
- **Execution tracking:** Total time, average per refresh
- **Success rate:** Complete/partial mission status
- **ETA calculation:** Dynamic time estimation

## 🛡️ Stealth Features

- Custom user agent
- Disabled web security
- No extension loading
- Optimized Chrome flags
- Silent operation mode

## 🎯 Use Cases

- **Web testing:** Stress test web applications
- **Automation:** Automated page refreshing
- **Monitoring:** Keep sessions active
- **Development:** Test refresh-dependent features

## 🔧 Advanced Configuration

Modify `refresh_bot.py` for advanced settings:
- Custom Chrome options
- Different browsers
- Proxy configuration
- Custom headers

## 🚨 Error Handling

- Graceful WebDriver failures
- Network timeout recovery
- User interruption handling
- Partial completion tracking

## 📁 Project Structure

```
refresho/
├── refresh_bot.py          # Main application
├── requirements.txt        # Dependencies
├── run_refresh_bot.bat    # Windows launcher
├── test_refresh_bot.py    # Test suite
└── README.md              # This file
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

This project is provided as-is without warranty.

## 🎉 Credits

**Developed with ❤️ by Addy@Xenonesis**

---

*"Hack the web, one refresh at a time!"* 🚀