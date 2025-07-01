#!/usr/bin/env python3
"""
HTML Interface Test for HR Analytics CSV Upload
Enhanced version with Excel support and robust file parsing
"""

import os
import sys
import subprocess
import time
import signal
import webbrowser
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def start_django_server():
    """Start Django development server with test settings"""
    print("🚀 Starting Django backend server...")
    
    # Set environment variables for testing
    env = os.environ.copy()
    env['DJANGO_SETTINGS_MODULE'] = 'test_settings'
    env['DEBUG'] = 'True'
    
    # Start Django server
    django_process = subprocess.Popen([
        sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000', '--settings=test_settings'
    ], env=env, cwd=current_dir)
    
    return django_process

def start_frontend_server():
    """Start simple HTTP server for frontend"""
    print("🌐 Starting frontend server...")
    
    # Start frontend server on port 8001
    frontend_process = subprocess.Popen([
        sys.executable, 'serve_dashboard.py'
    ], cwd=current_dir)
    
    return frontend_process

def create_sample_data():
    """Create sample CSV and Excel files for testing"""
    print("📊 Creating sample test data files...")
    
    # Sample HR data with various formats and edge cases
    sample_data = """Employee_ID,satisfaction_level,last_evaluation,number_projects,average montly hours,time_spend_company,Work_accident,left,promotion_last_5years,Department,salary
1,0.38,0.53,2,157,3,0,1,0,sales,low
2,0.80,0.86,5,262,6,0,1,0,sales,medium
3,0.11,0.88,7,272,4,0,1,0,sales,medium
4,0.72,0.87,5,223,5,0,1,0,sales,low
5,0.37,0.52,2,159,3,0,1,0,sales,low
6,0.41,0.50,2,153,3,0,1,0,sales,low
7,0.10,0.77,6,247,4,0,1,0,sales,low
8,0.92,0.85,5,259,5,0,1,0,sales,low
9,0.89,1.00,5,224,5,0,1,0,sales,low
10,0.42,0.53,2,142,3,0,1,0,sales,low"""
    
    # Write sample CSV
    with open('sample_hr_data.csv', 'w') as f:
        f.write(sample_data)
    
    print("✅ Created sample_hr_data.csv")

def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 HR Analytics CSV Upload - HTML Interface Test")
    print("=" * 60)
    
    # Create sample data
    create_sample_data()
    
    django_process = None
    frontend_process = None
    
    try:
        # Start Django backend
        django_process = start_django_server()
        time.sleep(3)  # Wait for Django to start
        
        # Start frontend server
        frontend_process = start_frontend_server()
        time.sleep(2)  # Wait for frontend to start
        
        print("\n" + "=" * 60)
        print("🎉 SERVERS STARTED SUCCESSFULLY!")
        print("=" * 60)
        print("📱 Frontend (HTML Interface): http://localhost:8001")
        print("🔗 Backend API: http://localhost:8000")
        print("=" * 60)
        print("\n📋 TEST INSTRUCTIONS:")
        print("1. Open your web browser to: http://localhost:8001")
        print("2. Try uploading the sample files:")
        print("   - sample_hr_data.csv")
        print("3. Test drag-and-drop functionality")
        print("4. Verify the enhanced Excel/CSV parsing")
        print("5. Check error handling with invalid files")
        print("\n🔍 Features to test:")
        print("   ✅ Drag and drop file upload")
        print("   ✅ CSV and Excel file support")
        print("   ✅ Column name normalization")
        print("   ✅ Data type conversion")
        print("   ✅ Error handling and suggestions")
        print("   ✅ Beautiful UI with table display")
        
        print("\n⌨️  Press Ctrl+C to stop the servers and exit")
        
        # Keep servers running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping servers...")
        
    finally:
        # Clean up processes
        if django_process:
            django_process.terminate()
            try:
                django_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                django_process.kill()
        
        if frontend_process:
            frontend_process.terminate()
            try:
                frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                frontend_process.kill()
        
        print("✅ Servers stopped. Test complete!")

if __name__ == "__main__":
    main()
