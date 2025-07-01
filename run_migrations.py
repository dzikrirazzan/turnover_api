#!/usr/bin/env python
"""
Script to run Django migrations and seed data for production deployment.
This can be executed as a one-time job in DigitalOcean.
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Run migrations and seed data."""
    # Add the backend directory to the Python path
    sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), 'backend'))
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.turnover_prediction.settings')
    django.setup()
    
    print("Starting production database setup...")
    
    # Run migrations
    print("1. Applying database migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Seed departments
    print("2. Seeding department data...")
    execute_from_command_line(['manage.py', 'seed_data'])
    
    print("Production database setup completed successfully!")

if __name__ == '__main__':
    main()
