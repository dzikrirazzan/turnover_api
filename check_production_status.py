#!/usr/bin/env python3
"""
Check production status dan environment variables
"""

import requests
import json

def check_production_status():
    """Check status production dan environment"""
    
    base_url = "https://turnover-api-hd7ze.ondigitalocean.app"
    
    print("🔍 Checking production status...")
    print(f"🌐 API URL: {base_url}")
    print()
    
    # Test 1: Health check
    print("1️⃣ Health check...")
    try:
        response = requests.get(f"{base_url}/api/health/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ API is running")
        else:
            print("❌ API not responding")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test 2: API info
    print("2️⃣ API info...")
    try:
        response = requests.get(f"{base_url}/api/info/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Name: {data.get('data', {}).get('api_name', 'Unknown')}")
            print(f"✅ Version: {data.get('data', {}).get('version', 'Unknown')}")
        else:
            print("❌ API info not available")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test 3: CSRF test dengan referer yang berbeda
    print("3️⃣ CSRF test with different referer...")
    
    test_data = {
        "email": "status.test@smarten.com",
        "password": "SecurePass123!",
        "password_confirm": "SecurePass123!",
        "first_name": "Status",
        "last_name": "Test",
        "department": 1,
        "position": "Developer"
    }
    
    # Test dengan referer yang berbeda-beda
    referer_tests = [
        ("https://postman.com", "Postman"),
        ("https://www.postman.com", "Postman WWW"),
        ("https://app.postman.com", "Postman App"),
        ("https://turnover-api-hd7ze.ondigitalocean.app", "API Domain"),
        ("", "Empty Referer"),
        (None, "No Referer")
    ]
    
    for referer, description in referer_tests:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "PostmanRuntime/7.32.3"
        }
        
        if referer:
            headers["Referer"] = referer
        
        try:
            response = requests.post(
                f"{base_url}/api/register/",
                json=test_data,
                headers=headers
            )
            
            print(f"  {description}: {response.status_code}")
            if "CSRF" in response.text:
                print(f"    ❌ CSRF error with {description}")
            else:
                print(f"    ✅ No CSRF error with {description}")
                
        except Exception as e:
            print(f"    ❌ Error with {description}: {e}")
    
    print()
    print("🎯 Production Status:")
    print("- If all tests show ✅, CSRF fix is working")
    print("- If any test shows ❌ CSRF, environment needs update")
    print("- Check DigitalOcean dashboard for environment variables")

if __name__ == "__main__":
    check_production_status() 