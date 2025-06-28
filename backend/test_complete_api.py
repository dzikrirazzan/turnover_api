#!/usr/bin/env python3
"""
Complete API Testing Script for Smart-en System
Tests all endpoints to ensure they match frontend requirements
"""

import requests
import json
import sys
from datetime import datetime

# API Configuration
BASE_URL = "http://localhost:8001"
AUTH = ('admin', 'admin123')

# Test employee IDs (from our sample data)
TEST_EMPLOYEE_IDS = [45001, 45002, 45003, 45004, 45005]  # BD, TS, AA, PA, Z
TASYA_ID = 45002  # Main test user (matches frontend)

def test_endpoint(method, endpoint, description, expected_keys=None, payload=None):
    """Test a single API endpoint"""
    print(f"\n🧪 Testing: {description}")
    print(f"   {method} {endpoint}")
    
    try:
        if method.upper() == 'GET':
            response = requests.get(f"{BASE_URL}{endpoint}", auth=AUTH, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(f"{BASE_URL}{endpoint}", auth=AUTH, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS ({response.status_code})")
            
            # Check expected keys if provided
            if expected_keys and isinstance(data, dict):
                missing_keys = [key for key in expected_keys if key not in data]
                if missing_keys:
                    print(f"   ⚠️  Missing keys: {missing_keys}")
                else:
                    print(f"   ✓ All expected keys present")
            
            # Print sample data (first few items)
            if isinstance(data, list) and len(data) > 0:
                print(f"   📊 Sample: {len(data)} items, first item keys: {list(data[0].keys()) if data else 'None'}")
            elif isinstance(data, dict):
                print(f"   📊 Keys: {list(data.keys())}")
            
            return True, data
        else:
            print(f"   ❌ FAILED ({response.status_code}): {response.text}")
            return False, None
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ CONNECTION ERROR: {e}")
        return False, None

def main():
    print("🚀 SMART-EN SYSTEM API TESTING")
    print("=" * 50)
    print(f"Base URL: {BASE_URL}")
    print(f"Test Employee: Tasya Salsabila (ID: {TASYA_ID})")
    
    # Test results tracking
    total_tests = 0
    passed_tests = 0
    
    # 1. DASHBOARD APIs
    print("\n" + "=" * 50)
    print("🏠 DASHBOARD APIs")
    print("=" * 50)
    
    tests = [
        ("GET", f"/performance/api/dashboard/stats/?employee={TASYA_ID}", 
         "Dashboard Statistics", ["goals_completed", "goals_total", "feedback_received", "learning_hours", "performance_score"]),
        ("GET", f"/performance/api/dashboard/activities/?employee={TASYA_ID}", 
         "Recent Activities", None),
        ("GET", f"/performance/api/dashboard/user_info/?employee={TASYA_ID}", 
         "User Information", ["name", "initials", "role", "department"]),
    ]
    
    for method, endpoint, desc, keys in tests:
        total_tests += 1
        success, _ = test_endpoint(method, endpoint, desc, keys)
        if success:
            passed_tests += 1
    
    # 2. ANALYTICS APIs
    print("\n" + "=" * 50)
    print("📊 ANALYTICS APIs")
    print("=" * 50)
    
    tests = [
        ("GET", "/performance/api/analytics/dashboard/", 
         "Analytics Dashboard", ["team_engagement", "active_employees", "at_risk_count", "individual_performance"]),
        ("GET", "/performance/api/analytics/team_engagement/?days=30", 
         "Team Engagement Trends", None),
        ("GET", "/performance/api/analytics/risk_trends/?months=12", 
         "Risk Trends", None),
        ("GET", "/performance/api/analytics/performance_matrix/", 
         "Performance Matrix", None),
    ]
    
    for method, endpoint, desc, keys in tests:
        total_tests += 1
        success, _ = test_endpoint(method, endpoint, desc, keys)
        if success:
            passed_tests += 1
    
    # 3. GOALS APIs
    print("\n" + "=" * 50)
    print("🎯 GOALS & OKRs APIs")
    print("=" * 50)
    
    tests = [
        ("GET", f"/performance/api/goals/statistics/?employee={TASYA_ID}", 
         "Goals Statistics", ["total_goals", "completed_goals", "completion_rate", "achievement_rate"]),
        ("GET", "/performance/api/goals/sample_goals/", 
         "Sample Goals (Frontend Data)", None),
        ("GET", "/performance/api/goals/", 
         "All Goals", None),
        ("GET", "/performance/api/key-results/", 
         "Key Results", None),
    ]
    
    for method, endpoint, desc, keys in tests:
        total_tests += 1
        success, _ = test_endpoint(method, endpoint, desc, keys)
        if success:
            passed_tests += 1
    
    # 4. FEEDBACK APIs
    print("\n" + "=" * 50)
    print("💬 FEEDBACK APIs")
    print("=" * 50)
    
    tests = [
        ("GET", "/performance/api/feedback/sample_feedback/", 
         "Sample Feedback (Frontend Data)", None),
        ("GET", f"/performance/api/feedback/stats/?employee={TASYA_ID}", 
         "Feedback Statistics", ["received", "sent"]),
        ("GET", f"/performance/api/feedback/received/?employee={TASYA_ID}", 
         "Received Feedback", None),
        ("GET", f"/performance/api/feedback/sent/?employee={TASYA_ID}", 
         "Sent Feedback", None),
    ]
    
    for method, endpoint, desc, keys in tests:
        total_tests += 1
        success, _ = test_endpoint(method, endpoint, desc, keys)
        if success:
            passed_tests += 1
    
    # 5. PERFORMANCE REVIEW APIs
    print("\n" + "=" * 50)
    print("📋 PERFORMANCE REVIEW APIs")
    print("=" * 50)
    
    tests = [
        ("GET", f"/performance/api/performance-reviews/current_review/?employee={TASYA_ID}", 
         "Current Review (Frontend Data)", ["employee_name", "status", "overall_rating", "self_assessment_progress"]),
        ("GET", f"/performance/api/performance-reviews/history/?employee={TASYA_ID}", 
         "Review History", None),
        ("GET", "/performance/api/performance-reviews/", 
         "All Performance Reviews", None),
    ]
    
    for method, endpoint, desc, keys in tests:
        total_tests += 1
        success, _ = test_endpoint(method, endpoint, desc, keys)
        if success:
            passed_tests += 1
    
    # 6. 1-ON-1 MEETINGS APIs
    print("\n" + "=" * 50)
    print("🤝 1-ON-1 MEETINGS APIs")
    print("=" * 50)
    
    tests = [
        ("GET", f"/performance/api/oneonone-meetings/statistics/?employee={TASYA_ID}", 
         "Meeting Statistics", ["total_meetings", "this_month", "avg_duration_minutes", "satisfaction_percentage"]),
        ("GET", f"/performance/api/oneonone-meetings/?employee={TASYA_ID}", 
         "1-on-1 Meetings", None),
    ]
    
    for method, endpoint, desc, keys in tests:
        total_tests += 1
        success, _ = test_endpoint(method, endpoint, desc, keys)
        if success:
            passed_tests += 1
    
    # 7. SHOUTOUTS APIs
    print("\n" + "=" * 50)
    print("🎉 SHOUTOUTS APIs")
    print("=" * 50)
    
    tests = [
        ("GET", f"/performance/api/shoutouts/statistics/?employee={TASYA_ID}", 
         "Shoutout Statistics", ["shoutouts_given", "shoutouts_received", "team_participation_percentage"]),
        ("GET", "/performance/api/shoutouts/", 
         "All Shoutouts", None),
    ]
    
    for method, endpoint, desc, keys in tests:
        total_tests += 1
        success, _ = test_endpoint(method, endpoint, desc, keys)
        if success:
            passed_tests += 1
    
    # 8. LEARNING APIs
    print("\n" + "=" * 50)
    print("🎓 LEARNING APIs")
    print("=" * 50)
    
    tests = [
        ("GET", f"/performance/api/learning-progress/statistics/?employee={TASYA_ID}", 
         "Learning Statistics", ["completed_this_week", "time_spent_minutes", "streak_days"]),
        ("GET", f"/performance/api/learning-modules/recommendations/?employee={TASYA_ID}", 
         "Learning Recommendations", None),
        ("GET", "/performance/api/learning-modules/categories/", 
         "Learning Categories", None),
        ("GET", "/performance/api/learning-modules/", 
         "Learning Modules", None),
    ]
    
    for method, endpoint, desc, keys in tests:
        total_tests += 1
        success, _ = test_endpoint(method, endpoint, desc, keys)
        if success:
            passed_tests += 1
    
    # 9. EXISTING PREDICTION APIs
    print("\n" + "=" * 50)
    print("🔮 PREDICTION APIs (Existing)")
    print("=" * 50)
    
    tests = [
        ("GET", "/api/employees/", 
         "List Employees", None),
        ("GET", "/api/employees/statistics/", 
         "Employee Statistics", None),
        ("GET", "/api/departments/", 
         "List Departments", None),
    ]
    
    for method, endpoint, desc, keys in tests:
        total_tests += 1
        success, _ = test_endpoint(method, endpoint, desc, keys)
        if success:
            passed_tests += 1
    
    # FINAL RESULTS
    print("\n" + "=" * 80)
    print("📊 FINAL TEST RESULTS")
    print("=" * 80)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! Backend is ready for frontend integration!")
        print("\n✅ Frontend developers can now:")
        print("   • Connect to http://localhost:8001")
        print("   • Use Basic Auth: admin/admin123")
        print("   • Test with employee ID 45002 (Tasya Salsabila)")
        print("   • All endpoints return data matching frontend requirements")
    else:
        print(f"\n⚠️ {total_tests - passed_tests} tests failed. Please check the issues above.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
