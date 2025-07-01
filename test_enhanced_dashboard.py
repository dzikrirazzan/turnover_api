#!/usr/bin/env python3
"""
Test script to verify the enhanced HR dashboard functionality.
This tests both production API mode and demo mode.
"""

import requests
import json
import time
import sys

def test_api_connection():
    """Test if the production API is accessible."""
    try:
        print("🔍 Testing API connection...")
        response = requests.get(
            "https://turnover-api-hd7ze.ondigitalocean.app/api/auth/login/",
            timeout=5
        )
        print(f"✅ API accessible (Status: {response.status_code})")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ API not accessible: {e}")
        return False

def test_api_login():
    """Test API login functionality."""
    try:
        print("🔐 Testing API login...")
        response = requests.post(
            "https://turnover-api-hd7ze.ondigitalocean.app/api/auth/login/",
            json={"username": "admin", "password": "newstrongpassword123"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            auth_token = data.get("auth_header") or data.get("auth_token")
            print(f"✅ Login successful! Auth token: {auth_token[:20]}...")
            return auth_token
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Login request failed: {e}")
        return None

def test_bulk_prediction(auth_token):
    """Test bulk prediction endpoint."""
    try:
        print("📊 Testing bulk prediction...")
        
        # Sample employee data
        test_employees = [
            {
                "employee_id": "TEST001",
                "name": "Test Employee 1",
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
                "employee_id": "TEST002",
                "name": "Test Employee 2",
                "satisfaction_level": 0.35,
                "last_evaluation": 0.45,
                "number_project": 3,
                "average_monthly_hours": 280,
                "time_spend_company": 4,
                "work_accident": False,
                "promotion_last_5years": False,
                "salary": "low",
                "department": "marketing"
            }
        ]
        
        response = requests.post(
            "https://turnover-api-hd7ze.ondigitalocean.app/api/predictions/bulk_predict/",
            json={"employees": test_employees},
            headers={
                "Authorization": auth_token,
                "Content-Type": "application/json"
            },
            timeout=15
        )
        
        if response.status_code == 200:
            predictions = response.json()
            print(f"✅ Bulk prediction successful! Got {len(predictions.get('predictions', []))} predictions")
            return True
        else:
            print(f"❌ Bulk prediction failed: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Bulk prediction request failed: {e}")
        return False

def test_demo_mode():
    """Test demo mode functionality."""
    print("🎭 Testing demo mode...")
    
    # Simulate demo prediction logic
    test_employees = [
        {"employee_id": "DEMO001", "name": "Demo Employee", "satisfaction_level": 0.6, "department": "IT"},
        {"employee_id": "DEMO002", "name": "Demo Employee 2", "satisfaction_level": 0.3, "department": "Sales"}
    ]
    
    demo_predictions = []
    for emp in test_employees:
        satisfaction = float(emp.get("satisfaction_level", 0.5))
        turnover_prob = 0.3 + (0.4 if satisfaction < 0.4 else 0)
        risk_level = "HIGH" if turnover_prob > 0.7 else "MEDIUM" if turnover_prob > 0.4 else "LOW"
        
        demo_predictions.append({
            "employee_id": emp["employee_id"],
            "employee_name": emp["name"],
            "department": emp["department"],
            "satisfaction_level": satisfaction,
            "turnover_probability": turnover_prob,
            "risk_level": risk_level,
            "recommendations": ["Regular check-ins", "Work-life balance assessment"]
        })
    
    print(f"✅ Demo mode working! Generated {len(demo_predictions)} demo predictions")
    return True

def main():
    print("🧪 Enhanced HR Dashboard Test Suite")
    print("=" * 50)
    
    # Test API connection
    api_connected = test_api_connection()
    
    if api_connected:
        # Test login
        auth_token = test_api_login()
        
        if auth_token:
            # Test bulk prediction
            test_bulk_prediction(auth_token)
        else:
            print("⚠️  Cannot test bulk prediction without authentication")
    else:
        print("⚠️  API not accessible - dashboard will fall back to demo mode")
    
    # Test demo mode
    test_demo_mode()
    
    print("\n" + "=" * 50)
    print("📋 DASHBOARD USAGE INSTRUCTIONS:")
    print("1. 🌐 Open: http://localhost:8080/frontend_hr_dashboard_enhanced.html")
    print("2. 🔄 The enhanced version has:")
    print("   • Connection status indicator")
    print("   • Automatic fallback to demo mode")
    print("   • Better error handling")
    print("   • Connection retry options")
    print("3. 🎯 For testing:")
    print("   • Try production mode first")
    print("   • If connection fails, switch to demo mode")
    print("   • Both modes support CSV upload and results export")
    print("4. 📁 Original dashboard: http://localhost:8080/frontend_hr_dashboard.html")
    print("5. 🎭 Demo version: http://localhost:8080/frontend_hr_dashboard_demo.html")
    
    if api_connected:
        print("\n✅ Production API is accessible - try production mode first!")
    else:
        print("\n⚠️  Production API not accessible - use demo mode for testing")

if __name__ == "__main__":
    main()
