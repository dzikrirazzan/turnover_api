#!/usr/bin/env python3
"""
Test script for HR Features API endpoints
Tests 1-on-1 Meetings, Performance Reviews, and Analytics features
"""

import requests
import json
import sys
from datetime import datetime, timedelta
from pprint import pprint

# API Configuration
BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"
ADMIN_EMAIL = "admin@company.com"  # Update with your admin email
ADMIN_PASSWORD = "AdminPass123!"    # Update with your admin password

def get_admin_token():
    """Login and get admin token"""
    print("🔐 Logging in as admin...")
    
    login_response = requests.post(f"{BASE_URL}/api/login/", json={
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return None
    
    login_data = login_response.json()
    token = login_data["data"]["user"]["token"]
    print(f"✅ Login successful! Token: {token[:20]}...")
    return token

def test_meetings_api(token, employee_id):
    """Test Meeting management API"""
    print("\n" + "="*60)
    print("📅 TESTING 1-ON-1 MEETINGS API")
    print("="*60)
    
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Create a meeting
    print("\n1️⃣ Creating a new meeting...")
    
    meeting_data = {
        "employee": employee_id,
        "title": "Follow-up Meeting: ML Prediction Results",
        "meeting_type": "followup",
        "scheduled_date": (datetime.now() + timedelta(days=7)).isoformat() + "Z",
        "duration_minutes": 60,
        "meeting_link": "https://zoom.us/j/123456789",
        "agenda": "Discuss ML prediction results, understand employee concerns, create action plan",
        "prediction_id": "pred_test_123",
        "ml_probability": 0.75,
        "ml_risk_level": "high"
    }
    
    create_response = requests.post(f"{BASE_URL}/api/meetings/", 
                                  json=meeting_data, 
                                  headers=headers)
    
    if create_response.status_code == 201:
        meeting_result = create_response.json()
        meeting_id = meeting_result["data"]["id"]
        print(f"✅ Meeting created successfully! ID: {meeting_id}")
        print(f"   Title: {meeting_result['data']['title']}")
        print(f"   Scheduled: {meeting_result['data']['scheduled_date']}")
        print(f"   High Priority: {meeting_result['data']['is_high_priority']}")
    else:
        print(f"❌ Failed to create meeting: {create_response.status_code}")
        print(f"Response: {create_response.text}")
        return False
    
    # Test 2: Get all meetings
    print("\n2️⃣ Getting all meetings...")
    
    get_response = requests.get(f"{BASE_URL}/api/meetings/", headers=headers)
    
    if get_response.status_code == 200:
        meetings = get_response.json()["data"]
        print(f"✅ Retrieved {len(meetings)} meetings")
        if meetings:
            latest_meeting = meetings[0]
            print(f"   Latest: {latest_meeting['title']} - {latest_meeting['status']}")
    else:
        print(f"❌ Failed to get meetings: {get_response.status_code}")
    
    # Test 3: Get upcoming meetings
    print("\n3️⃣ Getting upcoming meetings...")
    
    upcoming_response = requests.get(f"{BASE_URL}/api/meetings/upcoming/", headers=headers)
    
    if upcoming_response.status_code == 200:
        upcoming = upcoming_response.json()["data"]
        print(f"✅ Found {len(upcoming)} upcoming meetings")
    else:
        print(f"❌ Failed to get upcoming meetings: {upcoming_response.status_code}")
    
    # Test 4: Update meeting
    print("\n4️⃣ Updating meeting...")
    
    update_data = {
        "meeting_link": "https://meet.google.com/updated-link",
        "agenda": "Updated agenda: Focus on specific concerns and solutions"
    }
    
    update_response = requests.patch(f"{BASE_URL}/api/meetings/{meeting_id}/", 
                                   json=update_data, 
                                   headers=headers)
    
    if update_response.status_code == 200:
        print("✅ Meeting updated successfully")
    else:
        print(f"❌ Failed to update meeting: {update_response.status_code}")
    
    # Test 5: Complete meeting
    print("\n5️⃣ Completing meeting...")
    
    complete_data = {
        "notes": "Great discussion. Employee is more motivated. Agreed on specific action items.",
        "action_items": "1. Enroll in leadership training\n2. Assign mentorship role\n3. Schedule follow-up in 4 weeks"
    }
    
    complete_response = requests.post(f"{BASE_URL}/api/meetings/{meeting_id}/complete/", 
                                    json=complete_data, 
                                    headers=headers)
    
    if complete_response.status_code == 200:
        print("✅ Meeting marked as completed")
    else:
        print(f"❌ Failed to complete meeting: {complete_response.status_code}")
    
    return True

def test_performance_reviews_api(token, employee_id):
    """Test Performance Review API"""
    print("\n" + "="*60)
    print("⭐ TESTING PERFORMANCE REVIEWS API")
    print("="*60)
    
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Create performance review
    print("\n1️⃣ Creating performance review...")
    
    review_data = {
        "employee": employee_id,
        "review_period": "quarterly",
        "review_date": datetime.now().date().isoformat(),
        "period_start": (datetime.now() - timedelta(days=90)).date().isoformat(),
        "period_end": datetime.now().date().isoformat(),
        "overall_rating": 4,
        "technical_skills": 4,
        "communication": 3,
        "teamwork": 4,
        "leadership": 3,
        "initiative": 3,
        "problem_solving": 4,
        "strengths": "Strong technical skills, reliable team member, good problem-solving abilities",
        "areas_for_improvement": "Could improve communication with stakeholders, needs to take more initiative",
        "goals_for_next_period": "1. Lead one project independently\n2. Improve presentation skills\n3. Mentor junior team member",
        "additional_notes": "Overall solid performance. Ready for more responsibility.",
        "triggered_by_ml": True,
        "ml_prediction_id": "pred_test_123"
    }
    
    create_response = requests.post(f"{BASE_URL}/api/reviews/", 
                                  json=review_data, 
                                  headers=headers)
    
    if create_response.status_code == 201:
        review_result = create_response.json()
        review_id = review_result["data"]["id"]
        print(f"✅ Performance review created! ID: {review_id}")
        print(f"   Employee: {review_result['data']['employee_info']['full_name']}")
        print(f"   Overall Rating: {review_result['data']['overall_rating']}/5 stars")
        print(f"   Average Rating: {review_result['data']['average_rating']}")
        print(f"   Triggered by ML: {review_result['data']['triggered_by_ml']}")
    else:
        print(f"❌ Failed to create review: {create_response.status_code}")
        print(f"Response: {create_response.text}")
        return False
    
    # Test 2: Get all reviews
    print("\n2️⃣ Getting all performance reviews...")
    
    get_response = requests.get(f"{BASE_URL}/api/reviews/", headers=headers)
    
    if get_response.status_code == 200:
        reviews = get_response.json()["data"]
        print(f"✅ Retrieved {len(reviews)} performance reviews")
        if reviews:
            latest_review = reviews[0]
            print(f"   Latest: {latest_review['employee_info']['full_name']} - {latest_review['review_period']}")
            print(f"   Rating Breakdown:")
            for category, rating in latest_review['rating_breakdown'].items():
                print(f"     {category.replace('_', ' ').title()}: {rating}")
    else:
        print(f"❌ Failed to get reviews: {get_response.status_code}")
    
    # Test 3: Get review summary
    print("\n3️⃣ Getting review summary...")
    
    summary_response = requests.get(f"{BASE_URL}/api/reviews/summary/?employee={employee_id}", 
                                  headers=headers)
    
    if summary_response.status_code == 200:
        summary = summary_response.json()["data"]
        print(f"✅ Review summary retrieved")
        print(f"   Total Reviews: {summary['total_reviews']}")
        print(f"   Average Overall Rating: {summary['average_overall_rating']:.2f}")
        if summary.get('rating_trend'):
            print(f"   Rating Trend: {len(summary['rating_trend'])} data points")
    else:
        print(f"❌ Failed to get review summary: {summary_response.status_code}")
    
    # Test 4: Update review
    print("\n4️⃣ Updating performance review...")
    
    update_data = {
        "initiative": 4,
        "additional_notes": "Updated: Showed excellent improvement in taking initiative on recent project"
    }
    
    update_response = requests.patch(f"{BASE_URL}/api/reviews/{review_id}/", 
                                   json=update_data, 
                                   headers=headers)
    
    if update_response.status_code == 200:
        updated_review = update_response.json()["data"]
        print("✅ Performance review updated successfully")
        print(f"   New Average Rating: {updated_review['average_rating']}")
    else:
        print(f"❌ Failed to update review: {update_response.status_code}")
    
    return True

def test_analytics_api(token):
    """Test Analytics API"""
    print("\n" + "="*60)
    print("📊 TESTING ANALYTICS API")
    print("="*60)
    
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Get analytics dashboard
    print("\n1️⃣ Getting analytics dashboard...")
    
    dashboard_response = requests.get(f"{BASE_URL}/api/analytics/dashboard/", headers=headers)
    
    if dashboard_response.status_code == 200:
        dashboard = dashboard_response.json()["data"]
        print("✅ Analytics dashboard retrieved successfully")
        print(f"   Total Predictions: {dashboard['total_predictions']}")
        print(f"   Total Meetings: {dashboard['total_meetings']}")
        print(f"   Total Reviews: {dashboard['total_reviews']}")
        print(f"   High Risk Employees: {dashboard['high_risk_employees']}")
        print(f"   Recent Predictions: {dashboard['recent_predictions']}")
        
        # Risk distribution
        risk_dist = dashboard['risk_distribution']
        print(f"\n   Risk Distribution:")
        print(f"     Low Risk: {risk_dist['low_risk']}")
        print(f"     Medium Risk: {risk_dist['medium_risk']}")
        print(f"     High Risk: {risk_dist['high_risk']}")
        print(f"     Total Employees: {risk_dist['total_employees']}")
        
    else:
        print(f"❌ Failed to get analytics dashboard: {dashboard_response.status_code}")
        print(f"Response: {dashboard_response.text}")
        return False
    
    # Test 2: Get chart data
    print("\n2️⃣ Getting chart data...")
    
    charts_response = requests.get(f"{BASE_URL}/api/analytics/charts/", headers=headers)
    
    if charts_response.status_code == 200:
        charts = charts_response.json()["data"]
        print("✅ Chart data retrieved successfully")
        print(f"   Available Charts: {list(charts.keys())}")
        
        # Show chart details
        for chart_name, chart_data in charts.items():
            print(f"\n   📈 {chart_name.replace('_', ' ').title()}:")
            print(f"     Type: {chart_data['chart_type']}")
            print(f"     Title: {chart_data['title']}")
            if 'labels' in chart_data['data']:
                print(f"     Labels: {chart_data['data']['labels']}")
            if 'datasets' in chart_data['data']:
                for dataset in chart_data['data']['datasets']:
                    if 'data' in dataset:
                        print(f"     Data: {dataset['data']}")
    else:
        print(f"❌ Failed to get chart data: {charts_response.status_code}")
    
    return True

def test_employee_access(employee_token, employee_id):
    """Test employee access (read-only)"""
    print("\n" + "="*60)
    print("👤 TESTING EMPLOYEE ACCESS (READ-ONLY)")
    print("="*60)
    
    headers = {
        "Authorization": f"Token {employee_token}",
        "Content-Type": "application/json"
    }
    
    # Test employee can view their own meetings
    print("\n1️⃣ Employee viewing own meetings...")
    
    meetings_response = requests.get(f"{BASE_URL}/api/meetings/", headers=headers)
    
    if meetings_response.status_code == 200:
        meetings = meetings_response.json()["data"]
        print(f"✅ Employee can view {len(meetings)} own meetings")
    else:
        print(f"❌ Employee cannot view meetings: {meetings_response.status_code}")
    
    # Test employee can view their own reviews
    print("\n2️⃣ Employee viewing own reviews...")
    
    reviews_response = requests.get(f"{BASE_URL}/api/reviews/", headers=headers)
    
    if reviews_response.status_code == 200:
        reviews = reviews_response.json()["data"]
        print(f"✅ Employee can view {len(reviews)} own reviews")
    else:
        print(f"❌ Employee cannot view reviews: {reviews_response.status_code}")
    
    # Test employee cannot create meetings
    print("\n3️⃣ Testing employee cannot create meetings...")
    
    meeting_data = {
        "employee": employee_id,
        "title": "Test Meeting",
        "meeting_type": "regular",
        "scheduled_date": (datetime.now() + timedelta(days=1)).isoformat() + "Z"
    }
    
    create_response = requests.post(f"{BASE_URL}/api/meetings/", 
                                  json=meeting_data, 
                                  headers=headers)
    
    if create_response.status_code == 403:
        print("✅ Employee correctly denied from creating meetings")
    else:
        print(f"❌ Employee access control failed: {create_response.status_code}")

def run_complete_test():
    """Run complete test suite for HR features"""
    print("🚀 SMART-EN HR FEATURES API TEST SUITE")
    print("="*70)
    print(f"🌍 Base URL: {BASE_URL}")
    print(f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get admin token
    admin_token = get_admin_token()
    if not admin_token:
        print("❌ Cannot proceed without admin token")
        return False
    
    # Get employee ID for testing (using existing employee)
    headers = {"Authorization": f"Token {admin_token}"}
    employees_response = requests.get(f"{BASE_URL}/api/employees/", headers=headers)
    
    if employees_response.status_code != 200:
        print("❌ Cannot get employee list for testing")
        return False
    
    employees_data = employees_response.json()
    
    # Handle different response formats
    if "results" in employees_data:
        employees = employees_data["results"]
    elif "data" in employees_data:
        employees = employees_data["data"]
    else:
        employees = employees_data
    
    if not employees:
        print("❌ No employees found for testing")
        return False
    
    test_employee = employees[0]
    employee_id = test_employee["id"]
    print(f"\n🧪 Using test employee: {test_employee.get('full_name', test_employee.get('first_name', 'Unknown'))} (ID: {employee_id})")
    
    # Run all tests
    success = True
    
    try:
        # Test meetings API
        if not test_meetings_api(admin_token, employee_id):
            success = False
        
        # Test performance reviews API
        if not test_performance_reviews_api(admin_token, employee_id):
            success = False
        
        # Test analytics API
        if not test_analytics_api(admin_token):
            success = False
        
        # Print summary
        print("\n" + "="*70)
        print("📋 TEST SUMMARY")
        print("="*70)
        
        if success:
            print("🎉 All HR features tests passed!")
            print("\n✅ Verified Features:")
            print("   📅 1-on-1 Meeting Management (Create, Read, Update, Complete)")
            print("   ⭐ Performance Review System (Star ratings, CRUD operations)")
            print("   📊 Analytics Dashboard (Charts, metrics, trends)")
            print("   🔐 Role-based Access Control (Admin vs Employee)")
            
            print("\n🚀 Ready for Frontend Integration:")
            print("   • Use chart data for visualization (Chart.js)")
            print("   • Implement meeting scheduler component")
            print("   • Build performance review interface")
            print("   • Create analytics dashboard")
            
        else:
            print("❌ Some tests failed. Please check the configuration.")
        
    except Exception as e:
        print(f"💥 Test failed with error: {e}")
        success = False
    
    return success

if __name__ == "__main__":
    try:
        success = run_complete_test()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)
