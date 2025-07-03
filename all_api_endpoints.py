#!/usr/bin/env python3
"""
Complete API Endpoint Discovery for SMART-EN Turnover Prediction API
Generates comprehensive list of all available endpoints
"""

import os
import json
from datetime import datetime

def generate_complete_endpoint_list():
    """Generate complete list of all API endpoints"""
    
    BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"
    
    endpoints = {
        "info": {
            "name": "API Information & Health",
            "endpoints": [
                {
                    "name": "Health Check",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/health/",
                    "auth_required": False,
                    "description": "Check API health status",
                    "response_format": "StandardResponse with health data"
                },
                {
                    "name": "API Info",
                    "method": "GET", 
                    "url": f"{BASE_URL}/api/info/",
                    "auth_required": False,
                    "description": "Get API information and features",
                    "response_format": "StandardResponse with API details"
                }
            ]
        },
        
        "authentication": {
            "name": "Authentication & User Management",
            "endpoints": [
                {
                    "name": "Register Employee",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/register/",
                    "auth_required": False,
                    "description": "Register new employee with complete data",
                    "body_example": {
                        "email": "newuser@example.com",
                        "password": "securepass123",
                        "password_confirm": "securepass123",
                        "first_name": "John",
                        "last_name": "Doe",
                        "phone_number": "+6281234567890",
                        "date_of_birth": "1990-01-01",
                        "gender": "M",
                        "marital_status": "single",
                        "education_level": "bachelor",
                        "address": "Test Address",
                        "position": "Developer",
                        "department": 1,
                        "hire_date": "2024-01-01"
                    },
                    "response_format": "StandardResponse with employee data and token"
                },
                {
                    "name": "Login Employee",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/login/",
                    "auth_required": False,
                    "description": "Login with email and password",
                    "body_example": {
                        "email": "admin@company.com",
                        "password": "AdminPass123!"
                    },
                    "response_format": "StandardResponse with user data and token"
                },
                {
                    "name": "User Profile",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/profile/",
                    "auth_required": True,
                    "description": "Get current user profile with complete data",
                    "response_format": "Complete user data with token"
                },
                {
                    "name": "Logout Employee",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/logout/",
                    "auth_required": True,
                    "description": "Logout current user",
                    "response_format": "StandardResponse with success message"
                }
            ]
        },
        
        "departments": {
            "name": "Department Management",
            "endpoints": [
                {
                    "name": "List Departments",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/departments/",
                    "auth_required": True,
                    "description": "Get all departments with pagination",
                    "query_params": ["page", "page_size"],
                    "response_format": "Django REST pagination format"
                },
                {
                    "name": "List Departments (Simple)",
                    "method": "GET", 
                    "url": f"{BASE_URL}/api/list-departments/",
                    "auth_required": False,
                    "description": "Get simple list of departments",
                    "response_format": "StandardResponse with department list"
                },
                {
                    "name": "Create Department",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/departments/",
                    "auth_required": True,
                    "admin_only": True,
                    "description": "Create new department",
                    "body_example": {
                        "name": "Engineering",
                        "description": "Software Engineering Department"
                    },
                    "response_format": "StandardResponse with created department"
                },
                {
                    "name": "Get Department Detail",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/departments/{{id}}/",
                    "auth_required": True,
                    "description": "Get specific department details",
                    "response_format": "Department data"
                },
                {
                    "name": "Update Department",
                    "method": "PUT",
                    "url": f"{BASE_URL}/api/departments/{{id}}/",
                    "auth_required": True,
                    "admin_only": True,
                    "description": "Update department information",
                    "response_format": "Updated department data"
                },
                {
                    "name": "Partial Update Department",
                    "method": "PATCH",
                    "url": f"{BASE_URL}/api/departments/{{id}}/",
                    "auth_required": True,
                    "admin_only": True,
                    "description": "Partially update department",
                    "response_format": "Updated department data"
                },
                {
                    "name": "Delete Department",
                    "method": "DELETE",
                    "url": f"{BASE_URL}/api/departments/{{id}}/",
                    "auth_required": True,
                    "admin_only": True,
                    "description": "Delete department",
                    "response_format": "No content (204)"
                },
                {
                    "name": "Get Department Employees",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/departments/{{id}}/employees/",
                    "auth_required": True,
                    "description": "Get all employees in specific department",
                    "response_format": "StandardResponse with employee list"
                }
            ]
        },
        
        "employees": {
            "name": "Employee Management (Admin Only)",
            "endpoints": [
                {
                    "name": "List All Employees",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/employees/",
                    "auth_required": True,
                    "admin_only": True,
                    "description": "Get all employees with pagination and filters",
                    "query_params": ["department", "role", "is_active", "page"],
                    "response_format": "Django REST pagination format"
                },
                {
                    "name": "List Employees (Simple)",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/list-employees/",
                    "auth_required": True,
                    "admin_only": True,
                    "description": "Get simple list of employees",
                    "response_format": "StandardResponse with employee list"
                },
                {
                    "name": "Create Employee",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/employees/",
                    "auth_required": True,
                    "admin_only": True,
                    "description": "Create new employee (admin function)",
                    "body_example": {
                        "email": "employee@company.com",
                        "password": "pass123",
                        "password_confirm": "pass123",
                        "first_name": "Jane",
                        "last_name": "Smith",
                        "phone_number": "+6281234567891",
                        "date_of_birth": "1985-05-15",
                        "gender": "F", 
                        "marital_status": "married",
                        "education_level": "master",
                        "address": "Admin Created Address",
                        "position": "Senior Developer",
                        "department": 1,
                        "hire_date": "2024-02-01"
                    },
                    "response_format": "StandardResponse with created employee"
                },
                {
                    "name": "Get Employee Detail",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/employees/{{id}}/",
                    "auth_required": True,
                    "admin_only": True,
                    "description": "Get specific employee details",
                    "response_format": "Employee data"
                },
                {
                    "name": "Update Employee",
                    "method": "PUT",
                    "url": f"{BASE_URL}/api/employees/{{id}}/",
                    "auth_required": True,
                    "admin_only": True,
                    "description": "Update employee information",
                    "response_format": "StandardResponse with updated employee"
                },
                {
                    "name": "Partial Update Employee", 
                    "method": "PATCH",
                    "url": f"{BASE_URL}/api/employees/{{id}}/",
                    "auth_required": True,
                    "admin_only": True,
                    "description": "Partially update employee",
                    "response_format": "StandardResponse with updated employee"
                },
                {
                    "name": "Deactivate Employee",
                    "method": "DELETE",
                    "url": f"{BASE_URL}/api/employees/{{id}}/",
                    "auth_required": True,
                    "admin_only": True,
                    "description": "Soft delete employee (set inactive)",
                    "response_format": "StandardResponse with deactivation message"
                },
                {
                    "name": "Activate Employee",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/employees/{{id}}/activate/",
                    "auth_required": True,
                    "admin_only": True,
                    "description": "Reactivate deactivated employee",
                    "response_format": "StandardResponse with activation message"
                },
                {
                    "name": "Get Employee Performance Data",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/employees/{{id}}/performance_data/",
                    "auth_required": True,
                    "admin_only": True,
                    "description": "Get ML performance data for specific employee",
                    "response_format": "StandardResponse with performance data or 404"
                },
                {
                    "name": "Employee Statistics",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/employees/statistics/",
                    "auth_required": True,
                    "admin_only": True,
                    "description": "Get employee statistics and breakdown",
                    "response_format": "StandardResponse with statistics"
                }
            ]
        },
        
        "ml_performance": {
            "name": "ML Performance Data Management (Admin Only)",
            "endpoints": [
                {
                    "name": "List Performance Data",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance-data/",
                    "auth_required": True,
                    "admin_only": True,
                    "description": "Get all ML performance data records",
                    "response_format": "StandardResponse with performance data list"
                },
                {
                    "name": "Create Performance Data",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/performance-data/",
                    "auth_required": True,
                    "admin_only": True,
                    "description": "Create new ML performance data for employee",
                    "body_example": {
                        "employee": 1,
                        "satisfaction_level": 0.85,
                        "last_evaluation": 0.92,
                        "number_project": 5,
                        "average_monthly_hours": 160,
                        "time_spend_company": 3,
                        "work_accident": False,
                        "promotion_last_5years": True,
                        "left": False
                    },
                    "response_format": "StandardResponse with created performance data"
                },
                {
                    "name": "Data Separation Statistics",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/data-separation-stats/",
                    "auth_required": True,
                    "admin_only": True,
                    "description": "Get statistics about data separation implementation",
                    "response_format": "StandardResponse with separation statistics"
                }
            ]
        },
        
        "performance_app": {
            "name": "Performance Application (Goals, Reviews, etc.)",
            "endpoints": [
                {
                    "name": "List Goals",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/goals/",
                    "auth_required": True,
                    "description": "Get goals with optional employee filter",
                    "query_params": ["employee", "status"],
                    "response_format": "Goal list"
                },
                {
                    "name": "Create Goal",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/performance/goals/",
                    "auth_required": True,
                    "description": "Create new goal",
                    "body_example": {
                        "title": "Complete Project Alpha",
                        "description": "Finish the Alpha project by Q2",
                        "owner": 1,
                        "deadline": "2024-06-30",
                        "status": "in_progress"
                    },
                    "response_format": "Created goal data"
                },
                {
                    "name": "Get Goal Detail",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/goals/{{id}}/",
                    "auth_required": True,
                    "description": "Get specific goal details",
                    "response_format": "Goal data"
                },
                {
                    "name": "Update Goal",
                    "method": "PUT",
                    "url": f"{BASE_URL}/api/performance/goals/{{id}}/",
                    "auth_required": True,
                    "description": "Update goal",
                    "response_format": "Updated goal data"
                },
                {
                    "name": "Delete Goal",
                    "method": "DELETE",
                    "url": f"{BASE_URL}/api/performance/goals/{{id}}/",
                    "auth_required": True,
                    "description": "Delete goal",
                    "response_format": "No content"
                },
                {
                    "name": "Goal Statistics",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/goals/statistics/",
                    "auth_required": True,
                    "description": "Get goal statistics",
                    "query_params": ["employee"],
                    "response_format": "Goal statistics"
                },
                {
                    "name": "List Key Results",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/key-results/",
                    "auth_required": True,
                    "description": "Get key results",
                    "query_params": ["goal"],
                    "response_format": "Key results list"
                },
                {
                    "name": "Create Key Result",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/performance/key-results/",
                    "auth_required": True,
                    "description": "Create new key result",
                    "body_example": {
                        "goal": 1,
                        "title": "Increase performance by 20%",
                        "target_value": 100,
                        "current_value": 0,
                        "unit": "percent"
                    },
                    "response_format": "Created key result"
                },
                {
                    "name": "Update Key Result Progress",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/performance/key-results/{{id}}/update_progress/",
                    "auth_required": True,
                    "description": "Update key result progress",
                    "body_example": {
                        "current_value": 75
                    },
                    "response_format": "Updated key result"
                },
                {
                    "name": "List Feedback",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/feedback/",
                    "auth_required": True,
                    "description": "Get feedback with filters",
                    "query_params": ["recipient", "sender", "type"],
                    "response_format": "Feedback list"
                },
                {
                    "name": "Create Feedback",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/performance/feedback/",
                    "auth_required": True,
                    "description": "Give feedback to employee",
                    "body_example": {
                        "recipient": 2,
                        "feedback_type": "positive",
                        "content": "Great work on the project!",
                        "is_anonymous": False
                    },
                    "response_format": "Created feedback"
                },
                {
                    "name": "Feedback Received",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/feedback/received/",
                    "auth_required": True,
                    "description": "Get feedback received by current user",
                    "response_format": "Received feedback list"
                },
                {
                    "name": "Feedback Sent",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/feedback/sent/",
                    "auth_required": True,
                    "description": "Get feedback sent by current user",
                    "response_format": "Sent feedback list"
                },
                {
                    "name": "List Performance Reviews",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/reviews/",
                    "auth_required": True,
                    "description": "Get performance reviews",
                    "query_params": ["employee", "reviewer", "status"],
                    "response_format": "Review list"
                },
                {
                    "name": "Create Performance Review",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/performance/reviews/",
                    "auth_required": True,
                    "description": "Create performance review",
                    "body_example": {
                        "employee": 2,
                        "review_period_start": "2024-01-01",
                        "review_period_end": "2024-06-30",
                        "overall_rating": 4,
                        "strengths": "Good communication skills",
                        "areas_for_improvement": "Time management"
                    },
                    "response_format": "Created review"
                },
                {
                    "name": "List One-on-One Meetings",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/one-on-ones/",
                    "auth_required": True,
                    "description": "Get one-on-one meetings",
                    "query_params": ["employee", "manager"],
                    "response_format": "Meeting list"
                },
                {
                    "name": "Create One-on-One Meeting",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/performance/one-on-ones/",
                    "auth_required": True,
                    "description": "Schedule one-on-one meeting",
                    "body_example": {
                        "employee": 2,
                        "scheduled_date": "2024-07-15T10:00:00Z",
                        "agenda": "Quarterly review and goal setting",
                        "status": "scheduled"
                    },
                    "response_format": "Created meeting"
                },
                {
                    "name": "List Shoutouts",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/shoutouts/",
                    "auth_required": True,
                    "description": "Get public shoutouts/recognitions",
                    "response_format": "Shoutout list"
                },
                {
                    "name": "Create Shoutout",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/performance/shoutouts/",
                    "auth_required": True,
                    "description": "Give public recognition",
                    "body_example": {
                        "recipient": 2,
                        "message": "Amazing presentation today!",
                        "category": "teamwork"
                    },
                    "response_format": "Created shoutout"
                },
                {
                    "name": "Like Shoutout",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/performance/shoutouts/{{id}}/like/",
                    "auth_required": True,
                    "description": "Like/unlike a shoutout",
                    "response_format": "Like status"
                },
                {
                    "name": "List Learning Modules",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/learning/modules/",
                    "auth_required": True,
                    "description": "Get available learning modules",
                    "response_format": "Learning module list"
                },
                {
                    "name": "Create Learning Module",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/performance/learning/modules/",
                    "auth_required": True,
                    "description": "Create learning module",
                    "body_example": {
                        "title": "Python Advanced Concepts",
                        "description": "Advanced Python programming",
                        "category": "technical",
                        "duration_hours": 20,
                        "is_mandatory": False
                    },
                    "response_format": "Created module"
                },
                {
                    "name": "List Learning Progress",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/learning/progress/",
                    "auth_required": True,
                    "description": "Get learning progress",
                    "query_params": ["employee", "module"],
                    "response_format": "Progress list"
                },
                {
                    "name": "Update Learning Progress",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/performance/learning/progress/{{id}}/update/",
                    "auth_required": True,
                    "description": "Update learning progress",
                    "body_example": {
                        "progress_percentage": 75,
                        "notes": "Completed chapters 1-3"
                    },
                    "response_format": "Updated progress"
                },
                {
                    "name": "List Learning Goals",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/learning/goals/",
                    "auth_required": True,
                    "description": "Get learning goals",
                    "response_format": "Learning goal list"
                },
                {
                    "name": "Create Learning Goal",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/performance/learning/goals/",
                    "auth_required": True,
                    "description": "Set learning goal",
                    "body_example": {
                        "employee": 1,
                        "title": "Master React Framework",
                        "description": "Complete React certification",
                        "target_date": "2024-12-31",
                        "priority": "high"
                    },
                    "response_format": "Created learning goal"
                }
            ]
        },
        
        "analytics": {
            "name": "Analytics & Dashboard",
            "endpoints": [
                {
                    "name": "Dashboard Statistics",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/analytics/dashboard-stats/",
                    "auth_required": True,
                    "description": "Get dashboard statistics",
                    "response_format": "Dashboard stats"
                },
                {
                    "name": "Team Engagement",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/analytics/team-engagement/",
                    "auth_required": True,
                    "description": "Get team engagement metrics",
                    "response_format": "Engagement data"
                },
                {
                    "name": "Individual Performance",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/analytics/individual-performance/",
                    "auth_required": True,
                    "description": "Get individual performance metrics",
                    "query_params": ["employee", "start_date", "end_date"],
                    "response_format": "Performance metrics"
                },
                {
                    "name": "Analytics Dashboard",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/analytics/dashboard/",
                    "auth_required": True,
                    "description": "Get comprehensive analytics dashboard",
                    "response_format": "Analytics dashboard data"
                },
                {
                    "name": "List Analytics Metrics",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/analytics/metrics/",
                    "auth_required": True,
                    "description": "Get analytics metrics",
                    "response_format": "Metrics list"
                },
                {
                    "name": "Create Analytics Metric",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/performance/analytics/metrics/",
                    "auth_required": True,
                    "description": "Create analytics metric",
                    "body_example": {
                        "metric_name": "team_productivity",
                        "metric_value": 85.5,
                        "employee": 1,
                        "date_recorded": "2024-07-04"
                    },
                    "response_format": "Created metric"
                },
                {
                    "name": "List Dashboard Activities",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/dashboard/activities/",
                    "auth_required": True,
                    "description": "Get dashboard activities",
                    "response_format": "Activity list"
                },
                {
                    "name": "Create Dashboard Activity",
                    "method": "POST",
                    "url": f"{BASE_URL}/api/performance/dashboard/activities/",
                    "auth_required": True,
                    "description": "Create dashboard activity",
                    "body_example": {
                        "activity_type": "goal_completed",
                        "description": "John completed Q2 goals",
                        "employee": 1
                    },
                    "response_format": "Created activity"
                }
            ]
        },
        
        "sample_data": {
            "name": "Sample Data Endpoints (Development)",
            "endpoints": [
                {
                    "name": "Sample Goals",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/sample/goals/",
                    "auth_required": True,
                    "description": "Get sample goals data",
                    "response_format": "Sample goals list"
                },
                {
                    "name": "Sample Feedback",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/sample/feedback/",
                    "auth_required": True,
                    "description": "Get sample feedback data",
                    "response_format": "Sample feedback list"
                },
                {
                    "name": "Current Review",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/sample/current-review/",
                    "auth_required": True,
                    "description": "Get current review sample",
                    "response_format": "Current review data"
                },
                {
                    "name": "Categories",
                    "method": "GET",
                    "url": f"{BASE_URL}/api/performance/sample/categories/",
                    "auth_required": True,
                    "description": "Get sample categories",
                    "response_format": "Categories list"
                }
            ]
        }
    }
    
    return endpoints

def generate_endpoint_summary():
    """Generate summary of all endpoints"""
    endpoints = generate_complete_endpoint_list()
    
    total_endpoints = 0
    auth_required_count = 0
    admin_only_count = 0
    
    print("🚀 COMPLETE API ENDPOINT DISCOVERY")
    print("=" * 80)
    print(f"🕐 Generated at: {datetime.now()}")
    print(f"🌐 Base URL: https://turnover-api-hd7ze.ondigitalocean.app")
    
    for category_key, category in endpoints.items():
        print(f"\n📁 {category['name']}")
        print("-" * 60)
        
        for endpoint in category['endpoints']:
            total_endpoints += 1
            if endpoint.get('auth_required', False):
                auth_required_count += 1
            if endpoint.get('admin_only', False):
                admin_only_count += 1
                
            auth_badge = "🔒" if endpoint.get('auth_required', False) else "🔓"
            admin_badge = "👑" if endpoint.get('admin_only', False) else ""
            
            print(f"  {auth_badge}{admin_badge} {endpoint['method']} {endpoint['name']}")
            print(f"     URL: {endpoint['url']}")
            print(f"     Description: {endpoint['description']}")
            
            if 'query_params' in endpoint:
                print(f"     Query Params: {', '.join(endpoint['query_params'])}")
            
            if 'body_example' in endpoint:
                print(f"     Body Example: Available")
            
            print(f"     Response: {endpoint['response_format']}")
            print()
    
    print("📊 ENDPOINT SUMMARY")
    print("=" * 80)
    print(f"Total Endpoints: {total_endpoints}")
    print(f"Authentication Required: {auth_required_count}")
    print(f"Admin Only: {admin_only_count}")
    print(f"Public Endpoints: {total_endpoints - auth_required_count}")
    
    return endpoints

def save_endpoint_data():
    """Save endpoint data to JSON file"""
    endpoints = generate_complete_endpoint_list()
    
    # Save to JSON file
    with open('complete_api_endpoints.json', 'w', encoding='utf-8') as f:
        json.dump(endpoints, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Endpoint data saved to: complete_api_endpoints.json")
    return endpoints

if __name__ == "__main__":
    endpoints = generate_endpoint_summary()
    save_endpoint_data()
    
    print("\n✅ Complete API endpoint discovery finished!")
    print("📝 Use this data to create Postman collections or API documentation")
