import re
import socket
import requests
from urllib.parse import urlparse
from selenium.webdriver.common.by import By

class VAPTAnalyzer:
    @staticmethod
    def check_security_headers(url):
        """Check for common security headers"""
        headers = {}
        try:
            response = requests.head(url, timeout=10) # Use HEAD request for efficiency
            headers = response.headers
        except requests.exceptions.RequestException as e:
            print(f"\033[91m[VAPT ERROR] Failed to get headers for {url}: {e}\033[0m")
            return {}

        security_headers = {
            'Strict-Transport-Security': headers.get('Strict-Transport-Security'),
            'Content-Security-Policy': headers.get('Content-Security-Policy'),
            'X-Content-Type-Options': headers.get('X-Content-Type-Options'),
            'X-Frame-Options': headers.get('X-Frame-Options'),
            'Referrer-Policy': headers.get('Referrer-Policy'),
            'Permissions-Policy': headers.get('Permissions-Policy'),
            'Cross-Origin-Embedder-Policy': headers.get('Cross-Origin-Embedder-Policy'),
            'Cross-Origin-Opener-Policy': headers.get('Cross-Origin-Opener-Policy'),
            'Cross-Origin-Resource-Policy': headers.get('Cross-Origin-Resource-Policy'),
            'Feature-Policy': headers.get('Feature-Policy'), # Older name for Permissions-Policy
            'X-XSS-Protection': headers.get('X-XSS-Protection'),
            'Server': headers.get('Server'),
            'X-Powered-By': headers.get('X-Powered-By')
        }
        # Filter out None values
        return {k: v for k, v in security_headers.items() if v is not None}

    @staticmethod
    def test_sql_injection(url):
        """Test for SQL injection vulnerabilities"""
        print(f"\033[96m[VAPT] Testing SQL injection vulnerabilities...\033[0m")
        vulnerabilities = []
        
        # Common SQL injection payloads
        sql_payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "' UNION SELECT NULL--",
            "'; DROP TABLE users--",
            "' OR 'x'='x",
            "1' OR '1'='1' #",
            "admin'--",
            "' OR 1=1/*"
        ]
        
        # Test common parameters
        test_params = ['id', 'user', 'username', 'search', 'q', 'name', 'email']
        
        for param in test_params:
            for payload in sql_payloads:
                try:
                    test_url = f"{url}?{param}={payload}"
                    response = requests.get(test_url, timeout=5)
                    
                    # Check for SQL error patterns
                    error_patterns = [
                        'sql syntax',
                        'mysql_fetch',
                        'ora-',
                        'microsoft ole db',
                        'sqlite_',
                        'postgresql',
                        'warning: mysql',
                        'valid mysql result',
                        'mysqlclient',
                        'sql server'
                    ]
                    
                    response_text = response.text.lower()
                    for pattern in error_patterns:
                        if pattern in response_text:
                            vulnerabilities.append({
                                'parameter': param,
                                'payload': payload,
                                'pattern': pattern,
                                'url': test_url
                            })
                            break
                            
                except requests.exceptions.RequestException:
                    continue
                    
        return vulnerabilities

    @staticmethod
    def test_xss_vulnerabilities(url):
        """Test for XSS vulnerabilities"""
        print(f"\033[96m[VAPT] Testing XSS vulnerabilities...\033[0m")
        vulnerabilities = []
        
        # XSS payloads
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src=javascript:alert('XSS')>",
            "'><script>alert('XSS')</script>",
            "\"><script>alert('XSS')</script>",
            "<body onload=alert('XSS')>"
        ]
        
        test_params = ['search', 'q', 'name', 'comment', 'message', 'input']
        
        for param in test_params:
            for payload in xss_payloads:
                try:
                    test_url = f"{url}?{param}={payload}"
                    response = requests.get(test_url, timeout=5)
                    
                    if payload in response.text:
                        vulnerabilities.append({
                            'parameter': param,
                            'payload': payload,
                            'url': test_url,
                            'type': 'Reflected XSS'
                        })
                        
                except requests.exceptions.RequestException:
                    continue
                    
        return vulnerabilities
    
    @staticmethod
    def test_xss(url):
        """Alias for test_xss_vulnerabilities for backward compatibility"""
        return VAPTAnalyzer.test_xss_vulnerabilities(url)

    @staticmethod
    def check_sensitive_files(url):
        """Check for common sensitive files/directories"""
        sensitive_paths = [
            '/robots.txt',
            '/.env',
            '/.git/config',
            '/wp-config.php', # Common WordPress file
            '/admin/', # Common admin directory
            '/backup/', # Common backup directory
            '/temp/', # Common temp directory
            '/tmp/' # Common temp directory
        ]
        found_files = []
        base_url = urlparse(url).scheme + "://" + urlparse(url).netloc

        for path in sensitive_paths:
            target_url = base_url + path
            try:
                # Use a short timeout and check status code
                response = requests.get(target_url, timeout=5)
                # Consider 200 OK as potentially found, but also check for common "Not Found" content
                # This is a basic check, a real VAPT tool would be more sophisticated
                if response.status_code == 200:
                     # Simple check to avoid reporting generic 404 pages that return 200
                    if "not found" not in response.text.lower() and "page not found" not in response.text.lower():
                         found_files.append(target_url)
            except requests.exceptions.RequestException:
                # Ignore connection errors, timeouts, etc.
                pass
        return found_files

    @staticmethod
    def scan_ports(url, ports=[80, 443, 22, 21, 23, 25, 110, 143, 3306, 5432, 6379, 27017]):
        """Basic port scan for common ports"""
        open_ports = []
        domain = urlparse(url).netloc
        # Remove port if present in domain
        if ':' in domain:
            domain = domain.split(':')[0]

        # Avoid scanning IP addresses that might be internal
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain):
             print(f"\033[93m[VAPT INFO] Skipping port scan for IP address: {domain}\033[0m")
             return []

        print(f"\033[96m[VAPT] Starting basic port scan for {domain}...\033[0m")
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1) # Short timeout
            try:
                result = sock.connect_ex((domain, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"\033[92m[VAPT] Port {port} is OPEN\033[0m")
                sock.close()
            except socket.gaierror:
                print(f"\033[91m[VAPT ERROR] Hostname could not be resolved: {domain}\033[0m")
                return []
            except socket.error:
                 pass # Ignore other socket errors
            except Exception as e:
                 print(f"\033[91m[VAPT ERROR] Unexpected error during port scan on port {port}: {e}\033[0m")
                 pass # Catch any other exceptions
        print(f"\033[96m[VAPT] Basic port scan finished.\033[0m")
        return open_ports
    
    @staticmethod
    def check_cors_policy(url):
        """Check CORS policy configuration"""
        print(f"\033[96m[VAPT] Checking CORS policy...\033[0m")
        cors_headers = {}
        
        try:
            response = requests.options(url, timeout=10)
            cors_related = [
                'Access-Control-Allow-Origin',
                'Access-Control-Allow-Methods',
                'Access-Control-Allow-Headers',
                'Access-Control-Allow-Credentials',
                'Access-Control-Max-Age'
            ]
            
            for header in cors_related:
                if header in response.headers:
                    cors_headers[header] = response.headers[header]
                    
        except requests.exceptions.RequestException as e:
            print(f"\033[91m[VAPT ERROR] Failed to check CORS: {e}\033[0m")
        
        return cors_headers

    @staticmethod
    def perform_vapt_checks(url, driver):
        """Perform all VAPT checks"""
        vapt_results = {}
        print(f"\n\033[96m[VAPT] Starting comprehensive VAPT analysis for {url}...\033[0m")

        # Security Headers
        print(f"\033[96m[VAPT] Checking security headers...\033[0m")
        vapt_results['security_headers'] = VAPTAnalyzer.check_security_headers(url)
        print(f"\033[92m[VAPT] Security headers check complete.\033[0m")

        # Sensitive Files
        print(f"\033[96m[VAPT] Checking for sensitive files...\033[0m")
        vapt_results['sensitive_files'] = VAPTAnalyzer.check_sensitive_files(url)
        print(f"\033[92m[VAPT] Sensitive files check complete.\033[0m")

        # Port Scan
        print(f"\033[96m[VAPT] Performing basic port scan...\033[0m")
        vapt_results['open_ports'] = VAPTAnalyzer.scan_ports(url)
        print(f"\033[92m[VAPT] Basic port scan complete.\033[0m")

        # SQL Injection Testing
        vapt_results['sql_injection'] = VAPTAnalyzer.test_sql_injection(url)

        # XSS Testing
        vapt_results['xss_vulnerabilities'] = VAPTAnalyzer.test_xss_vulnerabilities(url)

        print(f"\033[96m[VAPT] Comprehensive VAPT analysis finished.\033[0m")
        return vapt_results

    @staticmethod
    def display_vapt_results(vapt_results):
        """Display VAPT results in terminal"""
        print(f"\n\033[96m+==============================================================+\033[0m")
        print(f"\033[96m|                      VAPT ANALYSIS REPORT                    |\033[0m")
        print(f"\033[96m+==============================================================+\033[0m")

        # Security Headers
        print(f"\033[96m[SECURITY HEADERS]\033[0m")
        if vapt_results.get('security_headers'):
            for header, value in vapt_results['security_headers'].items():
                truncated_value = value[:100] + "..." if len(value) > 100 else value
                print(f"\033[92m  • {header}: {truncated_value}\033[0m")
        else:
            print(f"\033[93m  No specific security headers found or could not retrieve.\033[0m")

        # SQL Injection Vulnerabilities
        print(f"\n\033[96m[SQL INJECTION VULNERABILITIES]\033[0m")
        if vapt_results.get('sql_injection'):
            for vuln in vapt_results['sql_injection']:
                print(f"\033[91m  [!] Parameter: {vuln['parameter']} | Pattern: {vuln['pattern']}\033[0m")
        else:
            print(f"\033[92m  No SQL injection vulnerabilities detected.\033[0m")

        # XSS Vulnerabilities
        print(f"\n\033[96m[XSS VULNERABILITIES]\033[0m")
        if vapt_results.get('xss_vulnerabilities'):
            for vuln in vapt_results['xss_vulnerabilities']:
                print(f"\033[91m  [!] {vuln['type']} in parameter: {vuln['parameter']}\033[0m")
        else:
            print(f"\033[92m  No XSS vulnerabilities detected.\033[0m")

        # Sensitive Files
        print(f"\n\033[96m[SENSITIVE FILES/DIRECTORIES]\033[0m")
        if vapt_results.get('sensitive_files'):
            for file_path in vapt_results['sensitive_files']:
                print(f"\033[91m  [!] Potentially found: {file_path}\033[0m")
        else:
            print(f"\033[92m  No common sensitive files/directories found.\033[0m")

        # Open Ports
        print(f"\n\033[96m[OPEN PORTS (BASIC SCAN)]\033[0m")
        if vapt_results.get('open_ports'):
            for port in vapt_results['open_ports']:
                service_info = {
                    22: "SSH", 80: "HTTP", 443: "HTTPS", 21: "FTP",
                    23: "Telnet", 25: "SMTP", 110: "POP3", 143: "IMAP",
                    3306: "MySQL", 5432: "PostgreSQL", 6379: "Redis", 27017: "MongoDB"
                }
                service = service_info.get(port, "Unknown")
                print(f"\033[91m  [!] Port {port} ({service}) is OPEN\033[0m")
        else:
            print(f"\033[92m  No common ports found open or scan skipped.\033[0m")

        print(f"\033[96m+==============================================================+\033[0m")

    @staticmethod
    def save_vapt_results(vapt_results, analysis_filename):
        """Append VAPT results to the saved analysis file"""
        import json
        
        if not analysis_filename:
            print(f"\033[91m[VAPT ERROR] Cannot save VAPT results, analysis filename is missing.\033[0m")
            return

        try:
            with open(analysis_filename, 'r+', encoding='utf-8') as f:
                analysis_data = json.load(f)
                analysis_data['vapt_results'] = vapt_results # Add VAPT results
                f.seek(0) # Rewind to the beginning
                json.dump(analysis_data, f, indent=2, ensure_ascii=False)
                f.truncate() # Truncate the rest of the file
            print(f"\033[95m[INTEL] VAPT results appended to: {analysis_filename}\033[0m")
        except FileNotFoundError:
            print(f"\033[91m[VAPT ERROR] Analysis file not found: {analysis_filename}\033[0m")
        except json.JSONDecodeError:
            print(f"\033[91m[VAPT ERROR] Failed to decode JSON from analysis file: {analysis_filename}\033[0m")
        except Exception as e:
            print(f"\033[91m[VAPT ERROR] Failed to save VAPT results: {e}\033[0m")