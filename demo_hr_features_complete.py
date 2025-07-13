#!/usr/bin/env python3
"""
Demo script for HR Features with dummy data
Shows chart data structures and API responses without requiring database
"""

import json
from datetime import datetime, timedelta
import random

def generate_sample_chart_data():
    """Generate sample chart data that would come from the API"""
    
    # Sample Risk Distribution Data
    risk_distribution = {
        "chart_type": "pie",
        "title": "Employee Risk Distribution",
        "data": {
            "labels": ["Low Risk", "Medium Risk", "High Risk"],
            "datasets": [{
                "data": [42, 18, 8],  # 42 low, 18 medium, 8 high risk employees
                "backgroundColor": ["#28a745", "#ffc107", "#dc3545"],
                "borderWidth": 2
            }]
        }
    }
    
    # Sample Department Analysis Data
    departments = ["Engineering", "Marketing", "HR", "Finance", "Sales", "Operations"]
    department_analysis = {
        "chart_type": "bar",
        "title": "Risk Analysis by Department",
        "data": {
            "labels": departments,
            "datasets": [{
                "label": "Average Risk Score (%)",
                "data": [35.2, 62.8, 28.1, 45.9, 71.3, 38.7],  # Risk scores per department
                "backgroundColor": "#4F46E5",
                "borderColor": "#3730A3",
                "borderWidth": 1
            }]
        }
    }
    
    # Sample Trend Analysis Data (last 6 months)
    months = []
    risk_values = []
    base_date = datetime.now()
    
    for i in range(6):
        month_date = base_date - timedelta(days=30*i)
        months.append(month_date.strftime("%b %Y"))
        # Generate realistic trend data (slightly increasing risk over time)
        risk_values.append(round(30 + (i * 3) + random.uniform(-5, 5), 1))
    
    months.reverse()
    risk_values.reverse()
    
    trend_analysis = {
        "chart_type": "line",
        "title": "Turnover Risk Trend (Last 6 Months)",
        "data": {
            "labels": months,
            "datasets": [{
                "label": "Average Risk %",
                "data": risk_values,
                "borderColor": "#EF4444",
                "backgroundColor": "rgba(239, 68, 68, 0.1)",
                "tension": 0.4,
                "fill": True
            }]
        }
    }
    
    return {
        "risk_distribution": risk_distribution,
        "department_analysis": department_analysis,
        "trend_analysis": trend_analysis
    }

def generate_sample_dashboard_data():
    """Generate sample dashboard statistics"""
    return {
        "total_predictions": 68,
        "total_meetings": 24,
        "total_reviews": 15,
        "high_risk_employees": 8,
        "recent_predictions": 12,
        "risk_distribution": {
            "low_risk": 42,
            "medium_risk": 18,
            "high_risk": 8,
            "total_employees": 68
        }
    }

def generate_sample_meeting_data():
    """Generate sample meeting data"""
    return [
        {
            "id": 1,
            "employee_name": "John Doe",
            "title": "Follow-up Meeting: High Turnover Risk Discussion",
            "meeting_type": "followup",
            "scheduled_date": "2025-07-15T14:00:00Z",
            "duration_minutes": 45,
            "meeting_link": "https://meet.google.com/abc-defg-hij",
            "agenda": "Discussion about career development and addressing concerns based on ML prediction results.",
            "status": "scheduled",
            "ml_probability": 0.85,
            "ml_risk_level": "high",
            "notes": "",
            "action_items": ""
        },
        {
            "id": 2,
            "employee_name": "Jane Smith",
            "title": "Regular Check-in Meeting",
            "meeting_type": "regular",
            "scheduled_date": "2025-07-18T10:00:00Z",
            "duration_minutes": 30,
            "meeting_link": "https://zoom.us/j/123456789",
            "agenda": "Monthly performance review and goal setting discussion.",
            "status": "completed",
            "ml_probability": 0.25,
            "ml_risk_level": "low",
            "notes": "Employee is performing well and satisfied with current role.",
            "action_items": "Continue current development path, schedule skills training."
        }
    ]

def generate_sample_performance_review_data():
    """Generate sample performance review data"""
    return [
        {
            "id": 1,
            "employee_name": "John Doe",
            "reviewer_name": "HR Manager",
            "review_period": "quarterly",
            "review_date": "2025-07-11",
            "period_start": "2025-04-01",
            "period_end": "2025-06-30",
            "overall_rating": 4,
            "technical_skills": 4,
            "communication": 3,
            "teamwork": 5,
            "leadership": 3,
            "initiative": 4,
            "problem_solving": 4,
            "average_rating": 3.86,
            "strengths": "Excellent technical skills and strong collaboration with team members. Shows great problem-solving abilities.",
            "areas_for_improvement": "Could improve communication skills, especially in presenting ideas to stakeholders.",
            "goals_for_next_period": "1. Complete communication skills workshop\\n2. Lead at least one project presentation\\n3. Mentor a junior team member",
            "additional_notes": "Employee has shown significant growth this quarter.",
            "is_final": True,
            "employee_acknowledged": True,
            "rating_breakdown": {
                "overall": 4,
                "technical_skills": 4,
                "communication": 3,
                "teamwork": 5,
                "leadership": 3,
                "initiative": 4,
                "problem_solving": 4,
                "average": 3.86
            }
        }
    ]

def demo_frontend_chart_data():
    """Demonstrate chart data structures for frontend"""
    
    print("🚀 HR FEATURES - FRONTEND CHART DATA DEMO")
    print("=" * 60)
    print(f"🕒 Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Generate chart data
    chart_data = generate_sample_chart_data()
    dashboard_data = generate_sample_dashboard_data()
    
    print("📊 CHART DATA FOR FRONTEND INTEGRATION")
    print("=" * 60)
    
    # 1. Risk Distribution Pie Chart
    print("\n🥧 1. RISK DISTRIBUTION PIE CHART")
    print("-" * 40)
    risk_chart = chart_data["risk_distribution"]
    print(f"Chart Type: {risk_chart['chart_type'].upper()}")
    print(f"Title: {risk_chart['title']}")
    print(f"Labels: {risk_chart['data']['labels']}")
    print(f"Data Values: {risk_chart['data']['datasets'][0]['data']}")
    print(f"Colors: {risk_chart['data']['datasets'][0]['backgroundColor']}")
    
    # Frontend data structure
    print("\n📝 Frontend Data Structure (X/Y Axis):")
    pie_data = {
        "chart_type": "pie",
        "x_axis": risk_chart['data']['labels'],
        "y_axis": risk_chart['data']['datasets'][0]['data'],
        "colors": risk_chart['data']['datasets'][0]['backgroundColor'],
        "percentages": [
            round(val / sum(risk_chart['data']['datasets'][0]['data']) * 100, 1) 
            for val in risk_chart['data']['datasets'][0]['data']
        ]
    }
    print(json.dumps(pie_data, indent=2))
    
    # 2. Department Analysis Bar Chart
    print("\n📊 2. DEPARTMENT ANALYSIS BAR CHART")
    print("-" * 40)
    dept_chart = chart_data["department_analysis"]
    print(f"Chart Type: {dept_chart['chart_type'].upper()}")
    print(f"Title: {dept_chart['title']}")
    print(f"Departments: {dept_chart['data']['labels']}")
    print(f"Risk Scores: {dept_chart['data']['datasets'][0]['data']}")
    
    # Frontend data structure
    print("\n📝 Frontend Data Structure (X/Y Axis):")
    bar_data = {
        "chart_type": "bar",
        "x_axis": dept_chart['data']['labels'],
        "y_axis": dept_chart['data']['datasets'][0]['data'],
        "x_label": "Department",
        "y_label": "Risk Score (%)",
        "color": dept_chart['data']['datasets'][0]['backgroundColor'],
        "max_value": 100
    }
    print(json.dumps(bar_data, indent=2))
    
    # 3. Trend Analysis Line Chart
    print("\n📈 3. TREND ANALYSIS LINE CHART")
    print("-" * 40)
    trend_chart = chart_data["trend_analysis"]
    print(f"Chart Type: {trend_chart['chart_type'].upper()}")
    print(f"Title: {trend_chart['title']}")
    print(f"Time Period: {trend_chart['data']['labels']}")
    print(f"Risk Values: {trend_chart['data']['datasets'][0]['data']}")
    
    # Frontend time series data
    print("\n📝 Frontend Time Series Data:")
    time_series = []
    for i, label in enumerate(trend_chart['data']['labels']):
        time_series.append({
            "date": label,
            "risk_percentage": trend_chart['data']['datasets'][0]['data'][i]
        })
    
    line_data = {
        "chart_type": "line",
        "time_series": time_series,
        "x_axis": trend_chart['data']['labels'],
        "y_axis": trend_chart['data']['datasets'][0]['data'],
        "x_label": "Month",
        "y_label": "Risk Percentage (%)"
    }
    print(json.dumps(line_data, indent=2))
    
    return chart_data, dashboard_data

def demo_api_responses():
    """Demonstrate API response formats"""
    
    print("\n" + "=" * 60)
    print("🔗 API RESPONSE FORMATS")
    print("=" * 60)
    
    # Dashboard API Response
    print("\n📊 GET /api/hr/analytics/dashboard/ Response:")
    dashboard_response = {
        "success": True,
        "message": "Analytics dashboard data retrieved",
        "data": generate_sample_dashboard_data()
    }
    print(json.dumps(dashboard_response, indent=2))
    
    # Charts API Response
    print("\n📈 GET /api/hr/analytics/charts/ Response:")
    charts_response = {
        "success": True,
        "message": "Chart data retrieved successfully",
        "data": generate_sample_chart_data()
    }
    print(json.dumps(charts_response, indent=2)[:500] + "... (truncated)")
    
    # Meetings API Response
    print("\n🤝 GET /api/hr/meetings/ Response:")
    meetings_response = {
        "success": True,
        "message": "Meetings retrieved successfully",
        "data": generate_sample_meeting_data()
    }
    print(json.dumps(meetings_response, indent=2)[:500] + "... (truncated)")
    
    # Performance Reviews API Response
    print("\n⭐ GET /api/hr/reviews/ Response:")
    reviews_response = {
        "success": True,
        "message": "Performance reviews retrieved successfully",
        "data": generate_sample_performance_review_data()
    }
    print(json.dumps(reviews_response, indent=2)[:500] + "... (truncated)")

def demo_frontend_integration():
    """Show frontend integration examples"""
    
    print("\n" + "=" * 60)
    print("💻 FRONTEND INTEGRATION EXAMPLES")
    print("=" * 60)
    
    print("\n📊 React + Chart.js Integration:")
    print("```jsx")
    print("import React, { useState, useEffect } from 'react';")
    print("import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, LineElement, PointElement } from 'chart.js';")
    print("import { Pie, Bar, Line } from 'react-chartjs-2';")
    print("")
    print("const HRAnalyticsDashboard = ({ adminToken }) => {")
    print("  const [chartData, setChartData] = useState(null);")
    print("")
    print("  useEffect(() => {")
    print("    fetch('/api/hr/analytics/charts/', {")
    print("      headers: { 'Authorization': `Token ${adminToken}` }")
    print("    })")
    print("    .then(res => res.json())")
    print("    .then(data => setChartData(data.data));")
    print("  }, []);")
    print("")
    print("  return (")
    print("    <div className='charts-grid'>")
    print("      <div className='chart-container'>")
    print("        <h3>Risk Distribution</h3>")
    print("        {chartData?.risk_distribution && (")
    print("          <Pie data={chartData.risk_distribution.data} />")
    print("        )}")
    print("      </div>")
    print("      {/* More charts... */}")
    print("    </div>")
    print("  );")
    print("};")
    print("```")
    
    print("\n📋 Meeting Scheduling Form:")
    print("```jsx")
    print("const ScheduleMeetingForm = ({ employeeId, mlPrediction }) => {")
    print("  const [formData, setFormData] = useState({")
    print("    employee: employeeId,")
    print("    title: mlPrediction?.risk_level === 'high' ? 'Urgent Discussion' : 'Regular Check-in',")
    print("    meeting_type: mlPrediction?.risk_level === 'high' ? 'urgent' : 'regular',")
    print("    ml_probability: mlPrediction?.probability")
    print("  });")
    print("  // ... rest of form logic")
    print("};")
    print("```")

def main():
    """Main demo function"""
    
    # Generate and display chart data
    chart_data, dashboard_data = demo_frontend_chart_data()
    
    # Show API response formats
    demo_api_responses()
    
    # Show frontend integration examples
    demo_frontend_integration()
    
    print("\n" + "=" * 60)
    print("🎯 HR FEATURES SUMMARY")
    print("=" * 60)
    print("✅ 1-on-1 Meeting Management: Fully designed")
    print("✅ Performance Review System: Complete with star ratings")
    print("✅ Analytics Dashboard: 3 chart types with frontend data")
    print("✅ Chart Data Structures: Ready for Chart.js integration")
    print("✅ API Response Formats: Standardized and documented")
    print("✅ Role-based Access: Admin/HR vs Employee permissions")
    print("✅ ML Integration: Prediction-triggered meetings and reviews")
    
    print("\n📋 NEXT STEPS:")
    print("1. Deploy backend changes and run migrations")
    print("2. Test endpoints with Postman collection")
    print("3. Integrate charts in frontend with provided data structures")
    print("4. Implement role-based UI components")
    print("5. Add real-time dashboard updates")
    
    print("\n📁 FILES CREATED:")
    print("• HR_FEATURES_COMPLETE_POSTMAN.json - Complete Postman collection")
    print("• HR_FEATURES_FRONTEND_CHART_GUIDE.md - Frontend integration guide")
    print("• backend/hr_features/ - Complete Django app with models, views, serializers")
    print("• test_hr_features_complete.py - Comprehensive test script")
    
    print("\n🎉 HR Features are ready for production deployment!")

if __name__ == "__main__":
    main()
