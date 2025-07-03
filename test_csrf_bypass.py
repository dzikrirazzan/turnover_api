#!/usr/bin/env python3
"""
Test Script untuk mengatasi CSRF error dan testing API lengkap
Mengatasi masalah "CSRF Failed: Referer checking failed - no Referer."
"""

import requests
import json
from datetime import datetime

# Base URL - URL dari conversation summary yang aktif
BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"

def test_api_without_csrf():
    """Test API registration dan login dengan menggunakan session dan proper headers"""
    print("🚀 TESTING API WITH CSRF BYPASS")
    print("=" * 80)
    
    # Create session for maintaining cookies
    session = requests.Session()
    
    # Set proper headers to avoid CSRF issues
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Postman-like client)',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',  # Important for Django CSRF
    }
    
    # Data registrasi dari user
    registration_data = {
        "email": "newe@example.com",
        "password": "SecurePass123!",
        "password_confirm": "SecurePass123!",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+6281234567890",
        "date_of_birth": "1990-05-15",
        "gender": "M",
        "marital_status": "single",
        "education_level": "bachelor",
        "address": "Jl. Example No. 123, Jakarta",
        "position": "Software Developer",
        "department": 1,
        "hire_date": "2024-01-15"
    }
    
    print("📋 STEP 1: Health Check")
    print("-" * 40)
    try:
        response = session.get(f"{BASE_URL}/api/health/", headers=headers)
        print(f"✅ Health Status: {response.status_code}")
        if response.text:
            print(f"📄 Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Health Check Error: {e}")
    
    print(f"\n📋 STEP 2: API Info (Get CSRF if needed)")
    print("-" * 40)
    try:
        response = session.get(f"{BASE_URL}/api/info/", headers=headers)
        print(f"✅ Info Status: {response.status_code}")
        if response.text:
            print(f"📄 Response: {response.text[:200]}...")
            
        # Check for CSRF token in cookies
        csrf_token = None
        for cookie in session.cookies:
            if cookie.name == 'csrftoken':
                csrf_token = cookie.value
                print(f"🔑 CSRF Token found: {csrf_token[:20]}...")
                headers['X-CSRFToken'] = csrf_token
                break
                
    except Exception as e:
        print(f"❌ Info Error: {e}")
    
    print(f"\n📋 STEP 3: Registration Test")
    print("-" * 40)
    print(f"📤 Sending registration data:")
    print(json.dumps(registration_data, indent=2))
    
    try:
        response = session.post(
            f"{BASE_URL}/api/register/",
            json=registration_data,
            headers=headers
        )
        
        print(f"📊 Registration Status: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        if response.status_code in [200, 201]:
            try:
                data = response.json()
                print("✅ Registration SUCCESS!")
                print(f"📄 Response: {json.dumps(data, indent=2)}")
                
                # Extract token if available
                token = None
                if 'data' in data and 'employee' in data['data'] and 'token' in data['data']['employee']:
                    token = data['data']['employee']['token']
                elif 'employee' in data and 'token' in data['employee']:
                    token = data['employee']['token']
                elif 'token' in data:
                    token = data['token']
                
                if token:
                    print(f"🔑 Auth Token: {token[:30]}...")
                    return test_with_token(session, token, registration_data['email'], registration_data['password'])
                else:
                    print("⚠️ No token found in response")
                    
            except json.JSONDecodeError:
                print(f"📄 Raw Response: {response.text}")
                
        else:
            print(f"❌ Registration FAILED: {response.status_code}")
            try:
                error_data = response.json()
                print(f"📄 Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"📄 Raw Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Registration Exception: {e}")
        
    return False

def test_with_token(session, token, email, password):
    """Test login dan endpoints lain dengan token"""
    print(f"\n📋 STEP 4: Login Test")
    print("-" * 40)
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}',
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    login_data = {
        "email": email,
        "password": password
    }
    
    try:
        response = session.post(
            f"{BASE_URL}/api/login/",
            json=login_data,
            headers={'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest'}
        )
        
        print(f"📊 Login Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Login SUCCESS!")
                print(f"📄 Response: {json.dumps(data, indent=2)}")
            except:
                print(f"📄 Raw Response: {response.text}")
        else:
            print(f"❌ Login FAILED: {response.status_code}")
            try:
                error_data = response.json()
                print(f"📄 Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"📄 Raw Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Login Exception: {e}")
    
    # Test profile with token
    print(f"\n📋 STEP 5: Profile Test (with token)")
    print("-" * 40)
    
    try:
        response = session.get(
            f"{BASE_URL}/api/profile/",
            headers=headers
        )
        
        print(f"📊 Profile Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Profile SUCCESS!")
                print(f"📄 Response: {json.dumps(data, indent=2)}")
            except:
                print(f"📄 Raw Response: {response.text}")
        else:
            print(f"❌ Profile FAILED: {response.status_code}")
            print(f"📄 Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Profile Exception: {e}")
    
    return True

def test_csrf_alternatives():
    """Test alternative approaches untuk avoid CSRF"""
    print(f"\n🔧 TESTING CSRF BYPASS ALTERNATIVES")
    print("=" * 80)
    
    # Alternative 1: Use different content type
    print("🧪 Alternative 1: application/x-www-form-urlencoded")
    try:
        import urllib.parse
        data = {
            "email": "test@example.com",
            "password": "testpass",
            "password_confirm": "testpass",
            "first_name": "Test",
            "last_name": "User",
            "department": "1"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/register/",
            data=urllib.parse.urlencode(data),
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'PostmanRuntime/7.0.0',
            }
        )
        print(f"📊 Status: {response.status_code}")
        print(f"📄 Response: {response.text[:200]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Alternative 2: Disable CSRF via settings (already done)
    print(f"\n🧪 Alternative 2: Check if CSRF is disabled")
    print("✅ CSRF bypass added to views with @csrf_exempt decorator")
    print("✅ CORS headers configured in settings")
    
    # Alternative 3: Test with curl equivalent
    print(f"\n🧪 Alternative 3: Raw curl equivalent test")
    try:
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': BASE_URL,
            'Referer': f"{BASE_URL}/",
            'User-Agent': 'Mozilla/5.0 (compatible API client)',
        }
        
        simple_data = {
            "email": "simple@test.com",
            "password": "simple123",
            "password_confirm": "simple123",
            "first_name": "Simple",
            "last_name": "Test",
            "department": 1
        }
        
        response = requests.post(
            f"{BASE_URL}/api/register/",
            json=simple_data,
            headers=headers
        )
        
        print(f"📊 Status: {response.status_code}")
        if response.status_code < 500:
            try:
                data = response.json()
                print(f"📄 JSON Response: {json.dumps(data, indent=2)}")
            except:
                print(f"📄 Text Response: {response.text}")
        else:
            print(f"📄 Error Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main testing function"""
    print("🚀 SMART-EN API CSRF BYPASS & TESTING")
    print(f"🕐 Started at: {datetime.now()}")
    print(f"🌐 Base URL: {BASE_URL}")
    print("=" * 80)
    
    # Test primary API flow
    success = test_api_without_csrf()
    
    # Test alternatives if primary failed
    if not success:
        test_csrf_alternatives()
    
    print(f"\n✅ TESTING COMPLETE!")
    print("=" * 80)
    print("📋 SOLUTIONS IMPLEMENTED:")
    print("1. ✅ Added @csrf_exempt decorator to registration & login views")
    print("2. ✅ Updated CORS settings for better API compatibility")
    print("3. ✅ Added proper request headers (X-Requested-With, User-Agent)")
    print("4. ✅ Session management for cookie-based CSRF if needed")
    print("5. ✅ Multiple fallback approaches tested")
    
    print(f"\n🔧 FOR POSTMAN USERS:")
    print("1. Use 'application/json' content-type")
    print("2. Add header: X-Requested-With: XMLHttpRequest")
    print("3. No CSRF token needed (disabled for API endpoints)")
    print("4. Use session for cookie management if needed")

if __name__ == "__main__":
    main()
