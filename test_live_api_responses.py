#!/usr/bin/env python3
"""
Script untuk menguji semua endpoint API DigitalOcean dan menganalisis struktur response
"""

import requests
import json
from datetime import datetime
import time

# Base URL production DigitalOcean
BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"

class APIResponseTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.auth_token = None
        self.admin_token = None
        self.test_results = []
        
    def log_response(self, endpoint, method, status_code, response_data, issues=None):
        """Log hasil test response"""
        result = {
            'endpoint': endpoint,
            'method': method,
            'status_code': status_code,
            'response_structure': self.analyze_response_structure(response_data),
            'issues': issues or [],
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        return result
    
    def analyze_response_structure(self, data):
        """Analisis struktur response untuk konsistensi"""
        if not isinstance(data, dict):
            return {"type": "non_dict", "structure": type(data).__name__}
        
        structure = {
            "type": "dict",
            "has_success": "success" in data,
            "has_message": "message" in data,
            "has_data": "data" in data,
            "has_errors": "errors" in data or "error" in data,
            "keys": list(data.keys()),
            "key_count": len(data.keys())
        }
        
        return structure
    
    def get_auth_token(self):
        """Dapatkan token untuk testing"""
        print("🔑 Getting authentication token...")
        
        # Coba login dengan user yang sudah ada
        login_data = {
            "email": "employeejon@example.com",
            "password": "securepassword123"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/login/",
                json=login_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'user' in data and 'token' in data['user']:
                    self.auth_token = data['user']['token']
                    print(f"✅ Token obtained: {self.auth_token[:20]}...")
                    return True
                elif 'token' in data:
                    self.auth_token = data['token']
                    print(f"✅ Token obtained: {self.auth_token[:20]}...")
                    return True
            
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
        except Exception as e:
            print(f"❌ Error getting token: {e}")
            return False
    
    def test_endpoint(self, endpoint, method="GET", data=None, auth_required=True):
        """Test single endpoint"""
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if auth_required and self.auth_token:
            headers['Authorization'] = f'Token {self.auth_token}'
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=headers)
            elif method == "PATCH":
                response = requests.patch(url, json=data, headers=headers)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            
            # Parse response
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text}
            
            # Analisis issues
            issues = []
            
            # Cek struktur standard
            if isinstance(response_data, dict):
                if response.status_code < 400:  # Success responses
                    if 'success' not in response_data:
                        issues.append("Missing 'success' field")
                    if 'message' not in response_data:
                        issues.append("Missing 'message' field")
                else:  # Error responses
                    if 'success' not in response_data or response_data.get('success') != False:
                        issues.append("Error response should have 'success': false")
                    if 'message' not in response_data and 'error' not in response_data:
                        issues.append("Missing error message")
            
            result = self.log_response(endpoint, method, response.status_code, response_data, issues)
            return result
            
        except Exception as e:
            error_result = {
                'endpoint': endpoint,
                'method': method,
                'status_code': 'ERROR',
                'response_structure': {"type": "exception", "error": str(e)},
                'issues': [f"Request failed: {str(e)}"],
                'timestamp': datetime.now().isoformat()
            }
            self.test_results.append(error_result)
            return error_result

    def test_core_endpoints(self):
        """Test endpoint inti"""
        print("\n🔍 TESTING CORE ENDPOINTS")
        print("=" * 50)
        
        # Health check (no auth)
        self.test_endpoint("/api/health/", auth_required=False)
        
        # API info (no auth)
        self.test_endpoint("/api/info/", auth_required=False)
        
        # User profile
        self.test_endpoint("/api/profile/")
        
        # Departments
        self.test_endpoint("/api/departments/")
        
        # Employees (admin only, might fail)
        self.test_endpoint("/api/employees/")
        
    def test_authentication_endpoints(self):
        """Test endpoint authentication"""
        print("\n🔐 TESTING AUTHENTICATION ENDPOINTS")
        print("=" * 50)
        
        # Register (create new user)
        timestamp = int(datetime.now().timestamp())
        register_data = {
            "email": f"api_test_{timestamp}@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "first_name": "API",
            "last_name": "Test",
            "phone_number": f"+628123{timestamp % 100000}",
            "date_of_birth": "1990-01-01",
            "gender": "M",
            "marital_status": "single",
            "education_level": "bachelor",
            "address": "Test Address",
            "position": "Test Position",
            "department": 1,
            "hire_date": "2024-01-01"
        }
        
        self.test_endpoint("/api/register/", "POST", register_data, auth_required=False)
        
        # Login
        login_data = {
            "email": "employeejon@example.com",
            "password": "securepassword123"
        }
        self.test_endpoint("/api/login/", "POST", login_data, auth_required=False)
        
        # Logout
        self.test_endpoint("/api/logout/", "POST")
    
    def generate_report(self):
        """Generate laporan hasil test"""
        print(f"\n📊 API RESPONSE ANALYSIS REPORT")
        print("=" * 60)
        print(f"🕐 Generated at: {datetime.now()}")
        print(f"🌐 Base URL: {self.base_url}")
        print(f"📋 Total endpoints tested: {len(self.test_results)}")
        
        # Kategorisasi hasil
        success_responses = [r for r in self.test_results if isinstance(r['status_code'], int) and r['status_code'] < 400]
        error_responses = [r for r in self.test_results if isinstance(r['status_code'], int) and r['status_code'] >= 400]
        failed_requests = [r for r in self.test_results if r['status_code'] == 'ERROR']
        
        print(f"✅ Successful responses: {len(success_responses)}")
        print(f"❌ Error responses: {len(error_responses)}")
        print(f"🔥 Failed requests: {len(failed_requests)}")
        
        # Analisis konsistensi
        print(f"\n🎯 CONSISTENCY ANALYSIS")
        print("=" * 60)
        
        inconsistent_responses = []
        for result in self.test_results:
            if result['issues']:
                inconsistent_responses.append(result)
        
        print(f"🚨 Inconsistent responses: {len(inconsistent_responses)}")
        
        # Detail issues
        if inconsistent_responses:
            print(f"\n📝 DETAILED ISSUES:")
            print("-" * 40)
            
            for result in inconsistent_responses:
                print(f"\n🔸 {result['method']} {result['endpoint']}")
                print(f"   Status: {result['status_code']}")
                print(f"   Structure: {result['response_structure']['keys'] if 'keys' in result['response_structure'] else 'N/A'}")
                for issue in result['issues']:
                    print(f"   ⚠️  {issue}")
        
        # Struktur response patterns
        print(f"\n📋 RESPONSE STRUCTURE PATTERNS")
        print("=" * 60)
        
        structure_patterns = {}
        for result in self.test_results:
            if 'keys' in result['response_structure']:
                pattern = tuple(sorted(result['response_structure']['keys']))
                if pattern not in structure_patterns:
                    structure_patterns[pattern] = []
                structure_patterns[pattern].append(result['endpoint'])
        
        for pattern, endpoints in structure_patterns.items():
            print(f"\n🏷️  Pattern {pattern}:")
            for endpoint in endpoints[:3]:
                print(f"   • {endpoint}")
            if len(endpoints) > 3:
                print(f"   • ... and {len(endpoints) - 3} more")
        
        # Rekomendasi perbaikan
        print(f"\n💡 IMPROVEMENT RECOMMENDATIONS")
        print("=" * 60)
        
        recommendations = []
        
        # Cek missing success field
        missing_success = [r for r in success_responses if not r['response_structure'].get('has_success')]
        if missing_success:
            recommendations.append(f"Add 'success': true to {len(missing_success)} successful responses")
        
        # Cek missing message field
        missing_message = [r for r in self.test_results if not r['response_structure'].get('has_message')]
        if missing_message:
            recommendations.append(f"Add 'message' field to {len(missing_message)} responses")
        
        # Cek error responses
        bad_error_responses = [r for r in error_responses if r['response_structure'].get('has_success') != False]
        if bad_error_responses:
            recommendations.append(f"Fix error response structure for {len(bad_error_responses)} endpoints")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
        
        if not recommendations:
            print("🎉 All responses follow consistent structure!")
        
        return {
            'total_tested': len(self.test_results),
            'successful': len(success_responses),
            'errors': len(error_responses),
            'failed': len(failed_requests),
            'inconsistent': len(inconsistent_responses),
            'recommendations': recommendations
        }

def main():
    print("🚀 LIVE API RESPONSE TESTING")
    print("=" * 60)
    print(f"🌐 Testing API: {BASE_URL}")
    
    tester = APIResponseTester()
    
    # Get authentication token
    if not tester.get_auth_token():
        print("❌ Cannot proceed without authentication token")
        return
    
    # Test endpoints
    tester.test_core_endpoints()
    tester.test_authentication_endpoints()
    
    # Generate report
    report = tester.generate_report()
    
    print(f"\n✅ Testing complete!")
    print(f"📊 Summary: {report['successful']} success, {report['errors']} errors, {report['inconsistent']} inconsistent")

if __name__ == "__main__":
    main()
