#!/usr/bin/env python3
"""
Simple HTTP server to serve the HR dashboard locally.
This avoids CORS issues that occur when opening HTML files directly in browser.
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

# Configuration
PORT = 8080
DASHBOARD_FILE = "frontend_hr_dashboard.html"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow requests to external APIs
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def main():
    # Change to the directory containing this script
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if dashboard file exists
    if not Path(DASHBOARD_FILE).exists():
        print(f"Error: {DASHBOARD_FILE} not found in {script_dir}")
        print("Please make sure you're running this script from the correct directory.")
        sys.exit(1)
    
    # Start the server
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"🚀 Starting HR Dashboard server...")
            print(f"📁 Serving files from: {script_dir}")
            print(f"🌐 Dashboard URL: http://localhost:{PORT}/{DASHBOARD_FILE}")
            print(f"🔗 Direct link: http://localhost:{PORT}/{DASHBOARD_FILE}")
            print("\n" + "="*60)
            print("INSTRUCTIONS:")
            print("1. The dashboard will open automatically in your browser")
            print("2. Use these credentials to login:")
            print("   Username: admin")
            print("   Password: newstrongpassword123")
            print("3. Upload a CSV file or use the template download")
            print("4. Press Ctrl+C to stop the server")
            print("="*60 + "\n")
            
            # Open browser automatically
            dashboard_url = f"http://localhost:{PORT}/{DASHBOARD_FILE}"
            print(f"🔄 Opening {dashboard_url} in your default browser...")
            webbrowser.open(dashboard_url)
            
            print(f"✅ Server running on port {PORT}")
            print("Waiting for connections...")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use. Try a different port or stop the existing server.")
            print(f"You can try running: lsof -ti:{PORT} | xargs kill")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
