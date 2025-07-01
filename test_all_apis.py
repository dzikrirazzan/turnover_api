#!/usr/bin/env python3
"""
Quick API Test Script for SMART-EN System
Tests all major endpoints to ensure they're working correctly
"""

import requests
import json
import base64
from datetime import datetime

# Configuration
BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"
USERNAME = "testuser"
PASSWORD = "testpassword123"

# Generate Basic Auth token
auth_token = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
headers = {
    "Authorization": f"Basic {auth_token}",
    "Content-Type": "application/json"
}

def test_endpoint(method, endpoint, data=None, auth_required=True):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    req_headers = headers if auth_required else {"Content-Type": "application/json"}
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=req_headers, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, headers=req_headers, json=data, timeout=30)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=req_headers, json=data, timeout=30)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=req_headers, timeout=30)
        
        status = "✅ PASS" if response.status_code < 400 else "❌ FAIL"
        print(f"{status} {method} {endpoint} - Status: {response.status_code}")
        
        if response.status_code >= 400:
            print(f"     Error: {response.text[:200]}")
        
        return response
    
    except Exception as e:
        print(f"❌ FAIL {method} {endpoint} - Error: {str(e)}")
        return None

def main():
    print("🚀 Testing SMART-EN System API Endpoints")
    print("=" * 50)
    
    # 1. System Health Check
    print("\n🔍 1. SYSTEM HEALTH")
    test_endpoint("GET", "/predictions/health/", auth_required=False)
    test_endpoint("GET", "/api/", auth_required=False)
    
    # 2. Authentication Tests
    print("\n🔐 2. AUTHENTICATION")
    
    # Register new user
    register_data = {
        "username": "apitest",
        "email": "apitest@example.com",
        "password": "testpass123",
        "first_name": "API",
        "last_name": "Test"
    }
    test_endpoint("POST", "/api/auth/register/", register_data, auth_required=False)
    
    # Login
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    test_endpoint("POST", "/api/auth/login/", login_data, auth_required=False)
    
    # Get profile
    test_endpoint("GET", "/api/auth/profile/")
    
    # 3. Department Tests
    print("\n🏢 3. DEPARTMENTS")
    test_endpoint("GET", "/api/departments/")
    
    # Create department
    dept_data = {
        "name": f"Test Department {datetime.now().strftime('%H%M%S')}",
        "description": "Test department created by API test"
    }
    dept_response = test_endpoint("POST", "/api/departments/", dept_data)
    
    # 4. Employee Tests
    print("\n👥 4. EMPLOYEES")
    test_endpoint("GET", "/api/employees/")
    
    # Create employee (if department was created successfully)
    if dept_response and dept_response.status_code < 400:
        try:
            dept_id = dept_response.json().get('id', 1)
        except:
            dept_id = 1
            
        emp_data = {
            "employee_id": f"TEST{datetime.now().strftime('%H%M%S')}",
            "name": "Test Employee",
            "email": f"test.employee.{datetime.now().strftime('%H%M%S')}@company.com",
            "department": dept_id,
            "hire_date": "2023-01-15",
            "satisfaction_level": 0.75,
            "last_evaluation": 0.80,
            "number_project": 5,
            "average_monthly_hours": 180,
            "time_spend_company": 2,
            "work_accident": False,
            "promotion_last_5years": False,
            "salary": "medium",
            "left": False
        }
        emp_response = test_endpoint("POST", "/api/employees/", emp_data)
    
    # Search employees
    test_endpoint("GET", "/api/employees/?search=test")
    
    # 5. Prediction Tests
    print("\n🤖 5. TURNOVER PREDICTIONS")
    
    # Custom prediction
    prediction_data = {
        "satisfaction_level": 0.38,
        "last_evaluation": 0.53,
        "number_project": 2,
        "average_monthly_hours": 157,
        "time_spend_company": 3,
        "work_accident": 0,
        "promotion_last_5years": 0,
        "department": "sales",
        "salary": "low"
    }
    test_endpoint("POST", "/predictions/predict-custom/", prediction_data)
    
    # Get predictions
    test_endpoint("GET", "/api/predictions/")
    
    # High risk employees
    test_endpoint("GET", "/predictions/high-risk/")
    
    # Model performance
    test_endpoint("GET", "/predictions/model-performance/")
    
    # Feature importance
    test_endpoint("GET", "/predictions/feature-importance/")
    
    # 6. Performance Management Tests
    print("\n🎯 6. PERFORMANCE MANAGEMENT")
    
    # Dashboard
    test_endpoint("GET", "/performance/api/dashboard/")
    
    # Reviews
    test_endpoint("GET", "/performance/api/reviews/")
    
    # Goals
    test_endpoint("GET", "/performance/api/goals/")
    
    # Feedback
    test_endpoint("GET", "/performance/api/feedback/")
    
    # 7. Analytics Tests
    print("\n📊 7. ANALYTICS & REPORTS")
    
    # Department analytics
    test_endpoint("GET", "/performance/api/analytics/department/")
    
    # Turnover analytics
    test_endpoint("GET", "/predictions/analytics/")
    
    # Performance trends
    test_endpoint("GET", "/performance/api/analytics/trends/")
    
    # Satisfaction report
    test_endpoint("GET", "/performance/api/reports/satisfaction/")
    
    # 8. ML Models
    print("\n🧠 8. ML MODELS")
    test_endpoint("GET", "/api/ml-models/")
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Completed!")
    print("📋 Check the results above for any failed endpoints")
    print("🔗 Base URL:", BASE_URL)

if __name__ == "__main__":
    main()
