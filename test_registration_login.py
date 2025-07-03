#!/usr/bin/env python3
"""
Test script untuk registrasi dan login API dengan data lengkap
"""

import requests
import json
from datetime import datetime

# Base URL
BASE_URL = "http://127.0.0.1:8000"

# Data registrasi yang Anda berikan
registration_data = {
    "email": "employeejon@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+6281234567890",
    "date_of_birth": "1990-05-10",
    "gender": "M",
    "marital_status": "single",
    "education_level": "bachelor",
    "address": "Jl. Contoh No. 123, Jakarta",
    "position": "Junior Staff",
    "department": 1, 
    "hire_date": "2023-01-01"
}

# Data login
login_data = {
    "email": "employeejon@example.com",
    "password": "securepassword123"
}

def test_api_request(method, endpoint, data=None, headers=None):
    """Helper function untuk testing API"""
    url = f"{BASE_URL}{endpoint}"
    
    # Configure session
    session = requests.Session()
    session.verify = False  # Disable SSL verification
    
    try:
        print(f"\n{'='*60}")
        print(f"🔍 {method.upper()} {endpoint}")
        
        if method.upper() == 'GET':
            response = session.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = session.post(url, json=data, headers=headers)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📝 Response Headers: {dict(response.headers)}")
        
        # Try to parse JSON
        try:
            response_json = response.json()
            print(f"📄 Response Data:")
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
            return response_json
        except:
            print(f"📄 Response Text: {response.text[:500]}...")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("🚀 Testing SMART-EN API Registration & Login")
    print(f"🕐 Started at: {datetime.now()}")
    
    # Test 1: Health Check
    print("\n" + "="*80)
    print("📋 TEST 1: Health Check")
    test_api_request("GET", "/api/health/")
    
    # Test 2: Registration dengan data lengkap
    print("\n" + "="*80)
    print("📋 TEST 2: Employee Registration")
    print("📤 Registration Data:")
    print(json.dumps(registration_data, indent=2, ensure_ascii=False))
    
    registration_response = test_api_request("POST", "/api/register/", registration_data)
    
    # Test 3: Login
    print("\n" + "="*80)
    print("📋 TEST 3: Employee Login")
    print("📤 Login Data:")
    print(json.dumps(login_data, indent=2, ensure_ascii=False))
    
    login_response = test_api_request("POST", "/api/login/", login_data)
    
    # Test 4: Get User Profile (jika login berhasil)
    if login_response and 'user' in login_response and 'token' in login_response['user']:
        token = login_response['user']['token']
        headers = {'Authorization': f'Token {token}'}
        
        print("\n" + "="*80)
        print("📋 TEST 4: Get User Profile with Token")
        print(f"🔑 Using Token: {token}")
        
        test_api_request("GET", "/api/profile/", headers=headers)
    
    print("\n" + "="*80)
    print("✅ Testing Complete!")
    print("\n📋 EXPECTED IMPROVEMENTS:")
    print("1. ✅ Registration should return complete employee data")
    print("2. ✅ Login should return user data with authentication token")
    print("3. ✅ Profile endpoint should return consistent data")
    print("4. ✅ Token authentication should work for protected endpoints")

if __name__ == "__main__":
    main()
