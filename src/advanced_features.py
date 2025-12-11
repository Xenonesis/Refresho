#!/usr/bin/env python3
"""
Advanced Features for REFRESHO v5.0+
New enhancements including API testing, performance monitoring, and more
"""

import time
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
import statistics

class PerformanceMonitor:
    """Monitor and analyze performance metrics"""
    
    def __init__(self):
        self.metrics = {
            'load_times': [],
            'response_times': [],
            'refresh_times': [],
            'errors': []
        }
    
    def record_load_time(self, duration: float):
        """Record page load time"""
        self.metrics['load_times'].append(duration)
    
    def record_response_time(self, duration: float):
        """Record response time"""
        self.metrics['response_times'].append(duration)
    
    def record_refresh_time(self, duration: float):
        """Record refresh time"""
        self.metrics['refresh_times'].append(duration)
    
    def record_error(self, error: str):
        """Record an error"""
        self.metrics['errors'].append({
            'timestamp': datetime.now().isoformat(),
            'error': error
        })
    
    def get_statistics(self) -> Dict:
        """Calculate and return performance statistics"""
        stats = {
            'load_times': self._calculate_stats(self.metrics['load_times']),
            'response_times': self._calculate_stats(self.metrics['response_times']),
            'refresh_times': self._calculate_stats(self.metrics['refresh_times']),
            'error_count': len(self.metrics['errors'])
        }
        return stats
    
    def _calculate_stats(self, data: List[float]) -> Dict:
        """Calculate statistical measures"""
        if not data:
            return {
                'count': 0,
                'min': 0,
                'max': 0,
                'mean': 0,
                'median': 0,
                'std_dev': 0
            }
        
        return {
            'count': len(data),
            'min': round(min(data), 3),
            'max': round(max(data), 3),
            'mean': round(statistics.mean(data), 3),
            'median': round(statistics.median(data), 3),
            'std_dev': round(statistics.stdev(data), 3) if len(data) > 1 else 0
        }
    
    def print_report(self):
        """Print performance report"""
        stats = self.get_statistics()
        
        print("\n\033[96m+==============================================================+\033[0m")
        print("\033[96m|                  PERFORMANCE ANALYSIS REPORT                 |\033[0m")
        print("\033[96m+==============================================================+\033[0m\n")
        
        print("\033[93m[LOAD TIMES]\033[0m")
        self._print_stats(stats['load_times'])
        
        print("\n\033[93m[RESPONSE TIMES]\033[0m")
        self._print_stats(stats['response_times'])
        
        print("\n\033[93m[REFRESH TIMES]\033[0m")
        self._print_stats(stats['refresh_times'])
        
        print(f"\n\033[91m[ERRORS] Total: {stats['error_count']}\033[0m")
    
    def _print_stats(self, stats: Dict):
        """Print statistics in formatted way"""
        print(f"  Count:   {stats['count']}")
        print(f"  Min:     {stats['min']}s")
        print(f"  Max:     {stats['max']}s")
        print(f"  Mean:    {stats['mean']}s")
        print(f"  Median:  {stats['median']}s")
        print(f"  Std Dev: {stats['std_dev']}s")

class APITester:
    """Test REST APIs and endpoints"""
    
    @staticmethod
    def test_endpoint(url: str, method: str = 'GET', headers: Optional[Dict] = None,
                      data: Optional[Dict] = None, timeout: int = 10) -> Dict:
        """Test a single API endpoint"""
        result = {
            'url': url,
            'method': method,
            'timestamp': datetime.now().isoformat(),
            'status_code': None,
            'response_time': None,
            'success': False,
            'error': None,
            'headers': {},
            'body_size': 0
        }
        
        try:
            start_time = time.time()
            
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=timeout)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=data, timeout=timeout)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=timeout)
            else:
                result['error'] = f"Unsupported method: {method}"
                return result
            
            result['response_time'] = round(time.time() - start_time, 3)
            result['status_code'] = response.status_code
            result['headers'] = dict(response.headers)
            result['body_size'] = len(response.content)
            result['success'] = 200 <= response.status_code < 300
            
        except requests.exceptions.Timeout:
            result['error'] = 'Request timeout'
        except requests.exceptions.ConnectionError:
            result['error'] = 'Connection error'
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    @staticmethod
    def test_multiple_endpoints(endpoints: List[Dict]) -> List[Dict]:
        """Test multiple API endpoints"""
        results = []
        
        print("\033[96m[API TESTING] Testing endpoints...\033[0m")
        
        for i, endpoint in enumerate(endpoints, 1):
            url = endpoint.get('url')
            method = endpoint.get('method', 'GET')
            headers = endpoint.get('headers')
            data = endpoint.get('data')
            
            print(f"\033[93m[{i}/{len(endpoints)}] Testing {method} {url}\033[0m")
            
            result = APITester.test_endpoint(url, method, headers, data)
            results.append(result)
            
            if result['success']:
                print(f"\033[92m  ✓ {result['status_code']} - {result['response_time']}s\033[0m")
            else:
                print(f"\033[91m  ✗ {result['error']}\033[0m")
        
        return results
    
    @staticmethod
    def generate_report(results: List[Dict]) -> Dict:
        """Generate summary report from API test results"""
        total = len(results)
        successful = sum(1 for r in results if r['success'])
        failed = total - successful
        
        response_times = [r['response_time'] for r in results if r['response_time']]
        avg_response = round(statistics.mean(response_times), 3) if response_times else 0
        
        return {
            'total_tests': total,
            'successful': successful,
            'failed': failed,
            'success_rate': round((successful / total * 100), 2) if total > 0 else 0,
            'avg_response_time': avg_response,
            'results': results
        }

class LoadTester:
    """Perform load testing on websites"""
    
    @staticmethod
    def run_load_test(url: str, num_requests: int = 10, 
                      concurrent: bool = False, delay: float = 0) -> Dict:
        """Run a simple load test"""
        print(f"\033[96m[LOAD TEST] Testing {url} with {num_requests} requests\033[0m")
        
        results = []
        start_time = time.time()
        
        for i in range(num_requests):
            request_start = time.time()
            
            try:
                response = requests.get(url, timeout=10)
                request_time = time.time() - request_start
                
                results.append({
                    'request_num': i + 1,
                    'status_code': response.status_code,
                    'response_time': round(request_time, 3),
                    'success': response.status_code == 200
                })
                
                print(f"\033[92m  [{i+1}/{num_requests}] {response.status_code} - {request_time:.3f}s\033[0m")
                
            except Exception as e:
                results.append({
                    'request_num': i + 1,
                    'status_code': None,
                    'response_time': None,
                    'success': False,
                    'error': str(e)
                })
                print(f"\033[91m  [{i+1}/{num_requests}] Error: {e}\033[0m")
            
            if delay > 0:
                time.sleep(delay)
        
        total_time = time.time() - start_time
        
        # Calculate statistics
        successful = sum(1 for r in results if r['success'])
        response_times = [r['response_time'] for r in results if r['response_time']]
        
        report = {
            'url': url,
            'total_requests': num_requests,
            'successful_requests': successful,
            'failed_requests': num_requests - successful,
            'success_rate': round((successful / num_requests * 100), 2),
            'total_time': round(total_time, 3),
            'avg_response_time': round(statistics.mean(response_times), 3) if response_times else 0,
            'min_response_time': round(min(response_times), 3) if response_times else 0,
            'max_response_time': round(max(response_times), 3) if response_times else 0,
            'requests_per_second': round(num_requests / total_time, 2)
        }
        
        return report
    
    @staticmethod
    def print_load_test_report(report: Dict):
        """Print load test report"""
        print("\n\033[96m+==============================================================+\033[0m")
        print("\033[96m|                     LOAD TEST REPORT                         |\033[0m")
        print("\033[96m+==============================================================+\033[0m\n")
        
        print(f"\033[93m[TARGET] {report['url']}\033[0m")
        print(f"\033[92m[REQUESTS] Total: {report['total_requests']} | Success: {report['successful_requests']} | Failed: {report['failed_requests']}\033[0m")
        print(f"\033[92m[SUCCESS RATE] {report['success_rate']}%\033[0m")
        print(f"\033[92m[TOTAL TIME] {report['total_time']}s\033[0m")
        print(f"\033[92m[REQUESTS/SEC] {report['requests_per_second']}\033[0m")
        print(f"\n\033[93m[RESPONSE TIMES]\033[0m")
        print(f"\033[92m  Average: {report['avg_response_time']}s\033[0m")
        print(f"\033[92m  Min:     {report['min_response_time']}s\033[0m")
        print(f"\033[92m  Max:     {report['max_response_time']}s\033[0m")

class ScheduledTester:
    """Schedule and run tests at intervals"""
    
    def __init__(self):
        self.scheduled_tests = []
    
    def add_test(self, url: str, interval: int, max_runs: Optional[int] = None):
        """Add a scheduled test"""
        test = {
            'url': url,
            'interval': interval,
            'max_runs': max_runs,
            'runs': 0,
            'last_run': None,
            'results': []
        }
        self.scheduled_tests.append(test)
    
    def run_scheduled_tests(self):
        """Run scheduled tests (simplified version)"""
        print("\033[96m[SCHEDULED TESTS] Running scheduled tests...\033[0m")
        
        for test in self.scheduled_tests:
            if test['max_runs'] and test['runs'] >= test['max_runs']:
                continue
            
            print(f"\033[93m[TEST] {test['url']}\033[0m")
            
            try:
                start = time.time()
                response = requests.get(test['url'], timeout=10)
                duration = time.time() - start
                
                result = {
                    'timestamp': datetime.now().isoformat(),
                    'status_code': response.status_code,
                    'response_time': round(duration, 3),
                    'success': response.status_code == 200
                }
                
                test['results'].append(result)
                test['runs'] += 1
                test['last_run'] = datetime.now().isoformat()
                
                print(f"\033[92m  ✓ {result['status_code']} - {result['response_time']}s\033[0m")
                
            except Exception as e:
                print(f"\033[91m  ✗ Error: {e}\033[0m")

if __name__ == "__main__":
    print("Advanced Features Module - REFRESHO v5.0+")
    print("Import this module to use enhanced testing capabilities")
