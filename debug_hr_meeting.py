#!/usr/bin/env python3
"""
Debug HR model creation issue via Django shell simulation
"""
import requests
import json

BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"

def debug_meeting_creation():
    """Debug meeting creation step by step"""
    print("🔍 Debugging Meeting Creation...")
    
    # Get admin token
    response = requests.post(f"{BASE_URL}/api/login/", json={
        "email": "admin@company.com",
        "password": "AdminPass123!"
    })
    
    if response.status_code != 200:
        print("❌ Login failed")
        return
    
    token = response.json()['data']['user']['token']
    headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
    
    # Test minimal meeting data
    minimal_meeting = {
        "employee": 42,
        "title": "Minimal Test Meeting",
        "meeting_type": "regular",
        "scheduled_date": "2025-07-15T14:00:00Z"
    }
    
    print("Testing minimal meeting creation...")
    response = requests.post(f"{BASE_URL}/api/hr/meetings/", headers=headers, json=minimal_meeting)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")
    
    # Test with required fields only
    if response.status_code != 201:
        print("\nTrying with duration_minutes...")
        minimal_meeting["duration_minutes"] = 30
        response = requests.post(f"{BASE_URL}/api/hr/meetings/", headers=headers, json=minimal_meeting)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
    
    # Test performance review creation (yang working)
    print("\n🔍 Testing Performance Review Creation (for comparison)...")
    minimal_review = {
        "employee": 42,
        "review_period": "quarterly",
        "review_date": "2025-07-13",
        "period_start": "2025-04-01", 
        "period_end": "2025-06-30",
        "overall_rating": 4
    }
    
    response = requests.post(f"{BASE_URL}/api/hr/reviews/", headers=headers, json=minimal_review)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")

if __name__ == "__main__":
    debug_meeting_creation()
