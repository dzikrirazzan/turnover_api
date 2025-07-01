#!/usr/bin/env python3
"""
Auto Load Training Data Script
Automatically loads HR analytics training data from repository CSV
Called during deployment or when production needs training data
"""

import os
import sys
import django
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turnover_prediction.settings')
django.setup()

from django.core.management import call_command
from django.db import connection
from predictions.models import Employee

def main():
    print("🚀 AUTO-LOADING HR ANALYTICS TRAINING DATA")
    print("=" * 50)
    
    # Check if sufficient training data exists
    existing_count = Employee.objects.filter(employee_id__startswith='HRA').count()
    
    if existing_count >= 10000:  # Need at least 10k samples for best ML accuracy
        print(f"📊 Found {existing_count} existing training employees")
        print("✅ Sufficient training data already exists")
        return
    
    print(f"📈 Only {existing_count} training employees found. Loading all 15k records...")
    print("🚀 Loading ALL training data from CSV for maximum ML accuracy...")
    
    print("📈 No training data found. Loading from CSV...")
    
    try:
        # Load training data
        call_command(
            'load_training_data',
            batch_size=200,
            max_records=15000,  # Load all data
            skip_existing=False,  # Force reload for complete dataset
            verbosity=2
        )
        
        # Verify load
        final_count = Employee.objects.filter(employee_id__startswith='HRA').count()
        total_employees = Employee.objects.count()
        
        print("\n🎉 SUCCESS! Training data loaded")
        print(f"   📊 Training employees: {final_count}")
        print(f"   👥 Total employees: {total_employees}")
        print(f"   🎯 Ready for ML training!")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()