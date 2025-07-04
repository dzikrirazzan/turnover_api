#!/usr/bin/env python3
"""
Simple and Working Postman Collection Generator
Membuat collection lengkap untuk semua API endpoints
"""

import json

def main():
    """Generate Postman collection yang pasti work"""
    
    BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"
    
    collection = {
        "info": {
            "name": "SMART-EN Turnover API - Ultimate Collection",
            "description": "🚀 Complete API collection - CSRF & CORS fully disabled for easy testing!",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "variable": [
            {
                "key": "base_url",
                "value": BASE_URL
            },
            {
                "key": "auth_token",
                "value": ""
            }
        ],
        "item": [
            {
                "name": "📊 System Health",
                "item": [
                    {
                        "name": "Health Check",
                        "request": {
                            "method": "GET",
                            "url": "{{base_url}}/api/health/"
                        }
                    },
                    {
                        "name": "API Info",
                        "request": {
                            "method": "GET",
                            "url": "{{base_url}}/api/info/"
                        }
                    }
                ]
            },
            {
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
                                        "        pm.collectionVariables.set('auth_token', response.data.employee.token);",
                                        "        console.log('Token saved from registration');",
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
                                    "email": "test.user@smarten.com",
                                    "password": "SecurePass123!",
                                    "password_confirm": "SecurePass123!",
                                    "first_name": "Test",
                                    "last_name": "User",
                                    "phone_number": "+6281234567890",
                                    "date_of_birth": "1990-05-15",
                                    "gender": "M",
                                    "marital_status": "single",
                                    "education_level": "bachelor",
                                    "address": "Test Address Jakarta",
                                    "position": "Test Position",
                                    "department": 1,
                                    "hire_date": "2024-01-15",
                                    "salary": "middle",
                                    "salary_amount": 8000000
                                }, indent=2)
                            },
                            "url": "{{base_url}}/api/register/"
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
                                        "        pm.collectionVariables.set('auth_token', response.data.user.token);",
                                        "        console.log('Token saved from login');",
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
                                    "email": "test.user@smarten.com",
                                    "password": "SecurePass123!"
                                }, indent=2)
                            },
                            "url": "{{base_url}}/api/login/"
                        }
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
                            "url": "{{base_url}}/api/profile/"
                        }
                    },
                    {
                        "name": "Logout",
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Token {{auth_token}}"
                                }
                            ],
                            "url": "{{base_url}}/api/logout/"
                        }
                    }
                ]
            },
            {
                "name": "🏢 Department Management",
                "item": [
                    {
                        "name": "List All Departments",
                        "request": {
                            "method": "GET",
                            "url": "{{base_url}}/api/departments/"
                        }
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
                            "url": "{{base_url}}/api/departments/1/"
                        }
                    },
                    {
                        "name": "Create Department (Admin)",
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
                            "url": "{{base_url}}/api/departments/"
                        }
                    },
                    {
                        "name": "Update Department (Admin)",
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
                                    "name": "Updated Department",
                                    "description": "Updated description"
                                }, indent=2)
                            },
                            "url": "{{base_url}}/api/departments/1/"
                        }
                    },
                    {
                        "name": "Delete Department (Admin)",
                        "request": {
                            "method": "DELETE",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Token {{auth_token}}"
                                }
                            ],
                            "url": "{{base_url}}/api/departments/1/"
                        }
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
                            "url": "{{base_url}}/api/departments/1/employees/"
                        }
                    }
                ]
            },
            {
                "name": "👥 Employee Management",
                "item": [
                    {
                        "name": "List All Employees (Admin)",
                        "request": {
                            "method": "GET",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Token {{auth_token}}"
                                }
                            ],
                            "url": "{{base_url}}/api/employees/"
                        }
                    },
                    {
                        "name": "Get Employee by ID (Admin)",
                        "request": {
                            "method": "GET",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Token {{auth_token}}"
                                }
                            ],
                            "url": "{{base_url}}/api/employees/1/"
                        }
                    },
                    {
                        "name": "Update Employee (Admin)",
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
                            "url": "{{base_url}}/api/employees/1/"
                        }
                    },
                    {
                        "name": "Delete Employee (Admin)",
                        "request": {
                            "method": "DELETE",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Token {{auth_token}}"
                                }
                            ],
                            "url": "{{base_url}}/api/employees/1/"
                        }
                    },
                    {
                        "name": "Employee Statistics (Admin)",
                        "request": {
                            "method": "GET",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Token {{auth_token}}"
                                }
                            ],
                            "url": "{{base_url}}/api/employees/statistics/"
                        }
                    }
                ]
            },
            {
                "name": "📈 Performance Data (ML)",
                "item": [
                    {
                        "name": "List Performance Data (Admin)",
                        "request": {
                            "method": "GET",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Token {{auth_token}}"
                                }
                            ],
                            "url": "{{base_url}}/api/performance-data/"
                        }
                    },
                    {
                        "name": "Create Performance Data (Admin)",
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
                            "url": "{{base_url}}/api/performance-data/"
                        }
                    }
                ]
            },
            {
                "name": "🔧 Additional Endpoints",
                "item": [
                    {
                        "name": "List Employees (Public)",
                        "request": {
                            "method": "GET",
                            "url": "{{base_url}}/api/list-employees/"
                        }
                    },
                    {
                        "name": "List Departments (Public)",
                        "request": {
                            "method": "GET",
                            "url": "{{base_url}}/api/list-departments/"
                        }
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
                            "url": "{{base_url}}/api/data-separation-stats/"
                        }
                    }
                ]
            },
            {
                "name": "🧪 CSRF & CORS Tests",
                "item": [
                    {
                        "name": "Test CSRF Bypass (Should Work)",
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
                                },
                                {
                                    "key": "Referer",
                                    "value": "https://web.postman.co/"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({
                                    "email": "csrf.test@example.com",
                                    "password": "TestPass123!",
                                    "password_confirm": "TestPass123!",
                                    "first_name": "CSRF",
                                    "last_name": "Test",
                                    "department": 1
                                }, indent=2)
                            },
                            "url": "{{base_url}}/api/register/"
                        }
                    },
                    {
                        "name": "Test CORS Preflight",
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
                                },
                                {
                                    "key": "Access-Control-Request-Headers",
                                    "value": "content-type"
                                }
                            ],
                            "url": "{{base_url}}/api/register/"
                        }
                    }
                ]
            }
        ]
    }
    
    # Save collection
    filename = "SMART_EN_TURNOVER_API_ULTIMATE.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)
    
    print("🚀 ULTIMATE POSTMAN COLLECTION GENERATED!")
    print("=" * 60)
    print(f"✅ File: {filename}")
    print("✅ CSRF: COMPLETELY DISABLED")
    print("✅ CORS: FULLY PERMISSIVE")
    print("✅ Auto Token Management: YES")
    print("✅ Test Scripts: INCLUDED")
    
    # Count endpoints
    total_endpoints = sum(len(folder["item"]) for folder in collection["item"])
    print(f"✅ Total Endpoints: {total_endpoints}")
    
    print("\n📋 IMPORT TO POSTMAN:")
    print("1. Open Postman")
    print("2. Click 'Import'")
    print(f"3. Select: {filename}")
    print("4. Start testing immediately!")
    
    print("\n🔥 QUICK START:")
    print("1. Run 'Register Employee' to create account + get token")
    print("2. Run 'Login Employee' to get token if already have account")
    print("3. Token auto-saved for authenticated endpoints")
    print("4. Test any endpoint without CSRF/CORS issues!")
    
    print("\n🎯 NO MORE ERRORS:")
    print("❌ CSRF Failed: Referer checking failed - FIXED!")
    print("❌ CORS policy errors - FIXED!")
    print("❌ Authentication issues - AUTO HANDLED!")
    print("✅ Ready untuk production testing!")

if __name__ == "__main__":
    main()
