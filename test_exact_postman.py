#!/usr/bin/env python3
"""
Test yang meniru Postman secara tepat
"""

import requests
import json

def test_exact_postman():
    """Test yang meniru Postman secara tepat"""
    
    base_url = "https://turnover-api-hd7ze.ondigitalocean.app"
    
    print("🧪 Testing exact Postman behavior...")
    print(f"🌐 API URL: {base_url}")
    print()
    
    # Data yang sama dengan user
    test_data = {
        "email": "exact.test@smarten.com",
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
        "salary": "medium",  # ✅ Correct value
        "salary_amount": 8000000
    }
    
    # Headers yang sama persis dengan Postman
    postman_headers = {
        "Content-Type": "application/json",
        "User-Agent": "PostmanRuntime/7.32.3",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    }
    
    print("1️⃣ Testing with exact Postman headers...")
    try:
        response = requests.post(
            f"{base_url}/api/register/",
            json=test_data,
            headers=postman_headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:300]}...")
        
        if response.status_code == 201:
            print("✅ SUCCESS! Exact Postman headers work")
        elif response.status_code == 400:
            print("⚠️ Validation error (normal)")
        elif "CSRF" in response.text:
            print("❌ CSRF error with exact Postman headers")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test dengan referer yang mungkin dikirim Postman
    print("2️⃣ Testing with possible Postman referer...")
    
    # Coba berbagai kemungkinan referer yang dikirim Postman
    possible_referers = [
        "https://postman.com",
        "https://www.postman.com", 
        "https://app.postman.com",
        "https://web.postman.com",
        "https://go.postman.co",
        "https://postman-echo.com",
        "https://turnover-api-hd7ze.ondigitalocean.app",
        "",
        None
    ]
    
    for referer in possible_referers:
        headers = postman_headers.copy()
        if referer:
            headers["Referer"] = referer
        
        try:
            response = requests.post(
                f"{base_url}/api/register/",
                json=test_data,
                headers=headers
            )
            
            referer_name = referer if referer else "No Referer"
            print(f"  {referer_name}: {response.status_code}")
            
            if "CSRF" in response.text:
                print(f"    ❌ CSRF error with referer: {referer_name}")
                print(f"    This might be the issue!")
            else:
                print(f"    ✅ No CSRF error with referer: {referer_name}")
                
        except Exception as e:
            print(f"    ❌ Error with {referer_name}: {e}")
    
    print()
    print("🎯 Analysis:")
    print("- If any test shows CSRF error, that's the Postman issue")
    print("- Check which referer causes CSRF error")
    print("- Update CSRF_TRUSTED_ORIGINS accordingly")

if __name__ == "__main__":
    test_exact_postman() 