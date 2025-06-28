
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

        # --- CSV Data ---
        print("--- Testing CSV Data ---")
        
        # Get CSV sample
        print("Testing: GET /api/csv-sample/")
        response = requests.get(f"{BASE_URL}/api/csv-sample/", headers=headers)
        print_response(response)
        
        # Load CSV data
        print("Testing: POST /api/load-csv-data/")
        response = requests.post(f"{BASE_URL}/api/load-csv-data/", headers=headers)
        print_response(response)

        # --- Core API ---
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

if __name__ == "__main__":
    main()
