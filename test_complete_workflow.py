#!/usr/bin/env python3
"""
End-to-End Test for HR Dashboard CSV Upload Feature
Tests complete workflow including frontend simulation
"""

import requests
import json
import csv
import io
import os
from pathlib import Path

# Configuration
API_BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"
USERNAME = "admin"
PASSWORD = "newstrongpassword123"

def create_test_csv():
    """Create a test CSV file"""
    test_data = [
        ["employee_id", "name", "satisfaction_level", "last_evaluation", "number_project", 
         "average_monthly_hours", "time_spend_company", "work_accident", "promotion_last_5years", 
         "salary", "department"],
        ["EMP001", "John Doe", "0.75", "0.85", "4", "180", "3", "false", "false", "medium", "IT"],
        ["EMP002", "Jane Smith", "0.45", "0.60", "2", "250", "6", "true", "false", "low", "sales"],
        ["EMP003", "Bob Johnson", "0.80", "0.90", "5", "160", "2", "false", "true", "high", "engineering"],
        ["EMP004", "Alice Wilson", "0.35", "0.45", "3", "280", "4", "false", "false", "low", "marketing"],
        ["EMP005", "Charlie Brown", "0.85", "0.95", "6", "170", "1", "false", "false", "high", "IT"]
    ]
    
    csv_path = Path("test_employees.csv")
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(test_data)
    
    print(f"✅ Test CSV created: {csv_path}")
    return csv_path

def parse_csv_to_employees(csv_path):
    """Parse CSV file to employee data format for API"""
    employees = []
    
    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            employee = {
                "employee_id": row["employee_id"],
                "satisfaction_level": float(row["satisfaction_level"]),
                "last_evaluation": float(row["last_evaluation"]),
                "number_project": int(row["number_project"]),
                "average_monthly_hours": int(row["average_monthly_hours"]),
                "time_spend_company": int(row["time_spend_company"]),
                "work_accident": row["work_accident"].lower() == "true",
                "promotion_last_5years": row["promotion_last_5years"].lower() == "true",
                "salary": row["salary"].lower(),
                "department": row["department"].lower()
            }
            employees.append(employee)
    
    return employees

def test_complete_workflow():
    """Test complete CSV upload workflow"""
    print("🚀 Starting Complete HR Dashboard Workflow Test")
    print("=" * 60)
    
    # Step 1: Login
    print("\n1️⃣ Testing Login...")
    response = requests.post(
        f"{API_BASE_URL}/api/auth/login/",
        json={"username": USERNAME, "password": PASSWORD}
    )
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.text}")
        return False
    
    data = response.json()
    auth_token = data.get("auth_header")
    print(f"✅ Login successful!")
    
    # Step 2: Create Test CSV
    print("\n2️⃣ Creating Test CSV...")
    csv_path = create_test_csv()
    
    # Step 3: Parse CSV (simulating frontend)
    print("\n3️⃣ Parsing CSV data...")
    employees = parse_csv_to_employees(csv_path)
    print(f"✅ Parsed {len(employees)} employees from CSV")
    
    # Step 4: Send Bulk Prediction Request
    print("\n4️⃣ Sending Bulk Prediction Request...")
    headers = {"Authorization": auth_token, "Content-Type": "application/json"}
    
    response = requests.post(
        f"{API_BASE_URL}/api/predictions/bulk_predict/",
        headers=headers,
        json={"employees": employees}
    )
    
    if response.status_code != 200:
        print(f"❌ Bulk prediction failed: {response.text}")
        return False
    
    data = response.json()
    predictions = data["predictions"]
    print(f"✅ Bulk prediction successful! Got {len(predictions)} predictions")
    
    # Step 5: Process Results (simulating frontend)
    print("\n5️⃣ Processing Results...")
    
    # Calculate statistics
    high_risk = len([p for p in predictions if p["risk_level"] == "High"])
    medium_risk = len([p for p in predictions if p["risk_level"] == "Medium"])
    low_risk = len([p for p in predictions if p["risk_level"] == "Low"])
    avg_probability = sum(p["probability"] for p in predictions) / len(predictions)
    
    # Transform to frontend format
    dashboard_data = {
        "total_employees": len(predictions),
        "summary": {
            "high_risk_count": high_risk,
            "medium_risk_count": medium_risk,
            "low_risk_count": low_risk,
            "average_probability": round(avg_probability, 3),
            "high_risk_percentage": round((high_risk / len(predictions) * 100), 1)
        },
        "predictions": []
    }
    
    for pred in predictions:
        # Find original employee data
        original_emp = next(e for e in employees if e["employee_id"] == pred["employee_id"])
        
        dashboard_pred = {
            "employee_id": pred["employee_id"],
            "employee_name": original_emp.get("name", pred["employee_id"]),
            "department": original_emp["department"],
            "satisfaction_level": original_emp["satisfaction_level"],
            "turnover_probability": pred["probability"],
            "risk_level": pred["risk_level"].upper(),
            "prediction": pred["prediction"],
            "recommendations": ["Analysis completed", "Monitor performance"]
        }
        dashboard_data["predictions"].append(dashboard_pred)
    
    print("✅ Results processed successfully!")
    
    # Step 6: Display Summary
    print("\n6️⃣ Dashboard Summary:")
    print(f"   📊 Total Employees: {dashboard_data['total_employees']}")
    print(f"   🔴 High Risk: {dashboard_data['summary']['high_risk_count']}")
    print(f"   🟡 Medium Risk: {dashboard_data['summary']['medium_risk_count']}")
    print(f"   🟢 Low Risk: {dashboard_data['summary']['low_risk_count']}")
    print(f"   📈 Average Probability: {dashboard_data['summary']['average_probability']}")
    print(f"   📊 High Risk %: {dashboard_data['summary']['high_risk_percentage']}%")
    
    # Step 7: Show Individual Results
    print("\n7️⃣ Individual Employee Results:")
    for pred in dashboard_data["predictions"]:
        risk_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
        print(f"   {risk_emoji.get(pred['risk_level'], '⚪')} {pred['employee_name']} ({pred['employee_id']}) - "
              f"{pred['risk_level']} Risk ({pred['turnover_probability']:.3f})")
    
    # Step 8: Export Results
    print("\n8️⃣ Exporting Results...")
    export_data = []
    export_data.append(["Employee ID", "Name", "Department", "Satisfaction Level", "Risk Level", "Turnover Probability"])
    
    for pred in dashboard_data["predictions"]:
        export_data.append([
            pred["employee_id"],
            pred["employee_name"],
            pred["department"],
            pred["satisfaction_level"],
            pred["risk_level"],
            pred["turnover_probability"]
        ])
    
    export_path = Path("prediction_results_export.csv")
    with open(export_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(export_data)
    
    print(f"✅ Results exported to: {export_path}")
    
    # Cleanup
    print("\n9️⃣ Cleanup...")
    csv_path.unlink(missing_ok=True)
    print("✅ Test files cleaned up")
    
    print("\n" + "=" * 60)
    print("🎉 Complete workflow test PASSED!")
    print("\n📝 Summary:")
    print("   ✅ Authentication works")
    print("   ✅ CSV parsing works")
    print("   ✅ Bulk prediction API works")
    print("   ✅ Results processing works")
    print("   ✅ Data export works")
    print("\n🌐 HR Dashboard is ready for production use!")
    print("   • Open frontend_hr_dashboard.html in browser")
    print("   • Login with admin/newstrongpassword123")
    print("   • Download CSV template and upload sample data")
    
    return True

def main():
    """Run the complete workflow test"""
    try:
        success = test_complete_workflow()
        if success:
            print("\n✅ All tests completed successfully!")
        else:
            print("\n❌ Some tests failed.")
    except Exception as e:
        print(f"\n💥 Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    main()
