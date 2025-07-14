#!/usr/bin/env python3
"""
🚀 SMART-EN API - Comprehensive Test for All Fixed Features (Version 2)
Testing all CRUD operations with proper ID handling and endpoint fixes
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"
FIXED_EMPLOYEE_ID = 27  # Using existing employee ID as requested

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(f"🚀 {title}")
    print("="*80)

def test_api_request(method, endpoint, data=None, headers=None):
    """Make API request with proper error handling"""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"\n🔍 {method} {endpoint}")
    if data:
        print(f"📤 Request Data: {json.dumps(data, indent=2)}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method == "PATCH":
            response = requests.patch(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        
        print(f"📊 Status Code: {response.status_code}")
        
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
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return {'success': False, 'error': str(e)}

def main():
    """Main test function"""
    print("🚀 Testing All Fixed Features - SMART-EN API (Version 2)")
    print(f"🕐 Started at: {datetime.now()}")
    print(f"🌐 Base URL: {BASE_URL}")
    print(f"👤 Fixed Employee ID: {FIXED_EMPLOYEE_ID}")
    
    # Global variables
    admin_token = None
    employee_token = None
    test_department_id = None
    
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
            user_data = login_response['data']['data']['user']
            admin_token = user_data['token']
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
    # 3. ADMIN ACCESS TO EXISTING EMPLOYEE DETAILS (ID 27)
    # ===============================================================
    print_section("3. ADMIN ACCESS TO EXISTING EMPLOYEE DETAILS")
    
    emp_detail_response = test_api_request("GET", f"/api/employees/{FIXED_EMPLOYEE_ID}/", headers=headers)
    
    if emp_detail_response['success']:
        print(f"✅ Admin can access employee {FIXED_EMPLOYEE_ID} details!")
        # Extract employee email for login test
        try:
            employee_email = emp_detail_response['data']['data']['email']
            print(f"📧 Employee email: {employee_email}")
        except:
            try:
                employee_email = emp_detail_response['data']['email']
                print(f"📧 Employee email: {employee_email}")
            except Exception as e:
                print(f"❌ Could not extract employee email: {e}")
                employee_email = None
    else:
        print(f"❌ Admin cannot access employee {FIXED_EMPLOYEE_ID} details!")
        employee_email = None
    
    # ===============================================================
    # 4. ADMIN PROFILE ACCESS
    # ===============================================================
    print_section("4. ADMIN PROFILE ACCESS")
    
    admin_profile_response = test_api_request("GET", "/api/profile/", headers=headers)
    
    if admin_profile_response['success']:
        print("✅ Admin can access own profile!")
    else:
        print("❌ Admin cannot access own profile!")
    
    # ===============================================================
    # 5. ADMIN UPDATE DEPARTMENT
    # ===============================================================
    print_section("5. ADMIN UPDATE DEPARTMENT")
    
    update_dept_data = {
        "name": f"Updated Test Department {timestamp}",
        "description": "Updated description for testing"
    }
    
    dept_update_response = test_api_request("PUT", f"/api/departments/{test_department_id}/", update_dept_data, headers)
    
    if dept_update_response['success']:
        print("✅ Admin can update department!")
    else:
        print("❌ Admin cannot update department!")
    
    # ===============================================================
    # 6. ADMIN UPDATE EMPLOYEE DATA (Using numeric ID)
    # ===============================================================
    print_section("6. ADMIN UPDATE EMPLOYEE DATA")
    
    update_employee_data = {
        "first_name": "Updated",
        "last_name": "Employee",
        "position": "Updated Position"
    }
    
    emp_update_response = test_api_request("PATCH", f"/api/employees/{FIXED_EMPLOYEE_ID}/", update_employee_data, headers)
    
    if emp_update_response['success']:
        print(f"✅ Admin can update employee {FIXED_EMPLOYEE_ID} data!")
    else:
        print(f"❌ Admin cannot update employee {FIXED_EMPLOYEE_ID} data!")
    
    # ===============================================================
    # 7. EMPLOYEE LOGIN (Use provided credentials)
    # ===============================================================
    print_section("7. EMPLOYEE LOGIN & PROFILE ACCESS")
    
    # Use provided employee credentials
    employee_login_data = {
        "email": "bravely@gmail.com",
        "password": "user123"
    }
    
    emp_login_response = test_api_request("POST", "/api/login/", employee_login_data)
    
    if emp_login_response['success']:
        try:
            employee_token = emp_login_response['data']['data']['user']['token']
            print(f"✅ Employee login successful!")
            print(f"🔑 Employee token: {employee_token[:20]}...")
            employee_login_success = True
        except Exception as e:
            print(f"❌ Error extracting employee token: {e}")
            employee_token = None
            employee_login_success = False
    else:
        print("❌ Employee login failed!")
        employee_token = None
        employee_login_success = False
    
    # ===============================================================
    # 8. EMPLOYEE PROFILE ACCESS
    # ===============================================================
    if employee_token:
        print_section("8. EMPLOYEE PROFILE ACCESS")
        
        emp_headers = {
            "Authorization": f"Token {employee_token}",
            "Content-Type": "application/json"
        }
        
        emp_profile_response = test_api_request("GET", "/api/profile/", headers=emp_headers)
        
        if emp_profile_response['success']:
            print("✅ Employee can access own profile!")
        else:
            print("❌ Employee cannot access own profile!")
    else:
        print_section("8. EMPLOYEE PROFILE ACCESS - SKIPPED")
        print("❌ No employee token available")
    
    # ===============================================================
    # 9. EMPLOYEE SELF-UPDATE (Test different endpoints)
    # ===============================================================
    if employee_token:
        print_section("9. EMPLOYEE SELF-UPDATE")
        
        emp_headers = {
            "Authorization": f"Token {employee_token}",
            "Content-Type": "application/json"
        }
        
        update_profile_data = {
            "first_name": "SelfUpdated",
            "phone_number": "+628123999999"
        }
        
        # Try PATCH on correct profile update endpoint
        profile_update_response = test_api_request("PATCH", "/api/profile/update/", update_profile_data, emp_headers)
        
        if profile_update_response['success']:
            print("✅ Employee can update own profile via PATCH!")
        else:
            print("❌ Employee cannot update via PATCH /api/profile/update/")
            
            # Try PUT on profile update endpoint
            profile_update_put_response = test_api_request("PUT", "/api/profile/update/", update_profile_data, emp_headers)
            
            if profile_update_put_response['success']:
                print("✅ Employee can update own profile via PUT!")
            else:
                print("❌ Employee cannot update own data via any method!")
    else:
        print_section("9. EMPLOYEE SELF-UPDATE - SKIPPED")
        print("❌ No employee token available")
    
    # ===============================================================
    # 10. SOFT DELETE EMPLOYEE (Test with admin token)
    # ===============================================================
    print_section("10. SOFT DELETE EMPLOYEE")
    
    # Use admin token for delete operation
    delete_response = test_api_request("DELETE", f"/api/employees/{FIXED_EMPLOYEE_ID}/", headers=headers)
    
    if delete_response['success']:
        print(f"✅ Employee {FIXED_EMPLOYEE_ID} soft delete successful!")
        
        # Verify employee is deactivated by checking status
        verify_response = test_api_request("GET", f"/api/employees/{FIXED_EMPLOYEE_ID}/", headers=headers)
        if verify_response['success']:
            try:
                is_active = verify_response['data']['data']['is_active']
                if not is_active:
                    print("✅ Employee successfully deactivated (is_active=False)!")
                else:
                    print("❌ Employee still active after delete!")
            except:
                print("⚠️ Could not verify employee deactivation status")
    else:
        print(f"❌ Employee {FIXED_EMPLOYEE_ID} soft delete failed!")
    
    # ===============================================================
    # 11. HARD DELETE DEPARTMENT
    # ===============================================================
    print_section("11. HARD DELETE DEPARTMENT")
    
    dept_delete_response = test_api_request("DELETE", f"/api/departments/{test_department_id}/", headers=headers)
    
    if dept_delete_response['success']:
        print(f"✅ Department {test_department_id} hard delete successful!")
    else:
        print(f"❌ Department {test_department_id} hard delete failed!")
    
    # ===============================================================
    # 12. TOKEN INVALIDATION TESTS
    # ===============================================================
    print_section("12. TOKEN INVALIDATION TESTS")
    
    # Test employee logout and token invalidation
    if employee_token:
        print("🚪 Testing employee logout...")
        emp_headers = {
            "Authorization": f"Token {employee_token}",
            "Content-Type": "application/json"
        }
        
        emp_logout_response = test_api_request("POST", "/api/logout/", headers=emp_headers)
        
        if emp_logout_response['success']:
            print("✅ Employee logout successful!")
            
            # Verify token invalidation
            print("🔍 Verifying employee token invalidation...")
            token_verify_response = test_api_request("GET", "/api/profile/", headers=emp_headers)
            
            if not token_verify_response['success'] and token_verify_response['status_code'] == 401:
                print("✅ Employee token invalidated successfully!")
            else:
                print("❌ Employee token still valid after logout!")
        else:
            print("❌ Employee logout failed!")
    
    # Test admin logout and token invalidation
    print("🚪 Testing admin logout...")
    admin_logout_response = test_api_request("POST", "/api/logout/", headers=headers)
    
    if admin_logout_response['success']:
        print("✅ Admin logout successful!")
        
        # Verify token invalidation
        print("🔍 Verifying admin token invalidation...")
        admin_token_verify_response = test_api_request("GET", "/api/profile/", headers=headers)
        
        if not admin_token_verify_response['success'] and admin_token_verify_response['status_code'] == 401:
            print("✅ Admin token invalidated successfully!")
        else:
            print("❌ Admin token still valid after logout!")
    else:
        print("❌ Admin logout failed!")
    
    # ===============================================================
    # 13. SUMMARY
    # ===============================================================
    print_section("SUMMARY")
    print("📊 Test Results Summary:")
    print("=" * 50)
    print("✅ Features tested:")
    print("   - Admin login")
    print("   - Create department")
    print(f"   - Admin access to employee {FIXED_EMPLOYEE_ID} details")
    print("   - Admin profile access")
    print("   - Admin update department")
    print(f"   - Admin update employee {FIXED_EMPLOYEE_ID} data")
    print("   - Employee login (if possible)")
    print("   - Employee profile access")
    print("   - Employee self-update")
    print(f"   - Soft delete employee {FIXED_EMPLOYEE_ID}")
    print("   - Hard delete department")
    print("   - Token invalidation (both admin and employee)")
    
    print(f"\n🕐 Test completed at: {datetime.now()}")

if __name__ == "__main__":
    main()
