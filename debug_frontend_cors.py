#!/usr/bin/env python3
"""
Debug Script untuk Frontend CORS Issue
Membantu troubleshoot koneksi dari Vercel ke DigitalOcean API
"""

import requests
import json
import time

BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"
FRONTEND_URL = "https://smart-en-system.vercel.app"

def test_basic_connectivity():
    """Test basic API connectivity"""
    print("🔌 TESTING BASIC API CONNECTIVITY")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/health/", timeout=10)
        print(f"✅ Health Check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except requests.Timeout:
        print("❌ TIMEOUT - Server tidak merespon dalam 10 detik")
        return False
    except requests.ConnectionError:
        print("❌ CONNECTION ERROR - Tidak bisa connect ke server")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
    
    return True

def test_cors_preflight():
    """Test CORS preflight request"""
    print("\n🌐 TESTING CORS PREFLIGHT (OPTIONS)")
    print("=" * 50)
    
    headers = {
        'Origin': FRONTEND_URL,
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'content-type'
    }
    
    try:
        response = requests.options(f"{BASE_URL}/api/register/", headers=headers, timeout=10)
        print(f"✅ CORS Preflight: {response.status_code}")
        
        cors_headers = {}
        for header, value in response.headers.items():
            if 'access-control' in header.lower():
                cors_headers[header] = value
        
        print("📋 CORS Headers:")
        for header, value in cors_headers.items():
            print(f"   {header}: {value}")
            
        if 'access-control-allow-origin' in cors_headers:
            allowed_origin = cors_headers['access-control-allow-origin']
            if allowed_origin == FRONTEND_URL or allowed_origin == '*':
                print("✅ Frontend origin allowed")
            else:
                print(f"❌ Frontend origin NOT allowed. Expected: {FRONTEND_URL}, Got: {allowed_origin}")
        
        return True
        
    except Exception as e:
        print(f"❌ CORS Preflight Error: {e}")
        return False

def test_actual_registration():
    """Test actual registration with CORS headers"""
    print("\n📝 TESTING ACTUAL REGISTRATION")
    print("=" * 50)
    
    headers = {
        'Content-Type': 'application/json',
        'Origin': FRONTEND_URL,
        'User-Agent': 'Mozilla/5.0 (compatible; Frontend-Test/1.0)'
    }
    
    test_data = {
        "email": f"frontend.test.{int(time.time())}@example.com",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
        "first_name": "Frontend",
        "last_name": "Test",
        "department": 1
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/register/",
            headers=headers,
            json=test_data,
            timeout=30  # Longer timeout for registration
        )
        
        print(f"✅ Registration: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Registration SUCCESS!")
            print(f"   User: {result['data']['employee']['full_name']}")
            print(f"   Token: {result['data']['employee']['token'][:20]}...")
            
            # Check CORS headers in response
            cors_headers = {}
            for header, value in response.headers.items():
                if 'access-control' in header.lower():
                    cors_headers[header] = value
            
            print("📋 Response CORS Headers:")
            for header, value in cors_headers.items():
                print(f"   {header}: {value}")
                
        else:
            print(f"❌ Registration Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
        return response.status_code == 201
        
    except requests.Timeout:
        print("❌ REGISTRATION TIMEOUT - Ini yang mungkin dialami frontend!")
        print("   Frontend mungkin tidak bisa menunggu response dari server")
        return False
    except Exception as e:
        print(f"❌ Registration Error: {e}")
        return False

def test_different_origins():
    """Test dengan berbagai origin untuk debug"""
    print("\n🧪 TESTING DIFFERENT ORIGINS")
    print("=" * 50)
    
    origins_to_test = [
        FRONTEND_URL,  # Frontend sebenarnya
        "https://web.postman.co",  # Postman
        "http://localhost:3000",  # Local
        "null",  # Browser file://
        "*"  # Wildcard
    ]
    
    for origin in origins_to_test:
        print(f"\n🔍 Testing origin: {origin}")
        headers = {
            'Origin': origin,
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'content-type'
        }
        
        try:
            response = requests.options(f"{BASE_URL}/api/register/", headers=headers, timeout=5)
            allowed_origin = response.headers.get('access-control-allow-origin', 'NOT SET')
            print(f"   Status: {response.status_code}")
            print(f"   Allowed Origin: {allowed_origin}")
            
            if allowed_origin == origin or allowed_origin == '*':
                print("   ✅ ALLOWED")
            else:
                print("   ❌ BLOCKED")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def generate_frontend_debug_code():
    """Generate JavaScript code untuk frontend debugging"""
    print("\n💻 FRONTEND DEBUG CODE")
    print("=" * 50)
    
    js_code = f'''
// Paste this code di browser console untuk debug CORS issue
async function debugAPIConnection() {{
    console.log('🔍 Testing API Connection from Frontend...');
    
    const BASE_URL = '{BASE_URL}';
    
    // Test 1: Health Check
    try {{
        console.log('1️⃣ Testing Health Check...');
        const healthResponse = await fetch(`${{BASE_URL}}/api/health/`, {{
            method: 'GET',
            mode: 'cors',
            credentials: 'include'
        }});
        console.log('✅ Health Check:', healthResponse.status);
        console.log('   Response:', await healthResponse.json());
    }} catch (error) {{
        console.error('❌ Health Check Error:', error);
    }}
    
    // Test 2: CORS Preflight
    try {{
        console.log('2️⃣ Testing CORS Preflight...');
        const preflightResponse = await fetch(`${{BASE_URL}}/api/register/`, {{
            method: 'OPTIONS',
            mode: 'cors',
            headers: {{
                'Origin': window.location.origin,
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'content-type'
            }}
        }});
        console.log('✅ CORS Preflight:', preflightResponse.status);
        console.log('   Headers:', Object.fromEntries(preflightResponse.headers.entries()));
    }} catch (error) {{
        console.error('❌ CORS Preflight Error:', error);
    }}
    
    // Test 3: Actual Registration
    try {{
        console.log('3️⃣ Testing Registration...');
        const registrationResponse = await fetch(`${{BASE_URL}}/api/register/`, {{
            method: 'POST',
            mode: 'cors',
            credentials: 'include',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{
                email: `test.${{Date.now()}}@example.com`,
                password: 'TestPass123!',
                password_confirm: 'TestPass123!',
                first_name: 'Debug',
                last_name: 'Test',
                department: 1
            }})
        }});
        
        console.log('✅ Registration:', registrationResponse.status);
        if (registrationResponse.ok) {{
            console.log('   Response:', await registrationResponse.json());
        }} else {{
            console.log('   Error:', await registrationResponse.text());
        }}
    }} catch (error) {{
        console.error('❌ Registration Error:', error);
        console.log('   Error details:', {{
            name: error.name,
            message: error.message,
            stack: error.stack
        }});
    }}
}}

// Run the debug function
debugAPIConnection();
'''
    
    print("Minta frontend developer untuk:")
    print("1. Buka browser dan pergi ke frontend Vercel")
    print("2. Buka Developer Tools (F12)")
    print("3. Pergi ke Console tab")
    print("4. Paste dan run code berikut:")
    print("\n" + "="*60)
    print(js_code)
    print("="*60)

def main():
    """Main debug function"""
    print("🚨 FRONTEND CORS DEBUG TOOL")
    print("="*60)
    print("Debugging koneksi dari Vercel frontend ke DigitalOcean API")
    print("="*60)
    
    # Run all tests
    connectivity_ok = test_basic_connectivity()
    if not connectivity_ok:
        print("\n❌ Server tidak accessible. Check DigitalOcean status!")
        return
    
    cors_ok = test_cors_preflight()
    registration_ok = test_actual_registration()
    
    test_different_origins()
    generate_frontend_debug_code()
    
    print("\n📊 SUMMARY")
    print("="*50)
    print(f"✅ Basic Connectivity: {'OK' if connectivity_ok else 'FAILED'}")
    print(f"✅ CORS Preflight: {'OK' if cors_ok else 'FAILED'}")
    print(f"✅ Registration API: {'OK' if registration_ok else 'FAILED'}")
    
    if connectivity_ok and cors_ok and registration_ok:
        print("\n🎉 API WORKING PERFECTLY!")
        print("   Problem ada di frontend implementation")
        print("   Minta developer check:")
        print("   1. Network timeout settings")
        print("   2. Fetch configuration")
        print("   3. Error handling")
        print("   4. Browser console untuk error details")
    else:
        print("\n❌ API ISSUES DETECTED!")
        print("   Need to fix server-side configuration")

if __name__ == "__main__":
    main()
