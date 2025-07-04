#!/usr/bin/env python3
"""
Complete Postman Collection Generator untuk SMART-EN Turnover API
Generate comprehensive Postman collection dengan semua endpoints
"""

import json
import uuid
from datetime import datetime

def generate_postman_collection():
    """Generate complete Postman collection"""
    
    # Base collection structure
    collection = {
        "info": {
            "name": "SMART-EN Turnover API - COMPLETE COLLECTION v3.0",
            "description": "Complete API collection untuk SMART-EN Turnover Prediction System\n\n🔧 **CSRF FIXED**: Semua endpoint sudah di-fix untuk Postman\n\n📋 **Features**:\n- Employee Registration & Authentication\n- Department Management\n- Performance Management\n- ML Data Management\n- Complete CRUD Operations\n\n🚀 **Quick Start**:\n1. Set environment variable: base_url = https://turnover-api-hd7ze.ondigitalocean.app\n2. Run 'Register Employee' untuk buat akun\n3. Run 'Login Employee' untuk get token\n4. Token akan auto-saved ke {{token}} variable\n\n⚡ **Pre-request Scripts** sudah include untuk auto-generate data",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
            "_exporter_id": "12345678",
            "_collection_link": "https://turnover-api-collection"
        },
        "event": [
            {
                "listen": "prerequest", 
                "script": {
                    "type": "text/javascript",
                    "exec": [
                        "// Global pre-request script untuk auto-generate data",
                        "if (!pm.globals.get('timestamp')) {",
                        "    pm.globals.set('timestamp', Date.now());",
                        "}",
                        "",
                        "// Auto-generate random data untuk testing",
                        "pm.globals.set('randomEmail', `test.${Date.now()}@smarten.com`);",
                        "pm.globals.set('randomFirstName', ['John', 'Jane', 'Ahmad', 'Siti', 'Budi'][Math.floor(Math.random() * 5)]);",
                        "pm.globals.set('randomLastName', ['Doe', 'Smith', 'Rahman', 'Sari', 'Santoso'][Math.floor(Math.random() * 5)]);",
                        ""
                    ]
                }
            }
        ],
        "variable": [
            {
                "key": "base_url",
                "value": "https://turnover-api-hd7ze.ondigitalocean.app",
                "type": "string"
            },
            {
                "key": "token",
                "value": "",
                "type": "string"
            },
            {
                "key": "user_id",
                "value": "",
                "type": "string"
            },
            {
                "key": "department_id", 
                "value": "1",
                "type": "string"
            }
        ],
        "item": []
    }
    
    # 1. AUTHENTICATION FOLDER
    auth_folder = {
        "name": "🔐 Authentication",
        "item": [
            {
                "name": "Register Employee",
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "exec": [
                                "if (pm.response.code === 201) {",
                                "    const response = pm.response.json();",
                                "    if (response.data && response.data.employee && response.data.employee.token) {",
                                "        pm.collectionVariables.set('token', response.data.employee.token);",
                                "        pm.collectionVariables.set('user_id', response.data.employee.id);",
                                "        console.log('✅ Registration successful! Token saved.');",
                                "    }",
                                "} else if (pm.response.code === 400) {",
                                "    console.log('⚠️ Registration failed - possibly duplicate email');",
                                "}"
                            ]
                        }
                    }
                ],
                "request": {
                    "method": "POST",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Accept", "value": "application/json"}
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "email": "{{randomEmail}}",
                            "password": "SecurePass123!",
                            "password_confirm": "SecurePass123!", 
                            "first_name": "{{randomFirstName}}",
                            "last_name": "{{randomLastName}}",
                            "phone_number": "+6281234567890",
                            "date_of_birth": "1990-05-15",
                            "gender": "M",
                            "marital_status": "single",
                            "education_level": "bachelor",
                            "address": "Jl. Example No. 123, Jakarta",
                            "position": "Software Developer",
                            "department": 1,
                            "hire_date": "2024-01-15",
                            "salary": "monthly",
                            "salary_amount": 10000000
                        }, indent=2)
                    },
                    "url": {
                        "raw": "{{base_url}}/api/register/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "register", ""]
                    }
                }
            },
            {
                "name": "Login Employee", 
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "exec": [
                                "if (pm.response.code === 200) {",
                                "    const response = pm.response.json();",
                                "    if (response.data && response.data.user && response.data.user.token) {",
                                "        pm.collectionVariables.set('token', response.data.user.token);",
                                "        pm.collectionVariables.set('user_id', response.data.user.id);",
                                "        console.log('✅ Login successful! Token saved.');",
                                "    }",
                                "}"
                            ]
                        }
                    }
                ],
                "request": {
                    "method": "POST",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Accept", "value": "application/json"}
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "email": "admin@smarten.com",
                            "password": "admin123"
                        }, indent=2)
                    },
                    "url": {
                        "raw": "{{base_url}}/api/login/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "login", ""]
                    }
                }
            },
            {
                "name": "User Profile",
                "request": {
                    "method": "GET",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "url": {
                        "raw": "{{base_url}}/api/profile/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "profile", ""]
                    }
                }
            },
            {
                "name": "Logout Employee",
                "request": {
                    "method": "POST", 
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "url": {
                        "raw": "{{base_url}}/api/logout/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "logout", ""]
                    }
                }
            }
        ]
    }
    
    # 2. BASIC ENDPOINTS
    basic_folder = {
        "name": "🏠 Basic Endpoints",
        "item": [
            {
                "name": "Health Check",
                "request": {
                    "method": "GET",
                    "header": [{"key": "Content-Type", "value": "application/json"}],
                    "url": {
                        "raw": "{{base_url}}/api/health/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "health", ""]
                    }
                }
            },
            {
                "name": "API Info",
                "request": {
                    "method": "GET",
                    "header": [{"key": "Content-Type", "value": "application/json"}],
                    "url": {
                        "raw": "{{base_url}}/api/info/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "info", ""]
                    }
                }
            }
        ]
    }
    
    # 3. DEPARTMENTS CRUD
    departments_folder = {
        "name": "🏢 Departments CRUD", 
        "item": [
            {
                "name": "List Departments (Public)",
                "request": {
                    "method": "GET",
                    "header": [{"key": "Content-Type", "value": "application/json"}],
                    "url": {
                        "raw": "{{base_url}}/api/departments-list/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "departments-list", ""]
                    }
                }
            },
            {
                "name": "List Departments (Admin)",
                "request": {
                    "method": "GET",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "url": {
                        "raw": "{{base_url}}/api/departments/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "departments", ""]
                    }
                }
            },
            {
                "name": "Create Department",
                "request": {
                    "method": "POST",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "name": "New Department",
                            "description": "Department created via Postman"
                        }, indent=2)
                    },
                    "url": {
                        "raw": "{{base_url}}/api/departments/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "departments", ""]
                    }
                }
            },
            {
                "name": "Get Department Details",
                "request": {
                    "method": "GET",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "url": {
                        "raw": "{{base_url}}/api/departments/{{department_id}}/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "departments", "{{department_id}}", ""]
                    }
                }
            },
            {
                "name": "Update Department",
                "request": {
                    "method": "PUT",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "name": "Updated Department Name",
                            "description": "Updated description"
                        }, indent=2)
                    },
                    "url": {
                        "raw": "{{base_url}}/api/departments/{{department_id}}/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "departments", "{{department_id}}", ""]
                    }
                }
            },
            {
                "name": "Delete Department",
                "request": {
                    "method": "DELETE",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "url": {
                        "raw": "{{base_url}}/api/departments/{{department_id}}/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "departments", "{{department_id}}", ""]
                    }
                }
            },
            {
                "name": "Get Department Employees",
                "request": {
                    "method": "GET",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "url": {
                        "raw": "{{base_url}}/api/departments/{{department_id}}/employees/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "departments", "{{department_id}}", "employees", ""]
                    }
                }
            }
        ]
    }
    
    # 4. EMPLOYEES CRUD
    employees_folder = {
        "name": "👥 Employees CRUD",
        "item": [
            {
                "name": "List All Employees",
                "request": {
                    "method": "GET",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "url": {
                        "raw": "{{base_url}}/api/employees/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "employees", ""]
                    }
                }
            },
            {
                "name": "List Employees (Function)",
                "request": {
                    "method": "GET",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "url": {
                        "raw": "{{base_url}}/api/employees-list/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "employees-list", ""]
                    }
                }
            },
            {
                "name": "Create Employee (Admin)",
                "request": {
                    "method": "POST",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "email": "new.employee@smarten.com",
                            "password": "SecurePass123!",
                            "password_confirm": "SecurePass123!",
                            "first_name": "New",
                            "last_name": "Employee",
                            "phone_number": "+6281234567891",
                            "date_of_birth": "1995-03-20",
                            "gender": "F",
                            "marital_status": "married",
                            "education_level": "master",
                            "address": "Jl. New Address No. 456",
                            "position": "Data Analyst",
                            "department": 1,
                            "hire_date": "2024-02-01",
                            "salary": "monthly",
                            "salary_amount": 12000000
                        }, indent=2)
                    },
                    "url": {
                        "raw": "{{base_url}}/api/employees/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "employees", ""]
                    }
                }
            },
            {
                "name": "Get Employee Details",
                "request": {
                    "method": "GET",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "url": {
                        "raw": "{{base_url}}/api/employees/{{user_id}}/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "employees", "{{user_id}}", ""]
                    }
                }
            },
            {
                "name": "Update Employee",
                "request": {
                    "method": "PUT",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "first_name": "Updated",
                            "last_name": "Name",
                            "position": "Senior Developer",
                            "phone_number": "+6281234567899"
                        }, indent=2)
                    },
                    "url": {
                        "raw": "{{base_url}}/api/employees/{{user_id}}/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "employees", "{{user_id}}", ""]
                    }
                }
            },
            {
                "name": "Employee Statistics",
                "request": {
                    "method": "GET",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "url": {
                        "raw": "{{base_url}}/api/employees/statistics/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "employees", "statistics", ""]
                    }
                }
            }
        ]
    }
    
    # 5. ML PERFORMANCE DATA
    ml_folder = {
        "name": "🤖 ML Performance Data",
        "item": [
            {
                "name": "List Performance Data",
                "request": {
                    "method": "GET",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "url": {
                        "raw": "{{base_url}}/api/performance-data/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "performance-data", ""]
                    }
                }
            },
            {
                "name": "Create Performance Data",
                "request": {
                    "method": "POST",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "employee": "{{user_id}}",
                            "satisfaction_level": 0.75,
                            "last_evaluation": 0.85,
                            "number_project": 3,
                            "average_monthly_hours": 160,
                            "time_spend_company": 2,
                            "work_accident": 0,
                            "promotion_last_5years": 0,
                            "left": 0
                        }, indent=2)
                    },
                    "url": {
                        "raw": "{{base_url}}/api/performance-data/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "performance-data", ""]
                    }
                }
            },
            {
                "name": "Data Separation Stats",
                "request": {
                    "method": "GET",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "url": {
                        "raw": "{{base_url}}/api/data-stats/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "data-stats", ""]
                    }
                }
            }
        ]
    }
    
    # 6. PERFORMANCE MANAGEMENT (from performance app)
    performance_folder = {
        "name": "📊 Performance Management",
        "item": []
    }
    
    # Add performance endpoints
    performance_resources = [
        "goals", "key-results", "feedback", "performance-reviews", 
        "oneonone-meetings", "shoutouts", "learning-modules", 
        "learning-progress", "learning-goals"
    ]
    
    for resource in performance_resources:
        resource_folder = {
            "name": f"📋 {resource.title().replace('-', ' ')}",
            "item": [
                {
                    "name": f"List {resource.title()}",
                    "request": {
                        "method": "GET",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"},
                            {"key": "Authorization", "value": "Token {{token}}"}
                        ],
                        "url": {
                            "raw": f"{{{{base_url}}}}/api/{resource}/",
                            "host": ["{{base_url}}"],
                            "path": ["api", resource, ""]
                        }
                    }
                },
                {
                    "name": f"Create {resource.title()}",
                    "request": {
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"},
                            {"key": "Authorization", "value": "Token {{token}}"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps({
                                "title": f"Sample {resource.title()}",
                                "description": f"Created via Postman for {resource}"
                            }, indent=2)
                        },
                        "url": {
                            "raw": f"{{{{base_url}}}}/api/{resource}/",
                            "host": ["{{base_url}}"],
                            "path": ["api", resource, ""]
                        }
                    }
                }
            ]
        }
        performance_folder["item"].append(resource_folder)
    
    # Add analytics and dashboard
    analytics_folder = {
        "name": "📈 Analytics & Dashboard",
        "item": [
            {
                "name": "Analytics Data",
                "request": {
                    "method": "GET",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "url": {
                        "raw": "{{base_url}}/api/analytics/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "analytics", ""]
                    }
                }
            },
            {
                "name": "Dashboard Data", 
                "request": {
                    "method": "GET",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Token {{token}}"}
                    ],
                    "url": {
                        "raw": "{{base_url}}/api/dashboard/",
                        "host": ["{{base_url}}"],
                        "path": ["api", "dashboard", ""]
                    }
                }
            }
        ]
    }
    
    # Add all folders to collection
    collection["item"] = [
        auth_folder,
        basic_folder,
        departments_folder,
        employees_folder,
        ml_folder,
        performance_folder,
        analytics_folder
    ]
    
    return collection

def main():
    print("🚀 GENERATING COMPLETE POSTMAN COLLECTION")
    print("=" * 60)
    
    collection = generate_postman_collection()
    
    # Save collection
    filename = "SMARTEN_TURNOVER_API_COMPLETE_v3.0.json"
    with open(filename, 'w') as f:
        json.dump(collection, f, indent=2)
    
    print(f"✅ Collection generated: {filename}")
    print(f"📊 Total folders: {len(collection['item'])}")
    
    # Count total requests
    total_requests = 0
    for folder in collection['item']:
        if 'item' in folder:
            for item in folder['item']:
                if 'request' in item:
                    total_requests += 1
                elif 'item' in item:  # Nested folders
                    total_requests += len(item['item'])
    
    print(f"🔗 Total requests: {total_requests}")
    print("\n🎯 HOW TO USE:")
    print("1. Import file ke Postman")
    print("2. Set environment variable: base_url = https://turnover-api-hd7ze.ondigitalocean.app")
    print("3. Run 'Register Employee' untuk buat akun baru")
    print("4. Run 'Login Employee' untuk get authentication token")
    print("5. Token akan auto-saved untuk request selanjutnya")
    print("\n✨ CSRF FIXED - Ready untuk Postman testing!")

if __name__ == "__main__":
    main()
