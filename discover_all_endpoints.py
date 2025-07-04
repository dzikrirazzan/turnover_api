#!/usr/bin/env python3
"""
Complete API Endpoint Discovery untuk SMART-EN Turnover API
Scan semua URL dan ViewSet untuk generate Postman Collection
"""

import os
import sys
import django
import json
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turnover_prediction.settings')
sys.path.append('/Users/dzikrirazzan/Documents/code/turnover_api/backend')
django.setup()

from django.urls import get_resolver
from rest_framework.routers import DefaultRouter
from predictions.urls import router as predictions_router
from performance.urls import router as performance_router

def discover_all_endpoints():
    """Discover all API endpoints dari URLs dan ViewSets"""
    
    print("🔍 DISCOVERING ALL API ENDPOINTS")
    print("=" * 60)
    
    endpoints = {}
    
    # 1. Function-based views dari predictions
    function_endpoints = {
        "health_check": {
            "url": "/api/health/",
            "method": "GET",
            "description": "API health check endpoint",
            "auth_required": False,
            "headers": {"Content-Type": "application/json"}
        },
        "api_info": {
            "url": "/api/info/",
            "method": "GET", 
            "description": "API information and features",
            "auth_required": False,
            "headers": {"Content-Type": "application/json"}
        },
        "register_employee": {
            "url": "/api/register/",
            "method": "POST",
            "description": "Register new employee",
            "auth_required": False,
            "headers": {"Content-Type": "application/json"},
            "sample_data": {
                "email": "{{$randomEmail}}",
                "password": "SecurePass123!",
                "password_confirm": "SecurePass123!",
                "first_name": "{{$randomFirstName}}",
                "last_name": "{{$randomLastName}}",
                "phone_number": "+6281234567890",
                "date_of_birth": "1990-05-15",
                "gender": "M",
                "marital_status": "single",
                "education_level": "bachelor",
                "address": "Jl. Example No. 123, Jakarta",
                "position": "Software Developer",
                "department": 1,
                "hire_date": "2024-01-15",
                "salary": "monthly",
                "salary_amount": 10000000
            }
        },
        "login_employee": {
            "url": "/api/login/",
            "method": "POST",
            "description": "Login with email and password",
            "auth_required": False,
            "headers": {"Content-Type": "application/json"},
            "sample_data": {
                "email": "admin@smarten.com",
                "password": "admin123"
            }
        },
        "logout_employee": {
            "url": "/api/logout/",
            "method": "POST", 
            "description": "Logout current user",
            "auth_required": True,
            "headers": {"Content-Type": "application/json", "Authorization": "Token {{token}}"}
        },
        "user_profile": {
            "url": "/api/profile/",
            "method": "GET",
            "description": "Get current user profile",
            "auth_required": True,
            "headers": {"Content-Type": "application/json", "Authorization": "Token {{token}}"}
        },
        "list_departments": {
            "url": "/api/departments-list/",
            "method": "GET", 
            "description": "List all departments (public)",
            "auth_required": False,
            "headers": {"Content-Type": "application/json"}
        },
        "list_employees": {
            "url": "/api/employees-list/",
            "method": "GET",
            "description": "List all employees (admin only)",
            "auth_required": True,
            "headers": {"Content-Type": "application/json", "Authorization": "Token {{token}}"}
        },
        "manage_performance_data": {
            "url": "/api/performance-data/",
            "methods": ["GET", "POST"],
            "description": "Manage ML performance data (admin only)",
            "auth_required": True,
            "headers": {"Content-Type": "application/json", "Authorization": "Token {{token}}"},
            "sample_data": {
                "employee": 1,
                "satisfaction_level": 0.75,
                "last_evaluation": 0.85,
                "number_project": 3,
                "average_monthly_hours": 160,
                "time_spend_company": 2,
                "work_accident": 0,
                "promotion_last_5years": 0,
                "left": 0
            }
        },
        "data_separation_stats": {
            "url": "/api/data-stats/",
            "method": "GET",
            "description": "Get data separation statistics",
            "auth_required": True,
            "headers": {"Content-Type": "application/json", "Authorization": "Token {{token}}"}
        }
    }
    
    endpoints["Function Views"] = function_endpoints
    
    # 2. ViewSet endpoints dari predictions (CRUD operations)
    predictions_viewsets = {
        "departments": {
            "list": {"url": "/api/departments/", "method": "GET", "description": "List all departments"},
            "create": {"url": "/api/departments/", "method": "POST", "description": "Create new department",
                     "sample_data": {"name": "New Department", "description": "Department description"}},
            "retrieve": {"url": "/api/departments/{id}/", "method": "GET", "description": "Get department details"},
            "update": {"url": "/api/departments/{id}/", "method": "PUT", "description": "Update department"},
            "partial_update": {"url": "/api/departments/{id}/", "method": "PATCH", "description": "Partial update department"},
            "destroy": {"url": "/api/departments/{id}/", "method": "DELETE", "description": "Delete department"},
            "employees": {"url": "/api/departments/{id}/employees/", "method": "GET", "description": "Get employees in department"}
        },
        "employees": {
            "list": {"url": "/api/employees/", "method": "GET", "description": "List all employees (admin only)"},
            "create": {"url": "/api/employees/", "method": "POST", "description": "Create new employee (admin only)"},
            "retrieve": {"url": "/api/employees/{id}/", "method": "GET", "description": "Get employee details"},
            "update": {"url": "/api/employees/{id}/", "method": "PUT", "description": "Update employee"},
            "partial_update": {"url": "/api/employees/{id}/", "method": "PATCH", "description": "Partial update employee"},
            "destroy": {"url": "/api/employees/{id}/", "method": "DELETE", "description": "Delete employee"},
            "statistics": {"url": "/api/employees/statistics/", "method": "GET", "description": "Get employee statistics"}
        }
    }
    
    endpoints["Predictions ViewSets"] = predictions_viewsets
    
    # 3. Performance ViewSets (from performance app)
    performance_viewsets = {
        "goals": {
            "list": {"url": "/api/goals/", "method": "GET", "description": "List all goals"},
            "create": {"url": "/api/goals/", "method": "POST", "description": "Create new goal"},
            "retrieve": {"url": "/api/goals/{id}/", "method": "GET", "description": "Get goal details"},
            "update": {"url": "/api/goals/{id}/", "method": "PUT", "description": "Update goal"},
            "destroy": {"url": "/api/goals/{id}/", "method": "DELETE", "description": "Delete goal"}
        },
        "key-results": {
            "list": {"url": "/api/key-results/", "method": "GET", "description": "List all key results"},
            "create": {"url": "/api/key-results/", "method": "POST", "description": "Create new key result"},
            "retrieve": {"url": "/api/key-results/{id}/", "method": "GET", "description": "Get key result details"},
            "update": {"url": "/api/key-results/{id}/", "method": "PUT", "description": "Update key result"},
            "destroy": {"url": "/api/key-results/{id}/", "method": "DELETE", "description": "Delete key result"}
        },
        "feedback": {
            "list": {"url": "/api/feedback/", "method": "GET", "description": "List all feedback"},
            "create": {"url": "/api/feedback/", "method": "POST", "description": "Create new feedback"},
            "retrieve": {"url": "/api/feedback/{id}/", "method": "GET", "description": "Get feedback details"},
            "update": {"url": "/api/feedback/{id}/", "method": "PUT", "description": "Update feedback"},
            "destroy": {"url": "/api/feedback/{id}/", "method": "DELETE", "description": "Delete feedback"}
        },
        "performance-reviews": {
            "list": {"url": "/api/performance-reviews/", "method": "GET", "description": "List all performance reviews"},
            "create": {"url": "/api/performance-reviews/", "method": "POST", "description": "Create new performance review"},
            "retrieve": {"url": "/api/performance-reviews/{id}/", "method": "GET", "description": "Get performance review details"},
            "update": {"url": "/api/performance-reviews/{id}/", "method": "PUT", "description": "Update performance review"},
            "destroy": {"url": "/api/performance-reviews/{id}/", "method": "DELETE", "description": "Delete performance review"}
        },
        "oneonone-meetings": {
            "list": {"url": "/api/oneonone-meetings/", "method": "GET", "description": "List all one-on-one meetings"},
            "create": {"url": "/api/oneonone-meetings/", "method": "POST", "description": "Create new one-on-one meeting"},
            "retrieve": {"url": "/api/oneonone-meetings/{id}/", "method": "GET", "description": "Get meeting details"},
            "update": {"url": "/api/oneonone-meetings/{id}/", "method": "PUT", "description": "Update meeting"},
            "destroy": {"url": "/api/oneonone-meetings/{id}/", "method": "DELETE", "description": "Delete meeting"}
        },
        "shoutouts": {
            "list": {"url": "/api/shoutouts/", "method": "GET", "description": "List all shoutouts"},
            "create": {"url": "/api/shoutouts/", "method": "POST", "description": "Create new shoutout"},
            "retrieve": {"url": "/api/shoutouts/{id}/", "method": "GET", "description": "Get shoutout details"},
            "update": {"url": "/api/shoutouts/{id}/", "method": "PUT", "description": "Update shoutout"},
            "destroy": {"url": "/api/shoutouts/{id}/", "method": "DELETE", "description": "Delete shoutout"}
        },
        "learning-modules": {
            "list": {"url": "/api/learning-modules/", "method": "GET", "description": "List all learning modules"},
            "create": {"url": "/api/learning-modules/", "method": "POST", "description": "Create new learning module"},
            "retrieve": {"url": "/api/learning-modules/{id}/", "method": "GET", "description": "Get learning module details"},
            "update": {"url": "/api/learning-modules/{id}/", "method": "PUT", "description": "Update learning module"},
            "destroy": {"url": "/api/learning-modules/{id}/", "method": "DELETE", "description": "Delete learning module"}
        },
        "learning-progress": {
            "list": {"url": "/api/learning-progress/", "method": "GET", "description": "List all learning progress"},
            "create": {"url": "/api/learning-progress/", "method": "POST", "description": "Create new learning progress"},
            "retrieve": {"url": "/api/learning-progress/{id}/", "method": "GET", "description": "Get learning progress details"},
            "update": {"url": "/api/learning-progress/{id}/", "method": "PUT", "description": "Update learning progress"},
            "destroy": {"url": "/api/learning-progress/{id}/", "method": "DELETE", "description": "Delete learning progress"}
        },
        "learning-goals": {
            "list": {"url": "/api/learning-goals/", "method": "GET", "description": "List all learning goals"},
            "create": {"url": "/api/learning-goals/", "method": "POST", "description": "Create new learning goal"},
            "retrieve": {"url": "/api/learning-goals/{id}/", "method": "GET", "description": "Get learning goal details"},
            "update": {"url": "/api/learning-goals/{id}/", "method": "PUT", "description": "Update learning goal"},
            "destroy": {"url": "/api/learning-goals/{id}/", "method": "DELETE", "description": "Delete learning goal"}
        },
        "analytics": {
            "list": {"url": "/api/analytics/", "method": "GET", "description": "Get analytics data"},
        },
        "dashboard": {
            "list": {"url": "/api/dashboard/", "method": "GET", "description": "Get dashboard data"},
        }
    }
    
    endpoints["Performance ViewSets"] = performance_viewsets
    
    return endpoints

def main():
    endpoints = discover_all_endpoints()
    
    # Print summary
    total_endpoints = 0
    for category, items in endpoints.items():
        print(f"\n📋 {category}")
        print("-" * 40)
        
        if category == "Function Views":
            for name, config in items.items():
                methods = config.get('methods', [config.get('method')])
                for method in methods:
                    print(f"   {method} {config['url']} - {config['description']}")
                    total_endpoints += 1
        else:
            for resource, actions in items.items():
                print(f"   📁 {resource}")
                for action, config in actions.items():
                    print(f"      {config['method']} {config['url']} - {config['description']}")
                    total_endpoints += 1
    
    print(f"\n📊 TOTAL ENDPOINTS: {total_endpoints}")
    
    # Save to JSON for Postman generation
    with open('all_endpoints_discovered.json', 'w') as f:
        json.dump(endpoints, f, indent=2)
    
    print(f"\n💾 Endpoints saved to: all_endpoints_discovered.json")
    return endpoints

if __name__ == "__main__":
    main()
