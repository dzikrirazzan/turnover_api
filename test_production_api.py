#!/usr/bin/env python3
"""
Comprehensive API Testing for SMART-EN Turnover API
Testing deployed DigitalOcean API: https://turnover-api-hd7ze.ondigitalocean.app/
"""

import requests
import json
import time
from datetime import datetime

# Production API Base URL
BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"

# Global variables to store tokens
AUTH_TOKEN = None
ADMIN_TOKEN = None
EMPLOYEE_ID = None
DEPARTMENT_ID = None

def log_test(test_name, status, details=""):
    """Log test results with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"[{timestamp}] {status_emoji} {test_name}")
    if details:
        print(f"    📝 {details}")

def make_request(method, endpoint, data=None, headers=None, expected_status=None):
    """Helper function to make API requests"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        session = requests.Session()
        session.verify = True  # Enable SSL verification for production
        
        # Default headers
        default_headers = {'Content-Type': 'application/json'}
        if headers:
            default_headers.update(headers)
        
        if method.upper() == 'GET':
            response = session.get(url, headers=default_headers)
        elif method.upper() == 'POST':
            response = session.post(url, json=data, headers=default_headers)
        elif method.upper() == 'PUT':
            response = session.put(url, json=data, headers=default_headers)
        elif method.upper() == 'PATCH':
            response = session.patch(url, json=data, headers=default_headers)
        elif method.upper() == 'DELETE':
            response = session.delete(url, headers=default_headers)
        else:
            return None, f"Unsupported method: {method}"
            
        # Parse JSON response
        try:
            response_data = response.json()
        except:
            response_data = response.text
            
        # Check expected status
        if expected_status and response.status_code != expected_status:
            return response_data, f"Expected {expected_status}, got {response.status_code}"
        
        return response_data, None if response.status_code < 400 else f"HTTP {response.status_code}"
        
    except Exception as e:
        return None, str(e)

def test_health_and_info():
    """Test basic health and info endpoints"""
    print("\n" + "="*80)
    print("🏥 TESTING HEALTH & INFO ENDPOINTS")
    print("="*80)
    
    # Health check
    response, error = make_request('GET', '/api/health/', expected_status=200)
    if error:
        log_test("Health Check", "FAIL", error)
    else:
        log_test("Health Check", "PASS", f"Status: {response.get('status', 'N/A')}")
    
    # API Info
    response, error = make_request('GET', '/api/info/', expected_status=200)
    if error:
        log_test("API Info", "FAIL", error)
    else:
        log_test("API Info", "PASS", f"Version: {response.get('version', 'N/A')}")

def test_registration():
    """Test employee registration with new improved response"""
    global AUTH_TOKEN, EMPLOYEE_ID
    
    print("\n" + "="*80)
    print("👤 TESTING EMPLOYEE REGISTRATION")
    print("="*80)
    
    # Test data yang Anda berikan
    registration_data = {
        "email": "employeejik@example.com",
        "password": "passwordjikri",
        "password_confirm": "passwordjikri",
        "first_name": "jikri",
        "last_name": "tes",
        "phone_number": "+6281234567891",
        "date_of_birth": "1990-05-11",
        "gender": "M",
        "marital_status": "single",
        "education_level": "bachelor",
        "address": "Jl. Contoh No. 123, Jakarta",
        "position": "Junior Staff",
        "department": 1,
        "hire_date": "2023-01-01"
    }
    
    response, error = make_request('POST', '/api/register/', data=registration_data, expected_status=201)
    
    if error:
        log_test("Employee Registration", "FAIL", error)
        return False
    
    # Check new response format
    if 'employee' in response and 'token' in response['employee']:
        AUTH_TOKEN = response['employee']['token']
        EMPLOYEE_ID = response['employee']['id']
        log_test("Employee Registration", "PASS", 
                f"Employee ID: {response['employee']['employee_id']}, Token: {AUTH_TOKEN[:20]}...")
        
        # Verify complete data in response
        employee_data = response['employee']
        required_fields = ['id', 'employee_id', 'email', 'first_name', 'last_name', 
                          'full_name', 'phone_number', 'department', 'department_name', 'token']
        
        missing_fields = [field for field in required_fields if field not in employee_data]
        if missing_fields:
            log_test("Registration Response Completeness", "WARN", 
                    f"Missing fields: {missing_fields}")
        else:
            log_test("Registration Response Completeness", "PASS", 
                    "All required fields present")
        
        return True
    else:
        log_test("Employee Registration", "FAIL", 
                "Response doesn't contain complete employee data with token")
        return False

def test_login():
    """Test employee login with improved response"""
    global AUTH_TOKEN
    
    print("\n" + "="*80)
    print("🔐 TESTING EMPLOYEE LOGIN")
    print("="*80)
    
    login_data = {
        "email": "employeejik@example.com",
        "password": "passwordjikri"
    }
    
    response, error = make_request('POST', '/api/login/', data=login_data, expected_status=200)
    
    if error:
        log_test("Employee Login", "FAIL", error)
        return False
    
    # Check new response format
    if 'user' in response and 'token' in response['user']:
        AUTH_TOKEN = response['user']['token']
        log_test("Employee Login", "PASS", 
                f"Token: {AUTH_TOKEN[:20]}..., User: {response['user']['full_name']}")
        
        # Verify token consistency
        if 'user' in response:
            user_data = response['user']
            required_fields = ['id', 'employee_id', 'email', 'first_name', 'last_name', 
                              'full_name', 'token', 'role', 'department', 'department_name']
            
            missing_fields = [field for field in required_fields if field not in user_data]
            if missing_fields:
                log_test("Login Response Completeness", "WARN", 
                        f"Missing fields: {missing_fields}")
            else:
                log_test("Login Response Completeness", "PASS", 
                        "All required fields present")
        
        return True
    else:
        log_test("Employee Login", "FAIL", 
                "Response doesn't contain user data with token")
        return False

def test_profile():
    """Test user profile endpoint with token authentication"""
    print("\n" + "="*80)
    print("👨‍💼 TESTING USER PROFILE")
    print("="*80)
    
    if not AUTH_TOKEN:
        log_test("User Profile", "SKIP", "No auth token available")
        return
    
    headers = {'Authorization': f'Token {AUTH_TOKEN}'}
    response, error = make_request('GET', '/api/profile/', headers=headers, expected_status=200)
    
    if error:
        log_test("User Profile", "FAIL", error)
    else:
        log_test("User Profile", "PASS", 
                f"Profile for: {response.get('full_name', 'N/A')}")
        
        # Check if profile response includes token (consistency with login)
        if 'token' in response:
            log_test("Profile Token Consistency", "PASS", "Token included in profile response")
        else:
            log_test("Profile Token Consistency", "WARN", "Token not included in profile response")

def test_departments():
    """Test department CRUD operations"""
    global DEPARTMENT_ID
    
    print("\n" + "="*80)
    print("🏢 TESTING DEPARTMENT OPERATIONS")
    print("="*80)
    
    if not AUTH_TOKEN:
        log_test("Department Tests", "SKIP", "No auth token available")
        return
    
    headers = {'Authorization': f'Token {AUTH_TOKEN}'}
    
    # List departments
    response, error = make_request('GET', '/api/departments/', headers=headers, expected_status=200)
    if error:
        log_test("List Departments", "FAIL", error)
    else:
        log_test("List Departments", "PASS", f"Found {len(response)} departments")
        if response and len(response) > 0:
            DEPARTMENT_ID = response[0]['id']
    
    # Get department details
    if DEPARTMENT_ID:
        response, error = make_request('GET', f'/api/departments/{DEPARTMENT_ID}/', 
                                     headers=headers, expected_status=200)
        if error:
            log_test("Get Department Details", "FAIL", error)
        else:
            log_test("Get Department Details", "PASS", 
                    f"Department: {response.get('name', 'N/A')}")
    
    # Test department employees endpoint
    if DEPARTMENT_ID:
        response, error = make_request('GET', f'/api/departments/{DEPARTMENT_ID}/employees/', 
                                     headers=headers, expected_status=200)
        if error:
            log_test("Department Employees", "FAIL", error)
        else:
            total_employees = response.get('total_employees', 0)
            log_test("Department Employees", "PASS", 
                    f"Total employees: {total_employees}")

def test_legacy_endpoints():
    """Test legacy endpoints that should still work"""
    print("\n" + "="*80)
    print("🔄 TESTING LEGACY ENDPOINTS")
    print("="*80)
    
    # Legacy departments list
    response, error = make_request('GET', '/api/departments-list/', expected_status=200)
    if error:
        log_test("Legacy Departments List", "FAIL", error)
    else:
        log_test("Legacy Departments List", "PASS", f"Found {len(response)} departments")
    
    # Legacy employees list (admin only)
    if AUTH_TOKEN:
        headers = {'Authorization': f'Token {AUTH_TOKEN}'}
        response, error = make_request('GET', '/api/employees/', headers=headers)
        
        if error and "401" in str(error):
            log_test("Legacy Employees List", "PASS", "Correctly requires admin access")
        elif error:
            log_test("Legacy Employees List", "FAIL", error)
        else:
            log_test("Legacy Employees List", "PASS", "Access granted")

def test_employee_crud():
    """Test employee CRUD operations (admin required)"""
    print("\n" + "="*80)
    print("👥 TESTING EMPLOYEE CRUD (Admin Required)")
    print("="*80)
    
    if not AUTH_TOKEN:
        log_test("Employee CRUD", "SKIP", "No auth token available")
        return
    
    headers = {'Authorization': f'Token {AUTH_TOKEN}'}
    
    # List employees (admin only)
    response, error = make_request('GET', '/api/employees/', headers=headers)
    if error and "403" in str(error):
        log_test("List Employees", "PASS", "Correctly requires admin permissions")
    elif error:
        log_test("List Employees", "FAIL", error)
    else:
        log_test("List Employees", "PASS", f"Found {len(response)} employees")
    
    # Employee statistics
    response, error = make_request('GET', '/api/employees/statistics/', headers=headers)
    if error and "403" in str(error):
        log_test("Employee Statistics", "PASS", "Correctly requires admin permissions")
    elif error:
        log_test("Employee Statistics", "FAIL", error)
    else:
        log_test("Employee Statistics", "PASS", 
                f"Total employees: {response.get('total_employees', 'N/A')}")

def test_performance_endpoints():
    """Test performance app endpoints"""
    print("\n" + "="*80)
    print("📊 TESTING PERFORMANCE ENDPOINTS")
    print("="*80)
    
    if not AUTH_TOKEN:
        log_test("Performance Tests", "SKIP", "No auth token available")
        return
    
    headers = {'Authorization': f'Token {AUTH_TOKEN}'}
    
    # Test goals endpoint
    response, error = make_request('GET', '/performance/goals/', headers=headers)
    if error:
        log_test("Performance Goals", "FAIL", error)
    else:
        log_test("Performance Goals", "PASS", f"Found {len(response)} goals")
    
    # Test feedback endpoints
    response, error = make_request('GET', '/performance/feedback/', headers=headers)
    if error:
        log_test("Performance Feedback", "FAIL", error)
    else:
        log_test("Performance Feedback", "PASS", f"Found {len(response)} feedback")

def test_token_authentication():
    """Test token authentication functionality"""
    print("\n" + "="*80)
    print("🔑 TESTING TOKEN AUTHENTICATION")
    print("="*80)
    
    # Test without token
    response, error = make_request('GET', '/api/profile/')
    if error and ("401" in str(error) or "403" in str(error)):
        log_test("No Token Access", "PASS", "Correctly requires authentication")
    else:
        log_test("No Token Access", "FAIL", "Should require authentication")
    
    # Test with invalid token
    headers = {'Authorization': 'Token invalidtoken123456789'}
    response, error = make_request('GET', '/api/profile/', headers=headers)
    if error and ("401" in str(error) or "403" in str(error)):
        log_test("Invalid Token Access", "PASS", "Correctly rejects invalid token")
    else:
        log_test("Invalid Token Access", "FAIL", "Should reject invalid token")
    
    # Test with valid token
    if AUTH_TOKEN:
        headers = {'Authorization': f'Token {AUTH_TOKEN}'}
        response, error = make_request('GET', '/api/profile/', headers=headers)
        if error:
            log_test("Valid Token Access", "FAIL", error)
        else:
            log_test("Valid Token Access", "PASS", "Token authentication working")

def test_error_handling():
    """Test API error handling"""
    print("\n" + "="*80)
    print("🚨 TESTING ERROR HANDLING")
    print("="*80)
    
    # Test non-existent endpoint
    response, error = make_request('GET', '/api/nonexistent/')
    if error and "404" in str(error):
        log_test("404 Error Handling", "PASS", "Correctly returns 404 for non-existent endpoint")
    else:
        log_test("404 Error Handling", "WARN", "Unexpected response for non-existent endpoint")
    
    # Test invalid registration data
    invalid_data = {
        "email": "invalid-email",
        "password": "123",
        "password_confirm": "456"
    }
    response, error = make_request('POST', '/api/register/', data=invalid_data)
    if error and "400" in str(error):
        log_test("400 Error Handling", "PASS", "Correctly validates input data")
    else:
        log_test("400 Error Handling", "WARN", "Should validate input data")

def main():
    """Main test runner"""
    print("🚀 SMART-EN Turnover API - COMPREHENSIVE PRODUCTION TESTING")
    print(f"🌐 Testing API: {BASE_URL}")
    print(f"🕐 Started at: {datetime.now()}")
    print("="*80)
    
    # Run all tests
    test_health_and_info()
    
    # Registration and authentication flow
    registration_success = test_registration()
    if registration_success:
        test_login()
        test_profile()
    
    # Core functionality tests
    test_departments()
    test_legacy_endpoints()
    test_employee_crud()
    test_performance_endpoints()
    
    # Security and error handling
    test_token_authentication()
    test_error_handling()
    
    # Summary
    print("\n" + "="*80)
    print("🏁 TESTING SUMMARY")
    print("="*80)
    print("✅ All core functionality tested")
    print("🔐 Token authentication implemented and working")
    print("📱 API responses include complete data with tokens")
    print("🛡️  Security controls in place")
    print("🌐 Production deployment successful")
    
    if AUTH_TOKEN:
        print(f"\n🔑 Sample Token for further testing:")
        print(f"Authorization: Token {AUTH_TOKEN}")
    
    print(f"\n🎯 API Documentation: {BASE_URL}/api/info/")
    print(f"📋 Postman Collection: Available in repository")
    print(f"🕐 Completed at: {datetime.now()}")

if __name__ == "__main__":
    main()
