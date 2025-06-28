from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import models
from predictions.models import Department, Employee
import numpy as np
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Seed the database with sample employee data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--employees',
            type=int,
            default=500,
            help='Number of employees to create'
        )

    def handle(self, *args, **options):
        num_employees = options['employees']
        
        self.stdout.write(self.style.SUCCESS(f'Starting to seed {num_employees} employees...'))
        
        # Create departments
        departments_data = [
            ('IT', 'Information Technology'),
            ('Sales', 'Sales Department'),
            ('Marketing', 'Marketing Department'),
            ('HR', 'Human Resources'),
            ('Finance', 'Finance Department'),
            ('Operations', 'Operations Department'),
            ('Support', 'Customer Support'),
            ('R&D', 'Research and Development')
        ]
        
        departments = []
        for name, description in departments_data:
            dept, created = Department.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            departments.append(dept)
            if created:
                self.stdout.write(f'Created department: {name}')
        
        # Create a superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        
        admin_user = User.objects.get(username='admin')
        
        # Generate sample employees
        names = [
            'John Smith', 'Jane Doe', 'Michael Johnson', 'Sarah Williams', 'David Brown',
            'Emily Davis', 'Robert Miller', 'Lisa Wilson', 'William Moore', 'Jennifer Taylor',
            'Christopher Anderson', 'Amanda Thomas', 'Matthew Jackson', 'Jessica White',
            'Anthony Harris', 'Ashley Martin', 'Mark Thompson', 'Michelle Garcia',
            'Steven Martinez', 'Kimberly Robinson', 'Paul Clark', 'Linda Rodriguez',
            'Andrew Lewis', 'Barbara Lee', 'Kenneth Walker', 'Elizabeth Hall',
            'Joshua Allen', 'Helen Young', 'Kevin Hernandez', 'Maria King'
        ]
        
        # Clear existing employees if any
        Employee.objects.all().delete()
        
        employees_created = 0
        
        for i in range(num_employees):
            # Generate employee data with realistic correlations
            np.random.seed(i)  # For reproducible results
            
            # Basic info
            name = random.choice(names) + f" {i+1}"
            employee_id = f"EMP{i+1:04d}"
            email = f"employee{i+1}@company.com"
            department = random.choice(departments)
            
            # Hire date (within last 10 years)
            hire_date = date.today() - timedelta(days=random.randint(30, 3650))
            
            # Generate correlated features
            # Satisfaction level (key predictor according to the article)
            satisfaction = np.random.beta(2, 2)  # Bimodal distribution
            
            # Time in company
            time_company = max(1, int((date.today() - hire_date).days / 365))
            
            # Monthly hours (correlated with satisfaction)
            if satisfaction < 0.3:
                monthly_hours = int(np.random.normal(280, 30))  # Overworked
            elif satisfaction > 0.8:
                monthly_hours = int(np.random.normal(180, 20))  # Normal workload
            else:
                monthly_hours = int(np.random.normal(220, 40))  # Moderate workload
            
            monthly_hours = max(120, min(320, monthly_hours))  # Clamp values
            
            # Number of projects (correlated with hours)
            if monthly_hours > 260:
                num_projects = random.randint(5, 8)
            elif monthly_hours < 160:
                num_projects = random.randint(2, 4)
            else:
                num_projects = random.randint(3, 6)
            
            # Last evaluation
            if satisfaction > 0.7:
                last_eval = np.random.beta(8, 2)  # High performers
            else:
                last_eval = np.random.beta(2, 3)  # Lower performers
            
            # Salary (correlated with department and time)
            if department.name in ['IT', 'Finance']:
                salary_weights = [0.3, 0.5, 0.2]  # Higher salaries
            elif department.name in ['Sales', 'Marketing']:
                salary_weights = [0.4, 0.4, 0.2]
            else:
                salary_weights = [0.5, 0.4, 0.1]  # Lower salaries
            
            salary = np.random.choice(['low', 'medium', 'high'], p=salary_weights)
            
            # Work accident (random, low probability)
            work_accident = random.random() < 0.12
            
            # Promotion (less likely for dissatisfied employees)
            if satisfaction > 0.7 and time_company > 2:
                promotion_prob = 0.3
            elif time_company > 5:
                promotion_prob = 0.4
            else:
                promotion_prob = 0.1
            
            promotion = random.random() < promotion_prob
            
            # Calculate turnover probability based on features
            # Based on insights from the Medium article
            turnover_prob = (
                (1 - satisfaction) * 0.35 +  # Most important factor
                (monthly_hours - 200) / 200 * 0.2 +  # Overwork factor
                (time_company > 6 and not promotion) * 0.15 +  # Stagnation
                (salary == 'low') * 0.1 +  # Low salary
                (last_eval < 0.5) * 0.1 +  # Poor performance
                work_accident * 0.05 +  # Work accident
                np.random.normal(0, 0.05)  # Random noise
            )
            
            turnover_prob = max(0, min(1, turnover_prob))
            left = random.random() < turnover_prob
            
            # Create employee
            employee = Employee.objects.create(
                employee_id=employee_id,
                name=name,
                email=email,
                department=department,
                hire_date=hire_date,
                satisfaction_level=round(satisfaction, 2),
                last_evaluation=round(last_eval, 2),
                number_project=num_projects,
                average_monthly_hours=monthly_hours,
                time_spend_company=time_company,
                work_accident=work_accident,
                promotion_last_5years=promotion,
                salary=salary,
                left=left,
                created_by=admin_user
            )
            
            employees_created += 1
            
            if employees_created % 50 == 0:
                self.stdout.write(f'Created {employees_created} employees...')
        
        # Print statistics
        total_employees = Employee.objects.count()
        total_left = Employee.objects.filter(left=True).count()
        turnover_rate = (total_left / total_employees * 100) if total_employees > 0 else 0
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSeeding completed successfully!\n'
                f'Total employees created: {total_employees}\n'
                f'Employees who left: {total_left}\n'
                f'Turnover rate: {turnover_rate:.1f}%\n'
                f'Average satisfaction: {Employee.objects.aggregate(avg=models.Avg("satisfaction_level"))["avg"]:.2f}\n'
            )
        )
        
        # Department breakdown
        self.stdout.write('\nDepartment breakdown:')
        for dept in departments:
            dept_employees = Employee.objects.filter(department=dept)
            dept_left = dept_employees.filter(left=True).count()
            dept_turnover = (dept_left / dept_employees.count() * 100) if dept_employees.count() > 0 else 0
            
            self.stdout.write(
                f'{dept.name}: {dept_employees.count()} employees, '
                f'{dept_left} left ({dept_turnover:.1f}% turnover)'
            )
