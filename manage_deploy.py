#!/usr/bin/env python3
"""
Deployment-ready Django management script for SMART-EN System
Handles database-free static file collection for DigitalOcean builds
"""

import os
import sys
import django
from pathlib import Path

def main():
    """Run administrative tasks."""
    
    # Add the backend directory to Python path
    backend_dir = Path(__file__).parent / 'backend'
    if backend_dir.exists():
        sys.path.insert(0, str(backend_dir))
        os.chdir(str(backend_dir))
        
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turnover_prediction.settings')
    
    # Special handling for collectstatic during build
    if len(sys.argv) > 1 and sys.argv[1] == 'collectstatic':
        # Set environment variable to indicate we're collecting static files
        os.environ['DJANGO_COLLECTSTATIC'] = '1'
        # Disable database for collectstatic
        os.environ['DATABASE_URL'] = 'sqlite:///tmp/build.db'
        
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
