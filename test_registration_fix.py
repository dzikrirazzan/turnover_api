#!/usr/bin/env python
"""
Test script to verify the registration endpoint is working.
Run this after deploying the fix to confirm everything is working.
"""
import requests
import json
import sys

def test_registration():
    """Test the registration endpoint with sample data."""
    url = "https://turnover-api-hd7ze.ondigitalocean.app/api/auth/register/"
    
    test_cases = [
        {
            "name": "Valid Registration",
            "data": {
                "email": "test_final@example.com",
                "first_name": "Final",
                "last_name": "Test",
                "employee_id": "EMP_FINAL_001",
                "phone_number": "08123456789",
                "password": "testpassword123",
                "password_confirm": "testpassword123"
            },
            "expected_status": 201
        },
        {
            "name": "Duplicate Email",
            "data": {
                "email": "test_final@example.com",  # Same email as above
                "first_name": "Duplicate",
                "last_name": "Test",
                "employee_id": "EMP_DUP_001",
                "phone_number": "08123456789",
                "password": "testpassword123",
                "password_confirm": "testpassword123"
            },
            "expected_status": 400
        }
    ]
    
    print("🧪 Testing Registration Endpoint")
    print("=" * 50)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test['name']}")
        print(f"   Data: {test['data']['email']}, {test['data']['employee_id']}")
        
        try:
            response = requests.post(url, json=test['data'], timeout=30)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == test['expected_status']:
                print("   ✅ PASSED")
            else:
                print(f"   ❌ FAILED - Expected {test['expected_status']}, got {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.RequestException as e:
            print(f"   ❌ ERROR: {e}")
    
    print("\n" + "=" * 50)

def test_login():
    """Test login with a registered user."""
    login_url = "https://turnover-api-hd7ze.ondigitalocean.app/api/auth/login/"
    
    login_data = {
        "email": "test_final@example.com",
        "password": "testpassword123"
    }
    
    print("\n🔐 Testing Login Endpoint")
    print("=" * 50)
    
    try:
        response = requests.post(login_url, json=login_data, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login working!")
            data = response.json()
            if 'access_token' in data:
                print("✅ Access token received")
            else:
                print("⚠️ No access token in response")
        else:
            print(f"❌ Login failed: {response.text}")
            
    except requests.RequestException as e:
        print(f"❌ ERROR: {e}")

def main():
    print("🚀 Testing Turnover API Registration Fix")
    print("🌐 API Base: https://turnover-api-hd7ze.ondigitalocean.app")
    print("📅 Test Date: July 2, 2025")
    
    test_registration()
    test_login()
    
    print("\n🎉 Testing completed!")
    print("\nIf registration is working, the 'field registernya' issue is fixed! 🎊")

if __name__ == '__main__':
    main()
