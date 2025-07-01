#!/usr/bin/env python3
"""
Setup script for static files - ensures all static directories exist
and creates basic static files if they don't exist.
"""

import os
import sys
from pathlib import Path

def setup_static_files():
    """Create static files structure and basic files"""
    
    # Get the backend directory
    backend_dir = Path(__file__).parent
    static_dir = backend_dir / 'static'
    css_dir = static_dir / 'css'
    js_dir = static_dir / 'js'
    
    # Create directories
    css_dir.mkdir(parents=True, exist_ok=True)
    js_dir.mkdir(parents=True, exist_ok=True)
    
    # Create basic CSS file if it doesn't exist
    admin_css = css_dir / 'admin.css'
    if not admin_css.exists():
        admin_css.write_text('''/* SMART-EN System - Basic CSS */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

.admin-header {
  background-color: #417690;
  color: white;
  padding: 10px;
}

.api-info {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 5px;
  padding: 15px;
  margin: 10px 0;
}

.success {
  color: #28a745;
}

.error {
  color: #dc3545;
}
''')
    
    # Create basic JS file if it doesn't exist
    admin_js = js_dir / 'admin.js'
    if not admin_js.exists():
        admin_js.write_text('''// SMART-EN System - Basic JavaScript
console.log("SMART-EN System Backend - Static files loaded successfully");

// Basic utility functions
window.smartEN = {
  version: "1.0.0",
  apiBase: window.location.origin,

  formatDate: function (date) {
    return new Date(date).toLocaleDateString();
  },

  showMessage: function (message, type = "info") {
    console.log(`[${type.toUpperCase()}] ${message}`);
  },
};

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", function () {
  console.log("SMART-EN System initialized");
});
''')
    
    print(f"✅ Static files setup completed:")
    print(f"   - Static directory: {static_dir}")
    print(f"   - CSS files: {css_dir}")
    print(f"   - JS files: {js_dir}")
    
    return True

if __name__ == "__main__":
    try:
        setup_static_files()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error setting up static files: {e}")
        sys.exit(1)
