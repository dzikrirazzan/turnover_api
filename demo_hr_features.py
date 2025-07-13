#!/usr/bin/env python3
"""
Demo script untuk HR Features - menggunakan data dummy untuk demonstrate fitur
Karena backend belum implement endpoint HR, ini menunjukkan struktur data dan response
"""

import json
from datetime import datetime, timedelta
from pprint import pprint

def demo_hr_features():
    """Demo all HR features with sample data"""
    
    print("🚀 SMART-EN HR FEATURES - DEMO MODE")
    print("="*70)
    print("⚠️  Demo dengan data dummy - Backend belum implement")
    print(f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Sample employee data
    sample_employee = {
        "id": 39,
        "full_name": "Bravely Dirgayuska",
        "email": "bravely@company.com",
        "department": "Information Technology",
        "position": "Sales Representative"
    }
    
    print(f"\n🧪 Demo Employee: {sample_employee['full_name']} (ID: {sample_employee['id']})")
    
    # Demo 1: Meeting Management
    demo_meetings(sample_employee)
    
    # Demo 2: Performance Reviews
    demo_performance_reviews(sample_employee)
    
    # Demo 3: Analytics & Charts
    demo_analytics()
    
    # Demo 4: Integration Guide
    demo_integration_guide()

def demo_meetings(employee):
    """Demo Meeting Management features"""
    print("\n" + "="*60)
    print("📅 DEMO: 1-ON-1 MEETINGS MANAGEMENT")
    print("="*60)
    
    # Sample meeting creation
    print("\n1️⃣ Creating Meeting (Based on ML Prediction)")
    meeting_data = {
        "employee": employee["id"],
        "title": "Follow-up Meeting: High Risk Employee",
        "meeting_type": "followup",
        "scheduled_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "duration_minutes": 60,
        "meeting_link": "https://zoom.us/j/123456789",
        "agenda": "Discuss ML prediction results (85% risk), understand concerns, create retention plan",
        "prediction_id": "pred_20250111_123456",
        "ml_probability": 0.85,
        "ml_risk_level": "high"
    }
    
    print("📝 Meeting Request Body:")
    pprint(meeting_data)
    
    # Sample meeting response
    meeting_response = {
        "success": True,
        "message": "Meeting scheduled successfully",
        "data": {
            "id": 1,
            "employee_info": {
                "id": employee["id"],
                "full_name": employee["full_name"],
                "email": employee["email"]
            },
            "scheduled_by_info": {
                "id": 1,
                "full_name": "HR Manager",
                "email": "hr@company.com"
            },
            "title": meeting_data["title"],
            "meeting_type": meeting_data["meeting_type"],
            "scheduled_date": meeting_data["scheduled_date"],
            "duration_minutes": meeting_data["duration_minutes"],
            "meeting_link": meeting_data["meeting_link"],
            "agenda": meeting_data["agenda"],
            "status": "scheduled",
            "is_high_priority": True,  # Because ml_probability > 0.7
            "created_at": datetime.now().isoformat()
        }
    }
    
    print("\n✅ Meeting Response:")
    pprint(meeting_response)
    
    # Demo meeting list
    print("\n2️⃣ Getting All Meetings")
    meetings_list = {
        "success": True,
        "message": "Meetings retrieved successfully",
        "data": [
            {
                "id": 1,
                "title": "Follow-up Meeting: High Risk Employee",
                "employee_info": {"full_name": employee["full_name"]},
                "scheduled_date": meeting_data["scheduled_date"],
                "status": "scheduled",
                "is_high_priority": True,
                "ml_risk_level": "high"
            },
            {
                "id": 2,
                "title": "Regular Check-in",
                "employee_info": {"full_name": "John Doe"},
                "scheduled_date": (datetime.now() + timedelta(days=3)).isoformat(),
                "status": "scheduled",
                "is_high_priority": False,
                "ml_risk_level": "low"
            }
        ]
    }
    
    print("📋 Meetings List:")
    pprint(meetings_list)

def demo_performance_reviews(employee):
    """Demo Performance Review features"""
    print("\n" + "="*60)
    print("⭐ DEMO: PERFORMANCE REVIEWS")
    print("="*60)
    
    # Sample review creation
    print("\n1️⃣ Creating Performance Review (with Star Ratings)")
    review_data = {
        "employee": employee["id"],
        "review_period": "quarterly",
        "review_date": datetime.now().date().isoformat(),
        "period_start": (datetime.now() - timedelta(days=90)).date().isoformat(),
        "period_end": datetime.now().date().isoformat(),
        "overall_rating": 3,
        "technical_skills": 4,
        "communication": 2,  # Low score - matches ML prediction concerns
        "teamwork": 3,
        "leadership": 2,     # Low score
        "initiative": 2,     # Low score  
        "problem_solving": 4,
        "strengths": "Strong technical abilities, good problem-solving skills, meets deadlines consistently",
        "areas_for_improvement": "Communication needs improvement, lacks initiative, limited leadership skills, appears disengaged",
        "goals_for_next_period": "1. Improve communication with team and stakeholders\n2. Take leadership role in small project\n3. Participate more in team discussions",
        "additional_notes": "Review triggered by ML prediction showing 85% turnover risk. Focus on engagement and career development.",
        "triggered_by_ml": True,
        "ml_prediction_id": "pred_20250111_123456"
    }
    
    print("📝 Review Request Body:")
    pprint(review_data)
    
    # Sample review response
    review_response = {
        "success": True,
        "message": "Performance review created successfully",
        "data": {
            "id": 1,
            "employee_info": {
                "id": employee["id"],
                "full_name": employee["full_name"],
                "email": employee["email"]
            },
            "reviewer_info": {
                "id": 1,
                "full_name": "HR Manager",
                "email": "hr@company.com"
            },
            **review_data,
            "average_rating": 2.86,  # Calculated average
            "rating_breakdown": {
                "overall": 3,
                "technical_skills": 4,
                "communication": 2,
                "teamwork": 3,
                "leadership": 2,
                "initiative": 2,
                "problem_solving": 4,
                "average": 2.86
            },
            "is_final": False,
            "employee_acknowledged": False,
            "created_at": datetime.now().isoformat()
        }
    }
    
    print("\n✅ Review Response:")
    pprint(review_response)
    
    # Demo review summary
    print("\n2️⃣ Performance Review Summary")
    review_summary = {
        "success": True,
        "message": "Review summary retrieved",
        "data": {
            "total_reviews": 4,
            "average_overall_rating": 3.25,
            "latest_review": review_response["data"],
            "rating_trend": [
                {"date": "2025-01", "rating": 3},
                {"date": "2024-10", "rating": 3},
                {"date": "2024-07", "rating": 4},
                {"date": "2024-04", "rating": 3}
            ]
        }
    }
    
    print("📊 Review Summary:")
    pprint(review_summary)

def demo_analytics():
    """Demo Analytics & Charts features"""
    print("\n" + "="*60)
    print("📊 DEMO: ANALYTICS & CHARTS")
    print("="*60)
    
    # Sample analytics dashboard
    print("\n1️⃣ Analytics Dashboard")
    analytics_data = {
        "success": True,
        "message": "Analytics dashboard data retrieved",
        "data": {
            "total_predictions": 150,
            "total_meetings": 45,
            "total_reviews": 120,
            "high_risk_employees": 12,
            "recent_predictions": 25,
            "risk_distribution": {
                "low_risk": 95,      # 63%
                "medium_risk": 43,   # 29%
                "high_risk": 12,     # 8%
                "total_employees": 150
            },
            "department_analysis": [
                {
                    "department": "Engineering",
                    "employee_count": 45,
                    "average_risk": 15.2,
                    "high_risk_count": 3
                },
                {
                    "department": "Marketing", 
                    "employee_count": 30,
                    "average_risk": 32.1,
                    "high_risk_count": 5
                },
                {
                    "department": "HR",
                    "employee_count": 15,
                    "average_risk": 8.5,
                    "high_risk_count": 0
                },
                {
                    "department": "Finance",
                    "employee_count": 25,
                    "average_risk": 28.3,
                    "high_risk_count": 2
                }
            ],
            "trend_analysis": [
                {"month": "Jan 2025", "average_risk": 22.5, "prediction_count": 25},
                {"month": "Dec 2024", "average_risk": 18.9, "prediction_count": 22},
                {"month": "Nov 2024", "average_risk": 25.1, "prediction_count": 30},
                {"month": "Oct 2024", "average_risk": 19.7, "prediction_count": 28},
                {"month": "Sep 2024", "average_risk": 21.3, "prediction_count": 26},
                {"month": "Aug 2024", "average_risk": 23.8, "prediction_count": 19}
            ]
        }
    }
    
    print("📈 Analytics Dashboard:")
    pprint(analytics_data)
    
    # Sample chart data for frontend
    print("\n2️⃣ Chart Data for Frontend (Chart.js Format)")
    chart_data = {
        "success": True,
        "message": "Chart data retrieved successfully",
        "data": {
            # Pie chart for risk distribution
            "risk_distribution": {
                "chart_type": "pie",
                "title": "Employee Risk Distribution",
                "data": {
                    "labels": ["Low Risk", "Medium Risk", "High Risk"],
                    "datasets": [{
                        "data": [95, 43, 12],
                        "backgroundColor": ["#28a745", "#ffc107", "#dc3545"],
                        "borderWidth": 2
                    }]
                }
            },
            
            # Bar chart for department analysis
            "department_analysis": {
                "chart_type": "bar",
                "title": "Risk Analysis by Department",
                "data": {
                    "labels": ["Engineering", "Marketing", "HR", "Finance"],
                    "datasets": [{
                        "label": "Average Risk Score (%)",
                        "data": [15.2, 32.1, 8.5, 28.3],
                        "backgroundColor": "#4F46E5",
                        "borderColor": "#3730A3",
                        "borderWidth": 1
                    }]
                }
            },
            
            # Line chart for trend analysis
            "trend_analysis": {
                "chart_type": "line",
                "title": "Turnover Risk Trend (Last 6 Months)",
                "data": {
                    "labels": ["Aug 2024", "Sep 2024", "Oct 2024", "Nov 2024", "Dec 2024", "Jan 2025"],
                    "datasets": [{
                        "label": "Average Risk %",
                        "data": [23.8, 21.3, 19.7, 25.1, 18.9, 22.5],
                        "borderColor": "#EF4444",
                        "backgroundColor": "rgba(239, 68, 68, 0.1)",
                        "tension": 0.4,
                        "fill": True
                    }]
                }
            },
            
            # Horizontal bar for risk factors impact
            "risk_factors_impact": {
                "chart_type": "horizontalBar",
                "title": "Risk Factors Impact Analysis",
                "data": {
                    "labels": ["Satisfaction Level", "Last Evaluation", "Working Hours", "Number Projects", "Promotion History", "Work Accidents"],
                    "datasets": [{
                        "label": "Average Impact (%)",
                        "data": [35, 28, 18, 12, 5, 2],
                        "backgroundColor": ["#EF4444", "#F97316", "#EAB308", "#22C55E", "#3B82F6", "#8B5CF6"]
                    }]
                }
            },
            
            # Scatter plot for satisfaction vs performance
            "satisfaction_performance": {
                "chart_type": "scatter", 
                "title": "Satisfaction vs Performance Risk",
                "data": {
                    "datasets": [{
                        "label": "Employees",
                        "data": [
                            {"x": 65, "y": 82, "employee": "John Doe", "risk": "low"},
                            {"x": 30, "y": 45, "employee": "Jane Smith", "risk": "high"},
                            {"x": 75, "y": 88, "employee": "Bob Wilson", "risk": "low"},
                            {"x": 45, "y": 60, "employee": "Alice Brown", "risk": "medium"}
                        ],
                        "backgroundColor": "#4F46E5",
                        "pointRadius": 8,
                        "pointHoverRadius": 12
                    }]
                },
                "options": {
                    "scales": {
                        "x": {"title": {"display": True, "text": "Satisfaction Level (%)"}},
                        "y": {"title": {"display": True, "text": "Last Evaluation (%)"}}
                    }
                }
            }
        }
    }
    
    print("📊 Chart Data:")
    pprint(chart_data)

def demo_integration_guide():
    """Demo Frontend Integration Guide"""
    print("\n" + "="*60)
    print("🚀 FRONTEND INTEGRATION GUIDE")
    print("="*60)
    
    print("""
🎯 NEXT STEPS FOR FRONTEND IMPLEMENTATION:

1️⃣ INSTALL DEPENDENCIES:
   npm install chart.js react-chartjs-2
   npm install @mui/material @emotion/react @emotion/styled
   npm install date-fns axios

2️⃣ CHART COMPONENTS (React):
   
   // PieChart.jsx
   import { Pie } from 'react-chartjs-2';
   
   function RiskDistributionChart({ data }) {
     return <Pie data={data.risk_distribution.data} />;
   }
   
   // BarChart.jsx
   import { Bar } from 'react-chartjs-2';
   
   function DepartmentAnalysisChart({ data }) {
     return <Bar data={data.department_analysis.data} />;
   }

3️⃣ MEETING SCHEDULER COMPONENT:
   
   function MeetingScheduler({ employeeId, mlPrediction }) {
     const [meeting, setMeeting] = useState({
       title: '',
       scheduled_date: '',
       meeting_link: '',
       agenda: '',
       meeting_type: 'followup'
     });
     
     const scheduleMeeting = async () => {
       const response = await fetch('/api/meetings/', {
         method: 'POST',
         headers: {
           'Authorization': `Token ${token}`,
           'Content-Type': 'application/json'
         },
         body: JSON.stringify({
           employee: employeeId,
           ...meeting,
           ml_probability: mlPrediction.probability,
           ml_risk_level: mlPrediction.risk_level
         })
       });
       // Handle response
     };
   }

4️⃣ PERFORMANCE REVIEW COMPONENT:
   
   function PerformanceReviewForm({ employeeId }) {
     const [review, setReview] = useState({
       overall_rating: 3,
       technical_skills: 3,
       communication: 3,
       // ... other ratings
     });
     
     const StarRating = ({ rating, onChange, label }) => (
       <div className="star-rating">
         <label>{label}</label>
         {[1, 2, 3, 4, 5].map(star => (
           <span
             key={star}
             className={`star ${star <= rating ? 'filled' : ''}`}
             onClick={() => onChange(star)}
           >
             ⭐
           </span>
         ))}
       </div>
     );
   }

5️⃣ ANALYTICS DASHBOARD:
   
   function AnalyticsDashboard() {
     const [analytics, setAnalytics] = useState(null);
     
     useEffect(() => {
       fetch('/api/analytics/dashboard/', {
         headers: { 'Authorization': `Token ${token}` }
       })
       .then(res => res.json())
       .then(data => setAnalytics(data));
     }, []);
     
     return (
       <div className="analytics-dashboard">
         <div className="metrics-grid">
           <MetricCard title="Total Predictions" value={analytics.total_predictions} />
           <MetricCard title="High Risk Employees" value={analytics.high_risk_employees} />
         </div>
         
         <div className="charts-grid">
           <RiskDistributionChart data={analytics.chart_data} />
           <DepartmentAnalysisChart data={analytics.chart_data} />
         </div>
       </div>
     );
   }

6️⃣ API ENDPOINTS STRUCTURE:
   Base URL: https://turnover-api-hd7ze.ondigitalocean.app
   
   📅 Meetings:
   - POST /api/meetings/          # Create meeting
   - GET  /api/meetings/          # List meetings
   - PUT  /api/meetings/{id}/     # Update meeting
   - POST /api/meetings/{id}/complete/  # Complete meeting
   
   ⭐ Reviews:
   - POST /api/reviews/           # Create review
   - GET  /api/reviews/           # List reviews
   - PUT  /api/reviews/{id}/      # Update review
   - GET  /api/reviews/summary/   # Get summary
   
   📊 Analytics:
   - GET  /api/analytics/dashboard/  # Complete dashboard
   - GET  /api/analytics/charts/     # Chart data

7️⃣ ROLE-BASED ACCESS:
   
   Admin/HR:
   ✅ Create/edit meetings and reviews
   ✅ View all employees' data
   ✅ Access analytics dashboard
   
   Employee:
   ✅ View own meetings (read-only)
   ✅ View own reviews (read-only)
   ✅ Acknowledge reviews
   ❌ Cannot create/edit data

8️⃣ WORKFLOW INTEGRATION:
   
   ML Prediction → Schedule Meeting → Conduct Review → Track Analytics
   
   1. Get ML prediction (high risk employee)
   2. Auto-schedule follow-up meeting
   3. Create performance review based on meeting
   4. Track progress in analytics dashboard
   5. Generate insights and trends

🎉 READY FOR IMPLEMENTATION!
   All data structures and API formats are ready.
   Start with implementing the backend endpoints,
   then build the frontend components.
""")

if __name__ == "__main__":
    demo_hr_features()
    
    print("\n" + "="*70)
    print("✅ DEMO COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("📋 Features Demonstrated:")
    print("   📅 1-on-1 Meeting Management")
    print("   ⭐ Performance Review System (Star Ratings)")
    print("   📊 Analytics Dashboard (Multiple Chart Types)")
    print("   🎯 Frontend Integration Examples")
    print("   🔐 Role-based Access Control")
    print("\n🚀 Ready for Backend Implementation & Frontend Development!")
