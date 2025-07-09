#!/usr/bin/env python3
"""
Test dengan data yang benar untuk verifikasi API
"""

import requests
import json

def test_correct_data():
    """Test dengan data yang benar"""
    
    base_url = "https://turnover-api-hd7ze.ondigitalocean.app"
    
    print("🧪 Testing with correct data format...")
    print(f"🌐 API URL: {base_url}")
    print()
    
    # Data yang benar sesuai model
    correct_data = {
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
        "salary": "medium",  # ✅ Correct: 'medium' not 'middle'
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
    
    print("1️⃣ Testing with correct salary value ('medium')...")
    try:
        response = requests.post(
            f"{base_url}/api/register/",
            json=correct_data,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:400]}...")
        
        if response.status_code == 201:
            print("✅ SUCCESS! Registration works with correct data")
            print("🎉 CSRF fix is working properly!")
        elif response.status_code == 400:
            print("⚠️ Validation error (check response for details)")
            print("This might be due to department ID not existing")
        elif "CSRF" in response.text:
            print("❌ CSRF error still present")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test dengan data minimal (tanpa salary)
    print("2️⃣ Testing with minimal data (no salary)...")
    
    minimal_data = {
        "email": "test.minimal@smarten.com",
        "password": "SecurePass123!",
        "password_confirm": "SecurePass123!",
        "first_name": "Test",
        "last_name": "Minimal",
        "department": 1,
        "position": "Developer"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/register/",
            json=minimal_data,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:400]}...")
        
        if response.status_code == 201:
            print("✅ SUCCESS! Minimal registration works")
        elif response.status_code == 400:
            print("⚠️ Validation error with minimal data")
        elif "CSRF" in response.text:
            print("❌ CSRF error with minimal data")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("🎯 Summary:")
    print("- If you see ✅ SUCCESS, CSRF fix is working")
    print("- If you see ❌ CSRF error, environment variables need update")
    print("- If you see ⚠️ validation error, that's normal (data issues)")

if __name__ == "__main__":
    test_correct_data() 