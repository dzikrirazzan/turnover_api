#!/usr/bin/env python3
"""
Test CSV Upload Flow for HR Dashboard
Tests the complete workflow from login to CSV processing
"""

import requests
import json
import csv
import io

# Configuration
API_BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"
USERNAME = "admin"
PASSWORD = "newstrongpassword123"

def test_login():
    """Test user login"""
    print("🔐 Testing login...")
    
    response = requests.post(
        f"{API_BASE_URL}/api/auth/login/",
        json={"username": USERNAME, "password": PASSWORD}
    )
    
    if response.status_code == 200:
        data = response.json()
        auth_token = data.get("auth_header")
        print(f"✅ Login successful! Token: {auth_token[:20]}...")
        return auth_token
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_single_prediction(auth_token):
    """Test single employee prediction"""
    print("\n🔮 Testing single prediction...")
    
    headers = {"Authorization": auth_token, "Content-Type": "application/json"}
    
    employee_data = {
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
    
    response = requests.post(
        f"{API_BASE_URL}/api/predictions/predict/",
        headers=headers,
        json=employee_data
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Prediction successful!")
        print(f"   Probability: {data['probability']:.3f}")
        print(f"   Risk Level: {data['risk_level']}")
        print(f"   Recommendations: {len(data['recommendations'])} items")
        return True
    else:
        print(f"❌ Prediction failed: {response.text}")
        return False

def test_bulk_prediction(auth_token):
    """Test bulk prediction (simulating CSV upload)"""
    print("\n📊 Testing bulk prediction...")
    
    headers = {"Authorization": auth_token, "Content-Type": "application/json"}
    
    employees_data = {
        "employees": [
            {
                "employee_id": "EMP001",
                "satisfaction_level": 0.75,
                "last_evaluation": 0.85,
                "number_project": 4,
                "average_monthly_hours": 180,
                "time_spend_company": 3,
                "work_accident": False,
                "promotion_last_5years": False,
                "salary": "medium",
                "department": "IT"
            },
            {
                "employee_id": "EMP002",
                "satisfaction_level": 0.45,
                "last_evaluation": 0.60,
                "number_project": 2,
                "average_monthly_hours": 250,
                "time_spend_company": 6,
                "work_accident": True,
                "promotion_last_5years": False,
                "salary": "low",
                "department": "sales"
            },
            {
                "employee_id": "EMP003",
                "satisfaction_level": 0.80,
                "last_evaluation": 0.90,
                "number_project": 5,
                "average_monthly_hours": 160,
                "time_spend_company": 2,
                "work_accident": False,
                "promotion_last_5years": True,
                "salary": "high",
                "department": "engineering"
            }
        ]
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/predictions/bulk_predict/",
        headers=headers,
        json=employees_data
    )
    
    if response.status_code == 200:
        data = response.json()
        predictions = data["predictions"]
        print(f"✅ Bulk prediction successful!")
        print(f"   Processed {len(predictions)} employees")
        
        # Calculate statistics
        high_risk = len([p for p in predictions if p["risk_level"] == "High"])
        medium_risk = len([p for p in predictions if p["risk_level"] == "Medium"])
        low_risk = len([p for p in predictions if p["risk_level"] == "Low"])
        avg_prob = sum(p["probability"] for p in predictions) / len(predictions)
        
        print(f"   High Risk: {high_risk}")
        print(f"   Medium Risk: {medium_risk}")
        print(f"   Low Risk: {low_risk}")
        print(f"   Average Probability: {avg_prob:.3f}")
        
        return True
    else:
        print(f"❌ Bulk prediction failed: {response.text}")
        return False

def test_employees_endpoint(auth_token):
    """Test employees endpoint"""
    print("\n👥 Testing employees endpoint...")
    
    headers = {"Authorization": auth_token}
    
    response = requests.get(
        f"{API_BASE_URL}/api/employees/",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Employees endpoint working!")
        print(f"   Total employees in database: {data['count']}")
        if data['results']:
            emp = data['results'][0]
            print(f"   Sample employee: {emp['name']} ({emp['employee_id']})")
        return True
    else:
        print(f"❌ Employees endpoint failed: {response.text}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting HR Dashboard API Tests")
    print("=" * 50)
    
    # Test login
    auth_token = test_login()
    if not auth_token:
        print("❌ Cannot proceed without authentication")
        return
    
    # Test various endpoints
    success_count = 0
    total_tests = 4
    
    if test_employees_endpoint(auth_token):
        success_count += 1
    
    if test_single_prediction(auth_token):
        success_count += 1
    
    if test_bulk_prediction(auth_token):
        success_count += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📈 Test Summary: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 All tests passed! HR Dashboard is ready for use.")
        print("\n📝 Next steps:")
        print("   1. Open frontend_hr_dashboard.html in browser")
        print("   2. Login with admin/newstrongpassword123")
        print("   3. Download CSV template")
        print("   4. Upload CSV file for batch predictions")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    main()
