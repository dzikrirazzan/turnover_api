#!/usr/bin/env python3
"""
Test script untuk fitur delete department dan delete user/employee
"""

import requests
import json
import sys
from datetime import datetime

# Production API base URL
BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"

# Admin credentials untuk testing
ADMIN_CREDENTIALS = {
    "email": "admin@company.com",
    "password": "AdminPass123!"
}

class DeleteFeatureTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        
    def login(self):
        """Login sebagai admin untuk mendapatkan token"""
        print("🔐 Logging in as admin...")
        
        login_url = f"{BASE_URL}/api/login/"
        response = self.session.post(login_url, json=ADMIN_CREDENTIALS)
        
        if response.status_code == 200:
            data = response.json()
            # Handle different token response formats
            if 'data' in data and 'token' in data['data']:
                self.token = data['data']['token']
            elif 'token' in data:
                self.token = data['token']
            else:
                self.token = data.get('data', {}).get('user', {}).get('token')
            
            self.user_id = data.get('user', {}).get('id') or data.get('data', {}).get('user', {}).get('id')
            
            # Set authorization header
            self.session.headers.update({
                'Authorization': f'Token {self.token}' if self.token else '',
                'Content-Type': 'application/json'
            })
            
            print(f"✅ Login successful! User ID: {self.user_id}, Token: {self.token[:20] if self.token else 'None'}...")
            return True
        else:
            print(f"❌ Login failed! Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    
    def get_departments(self):
        """Get list of departments"""
        print("\n📁 Fetching departments...")
        
        url = f"{BASE_URL}/api/departments/"
        response = self.session.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Handle different response formats
            if isinstance(data, list):
                departments = data
            elif 'results' in data:
                departments = data['results']
            elif 'data' in data:
                departments = data['data']
            else:
                departments = []
            
            print(f"✅ Found {len(departments)} departments")
            
            for dept in departments[:3]:  # Show first 3
                print(f"   - {dept.get('id')}: {dept.get('name')}")
            
            return departments
        else:
            print(f"❌ Failed to get departments! Status: {response.status_code}")
            print(f"Response: {response.text}")
            return []
    
    def get_employees(self):
        """Get list of employees"""
        print("\n👥 Fetching employees...")
        
        url = f"{BASE_URL}/api/employees/"
        response = self.session.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Handle different response formats
            if isinstance(data, list):
                employees = data
            elif 'results' in data:
                employees = data['results']
            elif 'data' in data:
                employees = data['data']
            else:
                employees = []
            
            print(f"✅ Found {len(employees)} employees")
            
            for emp in employees[:3]:  # Show first 3
                print(f"   - {emp.get('id')}: {emp.get('first_name')} {emp.get('last_name')} (Active: {emp.get('is_active', 'N/A')})")
            
            return employees
        else:
            print(f"❌ Failed to get employees! Status: {response.status_code}")
            print(f"Response: {response.text}")
            return []
    
    def create_test_department(self):
        """Create test department untuk dihapus"""
        print("\n🏢 Creating test department...")
        
        test_dept_data = {
            "name": f"Test Department {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "description": "Department created for delete testing"
        }
        
        url = f"{BASE_URL}/api/departments/"
        response = self.session.post(url, json=test_dept_data)
        
        if response.status_code == 201:
            dept = response.json()
            print(f"✅ Test department created! ID: {dept.get('id')}, Name: {dept.get('name')}")
            return dept
        else:
            print(f"❌ Failed to create test department! Status: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    def create_test_employee(self, dept_id=None):
        """Create test employee untuk dihapus"""
        print("\n👤 Creating test employee...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        test_emp_data = {
            "first_name": "Test",
            "last_name": f"Employee{timestamp}",
            "email": f"test.employee.{timestamp}@company.com",
            "phone": "+628123456789",
            "hire_date": "2024-01-01",
            "is_active": True
        }
        
        if dept_id:
            test_emp_data["department"] = dept_id
        
        url = f"{BASE_URL}/api/employees/"
        response = self.session.post(url, json=test_emp_data)
        
        if response.status_code == 201:
            emp = response.json()
            print(f"✅ Test employee created! ID: {emp.get('id')}, Name: {emp.get('first_name')} {emp.get('last_name')}")
            return emp
        else:
            print(f"❌ Failed to create test employee! Status: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    def test_delete_department(self, dept_id):
        """Test delete department"""
        print(f"\n🗑️ Testing delete department ID: {dept_id}...")
        
        url = f"{BASE_URL}/api/departments/{dept_id}/"
        response = self.session.delete(url)
        
        print(f"Delete response status: {response.status_code}")
        
        if response.status_code in [200, 204]:
            print("✅ Department delete request successful!")
            
            # Verify deletion by trying to get the department
            get_response = self.session.get(url)
            if get_response.status_code == 404:
                print("✅ Department successfully deleted (404 on GET)")
                return True
            else:
                print(f"⚠️ Department still exists after delete (GET status: {get_response.status_code})")
                return False
        else:
            print(f"❌ Department delete failed! Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    
    def test_delete_employee(self, emp_id):
        """Test delete employee (should be soft delete)"""
        print(f"\n🗑️ Testing delete employee ID: {emp_id}...")
        
        url = f"{BASE_URL}/api/employees/{emp_id}/"
        response = self.session.delete(url)
        
        print(f"Delete response status: {response.status_code}")
        
        if response.status_code in [200, 204]:
            print("✅ Employee delete request successful!")
            
            # Verify soft deletion by checking is_active status
            get_response = self.session.get(url)
            if get_response.status_code == 200:
                emp_data = get_response.json()
                is_active = emp_data.get('is_active')
                if is_active == False:
                    print("✅ Employee successfully soft deleted (is_active = False)")
                    return True
                else:
                    print(f"⚠️ Employee not soft deleted (is_active = {is_active})")
                    return False
            elif get_response.status_code == 404:
                print("✅ Employee hard deleted (404 on GET)")
                return True
            else:
                print(f"⚠️ Unexpected response after delete (GET status: {get_response.status_code})")
                return False
        else:
            print(f"❌ Employee delete failed! Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    
    def run_comprehensive_test(self):
        """Run comprehensive delete tests"""
        print("🚀 Starting comprehensive delete feature tests...\n")
        
        # Login first
        if not self.login():
            return False
        
        # Get current data
        departments = self.get_departments()
        employees = self.get_employees()
        
        # Test 1: Create and delete test department
        print("\n" + "="*50)
        print("TEST 1: CREATE AND DELETE DEPARTMENT")
        print("="*50)
        
        test_dept = self.create_test_department()
        if test_dept:
            dept_delete_success = self.test_delete_department(test_dept['id'])
        else:
            dept_delete_success = False
        
        # Test 2: Create and delete test employee
        print("\n" + "="*50)
        print("TEST 2: CREATE AND DELETE EMPLOYEE")
        print("="*50)
        
        test_emp = self.create_test_employee(
            dept_id=departments[0]['id'] if departments else None
        )
        if test_emp:
            emp_delete_success = self.test_delete_employee(test_emp['id'])
        else:
            emp_delete_success = False
        
        # Test 3: Try deleting existing department (if any)
        print("\n" + "="*50)
        print("TEST 3: DELETE EXISTING DEPARTMENT (OPTIONAL)")
        print("="*50)
        
        existing_dept_delete_success = True  # Default to true since this is optional
        if departments:
            # Ask which department to delete for testing
            print("Available departments for testing:")
            for i, dept in enumerate(departments[:5]):
                print(f"   {i+1}. {dept.get('name')} (ID: {dept.get('id')})")
            
            print("\nSkipping existing department delete to avoid data loss...")
            print("(Use manual testing if needed)")
        
        # Test 4: Try deleting existing employee (if any)
        print("\n" + "="*50)
        print("TEST 4: DELETE EXISTING EMPLOYEE (OPTIONAL)")
        print("="*50)
        
        existing_emp_delete_success = True  # Default to true since this is optional
        if employees:
            print("Available employees for testing:")
            for i, emp in enumerate(employees[:5]):
                print(f"   {i+1}. {emp.get('first_name')} {emp.get('last_name')} (ID: {emp.get('id')}, Active: {emp.get('is_active')})")
            
            print("\nSkipping existing employee delete to avoid data loss...")
            print("(Use manual testing if needed)")
        
        # Summary
        print("\n" + "="*50)
        print("TEST SUMMARY")
        print("="*50)
        
        results = {
            "Department Create & Delete": "✅ PASS" if dept_delete_success else "❌ FAIL",
            "Employee Create & Delete": "✅ PASS" if emp_delete_success else "❌ FAIL",
            "Existing Department Delete": "✅ SKIP" if existing_dept_delete_success else "❌ FAIL",
            "Existing Employee Delete": "✅ SKIP" if existing_emp_delete_success else "❌ FAIL"
        }
        
        for test, result in results.items():
            print(f"{test}: {result}")
        
        overall_success = dept_delete_success and emp_delete_success
        print(f"\nOverall Result: {'✅ PASS' if overall_success else '❌ FAIL'}")
        
        return overall_success

def main():
    tester = DeleteFeatureTester()
    success = tester.run_comprehensive_test()
    
    if not success:
        print("\n⚠️ Some tests failed. Check the backend implementation!")
        sys.exit(1)
    else:
        print("\n🎉 All delete features working correctly!")
        sys.exit(0)

if __name__ == "__main__":
    main()
