import requests
import json

BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"

def print_response(response):
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response JSON: {response.json()}")
    except json.JSONDecodeError:
        print(f"Response Text: {response.text}")
    print("-" * 20)

def main():
    # --- Authentication ---
    print("--- Testing Authentication ---")
    
    # Register a new user
    print("Testing: POST /api/auth/register/")
    register_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "password_confirm": "testpassword"
    }
    response = requests.post(f"{BASE_URL}/api/auth/register/", json=register_data)
    print_response(response)
    
    # Log in to get the auth token
    print("Testing: POST /api/auth/login/")
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login/", json=login_data)
    print_response(response)
    
    if response.status_code == 200:
        auth_header = response.json().get("auth_header")
        headers = {"Authorization": auth_header}

        # --- Testing Core API ---
        print("--- Testing Core API ---")
        
        # Get departments
        print("Testing: GET /api/departments/")
        response = requests.get(f"{BASE_URL}/api/departments/", headers=headers)
        print_response(response)
        
        # Get employees
        print("Testing: GET /api/employees/")
        response = requests.get(f"{BASE_URL}/api/employees/", headers=headers)
        print_response(response)
        
        # Get employee statistics
        print("Testing: GET /api/employees/statistics/")
        response = requests.get(f"{BASE_URL}/api/employees/statistics/", headers=headers)
        print_response(response)
        
        # Get predictions
        print("Testing: GET /api/predictions/")
        response = requests.get(f"{BASE_URL}/api/predictions/", headers=headers)
        print_response(response)
        
        # Get models
        print("Testing: GET /api/models/")
        response = requests.get(f"{BASE_URL}/api/models/", headers=headers)
        print_response(response)
        
        # Get active model
        print("Testing: GET /api/models/active/")
        response = requests.get(f"{BASE_URL}/api/models/active/", headers=headers)
        print_response(response)

        # --- Testing ML Prediction with Custom Data ---
        print("--- Testing ML Prediction with Custom Data ---")
        
        # Sample employee data for prediction (adjust values as needed)
        sample_employee_data = {
            "satisfaction_level": 0.4,
            "last_evaluation": 0.5,
            "number_project": 2,
            "average_monthly_hours": 150,
            "time_spend_company": 3,
            "work_accident": False,
            "promotion_last_5years": False,
            "salary": "low",
            "department": "sales"
        }
        
        print("Testing: POST /api/predictions/predict/ with custom data (Low Risk Example)")
        response = requests.post(f"{BASE_URL}/api/predictions/predict/", headers=headers, json=sample_employee_data)
        print_response(response)

        # Another sample for high risk
        high_risk_employee_data = {
            "satisfaction_level": 0.1,
            "last_evaluation": 0.9,
            "number_project": 6,
            "average_monthly_hours": 280,
            "time_spend_company": 5,
            "work_accident": False,
            "promotion_last_5years": False,
            "salary": "low",
            "department": "technical"
        }
        print("Testing: POST /api/predictions/predict/ with custom data (High Risk Example)")
        response = requests.post(f"{BASE_URL}/api/predictions/predict/", headers=headers, json=high_risk_employee_data)
        print_response(response)

if __name__ == "__main__":
    main()