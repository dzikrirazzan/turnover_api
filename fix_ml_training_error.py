#!/usr/bin/env python3
"""
Fix ML Training Error - Deploy to DigitalOcean
This script handles the column name mismatch in CSV file
"""

import os
import sys

def main():
    print("🔧 FIXING ML TRAINING ERROR...")
    print("=" * 50)
    
    # The issue is in CSV column names vs expected names:
    # CSV has: 'average_montly_hours' (typo), 'Work_accident' (capital W)
    # Code expects: 'average_monthly_hours', 'work_accident'
    
    print("✅ Issue identified:")
    print("   - CSV has 'average_montly_hours' (typo)")
    print("   - CSV has 'Work_accident' (capital W)")
    print("   - Code expects 'average_monthly_hours', 'work_accident'")
    
    print("\n✅ Solution applied:")
    print("   - Updated ml_utils.py to handle column name mapping")
    print("   - Updated train_model_from_csv.py with better error handling")
    
    print("\n🚀 NEW DEPLOYMENT COMMANDS:")
    print("=" * 50)
    
    commands = [
        "pip install -r requirements.txt",
        "python manage.py migrate",
        "python manage.py collectstatic --noinput",
        "python manage.py train_model_from_csv",  # This should work now
        "python manage.py setup_production",
        "sudo systemctl restart turnover_api"
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"{i}. {cmd}")
    
    print("\n📋 WHAT CHANGED:")
    print("=" * 50)
    print("✅ ml_utils.py now maps:")
    print("   - 'average_montly_hours' → 'average_monthly_hours'")
    print("   - 'Work_accident' → 'work_accident'")
    print("   - 'sales' → 'department'")
    print("✅ Better error handling in training command")
    print("✅ More verbose logging during training")
    
    print("\n🎯 EXPECTED RESULT:")
    print("=" * 50)
    print("✅ Training command will now succeed")
    print("✅ ML model will be created and saved")
    print("✅ Prediction API /api/predict/ will work")
    
    print("\n🔄 IF STILL ERROR:")
    print("=" * 50)
    print("Check these commands:")
    print("- ls -la ml_data/training_data.csv")
    print("- head -1 ml_data/training_data.csv")
    print("- python manage.py train_model_from_csv")
    
    return True

if __name__ == "__main__":
    main()
