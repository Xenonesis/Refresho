import os
import sys
import time
import string
import random
from datetime import datetime

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Display application banner"""
    banner = """
\033[92m
██████╗ ███████╗███████╗██████╗ ███████╗███████╗██╗  ██╗ ██████╗ 
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██║  ██║██╔═══██╗
██████╔╝█████╗  █████╗  ██████╔╝█████╗  ███████╗███████║██║   ██║
██╔══██╗██╔══╝  ██╔══╝  ██╔══██╗██╔══╝  ╚════██║██╔══██║██║   ██║
██║  ██║███████╗██║     ██║  ██║███████╗███████║██║  ██║╚██████╔╝
╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ 
\033[0m"""
    banner += """
\033[96m+==============================================================+\033[0m
\033[96m|              ADVANCED WEB REFRESHER TOOL v5.0              |\033[0m
\033[96m|                 Developed by Addy@Xenonesis                |\033[0m
\033[96m+==============================================================+\033[0m
"""
    print(banner)
    
    # Import here to avoid circular imports
    try:
        from .refresh_bot import SystemAnalyzer, HackerEffects
    except ImportError:
        from refresh_bot import SystemAnalyzer, HackerEffects
    
    # System info display
    sys_info = SystemAnalyzer.get_system_info()
    session_id = SystemAnalyzer.generate_session_id()
    
    print(f"\033[93m[SYSTEM] CPU: {sys_info['cpu_percent']}% | RAM: {sys_info['memory_percent']}% | DISK: {sys_info['disk_usage']}%\033[0m")
    print(f"\033[95m[SESSION] ID: {session_id} | CONNECTIONS: {sys_info['network_connections']} | BOOT: {sys_info['boot_time']}\033[0m")
    print(f"\033[91m[STATUS] INITIALIZING HACKER MODE...\033[0m")
    
    # Matrix effect
    try:
        HackerEffects.matrix_rain(1)
    except:
        # Skip matrix effect if not supported
        pass

def loading_animation():
    """Display loading animation"""
    phases = [
        "SCANNING NETWORK INTERFACES",
        "BYPASSING SECURITY PROTOCOLS", 
        "INJECTING PAYLOAD MODULES",
        "ESTABLISHING SECURE TUNNEL",
        "ACTIVATING STEALTH MODE",
        "LOADING EXPLOIT FRAMEWORK"
    ]
    
    for phase in phases:
        for i in range(10):
            chars = "/-\\|"
            sys.stdout.write(f"\r\033[92m[{chars[i % 4]}] {phase}{'.' * (i % 4)}\033[0m")
            sys.stdout.flush()
            time.sleep(0.1)
        print(f"\r\033[92m[✓] {phase} COMPLETE\033[0m" + " " * 20)
    
    print("\033[92m[>>>] ALL SYSTEMS OPERATIONAL [<<<]\033[0m")