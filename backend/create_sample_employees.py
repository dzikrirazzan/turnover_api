#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# Add the backend directory to the Python path
sys.path.append('/Users/dzikrirazzan/Documents/code/turnover_api/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turnover_prediction.settings')
django.setup()

from predictions.models import Employee, Department
from performance.models import (
    Goal, KeyResult, Feedback, PerformanceReview, OneOnOneMeeting,
    Shoutout, LearningModule, LearningProgress, LearningGoal,
    AnalyticsMetric, DashboardActivity
)
from django.contrib.auth.models import User
from django.utils import timezone

def create_sample_data():
    print("Creating sample data for Smart-en System...")
    
    # Create departments
    departments = [
        ("Engineering", "Software development and technical operations"),
        ("Product", "Product management and design"),
        ("Marketing", "Marketing and communications"),
        ("HR", "Human resources and people operations"),
        ("Sales", "Sales and business development")
    ]
    
    for dept_name, desc in departments:
        dept, created = Department.objects.get_or_create(
            name=dept_name,
            defaults={'description': desc}
        )
        if created:
            print(f"✓ Created department: {dept_name}")
    
    # Create employees that match frontend
    employees_data = [
        {
            'employee_id': 'BD001',
            'name': 'Bravely Dirgayuska',
            'email': 'bravely.dirgayuska@company.com',
            'department': 'Engineering',
            'satisfaction_level': 0.92,
            'last_evaluation': 0.88,
            'number_project': 4,
            'average_monthly_hours': 180,
            'time_spend_company': 3,
            'salary': 'high'
        },
        {
            'employee_id': 'DRA002',
            'name': 'Dzikri Razzan Athallah',
            'email': 'dzikri.athallah@company.com',
            'department': 'Engineering',
            'satisfaction_level': 0.75,
            'last_evaluation': 0.62,
            'number_project': 3,
            'average_monthly_hours': 160,
            'time_spend_company': 2,
            'salary': 'medium'
        },
        {
            'employee_id': 'TS003',
            'name': 'Tasya Salsabila',
            'email': 'tasya.salsabila@company.com',
            'department': 'Engineering',
            'satisfaction_level': 0.89,
            'last_evaluation': 0.91,
            'number_project': 5,
            'average_monthly_hours': 175,
            'time_spend_company': 4,
            'salary': 'high'
        },
        {
            'employee_id': 'A004',
            'name': 'Annisa Azalia Maulana',
            'email': 'annisa.azalia@company.com',
            'department': 'Product',
            'satisfaction_level': 0.68,
            'last_evaluation': 0.59,
            'number_project': 2,
            'average_monthly_hours': 140,
            'time_spend_company': 1,
            'salary': 'medium'
        },
        {
            'employee_id': 'PA005',
            'name': 'Putri Aulia Simanjuntak',
            'email': 'putri.aulia@company.com',
            'department': 'HR',
            'satisfaction_level': 0.81,
            'last_evaluation': 0.83,
            'number_project': 3,
            'average_monthly_hours': 165,
            'time_spend_company': 2,
            'salary': 'medium'
        },
        {
            'employee_id': 'Z006',
            'name': 'Zenith',
            'email': 'zenith@company.com',
            'department': 'Marketing',
            'satisfaction_level': 0.72,
            'last_evaluation': 0.68,
            'number_project': 2,
            'average_monthly_hours': 150,
            'time_spend_company': 1,
            'salary': 'medium'
        }
    ]
    
    for emp_data in employees_data:
        dept = Department.objects.get(name=emp_data['department'])
        emp, created = Employee.objects.get_or_create(
            employee_id=emp_data['employee_id'],
            defaults={
                'name': emp_data['name'],
                'email': emp_data['email'],
                'department': dept,
                'hire_date': timezone.now().date() - timedelta(days=emp_data['time_spend_company']*365),
                'satisfaction_level': emp_data['satisfaction_level'],
                'last_evaluation': emp_data['last_evaluation'],
                'number_project': emp_data['number_project'],
                'average_monthly_hours': emp_data['average_monthly_hours'],
                'time_spend_company': emp_data['time_spend_company'],
                'salary': emp_data['salary'],
                'work_accident': False,
                'promotion_last_5years': False,
                'left': False
            }
        )
        if created:
            print(f"✓ Created employee: {emp_data['name']}")
    
    print("✓ Sample data created successfully!")
    print("You can now test the APIs with employee IDs 1-6")

if __name__ == '__main__':
    create_sample_data()
