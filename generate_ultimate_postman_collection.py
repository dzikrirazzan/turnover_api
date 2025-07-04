#!/usr/bin/env python3
"""
Ultimate Postman Collection Generator
Membuat collection lengkap untuk semua API endpoints dengan test cases dan environments
"""

import json
import uuid
from datetime import datetime

def generate_uuid():
    """Generate UUID untuk Postman collection"""
    return str(uuid.uuid4())

def create_postman_collection():
    """Membuat Postman collection lengkap untuk SMART-EN Turnover API"""
    
    # Base URL production
    BASE_URL = "{{base_url}}"
    
    collection = {
        "info": {
            "_postman_id": generate_uuid(),
            "name": "SMART-EN Turnover API - Complete Collection",
            "description": "🚀 Complete API collection for SMART-EN Turnover Prediction System\n\n**Features:**\n- Employee Registration & Authentication\n- Department Management (CRUD)\n- Employee Management (CRUD)\n- Performance Data Management\n- Role-based Access Control\n- ML Prediction Endpoints\n\n**Setup:**\n1. Set environment variable `base_url` to your API URL\n2. Set environment variable `auth_token` after login\n3. Use the Login endpoint to get your token\n\n**CSRF/CORS:** Fully disabled for API testing convenience!",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
            "_exporter_id": "12345678"
        },
        "item": [],
        "variable": [
            {
                "key": "base_url",
                "value": "https://turnover-api-hd7ze.ondigitalocean.app",
                "type": "string"
            },
            {
                "key": "auth_token",
                "value": "",
                "type": "string"
            }
        ]
    }
    
    # 1. Health & Info Endpoints
    health_folder = {
        "name": "📊 Health & System Info",
        "item": [
            {
                "name": "Health Check",
                "request": {
                    "method": "GET",
                    "header": [],
                    "url": {
                        "raw": f"{BASE_URL}/api/health/",
                        "host": [f"{BASE_URL}"],
                        "path": ["api", "health", ""]
                    }
                },
                "response": []
            },
            {
                "name": "API Info",
                "request": {
                    "method": "GET", 
                    "header": [],
                    "url": {
                        "raw": f"{BASE_URL}/api/info/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "info", ""]
                    }
                },
                "response": []
            }
        ]
    }
    
    # 2. Authentication Endpoints
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
                                "        pm.environment.set('auth_token', response.data.employee.token);",
                                "        console.log('Token saved:', response.data.employee.token.substring(0, 20) + '...');",
                                "    }",
                                "}"
                            ]
                        }
                    }
                ],
                "request": {
                    "method": "POST",
                    "header": [
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        }
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "email": "john.doe@smarten.com",
                            "password": "SecurePass123!",
                            "password_confirm": "SecurePass123!",
                            "first_name": "John",
                            "last_name": "Doe",
                            "phone_number": "+6281234567890",
                            "date_of_birth": "1990-05-15",
                            "gender": "M",
                            "marital_status": "single",
                            "education_level": "bachelor",
                            "address": "Jl. Example No. 123, Jakarta",
                            "position": "Software Developer",
                            "department": 1,
                            "hire_date": "2024-01-15",
                            "salary": "middle",
                            "salary_amount": 8000000
                        }, indent=2)
                    },
                    "url": {
                        "raw": f"{BASE_URL}/api/register/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "register", ""]
                    }
                },
                "response": []
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
                                "        pm.environment.set('auth_token', response.data.user.token);",
                                "        console.log('Token saved:', response.data.user.token.substring(0, 20) + '...');",
                                "    }",
                                "}"
                            ]
                        }
                    }
                ],
                "request": {
                    "method": "POST",
                    "header": [
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        }
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "email": "john.doe@smarten.com",
                            "password": "SecurePass123!"
                        }, indent=2)
                    },
                    "url": {
                        "raw": f"{BASE_URL}/api/login/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "login", ""]
                    }
                },
                "response": []
            },
            {
                "name": "Logout Employee",
                "request": {
                    "method": "POST",
                    "header": [
                        {
                            "key": "Authorization",
                            "value": "Token {{auth_token}}"
                        }
                    ],
                    "url": {
                        "raw": f"{BASE_URL}/api/logout/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "logout", ""]
                    }
                },
                "response": []
            },
            {
                "name": "User Profile",
                "request": {
                    "method": "GET",
                    "header": [
                        {
                            "key": "Authorization",
                            "value": "Token {{auth_token}}"
                        }
                    ],
                    "url": {
                        "raw": f"{BASE_URL}/api/profile/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "profile", ""]
                    }
                },
                "response": []
            }
        ]
    }
    
    # 3. Department Management (CRUD)
    department_folder = {
        "name": "🏢 Department Management",
        "item": [
            {
                "name": "List All Departments",
                "request": {
                    "method": "GET",
                    "header": [],
                    "url": {
                        "raw": f"{BASE_URL}/api/departments/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "departments", ""]
                    }
                },
                "response": []
            },
            {
                "name": "Get Department by ID",
                "request": {
                    "method": "GET",
                    "header": [
                        {
                            "key": "Authorization",
                            "value": "Token {{auth_token}}"
                        }
                    ],
                    "url": {
                        "raw": f"{BASE_URL}/api/departments/1/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "departments", "1", ""]
                    }
                },
                "response": []
            },
            {
                "name": "Create Department (Admin Only)",
                "request": {
                    "method": "POST",
                    "header": [
                        {
                            "key": "Authorization",
                            "value": "Token {{auth_token}}"
                        },
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        }
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "name": "New Department",
                            "description": "Description of the new department"
                        }, indent=2)
                    },
                    "url": {
                        "raw": f"{BASE_URL}/api/departments/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "departments", ""]
                    }
                },
                "response": []
            },
            {
                "name": "Update Department (Admin Only)",
                "request": {
                    "method": "PUT",
                    "header": [
                        {
                            "key": "Authorization",
                            "value": "Token {{auth_token}}"
                        },
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        }
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "name": "Updated Department Name",
                            "description": "Updated description"
                        }, indent=2)
                    },
                    "url": {
                        "raw": f"{BASE_URL}/api/departments/1/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "departments", "1", ""]
                    }
                },
                "response": []
            },
            {
                "name": "Delete Department (Admin Only)",
                "request": {
                    "method": "DELETE",
                    "header": [
                        {
                            "key": "Authorization",
                            "value": "Token {{auth_token}}"
                        }
                    ],
                    "url": {
                        "raw": f"{BASE_URL}/api/departments/1/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "departments", "1", ""]
                    }
                },
                "response": []
            },
            {
                "name": "Get Department Employees",
                "request": {
                    "method": "GET",
                    "header": [
                        {
                            "key": "Authorization",
                            "value": "Token {{auth_token}}"
                        }
                    ],
                    "url": {
                        "raw": f"{BASE_URL}/api/departments/1/employees/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "departments", "1", "employees", ""]
                    }
                },
                "response": []
            }
        ]
    }
    
    # 4. Employee Management (CRUD)
    employee_folder = {
        "name": "👥 Employee Management",
        "item": [
            {
                "name": "List All Employees (Admin Only)",
                "request": {
                    "method": "GET",
                    "header": [
                        {
                            "key": "Authorization",
                            "value": "Token {{auth_token}}"
                        }
                    ],
                    "url": {
                        "raw": f"{BASE_URL}/api/employees/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "employees", ""]
                    }
                },
                "response": []
            },
            {
                "name": "Get Employee by ID (Admin Only)",
                "request": {
                    "method": "GET",
                    "header": [
                        {
                            "key": "Authorization",
                            "value": "Token {{auth_token}}"
                        }
                    ],
                    "url": {
                        "raw": f"{BASE_URL}/api/employees/1/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "employees", "1", ""]
                    }
                },
                "response": []
            },
            {
                "name": "Update Employee (Admin Only)",
                "request": {
                    "method": "PUT",
                    "header": [
                        {
                            "key": "Authorization",
                            "value": "Token {{auth_token}}"
                        },
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        }
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "first_name": "Updated",
                            "last_name": "Name",
                            "position": "Updated Position",
                            "role": "employee"
                        }, indent=2)
                    },
                    "url": {
                        "raw": f"{BASE_URL}/api/employees/1/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "employees", "1", ""]
                    }
                },
                "response": []
            },
            {
                "name": "Delete Employee (Admin Only)",
                "request": {
                    "method": "DELETE",
                    "header": [
                        {
                            "key": "Authorization",
                            "value": "Token {{auth_token}}"
                        }
                    ],
                    "url": {
                        "raw": f"{BASE_URL}/api/employees/1/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "employees", "1", ""]
                    }
                },
                "response": []
            },
            {
                "name": "Employee Statistics (Admin Only)",
                "request": {
                    "method": "GET",
                    "header": [
                        {
                            "key": "Authorization",
                            "value": "Token {{auth_token}}"
                        }
                    ],
                    "url": {
                        "raw": f"{BASE_URL}/api/employees/statistics/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "employees", "statistics", ""]
                    }
                },
                "response": []
            }
        ]
    }
    
    # 5. Performance Data Management
    performance_folder = {
        "name": "📈 Performance Data (ML)",
        "item": [
            {
                "name": "List Performance Data (Admin Only)",
                "request": {
                    "method": "GET",
                    "header": [
                        {
                            "key": "Authorization",
                            "value": "Token {{auth_token}}"
                        }
                    ],
                    "url": {
                        "raw": f"{BASE_URL}/api/performance-data/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "performance-data", ""]
                    }
                },
                "response": []
            },
            {
                "name": "Create Performance Data (Admin Only)",
                "request": {
                    "method": "POST",
                    "header": [
                        {
                            "key": "Authorization",
                            "value": "Token {{auth_token}}"
                        },
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        }
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "employee": 1,
                            "satisfaction_level": 0.75,
                            "last_evaluation": 0.85,
                            "number_project": 3,
                            "average_monthly_hours": 180,
                            "time_spend_company": 2,
                            "work_accident": 0,
                            "promotion_last_5years": 0,
                            "left": 0
                        }, indent=2)
                    },
                    "url": {
                        "raw": f"{BASE_URL}/api/performance-data/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "performance-data", ""]
                    }
                },
                "response": []
            }
        ]
    }
    
    # 6. Additional API Endpoints
    additional_folder = {
        "name": "🔧 Additional Endpoints",
        "item": [
            {
                "name": "List Employees (Public)",
                "request": {
                    "method": "GET",
                    "header": [],
                    "url": {
                        "raw": f"{BASE_URL}/api/list-employees/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "list-employees", ""]
                    }
                },
                "response": []
            },
            {
                "name": "List Departments (Public)",
                "request": {
                    "method": "GET",
                    "header": [],
                    "url": {
                        "raw": f"{BASE_URL}/api/list-departments/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "list-departments", ""]
                    }
                },
                "response": []
            },
            {
                "name": "Data Separation Stats",
                "request": {
                    "method": "GET",
                    "header": [
                        {
                            "key": "Authorization",
                            "value": "Token {{auth_token}}"
                        }
                    ],
                    "url": {
                        "raw": f"{BASE_URL}/api/data-separation-stats/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "data-separation-stats", ""]
                    }
                },
                "response": []
            }
        ]
    }
    
    # 7. Test Cases
    test_folder = {
        "name": "🧪 Test Cases & Examples",
        "item": [
            {
                "name": "Test CSRF Bypass",
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "exec": [
                                "pm.test('CSRF should be bypassed', function () {",
                                "    pm.expect(pm.response.code).to.not.equal(403);",
                                "});",
                                "",
                                "pm.test('No CSRF error in response', function () {",
                                "    const responseText = pm.response.text();",
                                "    pm.expect(responseText).to.not.include('CSRF');",
                                "});"
                            ]
                        }
                    }
                ],
                "request": {
                    "method": "POST",
                    "header": [
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        },
                        {
                            "key": "User-Agent",
                            "value": "PostmanRuntime/7.29.2"
                        }
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "email": "test.csrf@example.com",
                            "password": "TestPass123!",
                            "password_confirm": "TestPass123!",
                            "first_name": "CSRF",
                            "last_name": "Test",
                            "department": 1
                        }, indent=2)
                    },
                    "url": {
                        "raw": f"{BASE_URL}/api/register/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "register", ""]
                    }
                },
                "response": []
            },
            {
                "name": "Test CORS Headers",
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "exec": [
                                "pm.test('CORS headers should be present', function () {",
                                "    pm.expect(pm.response.headers.has('Access-Control-Allow-Origin')).to.be.true;",
                                "});"
                            ]
                        }
                    }
                ],
                "request": {
                    "method": "OPTIONS",
                    "header": [
                        {
                            "key": "Origin",
                            "value": "https://web.postman.co"
                        },
                        {
                            "key": "Access-Control-Request-Method",
                            "value": "POST"
                        }
                    ],
                    "url": {
                        "raw": f"{BASE_URL}/api/register/",
                        "host": [BASE_URL.replace("{{", "").replace("}}", "")],
                        "path": ["api", "register", ""]
                    }
                },
                "response": []
            }
        ]
    }
    
    # Add all folders to collection
    collection["item"] = [
        health_folder,
        auth_folder,
        department_folder,
        employee_folder,
        performance_folder,
        additional_folder,
        test_folder
    ]
    
    return collection

def create_environment():
    """Create Postman environment"""
    return {
        "id": generate_uuid(),
        "name": "SMART-EN Turnover API - Environments",
        "values": [
            {
                "key": "base_url",
                "value": "https://turnover-api-hd7ze.ondigitalocean.app",
                "description": "Production API URL",
                "enabled": True
            },
            {
                "key": "base_url_local",
                "value": "http://127.0.0.1:8000",
                "description": "Local development URL",
                "enabled": False
            },
            {
                "key": "auth_token",
                "value": "",
                "description": "Authentication token (auto-filled after login)",
                "enabled": True
            }
        ],
        "_postman_variable_scope": "environment"
    }

def main():
    """Generate and save complete Postman collection"""
    print("🚀 Generating Ultimate Postman Collection...")
    
    # Generate collection
    collection = create_postman_collection()
    environment = create_environment()
    
    # Save collection
    collection_filename = "SMART_EN_API_ULTIMATE_COLLECTION.json"
    with open(collection_filename, 'w', encoding='utf-8') as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)
    
    # Save environment  
    env_filename = "SMART_EN_API_ENVIRONMENT.json"
    with open(env_filename, 'w', encoding='utf-8') as f:
        json.dump(environment, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Collection saved: {collection_filename}")
    print(f"✅ Environment saved: {env_filename}")
    print("\n📋 POSTMAN IMPORT INSTRUCTIONS:")
    print("1. Open Postman")
    print("2. Click 'Import' button")
    print(f"3. Select and import: {collection_filename}")
    print(f"4. Select and import: {env_filename}")
    print("5. Select the imported environment in top-right dropdown")
    print("6. Start testing! 🎉")
    
    print("\n🔥 FEATURES INCLUDED:")
    print("- ✅ All CSRF protection disabled")
    print("- ✅ CORS fully configured")
    print("- ✅ Auto token management")
    print("- ✅ Complete CRUD operations")
    print("- ✅ Test scripts included")
    print("- ✅ Example data provided")
    print("- ✅ Environment variables setup")
    
    # Count endpoints
    total_endpoints = 0
    for folder in collection["item"]:
        total_endpoints += len(folder["item"])
    
    print(f"\n📊 COLLECTION STATS:")
    print(f"- Total Endpoints: {total_endpoints}")
    print(f"- Total Folders: {len(collection['item'])}")
    print(f"- Environment Variables: {len(environment['values'])}")

if __name__ == "__main__":
    main()
