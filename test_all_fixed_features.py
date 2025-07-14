#!/usr/bin/env python3
"""
Test script untuk semua fitur yang sudah diperbaiki:
- Admin login
- Create department
- Create employee  
- Employee profile access
- Admin profile access
- Admin access to employee details
- Admin access to update department
- Admin and employee access to update employee data
- Soft delete employee
- Hard delete department
- Employee logout with token invalidation
- Admin logout with token invalidation
"""

import requests
import json
import time
from datetime import datetime

# Base URL DigitalOcean
BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(f"🚀 {title}")
    print("="*80)

def test_api_request(method, endpoint, data=None, headers=None, expect_json=True):
    """Helper function untuk testing API"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        print(f"\n🔍 {method.upper()} {endpoint}")
        if data:
            print(f"📤 Request Data: {json.dumps(data, indent=2)}")
        
        response = requests.request(method, url, json=data, headers=headers, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if expect_json:
            try:
                response_data = response.json()
                print(f"📄 Response: {json.dumps(response_data, indent=2)}")
                return {
                    'success': response.status_code in [200, 201, 204],
                    'status_code': response.status_code,
                    'data': response_data
                }
            except:
                print(f"📄 Response Text: {response.text}")
                return {
                    'success': response.status_code in [200, 201, 204],
                    'status_code': response.status_code,
                    'data': response.text
                }
        else:
            print(f"📄 Response Text: {response.text}")
            return {
                'success': response.status_code in [200, 201, 204],
                'status_code': response.status_code,
                'data': response.text
            }
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            'success': False,
            'status_code': 0,
            'data': str(e)
        }

def main():
    print("🚀 Testing All Fixed Features - SMART-EN API")
    print(f"🕐 Started at: {datetime.now()}")
    print(f"🌐 Base URL: {BASE_URL}")
    
    # Global variables
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
    
    login_response = test_api_request("POST", "/api/login/", admin_login_data)
    
    if login_response['success']:
        try:
            # Extract token from different possible response formats
            response_data = login_response['data']
            if 'data' in response_data and 'user' in response_data['data']:
                admin_token = response_data['data']['user']['token']
            elif 'user' in response_data and 'token' in response_data['user']:
                admin_token = response_data['user']['token']
            elif 'data' in response_data and 'token' in response_data['data']:
                admin_token = response_data['data']['token']
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
    # 2. CREATE DEPARTMENT
    # ===============================================================
    print_section("2. CREATE DEPARTMENT")
    
    # Create unique department name with timestamp
    timestamp = int(time.time())
    test_department_data = {
        "name": f"Test Department {timestamp}",
        "description": "Department created for testing purposes"
    }
    
    headers = {
        "Authorization": f"Token {admin_token}",
        "Content-Type": "application/json"
    }
    
    print("📤 Creating test department:")
    dept_response = test_api_request("POST", "/api/departments/", test_department_data, headers)
    
    if dept_response['success']:
        try:
            # Extract department ID
            if 'data' in dept_response['data']:
                test_department_id = dept_response['data']['data']['id']
            else:
                test_department_id = dept_response['data']['id']
            print(f"✅ Department created with ID: {test_department_id}")
        except Exception as e:
            print(f"❌ Error extracting department ID: {e}")
            return
    else:
        print("❌ Failed to create department!")
        return
    
    # ===============================================================
    # 3. CREATE EMPLOYEE
    # ===============================================================
    print_section("3. CREATE EMPLOYEE")
    
    # Create unique employee with timestamp
    test_employee_data = {
        "email": f"testemployee{timestamp}@example.com",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
        "first_name": "Test",
        "last_name": "Employee",
        "phone_number": f"+628123456{timestamp % 10000}",
        "date_of_birth": "1995-01-01",
        "gender": "M",
        "marital_status": "single",
        "education_level": "bachelor",
        "address": "Test Address 123",
        "position": "Test Position",
        "department": test_department_id,
        "hire_date": "2024-01-01",
        "salary": "medium"
    }
    
    print("📤 Creating test employee:")
    emp_response = test_api_request("POST", "/api/employees/", test_employee_data, headers)
    
    if emp_response['success']:
        try:
            # Extract employee ID - handle different response formats
            response_data = emp_response['data']
            if 'data' in response_data:
                # Response has nested data structure
                employee_data = response_data['data']
                test_employee_id = employee_data.get('id') or employee_data.get('employee_id')
            else:
                # Response is direct
                test_employee_id = response_data.get('id') or response_data.get('employee_id')
            
            if test_employee_id:
                print(f"✅ Employee created with ID: {test_employee_id}")
            else:
                print(f"❌ Could not extract employee ID from response keys: {list(response_data.keys())}")
                return
        except Exception as e:
            print(f"❌ Error extracting employee ID: {e}")
            return
    else:
        print("❌ Failed to create employee!")
        return
    
    # ===============================================================
    # 4. EMPLOYEE LOGIN & PROFILE ACCESS
    # ===============================================================
    print_section("4. EMPLOYEE LOGIN & PROFILE ACCESS")
    
    employee_login_data = {
        "email": f"testemployee{timestamp}@example.com",
        "password": "TestPass123!"
    }
    
    emp_login_response = test_api_request("POST", "/api/login/", employee_login_data)
    
    if emp_login_response['success']:
        try:
            response_data = emp_login_response['data']
            if 'data' in response_data and 'user' in response_data['data']:
                employee_token = response_data['data']['user']['token']
            elif 'user' in response_data and 'token' in response_data['user']:
                employee_token = response_data['user']['token']
            elif 'data' in response_data and 'token' in response_data['data']:
                employee_token = response_data['data']['token']
            
            print(f"✅ Employee login successful! Token: {employee_token[:20]}...")
            
            # Test employee profile access
            print("\n🔍 Testing employee profile access...")
            employee_headers = {
                "Authorization": f"Token {employee_token}",
                "Content-Type": "application/json"
            }
            
            profile_response = test_api_request("GET", "/api/profile/", headers=employee_headers)
            if profile_response['success']:
                print("✅ Employee can access own profile!")
            else:
                print("❌ Employee cannot access own profile!")
                
        except Exception as e:
            print(f"❌ Error with employee login: {e}")
            return
    else:
        print("❌ Employee login failed!")
    
    # ===============================================================
    # 5. ADMIN PROFILE ACCESS
    # ===============================================================
    print_section("5. ADMIN PROFILE ACCESS")
    
    admin_profile_response = test_api_request("GET", "/api/profile/", headers=headers)
    if admin_profile_response['success']:
        print("✅ Admin can access own profile!")
    else:
        print("❌ Admin cannot access own profile!")
    
    # ===============================================================
    # 6. ADMIN ACCESS TO EMPLOYEE DETAILS
    # ===============================================================
    print_section("6. ADMIN ACCESS TO EMPLOYEE DETAILS")
    
    employee_detail_response = test_api_request("GET", f"/api/employees/{test_employee_id}/", headers=headers)
    if employee_detail_response['success']:
        print("✅ Admin can access employee details!")
    else:
        print("❌ Admin cannot access employee details!")
    
    # ===============================================================
    # 7. ADMIN UPDATE DEPARTMENT
    # ===============================================================
    print_section("7. ADMIN UPDATE DEPARTMENT")
    
    update_dept_data = {
        "name": f"Updated Test Department {timestamp}",
        "description": "Updated description for testing"
    }
    
    update_dept_response = test_api_request("PUT", f"/api/departments/{test_department_id}/", update_dept_data, headers)
    if update_dept_response['success']:
        print("✅ Admin can update department!")
    else:
        print("❌ Admin cannot update department!")
    
    # ===============================================================
    # 8. ADMIN UPDATE EMPLOYEE DATA
    # ===============================================================
    print_section("8. ADMIN UPDATE EMPLOYEE DATA")
    
    update_emp_data = {
        "first_name": "Updated",
        "last_name": "Employee",
        "position": "Updated Position"
    }
    
    update_emp_response = test_api_request("PATCH", f"/api/employees/{test_employee_id}/", update_emp_data, headers)
    if update_emp_response['success']:
        print("✅ Admin can update employee data!")
    else:
        print("❌ Admin cannot update employee data!")
    
    # ===============================================================
    # 9. EMPLOYEE SELF-UPDATE (if endpoint exists)
    # ===============================================================
    print_section("9. EMPLOYEE SELF-UPDATE")
    
    if employee_token:
        self_update_data = {
            "first_name": "SelfUpdated",
            "phone_number": "+628123999999"
        }
        
        # Try to update own profile
        self_update_response = test_api_request("PUT", "/api/profile/", self_update_data, employee_headers)
        if self_update_response['success']:
            print("✅ Employee can update own data!")
        else:
            print("❌ Employee cannot update own data (endpoint may not exist)!")
    
    # ===============================================================
    # 10. SOFT DELETE EMPLOYEE
    # ===============================================================
    print_section("10. SOFT DELETE EMPLOYEE")
    
    soft_delete_response = test_api_request("DELETE", f"/api/employees/{test_employee_id}/", headers=headers)
    if soft_delete_response['success']:
        print("✅ Employee soft delete successful!")
        
        # Verify employee is deactivated
        verify_response = test_api_request("GET", f"/api/employees/{test_employee_id}/", headers=headers)
        if verify_response['success']:
            employee_data = verify_response['data']
            if 'data' in employee_data:
                is_active = employee_data['data'].get('is_active', True)
            else:
                is_active = employee_data.get('is_active', True)
            
            if not is_active:
                print("✅ Employee successfully deactivated (soft delete)!")
            else:
                print("❌ Employee is still active after delete!")
        else:
            print("⚠️ Could not verify employee status after delete")
    else:
        print("❌ Employee soft delete failed!")
    
    # ===============================================================
    # 11. HARD DELETE DEPARTMENT
    # ===============================================================
    print_section("11. HARD DELETE DEPARTMENT")
    
    hard_delete_response = test_api_request("DELETE", f"/api/departments/{test_department_id}/", headers=headers)
    if hard_delete_response['success']:
        print("✅ Department hard delete successful!")
        
        # Verify department is completely removed
        verify_dept_response = test_api_request("GET", f"/api/departments/{test_department_id}/", headers=headers)
        if verify_dept_response['status_code'] == 404:
            print("✅ Department completely removed (hard delete)!")
        else:
            print("❌ Department still exists after delete!")
    else:
        print("❌ Department hard delete failed!")
    
    # ===============================================================
    # 12. EMPLOYEE LOGOUT WITH TOKEN INVALIDATION
    # ===============================================================
    print_section("12. EMPLOYEE LOGOUT WITH TOKEN INVALIDATION")
    
    if employee_token:
        print("🚪 Testing employee logout...")
        employee_logout_response = test_api_request("POST", "/api/logout/", headers=employee_headers, expect_json=False)
        
        if employee_logout_response['success']:
            print("✅ Employee logout successful!")
            
            # Verify token is invalidated
            print("🔍 Verifying employee token invalidation...")
            verify_logout_response = test_api_request("GET", "/api/profile/", headers=employee_headers)
            
            if verify_logout_response['status_code'] == 401:
                print("✅ Employee token invalidated successfully!")
            else:
                print("❌ Employee token still valid after logout!")
        else:
            print("❌ Employee logout failed!")
    
    # ===============================================================
    # 13. ADMIN LOGOUT WITH TOKEN INVALIDATION
    # ===============================================================
    print_section("13. ADMIN LOGOUT WITH TOKEN INVALIDATION")
    
    print("🚪 Testing admin logout...")
    admin_logout_response = test_api_request("POST", "/api/logout/", headers=headers, expect_json=False)
    
    if admin_logout_response['success']:
        print("✅ Admin logout successful!")
        
        # Verify token is invalidated
        print("🔍 Verifying admin token invalidation...")
        verify_admin_logout_response = test_api_request("GET", "/api/profile/", headers=headers)
        
        if verify_admin_logout_response['status_code'] == 401:
            print("✅ Admin token invalidated successfully!")
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
    print("   - Admin update department")
    print("   - Admin update employee data")
    print("   - Employee self-update (if endpoint exists)")
    print("   - Soft delete employee")
    print("   - Hard delete department")
    print("   - Employee logout with token invalidation")
    print("   - Admin logout with token invalidation")
    print("\n❌ If any features failed, check backend implementation.")
    print(f"\n🕐 Test completed at: {datetime.now()}")

if __name__ == "__main__":
    main()
