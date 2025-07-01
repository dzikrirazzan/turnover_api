#!/usr/bin/env python3
"""
SMART-EN System - Deployment Diagnosis Script
Test berbagai endpoint dan konfigurasi untuk debugging deployment
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def test_endpoint(endpoint, method="GET", data=None, auth=None, headers=None):
    """Test endpoint dengan berbagai konfigurasi"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if headers is None:
            headers = {}
        
        # Add common headers
        headers.update({
            'User-Agent': 'SMART-EN-Diagnosis/1.0',
            'Accept': 'application/json',
        })
        
        if method == "GET":
            response = requests.get(url, auth=auth, headers=headers, timeout=10)
        elif method == "POST":
            headers['Content-Type'] = 'application/json'
            response = requests.post(url, json=data, auth=auth, headers=headers, timeout=10)
        
        print(f"📍 {method} {endpoint}")
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code < 400:
            try:
                content = response.json()
                print(f"   Response: {json.dumps(content, indent=2)[:200]}...")
            except:
                print(f"   Content: {response.text[:200]}...")
        else:
            print(f"   Error: {response.text[:200]}...")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    print("🚀 SMART-EN SYSTEM - DEPLOYMENT DIAGNOSIS")
    print(f"🎯 Target: {BASE_URL}")
    print(f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Basic connectivity
    print_header("1. BASIC CONNECTIVITY TESTS")
    test_endpoint("/")
    test_endpoint("")
    test_endpoint("/health/")
    test_endpoint("/api/")
    
    # Test 2: Different host headers
    print_header("2. HOST HEADER TESTS")
    custom_headers = [
        {"Host": "turnover-api-hd7ze.ondigitalocean.app"},
        {"Host": "localhost:8000"},
        {"X-Forwarded-Host": "turnover-api-hd7ze.ondigitalocean.app"},
    ]
    
    for header in custom_headers:
        print(f"\n--- Testing with headers: {header} ---")
        test_endpoint("/api/", headers=header)
    
    # Test 3: CORS tests
    print_header("3. CORS CONFIGURATION TESTS")
    cors_headers = {
        "Origin": "https://smart-en-system.vercel.app",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "Authorization,Content-Type"
    }
    test_endpoint("/api/employees/", headers=cors_headers)
    
    # Test 4: Authentication endpoints
    print_header("4. AUTHENTICATION ENDPOINTS")
    
    # Test registration
    register_data = {
        "username": "testuser",
        "email": "test@example.com", 
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    test_endpoint("/api/auth/register/", "POST", register_data)
    
    # Test login
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    test_endpoint("/api/auth/login/", "POST", login_data)
    
    # Test 5: Different URL patterns
    print_header("5. URL PATTERN TESTS")
    url_patterns = [
        "/api/employees/",
        "/predictions/",
        "/performance/",
        "/admin/",
        "/api/departments/",
        "/api/predictions/",
        "/performance/api/",
        "/predictions/api/",
    ]
    
    for pattern in url_patterns:
        test_endpoint(pattern)
    
    # Test 6: With authentication
    print_header("6. BASIC AUTH TESTS")
    auth = ("admin", "admin123")
    
    auth_endpoints = [
        "/api/employees/",
        "/api/departments/", 
        "/api/predictions/",
        "/performance/api/dashboard/stats/?employee=1",
        "/performance/api/analytics/dashboard/",
    ]
    
    for endpoint in auth_endpoints:
        test_endpoint(endpoint, auth=auth)
    
    # Test 7: Django admin
    print_header("7. DJANGO ADMIN TEST")
    test_endpoint("/admin/")
    test_endpoint("/admin/login/")
    
    print_header("🎯 DIAGNOSIS COMPLETE")
    print("📋 CHECK RESULTS ABOVE FOR SPECIFIC ISSUES")
    
    # Diagnosis recommendations
    print("\n📝 COMMON ISSUES & SOLUTIONS:")
    print("1. HTTP 400 Bad Request:")
    print("   - ALLOWED_HOSTS tidak include domain DigitalOcean")
    print("   - CORS settings salah")
    print("   - Missing environment variables")
    
    print("\n2. HTTP 404 Not Found:")
    print("   - URL pattern salah di urls.py")
    print("   - Static files tidak ter-serve")
    
    print("\n3. HTTP 500 Internal Server Error:")
    print("   - Database connection error")
    print("   - Missing dependencies")
    print("   - Environment variables tidak set")
    
    print(f"\n🔧 NEXT STEPS:")
    print("1. Check DigitalOcean App Platform logs")
    print("2. Verify environment variables")
    print("3. Check ALLOWED_HOSTS setting")
    print("4. Test database connection")

if __name__ == "__main__":
    main()
