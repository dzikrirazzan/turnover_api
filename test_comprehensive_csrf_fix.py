#!/usr/bin/env python3
"""
Test script untuk memastikan CSRF sudah benar-benar disabled untuk API endpoints
"""

import requests
import json
import time

BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"

def test_csrf_fix():
    print("🔧 TESTING COMPREHENSIVE CSRF FIX")
    print("=" * 60)
    
    # Test data registrasi
    timestamp = int(time.time())
    test_data = {
        "email": f"test.{timestamp}@smarten.com",
        "password": "SecurePass123!",
        "password_confirm": "SecurePass123!",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "+6281234567890",
        "date_of_birth": "1990-05-15",
        "gender": "M",
        "marital_status": "single",
        "education_level": "bachelor",
        "address": "Test Address",
        "position": "Test Position",
        "department": 1,
        "hire_date": "2024-01-15"
    }
    
    print("🧪 Test 1: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/api/health/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Health Check OK")
        else:
            print("   ❌ Health Check Failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🧪 Test 2: Registration (CSRF Critical Test)")
    try:
        # Test dengan berbagai header combinations
        headers_combinations = [
            {
                'Content-Type': 'application/json',
                'User-Agent': 'PostmanRuntime/7.29.2'
            },
            {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                'Referer': 'https://web.postman.co/',
                'Origin': 'https://web.postman.co'
            },
            {
                'Content-Type': 'application/json',
                'User-Agent': 'curl/7.68.0'
            }
        ]
        
        for i, headers in enumerate(headers_combinations):
            print(f"\n   Test 2.{i+1}: Headers {list(headers.keys())}")
            test_data["email"] = f"test.{timestamp}.{i}@smarten.com"
            
            response = requests.post(
                f"{BASE_URL}/api/register/",
                json=test_data,
                headers=headers
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 201:
                print("   ✅ SUCCESS - CSRF BYPASS WORKING!")
                return True
            elif response.status_code == 400:
                error_data = response.json()
                if "email" in error_data.get("errors", {}):
                    print("   ✅ SUCCESS - Email exists (expected)")
                    return True
                else:
                    print(f"   ⚠️  Validation error: {error_data}")
            elif response.status_code == 403:
                error_data = response.json()
                if "CSRF" in str(error_data):
                    print("   ❌ CSRF ERROR STILL EXISTS!")
                    print(f"   Response: {error_data}")
                else:
                    print(f"   ❌ 403 Forbidden: {error_data}")
            else:
                print(f"   ❌ Unexpected status: {response.text}")
                
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    return False

if __name__ == "__main__":
    success = test_csrf_fix()
    print("\n" + "=" * 60)
    if success:
        print("🎉 CSRF FIX CONFIRMED - API READY FOR POSTMAN!")
    else:
        print("❌ CSRF ERROR STILL EXISTS - NEED MORE INVESTIGATION")
    print("=" * 60)
