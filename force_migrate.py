#!/usr/bin/env python
"""
Script to force a migration deployment to DigitalOcean.
This creates a small change to trigger a new deployment and migration.
"""

import os
import sys
from datetime import datetime

# Add backend to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def main():
    """Create a small change to force deployment"""
    
    # Create a deployment timestamp file
    timestamp_file = 'deployment_timestamp.txt'
    
    with open(timestamp_file, 'w') as f:
        f.write(f"Last deployment: {datetime.now().isoformat()}\n")
        f.write("This file is used to force new deployments with fresh migrations.\n")
    
    print(f"✅ Created {timestamp_file} with current timestamp")
    print("📦 Now commit and push this change to trigger a new deployment:")
    print("   git add .")
    print("   git commit -m 'Force migration deployment'")
    print("   git push origin main")
    print("\n🚀 This will trigger the release command which includes:")
    print("   - python run_migrations.py")
    print("   - python backend/manage.py fix_production_db --skip-test")
    
if __name__ == '__main__':
    main()
