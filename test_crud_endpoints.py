#!/usr/bin/env python3
"""
Test script for the new CRUD endpoints in SMART-EN Turnover API
Tests both Department and Employee ViewSets
"""

import requests
import json
import sys
from datetime import datetime

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000/api"

# Disable SSL warnings for development
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_endpoint(method, url, data=None, headers=None, expected_status=None):
    """Helper function to test an endpoint and display results"""
    try:
        # Configure session to handle any SSL issues
        session = requests.Session()
        session.verify = False  # Disable SSL verification for development
        
        if method.upper() == 'GET':
            response = session.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = session.post(url, json=data, headers=headers)
        elif method.upper() == 'PUT':
            response = session.put(url, json=data, headers=headers)
        elif method.upper() == 'PATCH':
            response = session.patch(url, json=data, headers=headers)
        elif method.upper() == 'DELETE':
            response = session.delete(url, headers=headers)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
            
        print(f"\n{'='*60}")
        print(f"🔍 {method.upper()} {url}")
        print(f"📊 Status: {response.status_code}")
        
        # Check if expected status matches
        if expected_status and response.status_code != expected_status:
            print(f"⚠️  Expected {expected_status}, got {response.status_code}")
        
        # Try to parse JSON response
        try:
            response_data = response.json()
            print(f"📝 Response:")
            print(json.dumps(response_data, indent=2))
        except:
            print(f"📝 Response (raw): {response.text[:200]}...")
            
        return response.status_code < 400
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 SMART-EN Turnover API - CRUD Endpoints Test")
    print(f"🕐 Test started at: {datetime.now()}")
    print(f"🌐 Base URL: {BASE_URL}")
    
    # Test server connectivity first
    print("\n" + "="*80)
    print("📋 CONNECTIVITY CHECK: Testing if Django server is running")
    try:
        response = requests.get("http://127.0.0.1:8000/", verify=False, timeout=5)
        print(f"✅ Server is responding (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Server connectivity failed: {e}")
        print("💡 Make sure Django server is running: python manage.py runserver")
        return
    
    # Test 1: API Root - Check if ViewSets are registered
    print("\n" + "="*80)
    print("📋 TEST 1: API Root - ViewSet Registration")
    test_endpoint("GET", f"{BASE_URL}/")
    
    # Test 2: Department CRUD Operations
    print("\n" + "="*80)
    print("📋 TEST 2: Department CRUD Operations")
    
    # List departments (should work without auth for viewing)
    test_endpoint("GET", f"{BASE_URL}/departments/", expected_status=200)
    
    # Try to create department (should require auth)
    dept_data = {
        "name": "Test Department",
        "description": "A test department for CRUD testing"
    }
    test_endpoint("POST", f"{BASE_URL}/departments/", data=dept_data, expected_status=401)
    
    # Test 3: Employee CRUD Operations  
    print("\n" + "="*80)
    print("📋 TEST 3: Employee CRUD Operations")
    
    # List employees (should require auth)
    test_endpoint("GET", f"{BASE_URL}/employees/", expected_status=401)
    
    # Test 4: Legacy Endpoints
    print("\n" + "="*80)
    print("📋 TEST 4: Legacy Endpoints")
    
    # Test legacy departments endpoint
    test_endpoint("GET", f"{BASE_URL}/departments-list/", expected_status=200)
    
    # Test 5: Health Check
    print("\n" + "="*80)
    print("📋 TEST 5: Health Check")
    
    test_endpoint("GET", f"{BASE_URL}/health/", expected_status=200)
    
    # Test 6: API Info
    print("\n" + "="*80)
    print("📋 TEST 6: API Info")
    
    test_endpoint("GET", f"{BASE_URL}/info/", expected_status=200)
    
    print("\n" + "="*80)
    print("✅ CRUD Endpoints Test Complete!")
    print("📝 Note: Authentication tests expected to fail (401) - this is correct behavior")
    print("🔐 For full testing, authentication tokens would be needed")

if __name__ == "__main__":
    main()
