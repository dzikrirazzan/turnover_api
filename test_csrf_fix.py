#!/usr/bin/env python3
"""
Test script untuk verifikasi CSRF fix
"""

import requests
import json
import sys

def test_csrf_fix():
    """Test apakah CSRF fix sudah bekerja"""
    
    base_url = "https://turnover-api-hd7ze.ondigitalocean.app"
    
    print("🧪 Testing CSRF fix...")
    print(f"🌐 API URL: {base_url}")
    print()
    
    # Test 1: Health check
    print("1️⃣ Testing health check...")
    try:
        response = requests.get(f"{base_url}/api/health/")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    print()
    
    # Test 2: Register endpoint (CSRF test)
    print("2️⃣ Testing register endpoint (CSRF test)...")
    
    test_data = {
        "email": "test_csrf@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test",
        "last_name": "CSRF",
        "department": 1,
        "position": "Developer"
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "PostmanRuntime/7.32.3"  # Simulate Postman
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/register/",
            json=test_data,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 201:
            print("✅ Register endpoint works (CSRF fix successful!)")
        elif response.status_code == 400:
            print("⚠️ Register endpoint responded but with validation error (CSRF might be fixed)")
            print("This is normal if department ID doesn't exist")
        elif "CSRF" in response.text:
            print("❌ CSRF error still present")
            print("Environment variables need to be updated")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Register test error: {e}")
    
    print()
    
    # Test 3: Login endpoint
    print("3️⃣ Testing login endpoint...")
    
    login_data = {
        "email": "test_csrf@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/login/",
            json=login_data,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login endpoint works")
        elif response.status_code == 400:
            print("⚠️ Login failed (user might not exist)")
        elif "CSRF" in response.text:
            print("❌ CSRF error in login endpoint")
        else:
            print(f"❌ Unexpected login response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Login test error: {e}")
    
    print()
    print("🎯 Test Summary:")
    print("- If you see ✅ for register/login, CSRF fix is working")
    print("- If you see ❌ with CSRF errors, update environment variables")
    print("- If you see ⚠️, that's normal (validation errors)")

if __name__ == "__main__":
    test_csrf_fix() 