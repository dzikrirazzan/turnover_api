#!/usr/bin/env python3
"""
Test untuk memverifikasi konsistensi response antara Register dan Login
"""

import requests
import json
from datetime import datetime

# Base URL production
BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"

def test_registration_login_consistency():
    """Test konsistensi response antara registration dan login"""
    print("🧪 Testing Registration vs Login Response Consistency")
    print(f"🕐 Test started at: {datetime.now()}")
    print(f"🌐 Base URL: {BASE_URL}")
    
    # Data registrasi unik
    timestamp = int(datetime.now().timestamp())
    test_data = {
        "email": f"consistency_test_{timestamp}@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Consistency",
        "last_name": "Test",
        "phone_number": f"+628123456{timestamp % 10000}",
        "date_of_birth": "1992-01-01",
        "gender": "M",
        "marital_status": "single",
        "education_level": "bachelor",
        "address": "Test Address for Consistency Check",
        "position": "Test Position",
        "department": 1,
        "hire_date": "2024-01-01"
    }
    
    print("\n" + "="*80)
    print("📝 STEP 1: Registration")
    print("="*80)
    
    # Test Registration
    try:
        reg_response = requests.post(
            f"{BASE_URL}/api/register/",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📊 Registration Status: {reg_response.status_code}")
        
        if reg_response.status_code == 201:
            reg_data = reg_response.json()
            print("✅ Registration successful!")
            print("📄 Registration Response Fields:")
            
            if 'employee' in reg_data:
                reg_fields = list(reg_data['employee'].keys())
                reg_fields.sort()
                for field in reg_fields:
                    print(f"   • {field}: {type(reg_data['employee'][field]).__name__}")
                
                # Extract data for login test
                email = reg_data['employee']['email']
                expected_token = reg_data['employee']['token']
                
                print(f"\n🔑 Generated Token: {expected_token[:20]}...")
                
        else:
            print(f"❌ Registration failed: {reg_response.text}")
            return
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    print("\n" + "="*80)
    print("📝 STEP 2: Login")
    print("="*80)
    
    # Test Login
    try:
        login_data = {
            "email": email,
            "password": "testpass123"
        }
        
        login_response = requests.post(
            f"{BASE_URL}/api/login/",
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📊 Login Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            print("✅ Login successful!")
            print("📄 Login Response Fields:")
            
            if 'user' in login_data:
                login_fields = list(login_data['user'].keys())
                login_fields.sort()
                for field in login_fields:
                    print(f"   • {field}: {type(login_data['user'][field]).__name__}")
                
                login_token = login_data['user']['token']
                print(f"\n🔑 Login Token: {login_token[:20]}...")
                
        else:
            print(f"❌ Login failed: {login_response.text}")
            return
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    print("\n" + "="*80)
    print("📝 STEP 3: Response Comparison")
    print("="*80)
    
    # Compare responses
    reg_employee = reg_data['employee']
    login_user = login_data['user']
    
    # Get all unique fields
    reg_fields = set(reg_employee.keys())
    login_fields = set(login_user.keys())
    all_fields = reg_fields.union(login_fields)
    
    print("🔍 Field Comparison:")
    print(f"📊 Registration fields: {len(reg_fields)}")
    print(f"📊 Login fields: {len(login_fields)}")
    print(f"📊 Total unique fields: {len(all_fields)}")
    
    # Fields only in registration
    reg_only = reg_fields - login_fields
    if reg_only:
        print(f"\n🟡 Fields ONLY in Registration ({len(reg_only)}):")
        for field in sorted(reg_only):
            print(f"   • {field}")
    
    # Fields only in login
    login_only = login_fields - reg_fields
    if login_only:
        print(f"\n🟡 Fields ONLY in Login ({len(login_only)}):")
        for field in sorted(login_only):
            print(f"   • {field}")
    
    # Common fields
    common_fields = reg_fields.intersection(login_fields)
    print(f"\n✅ Common Fields ({len(common_fields)}):")
    
    # Check for value differences in common fields
    differences = []
    for field in sorted(common_fields):
        reg_value = reg_employee[field]
        login_value = login_user[field]
        
        if reg_value != login_value:
            differences.append({
                'field': field,
                'registration': reg_value,
                'login': login_value
            })
            print(f"   ⚠️  {field}: REG={reg_value} vs LOGIN={login_value}")
        else:
            print(f"   ✅ {field}: {reg_value}")
    
    print("\n" + "="*80)
    print("📝 STEP 4: Token Consistency Check")
    print("="*80)
    
    if expected_token == login_token:
        print("✅ Tokens are CONSISTENT between registration and login")
    else:
        print("⚠️  Tokens are DIFFERENT:")
        print(f"   Registration: {expected_token}")
        print(f"   Login: {login_token}")
    
    print("\n" + "="*80)
    print("📋 SUMMARY")
    print("="*80)
    
    if not reg_only and not login_only and not differences:
        print("🎉 PERFECT! Registration and Login responses are 100% CONSISTENT!")
    else:
        print("📝 Response Consistency Analysis:")
        print(f"   • Fields only in Registration: {len(reg_only)}")
        print(f"   • Fields only in Login: {len(login_only)}")
        print(f"   • Value differences: {len(differences)}")
        
        if reg_only or login_only:
            print("\n💡 RECOMMENDATION: Consider making responses identical for better frontend consistency")
        
        if differences:
            print("\n⚠️  VALUE DIFFERENCES found - this might be expected (e.g., timestamps)")
    
    # Test authentication with token
    print("\n" + "="*80)
    print("📝 STEP 5: Token Authentication Test")
    print("="*80)
    
    headers = {'Authorization': f'Token {login_token}'}
    profile_response = requests.get(f"{BASE_URL}/api/profile/", headers=headers)
    
    print(f"📊 Profile endpoint status: {profile_response.status_code}")
    if profile_response.status_code == 200:
        print("✅ Token authentication is working!")
        profile_data = profile_response.json()
        print(f"📄 Profile response has {len(profile_data)} fields")
    else:
        print(f"❌ Token authentication failed: {profile_response.text}")

if __name__ == "__main__":
    test_registration_login_consistency()
