#!/usr/bin/env python3
"""
API Testing Script - Tests all available endpoints
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
test_user_token = None

def print_header(title):
    print(f"\n{'='*80}")
    print(f"🧪 {title}")
    print(f"{'='*80}")

def print_result(endpoint, method, status, success, message=""):
    status_icon = "✅" if success else "❌"
    print(f"{status_icon} {method} {endpoint} - {status} | {message}")

def test_endpoint(endpoint, method="GET", data=None, token=None, expected_status=[200]):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    if token:
        headers["Authorization"] = f"Basic {token}"  # Changed from Bearer to Basic
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        
        success = response.status_code in expected_status
        message = f"Response: {response.status_code}"
        
        if success and response.content:
            try:
                json_data = response.json()
                if 'count' in json_data:
                    message += f" | Count: {json_data['count']}"
                elif 'results' in json_data:
                    message += f" | Results: {len(json_data['results'])}"
                elif 'probability' in json_data:
                    message += f" | Probability: {json_data['probability']:.2f}"
                elif 'username' in json_data:
                    message += f" | User: {json_data['username']}"
                elif 'auth_token' in json_data:
                    message += " | Login Success"
                    return response.json()  # Return token data
            except:
                pass
        
        print_result(endpoint, method, response.status_code, success, message)
        return response.json() if success and response.content else None
        
    except Exception as e:
        print_result(endpoint, method, "ERROR", False, str(e))
        return None

def main():
    global test_user_token
    
    print_header("DJANGO TURNOVER PREDICTION API - LIVE TESTING")
    print(f"🎯 Base URL: {BASE_URL}")
    print(f"🕒 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test server connectivity
    print_header("1. SERVER CONNECTIVITY")
    test_endpoint("/", expected_status=[200, 404])  # Django might return 404 for root
    
    # Test authentication endpoints
    print_header("2. AUTHENTICATION ENDPOINTS")
    
    # Test registration (create test user)
    register_data = {
        "username": f"testuser_{int(time.time())}",
        "email": f"test_{int(time.time())}@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    register_response = test_endpoint("/api/auth/register/", "POST", register_data, expected_status=[201])
    
    # Test login
    login_data = {
        "username": register_data["username"],
        "password": register_data["password"]
    }
    
    login_response = test_endpoint("/api/auth/login/", "POST", login_data)
    if login_response and 'auth_token' in login_response:
        test_user_token = login_response['auth_token']
    
    # Test other auth endpoints
    test_endpoint("/api/auth/profile/", "GET", token=test_user_token)
    
    # Test refresh only if login was successful
    if login_response and 'refresh' in login_response:
        test_endpoint("/api/auth/refresh/", "POST", {"refresh": login_response['refresh']})
    
    # Check authentication
    test_endpoint("/api/auth/check/", "GET", token=test_user_token)
    
    # Test employee endpoints
    print_header("3. EMPLOYEE ENDPOINTS")
    test_endpoint("/api/employees/", "GET", token=test_user_token)
    test_endpoint("/api/employees/statistics/", "GET", token=test_user_token)
    test_endpoint("/api/employees/44999/", "GET", token=test_user_token)  # First ID
    test_endpoint("/api/employees/37500/", "GET", token=test_user_token)  # Mid-range ID  
    test_endpoint("/api/employees/30000/", "GET", token=test_user_token)  # Last ID
    
    # Test department endpoints
    print_header("4. DEPARTMENT ENDPOINTS")
    test_endpoint("/api/departments/", "GET", token=test_user_token)
    
    # Test prediction endpoints
    print_header("5. PREDICTION ENDPOINTS")
    
    # Single prediction
    prediction_data = {
        "satisfaction_level": 0.6,
        "last_evaluation": 0.8,
        "number_project": 4,
        "average_monthly_hours": 180,
        "time_spend_company": 3,
        "work_accident": 0,
        "promotion_last_5years": 0,
        "department": "sales",
        "salary": "medium"
    }
    
    test_endpoint("/api/predictions/predict/", "POST", prediction_data, token=test_user_token)
    
    # Bulk prediction
    bulk_data = {
        "employees": [prediction_data, {**prediction_data, "satisfaction_level": 0.3}]
    }
    test_endpoint("/api/predictions/bulk_predict/", "POST", bulk_data, token=test_user_token)
    
    # Test ML model endpoints
    print_header("6. ML MODEL ENDPOINTS")
    test_endpoint("/api/models/", "GET", token=test_user_token)
    test_endpoint("/api/models/active/", "GET", token=test_user_token)
    
    # Test prediction history
    print_header("7. PREDICTION HISTORY")
    test_endpoint("/api/predictions/", "GET", token=test_user_token)
    
    print_header("🎉 API TESTING COMPLETE")
    print("✨ All major endpoints have been tested!")
    print("📊 Check results above for detailed status of each endpoint")

if __name__ == "__main__":
    main()
