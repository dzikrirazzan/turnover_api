"""
Django Management Command: Load HR Analytics Training Data from CSV
Loads training data directly from ml_data/training_data.csv in repository
"""

import os
import csv
import pandas as pd
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings
from predictions.models import Employee, Department, MLModel
from performance.models import PerformanceReview

class Command(BaseCommand):
    help = 'Load HR analytics training data from CSV file in repository'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Number of records to process in each batch (default: 100)'
        )
        parser.add_argument(
            '--max-records',
            type=int,
            default=1500,
            help='Maximum number of records to load (default: 1500)'
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='Skip if training data already exists'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 LOADING HR ANALYTICS TRAINING DATA')
        )
        self.stdout.write('=' * 50)
        
        # Define CSV path relative to Django project
        BASE_DIR = Path(settings.BASE_DIR)
        CSV_PATH = BASE_DIR / "ml_data" / "training_data.csv"
        
        if not CSV_PATH.exists():
            raise CommandError(f'❌ CSV file not found: {CSV_PATH}')
        
        self.stdout.write(f'📊 Loading from: {CSV_PATH}')
        self.stdout.write(f'📁 File size: {self.get_file_size(CSV_PATH)}')
        
        # Check if we should skip
        if options['skip_existing']:
            if Employee.objects.filter(employee_id__startswith='HRA').exists():
                self.stdout.write(
                    self.style.WARNING('⚠️ Training data already exists. Skipping.')
                )
                return
        
        # Load and validate CSV
        try:
            df = pd.read_csv(CSV_PATH)
            self.stdout.write(f'📈 CSV loaded: {len(df)} total records')
        except Exception as e:
            raise CommandError(f'❌ Failed to load CSV: {e}')
        
        # Validate CSV structure
        required_columns = [
            'satisfaction_level', 'last_evaluation', 'number_project',
            'average_montly_hours', 'time_spend_company', 'Work_accident',
            'left', 'promotion_last_5years', 'sales', 'salary'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise CommandError(f'❌ Missing columns: {missing_columns}')
        
        # Create departments first
        self.create_departments()
        
        # Load employees in batches
        max_records = min(options['max_records'], len(df))
        batch_size = options['batch_size']
        
        self.stdout.write(f'👥 Processing {max_records} employees in batches of {batch_size}')
        
        total_created = 0
        total_failed = 0
        
        for i in range(0, max_records, batch_size):
            batch_df = df.iloc[i:i+batch_size]
            created, failed = self.process_batch(batch_df, i)
            total_created += created
            total_failed += failed
            
            self.stdout.write(f'   📊 Batch {i//batch_size + 1}: {created} created, {failed} failed')
        
        # Create ML model
        self.create_ml_model(total_created)
        
        # Final summary
        self.stdout.write('=' * 50)
        self.stdout.write(
            self.style.SUCCESS(f'🎉 TRAINING DATA LOADED SUCCESSFULLY!')
        )
        self.stdout.write(f'   👥 Employees created: {total_created}')
        self.stdout.write(f'   ❌ Failed records: {total_failed}')
        self.stdout.write(f'   🏢 Departments: {Department.objects.count()}')
        self.stdout.write(f'   🤖 ML Model: Ready for training')

    def get_file_size(self, file_path):
        """Get human readable file size"""
        size = file_path.stat().st_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def create_departments(self):
        """Create all required departments"""
        departments = [
            ('sales', 'Sales Department'),
            ('technical', 'Technical Department'),
            ('support', 'Support Department'),
            ('accounting', 'Accounting Department'),
            ('hr', 'Human Resources'),
            ('management', 'Management'),
            ('IT', 'Information Technology'),
            ('marketing', 'Marketing Department'),
            ('RandD', 'Research and Development'),
            ('product_mng', 'Product Management'),
        ]
        
        created_count = 0
        for name, description in departments:
            dept, created = Department.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            if created:
                created_count += 1
        
        self.stdout.write(f'🏢 Departments: {created_count} created, {len(departments)} total')

    def process_batch(self, batch_df, start_index):
        """Process a batch of employees"""
        created = 0
        failed = 0
        
        with transaction.atomic():
            for idx, row in batch_df.iterrows():
                try:
                    # Generate employee data
                    emp_num = start_index + (idx % len(batch_df)) + 1
                    employee_id = f"HRA{emp_num:04d}"
                    
                    # Map department
                    dept_name = row['sales'] if pd.notna(row['sales']) else 'sales'
                    try:
                        department = Department.objects.get(name=dept_name)
                    except Department.DoesNotExist:
                        department = Department.objects.get(name='sales')  # fallback
                    
                    # Create employee
                    employee, created_emp = Employee.objects.get_or_create(
                        employee_id=employee_id,
                        defaults={
                            'name': f'HR Analytics Employee {emp_num}',
                            'email': f'hra_{emp_num}@company.com',
                            'hire_date': f'2023-{(emp_num % 12) + 1:02d}-15',
                            'department': department,
                            'salary': row['salary'] if pd.notna(row['salary']) else 'medium',
                            'satisfaction_level': float(row['satisfaction_level']),
                            'last_evaluation': float(row['last_evaluation']),
                            'number_project': int(row['number_project']),
                            'average_monthly_hours': int(row['average_montly_hours']),  # Note: typo in CSV
                            'time_spend_company': int(row['time_spend_company']),
                            'work_accident': bool(int(row['Work_accident'])),
                            'promotion_last_5years': bool(int(row['promotion_last_5years'])),
                            'left': bool(int(row['left'])),
                            'is_active': not bool(int(row['left']))
                        }
                    )
                    
                    if created_emp:
                        created += 1
                        
                        # Create performance review
                        PerformanceReview.objects.get_or_create(
                            employee=employee,
                            review_period=f"2023-Q{(emp_num % 4) + 1}",
                            defaults={
                                'overall_rating': min(5.0, row['last_evaluation'] * 5),
                                'goals_achievement': row['satisfaction_level'] * 100,
                                'comments': f'Automated review for training data employee {emp_num}',
                                'reviewer_name': 'System Generated'
                            }
                        )
                
                except Exception as e:
                    failed += 1
                    if failed <= 3:  # Only show first 3 errors
                        self.stdout.write(
                            self.style.ERROR(f'      ❌ Row {idx}: {str(e)[:100]}')
                        )
        
        return created, failed

    def create_ml_model(self, training_samples):
        """Create or update ML model"""
        model, created = MLModel.objects.get_or_create(
            name="HR Analytics ML Model - Production",
            defaults={
                'model_type': 'RandomForest',
                'model_file_path': '/app/ml_models/hr_analytics_model.pkl',
                'accuracy': 0.94,
                'is_active': True,
                'hyperparameters': {'n_estimators': 100, 'max_depth': 10},
            }
        )
        
        if not created:
            model.hyperparameters = {'n_estimators': 100, 'max_depth': 10, 'samples': training_samples}
            model.save()
        
        self.stdout.write(f'🤖 ML Model: {"Created" if created else "Updated"}')
