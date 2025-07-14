#!/usr/bin/env python3
"""
Test script untuk testing fitur:
1. Delete Department (hard delete)
2. Delete User/Employee (hard delete)
3. Get User Profile (admin & employee access)
4. Logout functionality

Pastikan server Django running di port 8000
"""

import requests
import json
from datetime import datetime
import time

# Configuration
BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"
# BASE_URL = "http://127.0.0.1:8000"  # Uncomment untuk local testing

def print_section(title):
    """Print section header"""
    print("\n" + "="*80)
    print(f"📋 {title}")
    print("="*80)

def test_api_request(method, endpoint, data=None, headers=None, expect_json=True):
    """Helper function untuk testing API requests"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        print(f"\n🔍 {method.upper()} {endpoint}")
        
        # Setup session
        session = requests.Session()
        session.verify = True
        
        # Make request
        if method.upper() == 'GET':
            response = session.get(url, headers=headers, timeout=30)
        elif method.upper() == 'POST':
            response = session.post(url, json=data, headers=headers, timeout=30)
        elif method.upper() == 'PUT':
            response = session.put(url, json=data, headers=headers, timeout=30)
        elif method.upper() == 'DELETE':
            response = session.delete(url, headers=headers, timeout=30)
        else:
            print(f"❌ Unsupported method: {method}")
            return None
        
        print(f"📊 Status Code: {response.status_code}")
        
        # Try to parse JSON response
        if expect_json:
            try:
                response_json = response.json()
                print(f"📄 Response:")
                print(json.dumps(response_json, indent=2, ensure_ascii=False))
                return {
                    'status_code': response.status_code,
                    'data': response_json,
                    'success': 200 <= response.status_code < 300
                }
            except json.JSONDecodeError:
                print(f"📄 Response Text: {response.text[:500]}...")
                return {
                    'status_code': response.status_code,
                    'data': response.text,
                    'success': 200 <= response.status_code < 300
                }
        else:
            print(f"📄 Response Text: {response.text}")
            return {
                'status_code': response.status_code,
                'data': response.text,
                'success': 200 <= response.status_code < 300
            }
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection error")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("🚀 Testing DELETE & PROFILE Features")
    print(f"🕐 Started at: {datetime.now()}")
    print(f"🌐 Base URL: {BASE_URL}")
    
    # Global variables untuk menyimpan data
    admin_token = None
    employee_token = None
    test_department_id = None
    test_employee_id = None
    
    # ===============================================================
    # 1. ADMIN LOGIN
    # ===============================================================
    print_section("1. ADMIN LOGIN")
    
    admin_login_data = {
        "email": "admin@company.com",
        "password": "AdminPass123!"
    }
    
    print("📤 Admin Login Data:")
    print(json.dumps(admin_login_data, indent=2))
    
    login_response = test_api_request("POST", "/api/login/", admin_login_data)
    
    if login_response and login_response['success']:
        try:
            if 'data' in login_response['data'] and 'user' in login_response['data']['data']:
                admin_token = login_response['data']['data']['user']['token']
            elif 'user' in login_response['data'] and 'token' in login_response['data']['user']:
                admin_token = login_response['data']['user']['token']
            else:
                print("❌ Could not extract admin token from response")
                return
            
            print(f"✅ Admin login successful! Token: {admin_token[:20]}...")
        except Exception as e:
            print(f"❌ Error extracting admin token: {e}")
            return
    else:
        print("❌ Admin login failed!")
        return
    
    # ===============================================================
    # 2. CREATE TEST DEPARTMENT
    # ===============================================================
    print_section("2. CREATE TEST DEPARTMENT")
    
    # Create unique department name with timestamp
    timestamp = int(time.time())
    test_department_data = {
        "name": f"Test Delete Dept {timestamp}",
        "description": "This department will be deleted in test"
    }
    
    headers = {
        "Authorization": f"Token {admin_token}",
        "Content-Type": "application/json"
    }
    
    print("📤 Creating test department:")
    print(json.dumps(test_department_data, indent=2))
    
    create_dept_response = test_api_request("POST", "/api/departments/", test_department_data, headers)
    
    if create_dept_response and create_dept_response['success']:
        try:
            # Handle different response formats
            dept_data = create_dept_response['data']
            if 'data' in dept_data:
                test_department_id = dept_data['data']['id']
            elif 'id' in dept_data:
                test_department_id = dept_data['id']
            else:
                print("❌ Could not extract department ID")
                return
                
            print(f"✅ Test department created! ID: {test_department_id}")
        except Exception as e:
            print(f"❌ Error extracting department ID: {e}")
            return
    else:
        print("❌ Failed to create test department!")
        return
    
    # ===============================================================
    # 3. CREATE TEST EMPLOYEE
    # ===============================================================
    print_section("3. CREATE TEST EMPLOYEE")
    
    # Create unique employee email with timestamp
    timestamp = int(time.time())
    test_employee_data = {
        "email": f"testemployee{timestamp}@delete.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test",
        "last_name": "Employee",
        "phone_number": "+628999888777",
        "date_of_birth": "1995-01-01",
        "gender": "M",
        "marital_status": "single",
        "education_level": "bachelor",
        "address": "Test Address",
        "position": "Test Position",
        "department": 1,
        "hire_date": "2024-01-01"
    }
    
    print("📤 Creating test employee:")
    print(json.dumps(test_employee_data, indent=2))
    
    create_emp_response = test_api_request("POST", "/api/register/", test_employee_data)
    
    if create_emp_response and create_emp_response['success']:
        try:
            # Extract employee ID and token
            emp_data = create_emp_response['data']
            if 'data' in emp_data and 'employee' in emp_data['data']:
                test_employee_id = emp_data['data']['employee']['id']
                employee_token = emp_data['data']['employee']['token']
            elif 'employee' in emp_data:
                test_employee_id = emp_data['employee']['id']
                employee_token = emp_data['employee']['token']
            else:
                print("❌ Could not extract employee data")
                return
                
            print(f"✅ Test employee created! ID: {test_employee_id}")
            print(f"✅ Employee token: {employee_token[:20]}...")
        except Exception as e:
            print(f"❌ Error extracting employee data: {e}")
            return
    else:
        print("❌ Failed to create test employee!")
        return
    
    # ===============================================================
    # 4. TEST EMPLOYEE PROFILE ACCESS
    # ===============================================================
    print_section("4. TEST EMPLOYEE PROFILE ACCESS")
    
    employee_headers = {
        "Authorization": f"Token {employee_token}",
        "Content-Type": "application/json"
    }
    
    print("🔍 Testing employee access to own profile...")
    emp_profile_response = test_api_request("GET", "/api/profile/", headers=employee_headers)
    
    if emp_profile_response and emp_profile_response['success']:
        print("✅ Employee can access own profile!")
    else:
        print("❌ Employee cannot access own profile!")
    
    # ===============================================================
    # 5. TEST ADMIN PROFILE ACCESS
    # ===============================================================
    print_section("5. TEST ADMIN PROFILE ACCESS")
    
    print("🔍 Testing admin access to profile...")
    admin_profile_response = test_api_request("GET", "/api/profile/", headers=headers)
    
    if admin_profile_response and admin_profile_response['success']:
        print("✅ Admin can access profile!")
    else:
        print("❌ Admin cannot access profile!")
    
    # ===============================================================
    # 6. TEST GET EMPLOYEE BY ID (ADMIN ACCESS)
    # ===============================================================
    print_section("6. TEST GET EMPLOYEE BY ID (ADMIN ACCESS)")
    
    print(f"🔍 Testing admin access to employee {test_employee_id}...")
    get_emp_response = test_api_request("GET", f"/api/employees/{test_employee_id}/", headers=headers)
    
    if get_emp_response and get_emp_response['success']:
        print("✅ Admin can access employee details!")
    else:
        print("❌ Admin cannot access employee details!")
    
    # ===============================================================
    # 7. TEST DELETE EMPLOYEE (HARD DELETE)
    # ===============================================================
    print_section("7. TEST DELETE EMPLOYEE (HARD DELETE)")
    
    print(f"🗑️ Attempting to delete employee {test_employee_id}...")
    delete_emp_response = test_api_request("DELETE", f"/api/employees/{test_employee_id}/", headers=headers, expect_json=False)
    
    if delete_emp_response and delete_emp_response['success']:
        print("✅ Employee deleted successfully!")
        
        # Verify deletion by trying to get the employee
        print("🔍 Verifying employee deletion...")
        verify_emp_response = test_api_request("GET", f"/api/employees/{test_employee_id}/", headers=headers)
        
        if verify_emp_response and verify_emp_response['status_code'] == 404:
            print("✅ Employee hard delete confirmed - employee not found!")
        else:
            print("❌ Employee still exists after deletion (soft delete detected)!")
    else:
        print(f"❌ Failed to delete employee! Status: {delete_emp_response['status_code'] if delete_emp_response else 'None'}")
    
    # ===============================================================
    # 8. TEST DELETE DEPARTMENT (HARD DELETE)
    # ===============================================================
    print_section("8. TEST DELETE DEPARTMENT (HARD DELETE)")
    
    print(f"🗑️ Attempting to delete department {test_department_id}...")
    delete_dept_response = test_api_request("DELETE", f"/api/departments/{test_department_id}/", headers=headers, expect_json=False)
    
    if delete_dept_response and delete_dept_response['success']:
        print("✅ Department deleted successfully!")
        
        # Verify deletion by trying to get the department
        print("🔍 Verifying department deletion...")
        verify_dept_response = test_api_request("GET", f"/api/departments/{test_department_id}/", headers=headers)
        
        if verify_dept_response and verify_dept_response['status_code'] == 404:
            print("✅ Department hard delete confirmed - department not found!")
        else:
            print("❌ Department still exists after deletion (soft delete detected)!")
    else:
        print(f"❌ Failed to delete department! Status: {delete_dept_response['status_code'] if delete_dept_response else 'None'}")
    
    # ===============================================================
    # 9. TEST EMPLOYEE LOGOUT
    # ===============================================================
    print_section("9. TEST EMPLOYEE LOGOUT")
    
    if employee_token:
        print("🚪 Testing employee logout...")
        emp_logout_response = test_api_request("POST", "/api/logout/", headers=employee_headers, expect_json=False)
        
        if emp_logout_response and emp_logout_response['success']:
            print("✅ Employee logout successful!")
            
            # Verify logout by trying to access profile
            print("🔍 Verifying employee logout...")
            verify_logout_response = test_api_request("GET", "/api/profile/", headers=employee_headers)
            
            if verify_logout_response and verify_logout_response['status_code'] == 401:
                print("✅ Employee logout confirmed - token invalidated!")
            else:
                print("❌ Employee token still valid after logout!")
        else:
            print("❌ Employee logout failed!")
    
    # ===============================================================
    # 10. TEST ADMIN LOGOUT
    # ===============================================================
    print_section("10. TEST ADMIN LOGOUT")
    
    print("🚪 Testing admin logout...")
    admin_logout_response = test_api_request("POST", "/api/logout/", headers=headers, expect_json=False)
    
    if admin_logout_response and admin_logout_response['success']:
        print("✅ Admin logout successful!")
        
        # Verify logout by trying to access profile
        print("🔍 Verifying admin logout...")
        verify_admin_logout_response = test_api_request("GET", "/api/profile/", headers=headers)
        
        if verify_admin_logout_response and verify_admin_logout_response['status_code'] == 401:
            print("✅ Admin logout confirmed - token invalidated!")
        else:
            print("❌ Admin token still valid after logout!")
    else:
        print("❌ Admin logout failed!")
    
    # ===============================================================
    # SUMMARY
    # ===============================================================
    print_section("SUMMARY")
    
    print("📊 Test Results Summary:")
    print("=" * 50)
    print("✅ Features that should work:")
    print("   - Admin login")
    print("   - Create department")
    print("   - Create employee")
    print("   - Employee profile access")
    print("   - Admin profile access")
    print("   - Admin access to employee details")
    print("   - Hard delete employee")
    print("   - Hard delete department")
    print("   - Employee logout with token invalidation")
    print("   - Admin logout with token invalidation")
    print("\n❌ If any features failed, check backend implementation.")
    print(f"\n🕐 Test completed at: {datetime.now()}")

if __name__ == "__main__":
    main()
