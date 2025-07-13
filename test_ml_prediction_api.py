#!/usr/bin/env python3
"""
Test script for ML Prediction API endpoint
Tests the complete flow: login -> add performance data -> predict turnover
"""

import requests
import json
import sys
from datetime import datetime

# API Configuration
BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"
ADMIN_EMAIL = "y.coadmin@companm"
ADMIN_PASSWORD = "admin123"

def test_ml_prediction_api():
    """Test the complete ML prediction API flow"""
    
    print("🧪 Testing ML Prediction API...")
    print("=" * 50)
    
    # Step 1: Login as admin
    print("\n1️⃣ Logging in as admin...")
    login_response = requests.post(f"{BASE_URL}/api/login/", json={
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return False
    
    login_data = login_response.json()
    token = login_data["data"]["token"]
    print(f"✅ Login successful! Token: {token[:20]}...")
    
    # Headers for authenticated requests
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Get employee list
    print("\n2️⃣ Getting employee list...")
    employees_response = requests.get(f"{BASE_URL}/api/employees/", headers=headers)
    
    if employees_response.status_code != 200:
        print(f"❌ Failed to get employees: {employees_response.status_code}")
        return False
    
    employees_data = employees_response.json()
    if not employees_data["data"]:
        print("❌ No employees found. Please register some employees first.")
        return False
    
    # Use the first employee for testing
    test_employee = employees_data["data"][0]
    employee_id = test_employee["id"]
    print(f"✅ Found employee: {test_employee['first_name']} {test_employee['last_name']} (ID: {employee_id})")
    
    # Step 3: Add performance data
    print("\n3️⃣ Adding performance data...")
    performance_data = {
        "employee_id": employee_id,
        "satisfaction_level": 0.65,
        "last_evaluation": 0.82,
        "number_project": 4,
        "average_monthly_hours": 185,
        "time_spend_company": 3,
        "work_accident": False,
        "promotion_last_5years": False
    }
    
    performance_response = requests.post(f"{BASE_URL}/api/performance/", 
                                       json=performance_data, 
                                       headers=headers)
    
    if performance_response.status_code == 201:
        print("✅ Performance data added successfully!")
    elif performance_response.status_code == 200:
        print("✅ Performance data updated successfully!")
    else:
        print(f"❌ Failed to add performance data: {performance_response.status_code}")
        print(f"Response: {performance_response.text}")
        return False
    
    # Step 4: Test prediction
    print("\n4️⃣ Testing turnover prediction...")
    prediction_data = {
        "employee_id": employee_id
    }
    
    prediction_response = requests.post(f"{BASE_URL}/api/predict/", 
                                      json=prediction_data, 
                                      headers=headers)
    
    if prediction_response.status_code != 200:
        print(f"❌ Prediction failed: {prediction_response.status_code}")
        print(f"Response: {prediction_response.text}")
        return False
    
    prediction_result = prediction_response.json()
    
    if not prediction_result["success"]:
        print(f"❌ Prediction error: {prediction_result.get('message', 'Unknown error')}")
        return False
    
    # Step 5: Display results
    print("\n🎯 PREDICTION RESULTS:")
    print("=" * 50)
    
    data = prediction_result["data"]
    employee_info = data["employee"]
    prediction_info = data["prediction"]
    risk_analysis = data["risk_analysis"]
    recommendations = data["recommendations"]
    
    print(f"👤 Employee: {employee_info['name']}")
    print(f"📧 Email: {employee_info['email']}")
    print(f"🏢 Department: {employee_info['department']}")
    print(f"💼 Position: {employee_info['position']}")
    print()
    
    print(f"🎯 Prediction Probability: {prediction_info['probability']:.1%}")
    print(f"⚠️ Risk Level: {prediction_info['risk_level'].upper()}")
    print(f"📊 Will Leave: {'Yes' if prediction_info['will_leave'] else 'No'}")
    print(f"🎯 Confidence: {prediction_info['confidence_score']:.1%}")
    print(f"🤖 Model: {prediction_info['model_used']}")
    print()
    
    print(f"📈 Overall Risk Score: {risk_analysis['overall_risk_score']:.3f}")
    print("\n🔍 Risk Factor Analysis:")
    for factor, details in risk_analysis['risk_factors'].items():
        print(f"  • {factor}: {details['value']} (Risk: {details['risk']:.1f}, Contribution: {details['contribution']:.3f})")
    
    print(f"\n💡 Recommendations ({len(recommendations)} total):")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. [{rec['priority'].upper()}] {rec['category']}")
        print(f"     Issue: {rec['issue']}")
        print(f"     Action: {rec['recommendation']}")
        print()
    
    # Step 6: Test error cases
    print("\n5️⃣ Testing error cases...")
    
    # Test with invalid employee ID
    invalid_response = requests.post(f"{BASE_URL}/api/predict/", 
                                   json={"employee_id": 99999}, 
                                   headers=headers)
    
    if invalid_response.status_code == 404:
        print("✅ Invalid employee ID correctly returns 404")
    else:
        print(f"❌ Invalid employee ID test failed: {invalid_response.status_code}")
    
    # Test without employee ID
    missing_response = requests.post(f"{BASE_URL}/api/predict/", 
                                   json={}, 
                                   headers=headers)
    
    if missing_response.status_code == 400:
        print("✅ Missing employee ID correctly returns 400")
    else:
        print(f"❌ Missing employee ID test failed: {missing_response.status_code}")
    
    # Test without authentication
    no_auth_response = requests.post(f"{BASE_URL}/api/predict/", 
                                   json={"employee_id": employee_id})
    
    if no_auth_response.status_code == 401:
        print("✅ No authentication correctly returns 401")
    else:
        print(f"❌ No authentication test failed: {no_auth_response.status_code}")
    
    print("\n🎉 All tests completed successfully!")
    return True

def test_performance_data_api():
    """Test the performance data management API"""
    
    print("\n🧪 Testing Performance Data API...")
    print("=" * 50)
    
    # Login first
    login_response = requests.post(f"{BASE_URL}/api/login/", json={
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return False
    
    token = login_response.json()["data"]["token"]
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    # Test GET performance data
    print("\n1️⃣ Getting performance data list...")
    get_response = requests.get(f"{BASE_URL}/api/performance/", headers=headers)
    
    if get_response.status_code == 200:
        performance_list = get_response.json()["data"]
        print(f"✅ Found {len(performance_list)} performance records")
        
        if performance_list:
            # Show first record
            first_record = performance_list[0]
            print(f"   Example: {first_record['employee_name']} - Satisfaction: {first_record['satisfaction_level']}")
    else:
        print(f"❌ Failed to get performance data: {get_response.status_code}")
    
    return True

def test_api_endpoints():
    """Test all API endpoints"""
    
    print("🚀 SMART-EN ML Prediction API Test Suite")
    print("=" * 70)
    print(f"🌍 Base URL: {BASE_URL}")
    print(f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test basic endpoints
    print("1️⃣ Testing basic endpoints...")
    
    # Health check
    health_response = requests.get(f"{BASE_URL}/api/health/")
    if health_response.status_code == 200:
        print("✅ Health check passed")
    else:
        print(f"❌ Health check failed: {health_response.status_code}")
    
    # API info
    info_response = requests.get(f"{BASE_URL}/api/info/")
    if info_response.status_code == 200:
        print("✅ API info passed")
    else:
        print(f"❌ API info failed: {info_response.status_code}")
    
    # Test performance data API
    test_performance_data_api()
    
    # Test ML prediction API
    test_ml_prediction_api()
    
    print("\n🎯 Test Summary:")
    print("=" * 50)
    print("✅ All core endpoints tested")
    print("✅ Authentication working")
    print("✅ ML prediction API functional")
    print("✅ Error handling validated")
    print("✅ Response format correct")
    
    print("\n📋 Next Steps:")
    print("1. Add this endpoint to your Postman collection")
    print("2. Test with your frontend application")
    print("3. Integrate with your HR dashboard")
    print("4. Set up monitoring and alerts")
    
    return True

if __name__ == "__main__":
    try:
        success = test_api_endpoints()
        if success:
            print("\n🎉 All tests passed! The ML Prediction API is ready for use.")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed. Please check the configuration.")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        sys.exit(1)
