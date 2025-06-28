#!/usr/bin/env python3
"""
Test Recommendations Function
"""

import requests
import json
import base64

BASE_URL = "http://127.0.0.1:8000"

def test_recommendations():
    """Test recommendations untuk berbagai skenario"""
    print("🧪 TESTING RECOMMENDATIONS")
    print("=" * 50)
    
    # Setup auth
    auth_header = {
        'Authorization': f'Basic {base64.b64encode(b"admin:admin123").decode()}'
    }
    
    test_cases = [
        {
            "name": "Low Risk Employee (High Satisfaction)",
            "data": {
                "satisfaction_level": 0.9,  # High satisfaction
                "last_evaluation": 0.8,
                "number_project": 3,
                "average_monthly_hours": 160,
                "time_spend_company": 2,
                "work_accident": False,
                "promotion_last_5years": True,
                "salary": "high",
                "department": "IT"
            },
            "expected_recommendations": [
                "Employee appears to be in good standing",
                "Continue current management approach", 
                "High satisfaction - consider as mentor for other employees"
            ]
        },
        {
            "name": "High Risk Employee (Low Satisfaction)",
            "data": {
                "satisfaction_level": 0.2,  # Low satisfaction
                "last_evaluation": 0.4,
                "number_project": 7,
                "average_monthly_hours": 300,  # Overworked
                "time_spend_company": 6,
                "work_accident": False,
                "promotion_last_5years": False,  # No promotion
                "salary": "low",  # Low salary
                "department": "Sales"
            },
            "expected_recommendations": [
                "Consider conducting a satisfaction survey",
                "Employee may be overworked",
                "Consider career development opportunities",
                "Review compensation package"
            ]
        },
        {
            "name": "Medium Risk Employee",
            "data": {
                "satisfaction_level": 0.6,  # Medium satisfaction
                "last_evaluation": 0.7,
                "number_project": 5,
                "average_monthly_hours": 220,  # Bit overworked
                "time_spend_company": 3,
                "work_accident": False,
                "promotion_last_5years": False,
                "salary": "medium",
                "department": "Marketing"
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}️⃣ Testing: {test_case['name']}")
        print("-" * 40)
        
        response = requests.post(f"{BASE_URL}/api/predictions/predict/", 
                               json=test_case['data'], headers=auth_header)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: SUCCESS")
            print(f"📊 Prediction: {'Will Leave' if data['prediction'] else 'Will Stay'}")
            print(f"📈 Probability: {data['probability']:.3f}")
            print(f"🎯 Risk Level: {data['risk_level']}")
            print(f"💡 Recommendations ({len(data['recommendations'])} items):")
            
            if data['recommendations']:
                for rec in data['recommendations']:
                    print(f"   • {rec}")
            else:
                print("   ❌ NO RECOMMENDATIONS (This is the bug!)")
                
        else:
            print(f"❌ Status: FAILED ({response.status_code})")
            try:
                error = response.json()
                print(f"🔥 Error: {error}")
            except:
                print(f"🔥 Error: {response.text}")

if __name__ == "__main__":
    test_recommendations()
