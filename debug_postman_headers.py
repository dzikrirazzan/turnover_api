#!/usr/bin/env python3
"""
Debug script untuk test berbagai kombinasi header Postman
"""

import requests
import json

def debug_postman_headers():
    """Test berbagai kombinasi header untuk menemukan masalah CSRF"""
    
    base_url = "https://turnover-api-hd7ze.ondigitalocean.app"
    
    print("🔍 Debugging Postman CSRF issue...")
    print(f"🌐 API URL: {base_url}")
    print()
    
    # Data minimal untuk test
    test_data = {
        "email": "debug.test@smarten.com",
        "password": "SecurePass123!",
        "password_confirm": "SecurePass123!",
        "first_name": "Debug",
        "last_name": "Test",
        "department": 1,
        "position": "Developer"
    }
    
    # Test 1: Basic headers (tanpa referer)
    print("1️⃣ Testing with basic headers (no referer)...")
    basic_headers = {
        "Content-Type": "application/json",
        "User-Agent": "PostmanRuntime/7.32.3"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/register/",
            json=test_data,
            headers=basic_headers
        )
        print(f"Status: {response.status_code}")
        if "CSRF" in response.text:
            print("❌ CSRF error with basic headers")
        else:
            print("✅ No CSRF error with basic headers")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test 2: Dengan referer header
    print("2️⃣ Testing with referer header...")
    referer_headers = basic_headers.copy()
    referer_headers["Referer"] = "https://postman.com"
    
    try:
        response = requests.post(
            f"{base_url}/api/register/",
            json=test_data,
            headers=referer_headers
        )
        print(f"Status: {response.status_code}")
        if "CSRF" in response.text:
            print("❌ CSRF error with referer header")
            print("This is likely the Postman issue!")
        else:
            print("✅ No CSRF error with referer header")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test 3: Dengan origin header
    print("3️⃣ Testing with origin header...")
    origin_headers = basic_headers.copy()
    origin_headers["Origin"] = "https://postman.com"
    
    try:
        response = requests.post(
            f"{base_url}/api/register/",
            json=test_data,
            headers=origin_headers
        )
        print(f"Status: {response.status_code}")
        if "CSRF" in response.text:
            print("❌ CSRF error with origin header")
        else:
            print("✅ No CSRF error with origin header")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test 4: Dengan kedua header
    print("4️⃣ Testing with both referer and origin...")
    both_headers = basic_headers.copy()
    both_headers["Referer"] = "https://postman.com"
    both_headers["Origin"] = "https://postman.com"
    
    try:
        response = requests.post(
            f"{base_url}/api/register/",
            json=test_data,
            headers=both_headers
        )
        print(f"Status: {response.status_code}")
        if "CSRF" in response.text:
            print("❌ CSRF error with both headers")
        else:
            print("✅ No CSRF error with both headers")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test 5: Dengan empty referer
    print("5️⃣ Testing with empty referer...")
    empty_referer_headers = basic_headers.copy()
    empty_referer_headers["Referer"] = ""
    
    try:
        response = requests.post(
            f"{base_url}/api/register/",
            json=test_data,
            headers=empty_referer_headers
        )
        print(f"Status: {response.status_code}")
        if "CSRF" in response.text:
            print("❌ CSRF error with empty referer")
        else:
            print("✅ No CSRF error with empty referer")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("🎯 Analysis:")
    print("- If test 2 shows CSRF error, that's the Postman issue")
    print("- Postman automatically sends referer header")
    print("- Need to update CSRF_TRUSTED_ORIGINS in DigitalOcean")

if __name__ == "__main__":
    debug_postman_headers() 