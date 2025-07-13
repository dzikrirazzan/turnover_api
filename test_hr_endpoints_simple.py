#!/usr/bin/env python3
"""
Simple HR endpoints test script
"""
import requests
import json

BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"

def test_admin_login():
    """Test admin login"""
    print("🔐 Testing admin login...")
    response = requests.post(f"{BASE_URL}/api/login/", json={
        "email": "admin@company.com",
        "password": "AdminPass123!"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"Login response: {data}")
        # Handle different token response formats
        if 'data' in data and 'token' in data['data']:
            token = data['data']['token']
        elif 'token' in data:
            token = data['token']
        else:
            token = data.get('data', {}).get('user', {}).get('token')
        
        if token:
            print(f"✅ Login successful! Token: {token[:20]}...")
            return token
        else:
            print(f"❌ Token not found in response: {data}")
            return None
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        return None

def test_hr_endpoints(token):
    """Test HR endpoints"""
    headers = {"Authorization": f"Token {token}"}
    
    print("\n📋 Testing HR endpoints...")
    
    # Test meetings endpoint
    print("Testing /api/hr/meetings/...")
    response = requests.get(f"{BASE_URL}/api/hr/meetings/", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ Meetings endpoint working: {response.json()}")
    else:
        print(f"❌ Meetings endpoint error: {response.text[:200]}")
    
    # Test reviews endpoint
    print("\nTesting /api/hr/reviews/...")
    response = requests.get(f"{BASE_URL}/api/hr/reviews/", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ Reviews endpoint working: {response.json()}")
    else:
        print(f"❌ Reviews endpoint error: {response.text[:200]}")
    
    # Test employees to get valid employee_id
    print("\nTesting /api/employees/ to get employee IDs...")
    response = requests.get(f"{BASE_URL}/api/employees/", headers=headers)
    if response.status_code == 200:
        employees = response.json()
        print(f"✅ Found {len(employees)} employees")
        if employees:
            employee_id = employees[0]['id']
            print(f"Using employee_id: {employee_id}")
            
            # Test create meeting with valid employee_id
            print(f"\nTesting create meeting for employee {employee_id}...")
            meeting_data = {
                "employee": employee_id,
                "title": "Test Meeting",
                "meeting_type": "regular",
                "scheduled_date": "2025-07-15T14:00:00Z",
                "duration_minutes": 30,
                "agenda": "Test meeting from API"
            }
            
            response = requests.post(f"{BASE_URL}/api/hr/meetings/", 
                                   headers={**headers, "Content-Type": "application/json"},
                                   json=meeting_data)
            print(f"Create meeting status: {response.status_code}")
            if response.status_code == 201:
                print(f"✅ Meeting created: {response.json()}")
            else:
                print(f"❌ Create meeting error: {response.text[:300]}")
    else:
        print(f"❌ Cannot get employees: {response.status_code}")

if __name__ == "__main__":
    print("🚀 Testing HR Features API")
    print("=" * 50)
    
    token = test_admin_login()
    if token:
        test_hr_endpoints(token)
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")
