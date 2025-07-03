#!/usr/bin/env python3
"""
Complete API Endpoint Discovery for SMART-EN Turnover Prediction API
Generates comprehensive list of all available endpoints
"""

import os
import json
from datetime import datetime

# Base URL production DigitalOcean
BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"

def test_single_endpoint(endpoint, method="GET", auth_token=None, data=None):
    """Test single endpoint untuk melihat struktur response"""
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    
    if auth_token:
        headers['Authorization'] = f'Token {auth_token}'
    
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
        
        try:
            response_data = response.json()
        except:
            response_data = {"raw_response": response.text}
        
        return {
            'status_code': response.status_code,
            'response': response_data,
            'headers': dict(response.headers)
        }
        
    except Exception as e:
        return {
            'status_code': 'ERROR',
            'response': {'error': str(e)},
            'headers': {}
        }

def get_auth_token():
    """Dapatkan token untuk testing"""
    login_data = {
        "email": "employeejon@example.com",
        "password": "securepassword123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/login/",
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            # Struktur baru: {"success": true, "message": "...", "data": {"user": {...}}}
            if 'data' in data and 'user' in data['data'] and 'token' in data['data']['user']:
                return data['data']['user']['token']
        
        print(f"Login response: {response.text}")
        return None
        
    except Exception as e:
        print(f"Error getting token: {e}")
        return None

def discover_all_endpoints():
    """Discover semua endpoint dari API"""
    print("🔍 Discovering all API endpoints...")
    
    # Get auth token
    auth_token = get_auth_token()
    print(f"Auth token: {auth_token[:20] + '...' if auth_token else 'None'}")
    
    # List semua endpoint yang akan dites
    endpoints = [
        # Basic endpoints
        {"path": "/api/health/", "method": "GET", "auth": False, "name": "Health Check"},
        {"path": "/api/info/", "method": "GET", "auth": False, "name": "API Info"},
        {"path": "/", "method": "GET", "auth": False, "name": "API Root"},
        
        # Authentication endpoints
        {"path": "/api/register/", "method": "POST", "auth": False, "name": "Register Employee",
         "data": {
             "email": f"test_{int(datetime.now().timestamp())}@example.com",
             "password": "testpass123",
             "password_confirm": "testpass123",
             "first_name": "Test",
             "last_name": "User",
             "phone_number": "+6281234567890",
             "date_of_birth": "1990-01-01",
             "gender": "M",
             "marital_status": "single",
             "education_level": "bachelor",
             "address": "Test Address",
             "position": "Test Position",
             "department": 1,
             "hire_date": "2024-01-01"
         }},
        {"path": "/api/login/", "method": "POST", "auth": False, "name": "Login Employee",
         "data": {"email": "employeejon@example.com", "password": "securepassword123"}},
        {"path": "/api/logout/", "method": "POST", "auth": True, "name": "Logout Employee"},
        {"path": "/api/profile/", "method": "GET", "auth": True, "name": "User Profile"},
        
        # Department endpoints (ViewSet)
        {"path": "/api/departments/", "method": "GET", "auth": True, "name": "List Departments"},
        {"path": "/api/departments/", "method": "POST", "auth": True, "name": "Create Department",
         "data": {"name": "Test Department", "description": "Test description"}},
        {"path": "/api/departments/1/", "method": "GET", "auth": True, "name": "Get Department"},
        {"path": "/api/departments/1/", "method": "PUT", "auth": True, "name": "Update Department",
         "data": {"name": "Updated Department", "description": "Updated description"}},
        {"path": "/api/departments/1/", "method": "DELETE", "auth": True, "name": "Delete Department"},
        {"path": "/api/departments/1/employees/", "method": "GET", "auth": True, "name": "Department Employees"},
        
        # Employee endpoints (ViewSet)
        {"path": "/api/employees/", "method": "GET", "auth": True, "name": "List Employees"},
        {"path": "/api/employees/", "method": "POST", "auth": True, "name": "Create Employee",
         "data": {
             "email": f"admin_test_{int(datetime.now().timestamp())}@example.com",
             "password": "testpass123",
             "password_confirm": "testpass123",
             "first_name": "Admin",
             "last_name": "Test",
             "phone_number": "+6281234567891",
             "position": "Admin Position",
             "department": 1
         }},
        {"path": "/api/employees/3/", "method": "GET", "auth": True, "name": "Get Employee"},
        {"path": "/api/employees/3/", "method": "PUT", "auth": True, "name": "Update Employee",
         "data": {"first_name": "Updated", "last_name": "Employee"}},
        {"path": "/api/employees/3/", "method": "DELETE", "auth": True, "name": "Deactivate Employee"},
        {"path": "/api/employees/3/activate/", "method": "POST", "auth": True, "name": "Activate Employee"},
        {"path": "/api/employees/3/performance_data/", "method": "GET", "auth": True, "name": "Employee Performance Data"},
        {"path": "/api/employees/statistics/", "method": "GET", "auth": True, "name": "Employee Statistics"},
        
        # Legacy endpoints
        {"path": "/api/departments-list/", "method": "GET", "auth": False, "name": "List Departments (Legacy)"},
        {"path": "/api/employees-list/", "method": "GET", "auth": True, "name": "List Employees (Legacy)"},
        
        # Performance data endpoints
        {"path": "/api/performance/", "method": "GET", "auth": True, "name": "List Performance Data"},
        {"path": "/api/performance/", "method": "POST", "auth": True, "name": "Create Performance Data",
         "data": {
             "employee": 3,
             "satisfaction_level": 0.8,
             "last_evaluation": 0.9,
             "number_project": 3,
             "average_monthly_hours": 160,
             "time_spend_company": 2,
             "work_accident": False,
             "promotion_last_5years": False,
             "left": False
         }},
        
        # Stats endpoint
        {"path": "/api/stats/", "method": "GET", "auth": True, "name": "Data Separation Stats"},
    ]
    
    results = []
    
    for endpoint in endpoints:
        print(f"\n🔸 Testing {endpoint['method']} {endpoint['path']}")
        
        token = auth_token if endpoint['auth'] else None
        data = endpoint.get('data', None)
        
        result = test_single_endpoint(
            endpoint=endpoint['path'],
            method=endpoint['method'],
            auth_token=token,
            data=data
        )
        
        result['endpoint_info'] = endpoint
        results.append(result)
        
        print(f"   Status: {result['status_code']}")
        if result['status_code'] != 'ERROR':
            if 'success' in result['response']:
                print(f"   Success: {result['response']['success']}")
            if 'message' in result['response']:
                print(f"   Message: {result['response']['message']}")
    
    return results, auth_token

def generate_postman_collection(endpoints_results, auth_token):
    """Generate Postman Collection dari hasil discovery"""
    
    collection = {
        "info": {
            "name": "SMART-EN Turnover API - Complete Collection",
            "description": "Complete API collection for SMART-EN Turnover Prediction System with standardized responses",
            "version": "3.0.0",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "variable": [
            {
                "key": "base_url",
                "value": BASE_URL,
                "type": "string"
            },
            {
                "key": "auth_token",
                "value": auth_token or "your_auth_token_here",
                "type": "string"
            },
            {
                "key": "employee_id",
                "value": "3",
                "type": "string"
            },
            {
                "key": "department_id",
                "value": "1",
                "type": "string"
            }
        ],
        "item": []
    }
    
    # Group endpoints by category
    categories = {
        "Authentication & Core": [],
        "Department Management": [],
        "Employee Management": [],
        "Performance Data": [],
        "Legacy Endpoints": []
    }
    
    for result in endpoints_results:
        endpoint = result['endpoint_info']
        
        # Determine category
        path = endpoint['path']
        if path in ['/api/health/', '/api/info/', '/', '/api/register/', '/api/login/', '/api/logout/', '/api/profile/']:
            category = "Authentication & Core"
        elif 'departments' in path:
            category = "Department Management"
        elif 'employees' in path:
            category = "Employee Management"
        elif 'performance' in path or 'stats' in path:
            category = "Performance Data"
        else:
            category = "Legacy Endpoints"
        
        # Create request object
        request_obj = {
            "name": endpoint['name'],
            "request": {
                "method": endpoint['method'],
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "url": {
                    "raw": f"{{{{base_url}}}}{endpoint['path']}",
                    "host": ["{{base_url}}"],
                    "path": [p for p in endpoint['path'].split('/') if p]
                }
            },
            "response": []
        }
        
        # Add auth header if needed
        if endpoint['auth']:
            request_obj['request']['header'].append({
                "key": "Authorization",
                "value": "Token {{auth_token}}"
            })
        
        # Add body if POST/PUT
        if endpoint['method'] in ['POST', 'PUT', 'PATCH'] and 'data' in endpoint:
            request_obj['request']['body'] = {
                "mode": "raw",
                "raw": json.dumps(endpoint['data'], indent=2)
            }
        
        # Add example response
        if result['status_code'] != 'ERROR':
            example_response = {
                "name": f"Success - {endpoint['name']}",
                "originalRequest": request_obj['request'].copy(),
                "status": "OK" if result['status_code'] == 200 else "Created" if result['status_code'] == 201 else str(result['status_code']),
                "code": result['status_code'],
                "_postman_previewlanguage": "json",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "cookie": [],
                "body": json.dumps(result['response'], indent=2)
            }
            request_obj['response'].append(example_response)
        
        categories[category].append(request_obj)
    
    # Add categories to collection
    for category_name, items in categories.items():
        if items:  # Only add non-empty categories
            collection['item'].append({
                "name": category_name,
                "item": items
            })
    
    return collection

def main():
    print("🚀 COMPLETE API ENDPOINT DISCOVERY & POSTMAN COLLECTION GENERATION")
    print("=" * 80)
    print(f"🌐 Base URL: {BASE_URL}")
    
    # Discover all endpoints
    results, auth_token = discover_all_endpoints()
    
    print(f"\n📊 DISCOVERY RESULTS")
    print("=" * 50)
    print(f"Total endpoints tested: {len(results)}")
    
    successful = [r for r in results if r['status_code'] not in ['ERROR'] and r['status_code'] < 400]
    errors = [r for r in results if r['status_code'] == 'ERROR' or r['status_code'] >= 400]
    
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Errors: {len(errors)}")
    
    # Generate Postman Collection
    print(f"\n📝 GENERATING POSTMAN COLLECTION")
    print("=" * 50)
    
    collection = generate_postman_collection(results, auth_token)
    
    # Save to file
    output_file = "postman_collection.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Postman Collection saved to: {output_file}")
    print(f"📋 Collection contains:")
    for item in collection['item']:
        print(f"   • {item['name']}: {len(item['item'])} endpoints")
    
    print(f"\n💡 IMPORT INSTRUCTIONS:")
    print("1. Open Postman")
    print("2. Click 'Import'")
    print(f"3. Select the file: {output_file}")
    print("4. Collection will be imported with all endpoints ready to test")
    print(f"5. Update {{{{auth_token}}}} variable with your actual token: {auth_token[:20] + '...' if auth_token else 'Get from login endpoint'}")

if __name__ == "__main__":
    main()
