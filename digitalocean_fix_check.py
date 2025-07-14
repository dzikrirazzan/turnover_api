#!/usr/bin/env python3
"""
🔧 DigitalOcean Database Fix Script
Check and fix missing table issues for turnover API
"""

import requests
import json

# Test simple endpoint first
BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"

def test_simple_endpoint():
    """Test basic API connectivity"""
    try:
        response = requests.get(f"{BASE_URL}/api/health/")
        print(f"✅ API Health Check: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ API not accessible: {e}")

def test_department_list():
    """Test department listing"""
    try:
        # Login as admin first
        login_data = {
            "email": "admin@company.com",
            "password": "AdminPass123!"
        }
        
        login_response = requests.post(f"{BASE_URL}/api/login/", json=login_data)
        if login_response.status_code == 200:
            token = login_response.json()['data']['user']['token']
            
            headers = {
                "Authorization": f"Token {token}",
                "Content-Type": "application/json"
            }
            
            # Test department list
            dept_response = requests.get(f"{BASE_URL}/api/departments/", headers=headers)
            print(f"✅ Department List: {dept_response.status_code}")
            print(f"Response: {dept_response.text[:200]}...")
            
        else:
            print(f"❌ Login failed: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Department test failed: {e}")

if __name__ == "__main__":
    print("🔧 DigitalOcean Database Fix Check")
    print("=" * 50)
    
    print("\n1. Testing API Health:")
    test_simple_endpoint()
    
    print("\n2. Testing Department Access:")
    test_department_list()
    
    print("\n" + "=" * 50)
    print("🚀 Commands to run in DigitalOcean Console:")
    print("=" * 50)
    print()
    print("1. Check if app is running:")
    print("   sudo systemctl status gunicorn")
    print()
    print("2. Check database tables:")
    print("   cd /var/www/turnover_api")
    print("   python manage.py dbshell")
    print("   SHOW TABLES;")
    print("   \\q")
    print()
    print("3. Run migrations if needed:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
    print()
    print("4. Restart services:")
    print("   sudo systemctl restart gunicorn")
    print("   sudo systemctl restart nginx")
    print()
    print("5. Check logs if problems:")
    print("   sudo journalctl -u gunicorn -f")
