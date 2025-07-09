#!/usr/bin/env python3
"""
Test script untuk simulasi Postman secara tepat
"""

import requests
import json

def test_postman_simulation():
    """Simulasi Postman secara tepat"""
    
    base_url = "https://turnover-api-hd7ze.ondigitalocean.app"
    
    print("🧪 Simulating Postman behavior...")
    print(f"🌐 API URL: {base_url}")
    print()
    
    # Test data yang sama dengan user
    test_data = {
        "email": "test.user@smarten.com",
        "password": "SecurePass123!",
        "password_confirm": "SecurePass123!",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "+6281234567890",
        "date_of_birth": "1990-05-15",
        "gender": "M",
        "marital_status": "single",
        "education_level": "bachelor",
        "address": "Test Address Jakarta",
        "position": "Test Position",
        "department": 1,
        "hire_date": "2024-01-15",
        "salary": "middle",
        "salary_amount": 8000000
    }
    
    # Headers yang sama dengan Postman
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "PostmanRuntime/7.32.3",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    }
    
    print("1️⃣ Testing with Postman-like headers...")
    try:
        response = requests.post(
            f"{base_url}/api/register/",
            json=test_data,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:300]}...")
        
        if response.status_code == 201:
            print("✅ Success with Postman-like headers")
        elif "CSRF" in response.text:
            print("❌ CSRF error with Postman-like headers")
        else:
            print(f"⚠️ Other response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test dengan referer header (yang mungkin menyebabkan masalah)
    print("2️⃣ Testing with Referer header (Postman behavior)...")
    
    headers_with_referer = headers.copy()
    headers_with_referer["Referer"] = "https://postman.com"
    
    try:
        response = requests.post(
            f"{base_url}/api/register/",
            json=test_data,
            headers=headers_with_referer
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:300]}...")
        
        if response.status_code == 201:
            print("✅ Success with Referer header")
        elif "CSRF" in response.text:
            print("❌ CSRF error with Referer header")
            print("This is likely the issue!")
        else:
            print(f"⚠️ Other response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test dengan origin header
    print("3️⃣ Testing with Origin header...")
    
    headers_with_origin = headers.copy()
    headers_with_origin["Origin"] = "https://postman.com"
    
    try:
        response = requests.post(
            f"{base_url}/api/register/",
            json=test_data,
            headers=headers_with_origin
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:300]}...")
        
        if response.status_code == 201:
            print("✅ Success with Origin header")
        elif "CSRF" in response.text:
            print("❌ CSRF error with Origin header")
        else:
            print(f"⚠️ Other response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("🎯 Analysis:")
    print("- If test 2 shows CSRF error, that's the Postman issue")
    print("- Postman sends Referer header automatically")
    print("- Django checks Referer against CSRF_TRUSTED_ORIGINS")

if __name__ == "__main__":
    test_postman_simulation() 