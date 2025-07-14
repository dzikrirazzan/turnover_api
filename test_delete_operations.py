#!/usr/bin/env python3
"""
Test script untuk menguji fitur delete department dan delete employee
"""

import requests
import json
from datetime import datetime

# Base URL untuk production
BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"

# Admin credentials
admin_credentials = {
    "email": "admin@company.com",
    "password": "AdminPass123!"
}

def test_api_request(method, endpoint, data=None, headers=None):
    """Helper function untuk testing API"""
    url = f"{BASE_URL}{endpoint}"
    
    # Configure session
    session = requests.Session()
    session.verify = False  # Disable SSL verification for testing
    
    try:
        print(f"\n{'='*60}")
        print(f"🔍 {method.upper()} {endpoint}")
        
        if data:
            print(f"📤 Request Data:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        
        if method.upper() == 'GET':
            response = session.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = session.post(url, json=data, headers=headers)
        elif method.upper() == 'PUT':
            response = session.put(url, json=data, headers=headers)
        elif method.upper() == 'DELETE':
            response = session.delete(url, headers=headers)
        
        print(f"📊 Status Code: {response.status_code}")
        
        # Try to parse JSON
        try:
            response_json = response.json()
            print(f"📄 Response Data:")
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
            return response.status_code, response_json
        except:
            print(f"📄 Response Text: {response.text}")
            return response.status_code, response.text
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, str(e)

def login_as_admin():
    """Login sebagai admin dan return token"""
    print("🔐 Logging in as admin...")
    status, response = test_api_request("POST", "/api/login/", admin_credentials)
    
    if status == 200 and isinstance(response, dict):
        if 'data' in response and 'user' in response['data']:
            token = response['data']['user'].get('token')
            if token:
                print(f"✅ Login successful! Token: {token[:20]}...")
                return token
        elif 'user' in response and 'token' in response['user']:
            token = response['user']['token']
            print(f"✅ Login successful! Token: {token[:20]}...")
            return token
    
    print("❌ Login failed!")
    return None

def test_department_operations(token):
    """Test department CRUD operations"""
    headers = {'Authorization': f'Token {token}'}
    
    print("\n" + "="*80)
    print("🏢 TESTING DEPARTMENT OPERATIONS")
    
    # 1. Get existing departments
    print("\n📋 Step 1: Get existing departments")
    status, departments = test_api_request("GET", "/api/departments/", headers=headers)
    
    if status != 200:
        print("❌ Failed to get departments")
        return None
    
    if isinstance(departments, dict):
        if 'data' in departments:
            dept_list = departments['data']
        elif 'results' in departments:
            dept_list = departments['results']
        else:
            dept_list = departments
    elif isinstance(departments, list):
        dept_list = departments
    else:
        print("❌ Unexpected departments response format")
        return None
    
    print(f"📊 Found {len(dept_list)} departments")
    
    # 2. Create a test department
    print("\n📋 Step 2: Create test department")
    test_dept_data = {
        "name": "Test Department for Deletion",
        "description": "This department will be deleted in test"
    }
    
    status, new_dept = test_api_request("POST", "/api/departments/", test_dept_data, headers)
    
    if status != 201:
        print("❌ Failed to create test department")
        return None
    
    # Extract department ID
    if isinstance(new_dept, dict):
        if 'data' in new_dept:
            dept_id = new_dept['data'].get('id')
        else:
            dept_id = new_dept.get('id')
    else:
        print("❌ Failed to get department ID from response")
        return None
    
    print(f"✅ Created test department with ID: {dept_id}")
    
    # 3. Try to delete the department
    print("\n📋 Step 3: Delete test department")
    status, delete_response = test_api_request("DELETE", f"/api/departments/{dept_id}/", headers=headers)
    
    if status == 204 or status == 200:
        print("✅ Department deleted successfully!")
        
        # 4. Verify deletion
        print("\n📋 Step 4: Verify department deletion")
        status, verify = test_api_request("GET", f"/api/departments/{dept_id}/", headers=headers)
        
        if status == 404:
            print("✅ Department deletion verified!")
            return True
        else:
            print("⚠️ Department might still exist")
            return False
    else:
        print(f"❌ Failed to delete department. Status: {status}")
        return False

def test_employee_operations(token):
    """Test employee CRUD operations"""
    headers = {'Authorization': f'Token {token}'}
    
    print("\n" + "="*80)
    print("👥 TESTING EMPLOYEE OPERATIONS")
    
    # 1. Get existing employees
    print("\n📋 Step 1: Get existing employees")
    status, employees = test_api_request("GET", "/api/employees/", headers=headers)
    
    if status != 200:
        print("❌ Failed to get employees")
        return None
    
    if isinstance(employees, dict):
        if 'data' in employees:
            emp_list = employees['data']
        elif 'results' in employees:
            emp_list = employees['results']
        else:
            emp_list = employees
    elif isinstance(employees, list):
        emp_list = employees
    else:
        print("❌ Unexpected employees response format")
        return None
    
    print(f"📊 Found {len(emp_list)} employees")
    
    # 2. Create a test employee
    print("\n📋 Step 2: Create test employee")
    test_emp_data = {
        "email": "test.delete@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test",
        "last_name": "DeleteUser",
        "phone_number": "+6281234567999",
        "date_of_birth": "1990-01-01",
        "gender": "M",
        "marital_status": "single",
        "education_level": "bachelor",
        "address": "Test Address",
        "position": "Test Position",
        "department": 1,
        "hire_date": "2024-01-01",
        "salary": "monthly",
        "salary_amount": 5000000
    }
    
    status, new_emp = test_api_request("POST", "/api/employees/", test_emp_data, headers)
    
    if status != 201:
        print("❌ Failed to create test employee")
        # Try registration endpoint instead
        print("\n📋 Step 2b: Try registration endpoint")
        status, new_emp = test_api_request("POST", "/api/register/", test_emp_data)
        
        if status != 201:
            print("❌ Failed to create test employee via registration")
            return None
    
    # Extract employee ID
    if isinstance(new_emp, dict):
        if 'data' in new_emp and 'employee' in new_emp['data']:
            emp_id = new_emp['data']['employee'].get('id')
        elif 'data' in new_emp:
            emp_id = new_emp['data'].get('id')
        else:
            emp_id = new_emp.get('id')
    else:
        print("❌ Failed to get employee ID from response")
        return None
    
    print(f"✅ Created test employee with ID: {emp_id}")
    
    # 3. Try to delete the employee
    print("\n📋 Step 3: Delete test employee")
    status, delete_response = test_api_request("DELETE", f"/api/employees/{emp_id}/", headers=headers)
    
    if status == 204 or status == 200:
        print("✅ Employee deleted successfully!")
        
        # 4. Verify deletion
        print("\n📋 Step 4: Verify employee deletion")
        status, verify = test_api_request("GET", f"/api/employees/{emp_id}/", headers=headers)
        
        if status == 404:
            print("✅ Employee deletion verified!")
            return True
        else:
            print("⚠️ Employee might still exist")
            return False
    else:
        print(f"❌ Failed to delete employee. Status: {status}")
        return False

def main():
    print("🚀 Testing DELETE Operations for SMART-EN API")
    print(f"🕐 Started at: {datetime.now()}")
    print(f"🌐 Testing on: {BASE_URL}")
    
    # Login as admin
    token = login_as_admin()
    if not token:
        print("❌ Cannot proceed without admin token")
        return
    
    # Test department delete operations
    dept_result = test_department_operations(token)
    
    # Test employee delete operations  
    emp_result = test_employee_operations(token)
    
    # Summary
    print("\n" + "="*80)
    print("📋 TEST SUMMARY")
    print(f"🏢 Department Delete: {'✅ PASSED' if dept_result else '❌ FAILED'}")
    print(f"👥 Employee Delete: {'✅ PASSED' if emp_result else '❌ FAILED'}")
    
    if dept_result and emp_result:
        print("\n🎉 All delete operations working correctly!")
    else:
        print("\n⚠️ Some delete operations need fixing:")
        if not dept_result:
            print("   - Department delete functionality")
        if not emp_result:
            print("   - Employee delete functionality")

if __name__ == "__main__":
    main()
