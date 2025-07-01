#!/usr/bin/env python
"""
Script to fix the production database by running migrations and seeding data.
Run this on your DigitalOcean app to fix the registration field issues.
"""
import os
import sys
import django
import requests
import json
from django.core.management import execute_from_command_line
from django.db import connection

def check_database_connection():
    """Check if we can connect to the database."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_migrations_status():
    """Check which migrations are applied."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES LIKE 'django_migrations'")
            if not cursor.fetchone():
                print("❌ Django migrations table doesn't exist")
                return False
            
            cursor.execute("SELECT app, name FROM django_migrations WHERE app = 'predictions'")
            migrations = cursor.fetchall()
            print(f"✅ Applied migrations: {migrations}")
            return True
    except Exception as e:
        print(f"❌ Error checking migrations: {e}")
        return False

def check_employee_table_schema():
    """Check if the Employee table has the password field."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("DESCRIBE predictions_employee")
            columns = [row[0] for row in cursor.fetchall()]
            print(f"📋 Employee table columns: {columns}")
            
            if 'password' in columns:
                print("✅ Password field exists in Employee table")
                return True
            else:
                print("❌ Password field missing from Employee table")
                return False
    except Exception as e:
        print(f"❌ Error checking Employee table: {e}")
        return False

def test_registration_endpoint():
    """Test the registration endpoint."""
    try:
        url = "https://turnover-api-hd7ze.ondigitalocean.app/api/auth/register/"
        test_data = {
            "email": "test_fix@example.com",
            "first_name": "Test",
            "last_name": "Fix",
            "employee_id": "EMP_FIX_001",
            "phone_number": "08123456789",
            "password": "testpassword123",
            "password_confirm": "testpassword123"
        }
        
        response = requests.post(url, json=test_data)
        print(f"🧪 Registration test status: {response.status_code}")
        print(f"🧪 Registration test response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration endpoint working!")
            return True
        else:
            print("❌ Registration endpoint still broken")
            return False
    except Exception as e:
        print(f"❌ Error testing registration: {e}")
        return False

def main():
    """Main function to fix the production database."""
    print("🚀 Starting production database fix...")
    print("=" * 50)
    
    # Setup Django environment
    sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), 'backend'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.turnover_prediction.settings')
    django.setup()
    
    # Step 1: Check database connection
    print("\n📡 Step 1: Checking database connection...")
    if not check_database_connection():
        return
    
    # Step 2: Check current migrations status
    print("\n📋 Step 2: Checking migrations status...")
    check_migrations_status()
    
    # Step 3: Check Employee table schema
    print("\n🔍 Step 3: Checking Employee table schema...")
    schema_ok = check_employee_table_schema()
    
    # Step 4: Run migrations if needed
    if not schema_ok:
        print("\n🔧 Step 4: Applying database migrations...")
        try:
            execute_from_command_line(['manage.py', 'migrate'])
            print("✅ Migrations applied successfully!")
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return
    else:
        print("\n✅ Step 4: Database schema looks good, skipping migrations")
    
    # Step 5: Seed department data
    print("\n🌱 Step 5: Seeding department data...")
    try:
        execute_from_command_line(['manage.py', 'seed_data'])
        print("✅ Department data seeded successfully!")
    except Exception as e:
        print(f"⚠️ Seeding failed (might already exist): {e}")
    
    # Step 6: Verify Employee table schema again
    print("\n🔍 Step 6: Verifying Employee table schema...")
    check_employee_table_schema()
    
    # Step 7: Test registration endpoint
    print("\n🧪 Step 7: Testing registration endpoint...")
    test_registration_endpoint()
    
    print("\n" + "=" * 50)
    print("🎉 Production database fix completed!")
    print("📧 You can now test registration at:")
    print("   https://turnover-api-hd7ze.ondigitalocean.app/api/auth/register/")

if __name__ == '__main__':
    main()
