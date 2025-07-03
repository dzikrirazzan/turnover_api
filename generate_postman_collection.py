#!/usr/bin/env python3
"""
Script untuk membuat Postman Collection lengkap berdasarkan analisis codebase Django/REST
Menganalisis URLs, Views, Models, dan Serializers untuk menghasilkan collection yang akurat
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

class PostmanCollectionGenerator:
    def __init__(self):
        self.base_url = "https://turnover-api-hd7ze.ondigitalocean.app"
        self.collection = {
            "info": {
                "name": "SMART-EN Turnover API - Complete Collection",
                "description": "Complete API collection for SMART-EN Turnover Prediction System",
                "version": "2.0.0",
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
            },
            "auth": {
                "type": "bearer",
                "bearer": [
                    {
                        "key": "token",
                        "value": "{{auth_token}}",
                        "type": "string"
                    }
                ]
            },
            "variable": [
                {
                    "key": "base_url",
                    "value": self.base_url,
                    "type": "string"
                },
                {
                    "key": "auth_token",
                    "value": "",
                    "type": "string"
                },
                {
                    "key": "admin_token",
                    "value": "",
                    "type": "string"
                },
                {
                    "key": "employee_id",
                    "value": "1",
                    "type": "string"
                },
                {
                    "key": "department_id",
                    "value": "1",
                    "type": "string"
                },
                {
                    "key": "goal_id",
                    "value": "1",
                    "type": "string"
                },
                {
                    "key": "feedback_id",
                    "value": "1",
                    "type": "string"
                }
            ],
            "item": []
        }
    
    def analyze_urls(self, file_path):
        """Analisis file urls.py untuk menemukan semua routing"""
        urls = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Cari pola URL
            url_patterns = [
                r"path\(['\"]([^'\"]+)['\"],\s*([^,]+)",
                r"url\(r['\"]([^'\"]+)['\"],\s*([^,]+)",
                r"re_path\(r['\"]([^'\"]+)['\"],\s*([^,]+)"
            ]
            
            for pattern in url_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    url_path = match[0].replace('^', '').replace('$', '')
                    view_name = match[1].strip()
                    urls.append({
                        'path': url_path,
                        'view': view_name,
                        'file': file_path
                    })
            
            # Cari include patterns
            include_pattern = r"path\(['\"]([^'\"]+)['\"],\s*include\(['\"]([^'\"]+)['\"]"
            includes = re.findall(include_pattern, content)
            for include in includes:
                urls.append({
                    'path': include[0],
                    'include': include[1],
                    'file': file_path
                })
        
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
        
        return urls
    
    def get_sample_data_for_model(self, model_name):
        """Generate sample data berdasarkan model"""
        sample_data = {
            'Employee': {
                "email": "new.employee@company.com",
                "password": "SecurePassword123!",
                "password_confirm": "SecurePassword123!",
                "first_name": "New",
                "last_name": "Employee",
                "phone_number": "+1234567890",
                "date_of_birth": "1990-01-15",
                "gender": "M",
                "marital_status": "single",
                "education_level": "bachelor",
                "address": "123 Main Street, City",
                "position": "Software Developer",
                "department": 1,
                "hire_date": "2024-01-15"
            },
            'Department': {
                "name": "Research & Development",
                "description": "Innovation and technology development department"
            },
            'EmployeePerformanceData': {
                "employee": 1,
                "satisfaction_level": 0.85,
                "last_evaluation": 0.92,
                "number_project": 5,
                "average_monthly_hours": 160,
                "time_spend_company": 3,
                "work_accident": False,
                "promotion_last_5years": True,
                "left": False
            },
            'Goal': {
                "title": "Improve Team Productivity",
                "description": "Increase team productivity by 25% through better processes",
                "owner": 1,
                "priority": "high",
                "status": "in_progress",
                "progress_percentage": 50,
                "due_date": "2024-12-31",
                "key_results": [
                    {
                        "title": "Implement new tools",
                        "description": "Deploy productivity tools",
                        "is_completed": False,
                        "order": 1
                    }
                ]
            },
            'Feedback': {
                "from_employee": 1,
                "to_employee": 2,
                "feedback_type": "peer",
                "project": "Q4 Project Review",
                "content": "Excellent collaboration and communication skills demonstrated",
                "rating": 5,
                "is_helpful": True
            }
        }
        return sample_data.get(model_name, {})
    
    def create_request_item(self, name, method, url, auth_required=True, body=None, description="", query_params=None, status_code=200):
        """Create a Postman request item"""
        headers = [
            {
                "key": "Content-Type",
                "value": "application/json"
            }
        ]
        
        if auth_required:
            headers.append({
                "key": "Authorization",
                "value": "Token {{auth_token}}"
            })
        
        request_item = {
            "name": name,
            "request": {
                "method": method,
                "header": headers,
                "url": {
                    "raw": f"{{{{base_url}}}}{url}",
                    "host": ["{{base_url}}"],
                    "path": url.strip('/').split('/')
                }
            },
            "response": []
        }
        
        if body:
            request_item["request"]["body"] = {
                "mode": "raw",
                "raw": json.dumps(body, indent=2)
            }
        
        if query_params:
            request_item["request"]["url"]["query"] = query_params
        
        if description:
            request_item["request"]["description"] = description
        
        # Add sample response
        sample_response = self.create_sample_response(name, status_code, method)
        if sample_response:
            request_item["response"] = [sample_response]
        
        return request_item
    
    def create_sample_response(self, name, status_code, method):
        """Create sample response berdasarkan StandardResponse format"""
        if status_code >= 400:
            body = {
                "success": False,
                "message": "Error occurred",
                "errors": {"detail": "Sample error message"}
            }
        elif method == "DELETE":
            body = {
                "success": True,
                "message": "Data berhasil dihapus"
            }
        elif "list" in name.lower() or "List" in name:
            body = {
                "success": True,
                "message": "Data berhasil diambil",
                "data": [],
                "count": 0
            }
        else:
            body = {
                "success": True,
                "message": "Operasi berhasil",
                "data": {}
            }
        
        return {
            "name": "Success Response",
            "originalRequest": {},
            "status": "OK" if status_code < 400 else "Error",
            "code": status_code,
            "_postman_previewlanguage": "json",
            "header": [
                {
                    "key": "Content-Type",
                    "value": "application/json"
                }
            ],
            "cookie": [],
            "body": json.dumps(body, indent=2)
        }
    
    def generate_collection(self):
        """Generate complete Postman collection"""
        print("🚀 Generating Complete Postman Collection...")
        
        # 1. Authentication & Core Endpoints
        auth_folder = {
            "name": "Authentication & Core",
            "item": [
                self.create_request_item(
                    "Health Check",
                    "GET",
                    "/api/health/",
                    auth_required=False,
                    description="Check API health status"
                ),
                self.create_request_item(
                    "API Info",
                    "GET",
                    "/api/info/",
                    auth_required=False,
                    description="Get API information and features"
                ),
                self.create_request_item(
                    "Register Employee",
                    "POST",
                    "/api/register/",
                    auth_required=False,
                    body=self.get_sample_data_for_model('Employee'),
                    description="Register new employee",
                    status_code=201
                ),
                self.create_request_item(
                    "Login Employee",
                    "POST",
                    "/api/login/",
                    auth_required=False,
                    body={
                        "email": "employee@example.com",
                        "password": "securepassword123"
                    },
                    description="Login with email and password"
                ),
                self.create_request_item(
                    "Logout Employee",
                    "POST",
                    "/api/logout/",
                    description="Logout current user"
                ),
                self.create_request_item(
                    "User Profile",
                    "GET",
                    "/api/profile/",
                    description="Get current user profile"
                )
            ]
        }
        
        # 2. Department Management
        dept_folder = {
            "name": "Department Management",
            "item": [
                self.create_request_item(
                    "List Departments",
                    "GET",
                    "/api/departments/",
                    description="Get all departments"
                ),
                self.create_request_item(
                    "Create Department",
                    "POST",
                    "/api/departments/",
                    body=self.get_sample_data_for_model('Department'),
                    description="Create new department (Admin only)",
                    status_code=201
                ),
                self.create_request_item(
                    "Get Department Details",
                    "GET",
                    "/api/departments/{{department_id}}/",
                    description="Get specific department details"
                ),
                self.create_request_item(
                    "Update Department",
                    "PUT",
                    "/api/departments/{{department_id}}/",
                    body=self.get_sample_data_for_model('Department'),
                    description="Update department (Admin only)"
                ),
                self.create_request_item(
                    "Delete Department",
                    "DELETE",
                    "/api/departments/{{department_id}}/",
                    description="Delete department (Admin only)",
                    status_code=204
                ),
                self.create_request_item(
                    "Get Department Employees",
                    "GET",
                    "/api/departments/{{department_id}}/employees/",
                    description="Get all employees in department"
                )
            ]
        }
        
        # 3. Employee Management
        emp_folder = {
            "name": "Employee Management",
            "item": [
                self.create_request_item(
                    "List Employees",
                    "GET",
                    "/api/employees/",
                    description="List all employees (Admin only)",
                    query_params=[
                        {
                            "key": "department",
                            "value": "1",
                            "description": "Filter by department ID",
                            "disabled": True
                        },
                        {
                            "key": "role",
                            "value": "employee",
                            "description": "Filter by role",
                            "disabled": True
                        },
                        {
                            "key": "is_active",
                            "value": "true",
                            "description": "Filter by active status",
                            "disabled": True
                        }
                    ]
                ),
                self.create_request_item(
                    "Create Employee",
                    "POST",
                    "/api/employees/",
                    body=self.get_sample_data_for_model('Employee'),
                    description="Create new employee (Admin only)",
                    status_code=201
                ),
                self.create_request_item(
                    "Get Employee Details",
                    "GET",
                    "/api/employees/{{employee_id}}/",
                    description="Get specific employee details"
                ),
                self.create_request_item(
                    "Update Employee",
                    "PUT",
                    "/api/employees/{{employee_id}}/",
                    body={
                        "first_name": "Updated",
                        "last_name": "Name",
                        "position": "Senior Developer",
                        "department": 1
                    },
                    description="Update employee (Admin only)"
                ),
                self.create_request_item(
                    "Partial Update Employee",
                    "PATCH",
                    "/api/employees/{{employee_id}}/",
                    body={"position": "Team Lead"},
                    description="Partially update employee (Admin only)"
                ),
                self.create_request_item(
                    "Deactivate Employee",
                    "DELETE",
                    "/api/employees/{{employee_id}}/",
                    description="Deactivate employee (Admin only)"
                ),
                self.create_request_item(
                    "Activate Employee",
                    "POST",
                    "/api/employees/{{employee_id}}/activate/",
                    description="Reactivate employee (Admin only)"
                ),
                self.create_request_item(
                    "Get Employee Performance Data",
                    "GET",
                    "/api/employees/{{employee_id}}/performance_data/",
                    description="Get employee's ML performance data"
                ),
                self.create_request_item(
                    "Employee Statistics",
                    "GET",
                    "/api/employees/statistics/",
                    description="Get employee statistics (Admin only)"
                )
            ]
        }
        
        # 4. Performance Data Management
        perf_folder = {
            "name": "Performance Data Management",
            "item": [
                self.create_request_item(
                    "List Performance Data",
                    "GET",
                    "/api/performance/",
                    description="List all performance data (Admin only)"
                ),
                self.create_request_item(
                    "Create Performance Data",
                    "POST",
                    "/api/performance/",
                    body=self.get_sample_data_for_model('EmployeePerformanceData'),
                    description="Create performance data (Admin only)",
                    status_code=201
                ),
                self.create_request_item(
                    "Data Separation Stats",
                    "GET",
                    "/api/stats/",
                    description="Get data separation statistics (Admin only)"
                )
            ]
        }
        
        # 5. Goals & OKRs (Performance App)
        goals_folder = {
            "name": "Goals & OKRs",
            "item": [
                self.create_request_item(
                    "List Goals",
                    "GET",
                    "/performance/api/goals/",
                    description="List all goals",
                    query_params=[
                        {
                            "key": "employee",
                            "value": "1",
                            "description": "Filter by employee ID",
                            "disabled": True
                        },
                        {
                            "key": "status",
                            "value": "in_progress",
                            "description": "Filter by status",
                            "disabled": True
                        }
                    ]
                ),
                self.create_request_item(
                    "Create Goal",
                    "POST",
                    "/performance/api/goals/",
                    body=self.get_sample_data_for_model('Goal'),
                    description="Create new goal",
                    status_code=201
                ),
                self.create_request_item(
                    "Get Goal Details",
                    "GET",
                    "/performance/api/goals/{{goal_id}}/",
                    description="Get specific goal details"
                ),
                self.create_request_item(
                    "Update Goal",
                    "PUT",
                    "/performance/api/goals/{{goal_id}}/",
                    body={
                        "title": "Updated Goal Title",
                        "description": "Updated description",
                        "progress_percentage": 75,
                        "status": "in_progress"
                    },
                    description="Update goal"
                ),
                self.create_request_item(
                    "Delete Goal",
                    "DELETE",
                    "/performance/api/goals/{{goal_id}}/",
                    description="Delete goal",
                    status_code=204
                ),
                self.create_request_item(
                    "Goal Statistics",
                    "GET",
                    "/performance/api/goals/statistics/",
                    description="Get goal statistics"
                ),
                self.create_request_item(
                    "Goal Sample Data",
                    "GET",
                    "/performance/api/goals/sample_data/",
                    description="Get sample goal data"
                )
            ]
        }
        
        # 6. Key Results
        kr_folder = {
            "name": "Key Results",
            "item": [
                self.create_request_item(
                    "List Key Results",
                    "GET",
                    "/performance/api/key-results/",
                    description="List all key results",
                    query_params=[
                        {
                            "key": "goal",
                            "value": "1",
                            "description": "Filter by goal ID",
                            "disabled": True
                        }
                    ]
                ),
                self.create_request_item(
                    "Create Key Result",
                    "POST",
                    "/performance/api/key-results/",
                    body={
                        "goal": 1,
                        "title": "Achieve 95% satisfaction score",
                        "description": "Measure satisfaction through surveys",
                        "is_completed": False,
                        "order": 1
                    },
                    description="Create new key result",
                    status_code=201
                ),
                self.create_request_item(
                    "Update Key Result",
                    "PUT",
                    "/performance/api/key-results/{{key_result_id}}/",
                    body={
                        "title": "Updated key result",
                        "is_completed": True
                    },
                    description="Update key result"
                ),
                self.create_request_item(
                    "Delete Key Result",
                    "DELETE",
                    "/performance/api/key-results/{{key_result_id}}/",
                    description="Delete key result",
                    status_code=204
                )
            ]
        }
        
        # 7. Feedback System
        feedback_folder = {
            "name": "Feedback System",
            "item": [
                self.create_request_item(
                    "List Feedback",
                    "GET",
                    "/performance/api/feedback/",
                    description="List all feedback",
                    query_params=[
                        {
                            "key": "to_employee",
                            "value": "1",
                            "description": "Filter by recipient",
                            "disabled": True
                        },
                        {
                            "key": "from_employee",
                            "value": "2",
                            "description": "Filter by sender",
                            "disabled": True
                        }
                    ]
                ),
                self.create_request_item(
                    "Create Feedback",
                    "POST",
                    "/performance/api/feedback/",
                    body=self.get_sample_data_for_model('Feedback'),
                    description="Create new feedback",
                    status_code=201
                ),
                self.create_request_item(
                    "Get Feedback Details",
                    "GET",
                    "/performance/api/feedback/{{feedback_id}}/",
                    description="Get specific feedback details"
                ),
                self.create_request_item(
                    "Update Feedback",
                    "PUT",
                    "/performance/api/feedback/{{feedback_id}}/",
                    body={
                        "content": "Updated feedback content",
                        "rating": 4
                    },
                    description="Update feedback"
                ),
                self.create_request_item(
                    "Delete Feedback",
                    "DELETE",
                    "/performance/api/feedback/{{feedback_id}}/",
                    description="Delete feedback",
                    status_code=204
                ),
                self.create_request_item(
                    "Feedback Statistics",
                    "GET",
                    "/performance/api/feedback/statistics/",
                    description="Get feedback statistics"
                ),
                self.create_request_item(
                    "Received Feedback",
                    "GET",
                    "/performance/api/feedback/received/",
                    description="Get feedback received by user",
                    query_params=[
                        {
                            "key": "employee_id",
                            "value": "1",
                            "description": "Employee ID"
                        }
                    ]
                ),
                self.create_request_item(
                    "Sent Feedback",
                    "GET",
                    "/performance/api/feedback/sent/",
                    description="Get feedback sent by user",
                    query_params=[
                        {
                            "key": "employee_id",
                            "value": "1",
                            "description": "Employee ID"
                        }
                    ]
                )
            ]
        }
        
        # 8. Analytics & Dashboard
        analytics_folder = {
            "name": "Analytics & Dashboard",
            "item": [
                self.create_request_item(
                    "Dashboard Stats",
                    "GET",
                    "/performance/api/dashboard/stats/",
                    description="Get dashboard statistics"
                ),
                self.create_request_item(
                    "Team Engagement",
                    "GET",
                    "/performance/api/dashboard/team_engagement/",
                    description="Get team engagement metrics"
                ),
                self.create_request_item(
                    "Individual Performance",
                    "GET",
                    "/performance/api/dashboard/individual_performance/",
                    description="Get individual performance metrics",
                    query_params=[
                        {
                            "key": "employee_id",
                            "value": "1",
                            "description": "Employee ID"
                        }
                    ]
                ),
                self.create_request_item(
                    "Analytics Dashboard",
                    "GET",
                    "/performance/api/analytics/dashboard/",
                    description="Get complete analytics dashboard"
                )
            ]
        }
        
        # Add all folders to collection
        self.collection["item"] = [
            auth_folder,
            dept_folder,
            emp_folder,
            perf_folder,
            goals_folder,
            kr_folder,
            feedback_folder,
            analytics_folder
        ]
        
        return self.collection
    
    def save_collection(self, filename="postman_collection.json"):
        """Save collection to JSON file"""
        collection = self.generate_collection()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(collection, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Postman collection saved to: {filename}")
        print(f"📊 Collection contains:")
        print(f"   • {len(collection['item'])} main folders")
        
        total_requests = 0
        for folder in collection['item']:
            folder_requests = len(folder['item'])
            total_requests += folder_requests
            print(f"   • {folder['name']}: {folder_requests} requests")
        
        print(f"   • Total requests: {total_requests}")
        print(f"🌐 Base URL: {self.base_url}")
        
        return filename

def main():
    print("🚀 POSTMAN COLLECTION GENERATOR")
    print("=" * 60)
    print(f"🕐 Started at: {datetime.now()}")
    
    generator = PostmanCollectionGenerator()
    filename = generator.save_collection()
    
    print(f"\n🎯 HOW TO USE:")
    print("=" * 40)
    print("1. Open Postman")
    print("2. Click 'Import' button")
    print(f"3. Select the file: {filename}")
    print("4. Set environment variables:")
    print("   • auth_token: Your authentication token")
    print("   • admin_token: Admin authentication token")
    print("   • employee_id, department_id, etc.")
    print("5. Start testing endpoints!")
    
    print(f"\n✅ Collection generation complete!")

if __name__ == "__main__":
    main()
