#!/usr/bin/env python
"""
Load HR Analytics CSV data into the Django database
"""
import os
import sys
import django
import pandas as pd
from datetime import date, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turnover_prediction.settings')
django.setup()

from predictions.models import Employee, Department

def load_csv_data():
    """Load data from hr_analytics.csv into the database"""
    
    # Read CSV file
    csv_path = 'hr_analytics.csv'
    print(f"📊 Loading data from {csv_path}...")
    
    try:
        df = pd.read_csv(csv_path)
        print(f"✅ CSV loaded successfully! Shape: {df.shape}")
        
        # Print column names for verification
        print(f"📋 Columns: {list(df.columns)}")
        
        # Map department names (CSV uses different names)
        department_mapping = {
            'sales': 'Sales',
            'accounting': 'Accounting', 
            'hr': 'Human Resources',
            'technical': 'Technical',
            'support': 'Support',
            'management': 'Management',
            'IT': 'Information Technology',
            'product_mng': 'Product Management',
            'marketing': 'Marketing',
            'RandD': 'Research & Development'
        }
        
        # Create departments first
        print("🏢 Creating departments...")
        departments = {}
        for csv_dept, display_name in department_mapping.items():
            dept, created = Department.objects.get_or_create(
                name=display_name,
                defaults={'description': f'{display_name} Department'}
            )
            departments[csv_dept] = dept
            if created:
                print(f"  ✅ Created: {display_name}")
        
        # Clear existing employees (optional)
        print("🗑️  Clearing existing employees...")
        Employee.objects.all().delete()
        
        # Load employees from CSV
        print("👥 Loading employees from CSV...")
        employees_created = 0
        
        for index, row in df.iterrows():
            try:
                # Map salary to model choices (model expects string values: 'low', 'medium', 'high')
                salary_value = row['salary']  # CSV already contains 'low', 'medium', 'high'
                
                # Get department
                dept_name = row['sales']  # CSV column is named 'sales' but contains dept names
                department = departments.get(dept_name)
                
                if not department:
                    print(f"⚠️  Unknown department: {dept_name}, skipping row {index}")
                    continue
                
                # Calculate hire_date based on time_spend_company
                # Use a reference date (e.g., end of 2023) and subtract time spent
                reference_date = date(2023, 12, 31)
                years_at_company = int(row['time_spend_company'])
                # Add some random days (0-364) to make hire dates more realistic
                random_days = random.randint(0, 364)
                hire_date = reference_date - timedelta(days=(years_at_company * 365) + random_days)
                
                # Create employee
                employee = Employee.objects.create(
                    employee_id=f"EMP_{index + 1:04d}",
                    name=f"Employee_{index + 1:04d}",
                    email=f"employee{index + 1:04d}@company.com",
                    hire_date=hire_date,
                    satisfaction_level=row['satisfaction_level'],
                    last_evaluation=row['last_evaluation'],
                    number_project=row['number_project'],
                    average_monthly_hours=row['average_montly_hours'],  # Note: CSV has typo 'montly'
                    time_spend_company=row['time_spend_company'],
                    work_accident=bool(row['Work_accident']),
                    left=bool(row['left']),
                    promotion_last_5years=bool(row['promotion_last_5years']),
                    department=department,
                    salary=salary_value
                )
                
                employees_created += 1
                
                if employees_created % 1000 == 0:
                    print(f"  📈 Created {employees_created} employees...")
                    
            except Exception as e:
                print(f"❌ Error creating employee at row {index}: {e}")
                continue
        
        print(f"🎉 Successfully loaded {employees_created} employees from CSV!")
        
        # Print summary statistics
        print("\n📊 DATA SUMMARY:")
        print(f"Total Employees: {Employee.objects.count()}")
        print(f"Employees who left: {Employee.objects.filter(left=True).count()}")
        print(f"Turnover rate: {Employee.objects.filter(left=True).count() / Employee.objects.count() * 100:.1f}%")
        
        print("\n🏢 DEPARTMENT BREAKDOWN:")
        for dept in Department.objects.all():
            total = Employee.objects.filter(department=dept).count()
            left = Employee.objects.filter(department=dept, left=True).count()
            if total > 0:
                rate = left / total * 100
                print(f"  {dept.name}: {total} employees, {left} left ({rate:.1f}% turnover)")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ CSV file not found: {csv_path}")
        print("   Make sure hr_analytics.csv is in the same directory as this script")
        return False
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return False

if __name__ == '__main__':
    print("🚀 HR Analytics CSV Data Loader")
    print("=" * 50)
    
    success = load_csv_data()
    
    if success:
        print("\n✅ Data loading completed successfully!")
        print("\n🔥 Next steps:")
        print("   1. Run: python manage.py train_model --model-name csv_model_v1")
        print("   2. Test API: python test_api.py")
        print("   3. Start server: python manage.py runserver")
    else:
        print("\n❌ Data loading failed!")
        sys.exit(1)
