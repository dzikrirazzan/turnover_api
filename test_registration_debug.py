#!/usr/bin/env python3
"""
Quick registration test to debug the 400 error
"""

import requests
import json

BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"

def test_registration_detailed():
    """Test registration with detailed error reporting"""
    
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
    
    print("🔍 Testing registration with detailed error reporting...")
    print(f"📤 Sending data to: {BASE_URL}/api/register/")
    print(f"📋 Data: {json.dumps(registration_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/register/",
            json=registration_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"\n📊 Response Status: {response.status_code}")
        print(f"📝 Response Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"📄 Response Body (JSON):")
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
        except:
            print(f"📄 Response Body (Text):")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_unique_email():
    """Test with a unique email to avoid conflicts"""
    
    # Generate unique email with timestamp
    import time
    timestamp = int(time.time())
    
    registration_data = {
        "email": f"test{timestamp}@example.com",
        "password": "passwordjikri",
        "password_confirm": "passwordjikri",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "+6281234567999",
        "date_of_birth": "1990-05-11",
        "gender": "M",
        "marital_status": "single",
        "education_level": "bachelor",
        "address": "Jl. Test No. 123, Jakarta",
        "position": "Test Position",
        "department": 1,
        "hire_date": "2023-01-01"
    }
    
    print("\n" + "="*60)
    print("🔍 Testing registration with unique email...")
    print(f"📤 Sending data to: {BASE_URL}/api/register/")
    print(f"📧 Using email: {registration_data['email']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/register/",
            json=registration_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"\n📊 Response Status: {response.status_code}")
        
        try:
            response_json = response.json()
            print(f"📄 Response Body:")
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
            
            # Test login if registration successful
            if response.status_code == 201 and 'employee' in response_json:
                print("\n" + "="*60)
                print("🔐 Testing login with registered user...")
                
                login_data = {
                    "email": registration_data['email'],
                    "password": registration_data['password']
                }
                
                login_response = requests.post(
                    f"{BASE_URL}/api/login/",
                    json=login_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                print(f"📊 Login Status: {login_response.status_code}")
                try:
                    login_json = login_response.json()
                    print(f"📄 Login Response:")
                    print(json.dumps(login_json, indent=2, ensure_ascii=False))
                except:
                    print(f"📄 Login Response Text: {login_response.text}")
                
        except:
            print(f"📄 Response Body (Text): {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_registration_detailed()
    test_unique_email()
