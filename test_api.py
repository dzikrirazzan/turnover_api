
import requests
import json
import os

BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"

def print_response(response):
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response JSON: {response.json()}")
    except json.JSONDecodeError:
        print(f"Response Text: {response.text}")
    print("-" * 20)

def create_csv_file(filename, data):
    with open(filename, 'w') as f:
        for row in data:
            f.write(','.join(map(str, row)) + '\n')

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
    
    auth_header = None
    if response.status_code == 200:
        auth_header = response.json().get("auth_header")
        headers = {"Authorization": auth_header}

        # --- Testing Core API ---
        print("--- Testing Core API ---")
        
        # Get departments
        print("Testing: GET /api/departments/")
        response = requests.get(f"{BASE_URL}/api/departments/", headers=headers)
        print_response(response)
        
        # Create a department for employee creation
        print("Testing: POST /api/departments/ (for employee creation)")
        dept_data = {"name": "Test Dept", "description": "A department for testing"}
        response = requests.post(f"{BASE_URL}/api/departments/", headers=headers, json=dept_data)
        print_response(response)
        test_dept_id = None
        if response.status_code == 201:
            test_dept_id = response.json().get("id")

        # Get employees
        print("Testing: GET /api/employees/")
        response = requests.get(f"{BASE_URL}/api/employees/", headers=headers)
        print_response(response)
        
        # Create an employee for specific prediction test
        employee_id_for_prediction = None
        if test_dept_id:
            print("Testing: POST /api/employees/ (for specific prediction)")
            emp_data = {
                "employee_id": "TEST001",
                "name": "Test Employee",
                "email": "test.emp@company.com",
                "department": test_dept_id,
                "hire_date": "2023-06-01",
                "satisfaction_level": 0.8,
                "last_evaluation": 0.7,
                "number_project": 3,
                "average_monthly_hours": 160,
                "time_spend_company": 1,
                "work_accident": False,
                "promotion_last_5years": False,
                "salary": "medium"
            }
            response = requests.post(f"{BASE_URL}/api/employees/", headers=headers, json=emp_data)
            print_response(response)
            if response.status_code == 201:
                employee_id_for_prediction = response.json().get("id")

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

        # --- Testing New Features: CSV Upload and Template ---
        print("--- Testing New Features: CSV Upload and Template ---")

        # Test GET /api/predictions/csv-template/
        print("Testing: GET /api/predictions/csv-template/")
        response = requests.get(f"{BASE_URL}/api/predictions/csv-template/", headers=headers)
        print_response(response)
        if response.status_code == 200:
            try:
                with open("turnover_prediction_template.csv", "wb") as f:
                    f.write(response.content)
                print("CSV template downloaded successfully.")
            except Exception as e:
                print(f"Error saving CSV template: {e}")

        # Test POST /api/predictions/upload-csv/
        print("Testing: POST /api/predictions/upload-csv/ with valid CSV")
        csv_data = [
            ["employee_id", "name", "satisfaction_level", "last_evaluation", "number_project", "average_monthly_hours", "time_spend_company", "work_accident", "promotion_last_5years", "salary", "department"],
            ["CSVEMP001", "CSV Employee 1", 0.6, 0.7, 3, 180, 2, 0, 0, "medium", "sales"],
            ["CSVEMP002", "CSV Employee 2", 0.2, 0.9, 5, 280, 4, 0, 0, "low", "technical"]
        ]
        create_csv_file("test_upload.csv", csv_data)

        with open("test_upload.csv", "rb") as f:
            files = {'file': ('test_upload.csv', f, 'text/csv')}
            response = requests.post(f"{BASE_URL}/api/predictions/upload-csv/", headers=headers, files=files)
            print_response(response)

        # Test POST /api/predictions/upload-csv/ with invalid file type
        print("Testing: POST /api/predictions/upload-csv/ with invalid file type")
        with open("invalid.txt", "w") as f: f.write("not a csv")
        with open("invalid.txt", "rb") as f:
            files = {'file': ('invalid.txt', f, 'text/plain')}
            response = requests.post(f"{BASE_URL}/api/predictions/upload-csv/", headers=headers, files=files)
            print_response(response)

        # Test POST /api/predictions/upload-csv/ with missing columns
        print("Testing: POST /api/predictions/upload-csv/ with missing columns")
        missing_col_data = [
            ["employee_id", "name", "satisfaction_level"],
            ["CSVEMP003", "CSV Employee 3", 0.5]
        ]
        create_csv_file("missing_cols.csv", missing_col_data)
        with open("missing_cols.csv", "rb") as f:
            files = {'file': ('missing_cols.csv', f, 'text/csv')}
            response = requests.post(f"{BASE_URL}/api/predictions/upload-csv/", headers=headers, files=files)
            print_response(response)

        # Clean up created files
        for f in ["turnover_prediction_template.csv", "test_upload.csv", "invalid.txt", "missing_cols.csv"]:
            if os.path.exists(f):
                os.remove(f)

        # --- Test specific employee prediction after creation ---
        if employee_id_for_prediction:
            print(f"Testing: POST /api/employees/{employee_id_for_prediction}/predict_turnover/")
            response = requests.post(f"{BASE_URL}/api/employees/{employee_id_for_prediction}/predict_turnover/", headers=headers)
            print_response(response)

        # --- Test Logout ---
        print("--- Testing Logout ---")
        print("Testing: POST /api/auth/logout/")
        response = requests.post(f"{BASE_URL}/api/auth/logout/", headers=headers)
        print_response(response)

    else:
        print("Login failed. Cannot proceed with API tests.")

if __name__ == "__main__":
    main()
