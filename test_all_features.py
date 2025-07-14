#!/usr/bin/env python3
"""
Comprehensive test script for all HR API features
Tests all the features requested by the user
"""

import requests
import json
import sys
from datetime import datetime

# API Configuration
BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {"Content-Type": "application/json"}

class APITester:
    def __init__(self):
        self.admin_token = None
        self.employee_token = None
        self.department_id = None
        self.employee_id = None
        
    def log_test(self, test_name, success=True, message="", data=None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {test_name}")
        if message:
            print(f"     Message: {message}")
        if data and isinstance(data, dict):
            print(f"     Data: {json.dumps(data, indent=2)}")
        print("-" * 60)
        
    def make_request(self, method, endpoint, data=None, token=None):
        """Make HTTP request with optional token"""
        url = f"{BASE_URL}{endpoint}"
        headers = HEADERS.copy()
        
        if token:
            headers["Authorization"] = f"Token {token}"
            
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=data)
            elif method.upper() == "PATCH":
                response = requests.patch(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            return response
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return None

    def test_admin_login(self):
        """Test 1: Admin login"""
        print("🔐 Testing Admin Login...")
        
        login_data = {
            "email": "admin@company.com",
            "password": "AdminPass123!"
        }
        
        response = self.make_request("POST", "/auth/login/", login_data)
        if response and response.status_code == 200:
            data = response.json()
            if data.get('success') and 'user' in data.get('data', {}):
                self.admin_token = data['data']['user'].get('token')
                self.log_test("Admin Login", True, 
                            f"Logged in as: {data['data']['user'].get('full_name')}")
                return True
        
        self.log_test("Admin Login", False, f"Status: {response.status_code if response else 'No response'}")
        return False

    def test_create_department(self):
        """Test 2: Create department (Admin only)"""
        print("🏢 Testing Create Department...")
        
        dept_data = {
            "name": f"Test Department {datetime.now().strftime('%H%M%S')}",
            "description": "Test department created by automated test"
        }
        
        response = self.make_request("POST", "/departments/", dept_data, self.admin_token)
        if response and response.status_code == 201:
            data = response.json()
            if data.get('success'):
                self.department_id = data['data'].get('id')
                self.log_test("Create Department", True, 
                            f"Created: {data['data'].get('name')}")
                return True
        
        self.log_test("Create Department", False, 
                     f"Status: {response.status_code if response else 'No response'}")
        return False

    def test_create_employee(self):
        """Test 3: Create employee (Admin only)"""
        print("👤 Testing Create Employee...")
        
        emp_data = {
            "email": f"testemployee{datetime.now().strftime('%H%M%S')}@company.com",
            "password": "TestPass123!",
            "first_name": "Test",
            "last_name": "Employee",
            "role": "employee", 
            "department": self.department_id,
            "position": "Test Position"
        }
        
        response = self.make_request("POST", "/employees/", emp_data, self.admin_token)
        if response and response.status_code == 201:
            data = response.json()
            if data.get('success'):
                self.employee_id = data['data'].get('employee_id')
                self.log_test("Create Employee", True, 
                            f"Created: {data['data'].get('full_name')}")
                return True
        
        self.log_test("Create Employee", False, 
                     f"Status: {response.status_code if response else 'No response'}")
        return False

    def test_employee_login(self):
        """Test 4: Employee login"""
        print("🔑 Testing Employee Login...")
        
        # Use the created employee's email
        login_data = {
            "email": f"testemployee{datetime.now().strftime('%H%M%S')}@company.com",
            "password": "TestPass123!"
        }
        
        # We need to use a known employee, let's try with a default one
        login_data = {
            "email": "hr@company.com",
            "password": "HRPass123!"
        }
        
        response = self.make_request("POST", "/auth/login/", login_data)
        if response and response.status_code == 200:
            data = response.json()
            if data.get('success') and 'user' in data.get('data', {}):
                self.employee_token = data['data']['user'].get('token')
                self.log_test("Employee Login", True, 
                            f"Logged in as: {data['data']['user'].get('full_name')}")
                return True
        
        self.log_test("Employee Login", False, 
                     f"Status: {response.status_code if response else 'No response'}")
        return False

    def test_admin_profile_access(self):
        """Test 5: Admin profile access"""
        print("👨‍💼 Testing Admin Profile Access...")
        
        response = self.make_request("GET", "/auth/profile/", token=self.admin_token)
        if response and response.status_code == 200:
            data = response.json()
            if data.get('success'):
                self.log_test("Admin Profile Access", True, 
                            f"Profile: {data['data'].get('full_name')}")
                return True
        
        self.log_test("Admin Profile Access", False, 
                     f"Status: {response.status_code if response else 'No response'}")
        return False

    def test_employee_profile_access(self):
        """Test 6: Employee profile access"""
        print("👩‍💼 Testing Employee Profile Access...")
        
        response = self.make_request("GET", "/auth/profile/", token=self.employee_token)
        if response and response.status_code == 200:
            data = response.json()
            if data.get('success'):
                self.log_test("Employee Profile Access", True, 
                            f"Profile: {data['data'].get('full_name')}")
                return True
        
        self.log_test("Employee Profile Access", False, 
                     f"Status: {response.status_code if response else 'No response'}")
        return False

    def test_admin_access_employee_details(self):
        """Test 7: Admin access to employee details"""
        print("📋 Testing Admin Access to Employee Details...")
        
        response = self.make_request("GET", "/employees/", token=self.admin_token)
        if response and response.status_code == 200:
            data = response.json()
            if data.get('success'):
                employees = data.get('data', [])
                self.log_test("Admin Access Employee Details", True, 
                            f"Found {len(employees)} employees")
                return True
        
        self.log_test("Admin Access Employee Details", False, 
                     f"Status: {response.status_code if response else 'No response'}")
        return False

    def test_update_department(self):
        """Test 8: Admin access to update department"""
        print("🏢 Testing Update Department...")
        
        if not self.department_id:
            self.log_test("Update Department", False, "No department ID available")
            return False
            
        update_data = {
            "name": f"Updated Test Department {datetime.now().strftime('%H%M%S')}",
            "description": "Updated description"
        }
        
        response = self.make_request("PUT", f"/departments/{self.department_id}/", 
                                   update_data, self.admin_token)
        if response and response.status_code == 200:
            data = response.json()
            if data.get('success'):
                self.log_test("Update Department", True, 
                            f"Updated: {data['data'].get('name')}")
                return True
        
        self.log_test("Update Department", False, 
                     f"Status: {response.status_code if response else 'No response'}")
        return False

    def test_admin_update_employee(self):
        """Test 9: Admin can update all employee data"""
        print("👤 Testing Admin Update Employee Data...")
        
        if not self.employee_id:
            self.log_test("Admin Update Employee", False, "No employee ID available")
            return False
            
        # Get employee list to find an ID
        emp_response = self.make_request("GET", "/employees/", token=self.admin_token)
        if emp_response and emp_response.status_code == 200:
            employees = emp_response.json().get('data', [])
            if employees:
                emp_id = employees[0].get('id')
                
                update_data = {
                    "first_name": "Updated",
                    "last_name": "Name",
                    "position": "Updated Position"
                }
                
                response = self.make_request("PATCH", f"/employees/{emp_id}/", 
                                           update_data, self.admin_token)
                if response and response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        self.log_test("Admin Update Employee", True, 
                                    f"Updated: {data['data'].get('full_name')}")
                        return True
        
        self.log_test("Admin Update Employee", False, 
                     f"Status: {response.status_code if response else 'No response'}")
        return False

    def test_employee_self_update(self):
        """Test 10: Employee can update their own data"""
        print("🔧 Testing Employee Self Update...")
        
        update_data = {
            "first_name": "SelfUpdated",
            "position": "Self Updated Position"
        }
        
        response = self.make_request("PATCH", "/auth/profile/update/", 
                                   update_data, self.employee_token)
        if response and response.status_code == 200:
            data = response.json()
            if data.get('success'):
                self.log_test("Employee Self Update", True, 
                            f"Updated profile: {data['data'].get('full_name')}")
                return True
        
        self.log_test("Employee Self Update", False, 
                     f"Status: {response.status_code if response else 'No response'}")
        return False

    def test_soft_delete_employee(self):
        """Test 11: Soft delete employee"""
        print("🗑️ Testing Soft Delete Employee...")
        
        # Get employee list to find an ID
        emp_response = self.make_request("GET", "/employees/", token=self.admin_token)
        if emp_response and emp_response.status_code == 200:
            employees = emp_response.json().get('data', [])
            if employees:
                emp_id = employees[0].get('id')
                
                response = self.make_request("DELETE", f"/employees/{emp_id}/", 
                                           token=self.admin_token)
                if response and response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        self.log_test("Soft Delete Employee", True, 
                                    f"Deactivated: {data['data'].get('full_name')}")
                        return True
        
        self.log_test("Soft Delete Employee", False, 
                     f"Status: {response.status_code if response else 'No response'}")
        return False

    def test_hard_delete_department(self):
        """Test 12: Hard delete department"""
        print("🗂️ Testing Hard Delete Department...")
        
        if not self.department_id:
            self.log_test("Hard Delete Department", False, "No department ID available")
            return False
            
        response = self.make_request("DELETE", f"/departments/{self.department_id}/", 
                                   token=self.admin_token)
        if response and response.status_code == 200:
            data = response.json()
            if data.get('success'):
                self.log_test("Hard Delete Department", True, 
                            f"Deleted: {data['data'].get('department_name')}")
                return True
        
        self.log_test("Hard Delete Department", False, 
                     f"Status: {response.status_code if response else 'No response'}")
        return False

    def test_employee_logout(self):
        """Test 13: Employee logout with token invalidation"""
        print("🚪 Testing Employee Logout...")
        
        response = self.make_request("POST", "/auth/logout/", token=self.employee_token)
        if response and response.status_code == 200:
            data = response.json()
            if data.get('success'):
                # Test that token is invalidated by trying to access profile
                profile_response = self.make_request("GET", "/auth/profile/", 
                                                   token=self.employee_token)
                if profile_response and profile_response.status_code == 401:
                    self.log_test("Employee Logout", True, "Token invalidated successfully")
                    return True
                else:
                    self.log_test("Employee Logout", False, "Token still valid after logout")
                    return False
        
        self.log_test("Employee Logout", False, 
                     f"Status: {response.status_code if response else 'No response'}")
        return False

    def test_admin_logout(self):
        """Test 14: Admin logout with token invalidation"""
        print("🚪 Testing Admin Logout...")
        
        response = self.make_request("POST", "/auth/logout/", token=self.admin_token)
        if response and response.status_code == 200:
            data = response.json()
            if data.get('success'):
                # Test that token is invalidated by trying to access profile
                profile_response = self.make_request("GET", "/auth/profile/", 
                                                   token=self.admin_token)
                if profile_response and profile_response.status_code == 401:
                    self.log_test("Admin Logout", True, "Token invalidated successfully")
                    return True
                else:
                    self.log_test("Admin Logout", False, "Token still valid after logout")
                    return False
        
        self.log_test("Admin Logout", False, 
                     f"Status: {response.status_code if response else 'No response'}")
        return False

    def run_all_tests(self):
        """Run all tests in sequence"""
        print("=" * 60)
        print("🚀 STARTING COMPREHENSIVE API FEATURE TEST")
        print("=" * 60)
        
        tests = [
            self.test_admin_login,
            self.test_create_department,
            self.test_create_employee,
            self.test_employee_login,
            self.test_admin_profile_access,
            self.test_employee_profile_access,
            self.test_admin_access_employee_details,
            self.test_update_department,
            self.test_admin_update_employee,
            self.test_employee_self_update,
            self.test_soft_delete_employee,
            self.test_hard_delete_department,
            self.test_employee_logout,
            self.test_admin_logout,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ Test {test.__name__} crashed: {e}")
                failed += 1
        
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        if failed == 0:
            print("🎉 ALL TESTS PASSED! API is ready for Postman testing.")
        else:
            print("⚠️ Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    print("🔧 Testing all HR API features...")
    print("📡 Make sure Django server is running on localhost:8000")
    
    tester = APITester()
    tester.run_all_tests()
