# 🚀 SMART-EN System - Complete Postman Testing Guide

## 📋 Overview

This guide provides comprehensive testing instructions for the **SMART-EN System Complete API Collection** containing **50+ endpoints** across 7 major categories:

- 🔐 **Authentication** (7 endpoints)
- 🏢 **Departments** (5 endpoints)
- 👥 **Employees** (8 endpoints)
- 🤖 **Turnover Predictions** (9 endpoints)
- 🎯 **Performance Management** (30+ endpoints)
- 📊 **Analytics & Reports** (10 endpoints)
- ⚙️ **System & Admin** (6 endpoints)

## 📁 **Files yang Tersedia**

1. **`SMART-EN-Complete-API.postman_collection.json`** - Collection lengkap semua API endpoints
2. **`SMART-EN-Production.postman_environment.json`** - Environment variables untuk production
3. **`test_all_apis.py`** - Python script untuk automated testing

## 🔧 **Cara Import ke Postman**

### **Step 1: Import Collection**

1. Buka **Postman**
2. Klik **"Import"** (tombol di kiri atas)
3. Drag & drop file `SMART-EN-Complete-API.postman_collection.json`
4. Klik **"Import"**

### **Step 2: Import Environment**

1. Klik **"Import"** lagi
2. Drag & drop file `SMART-EN-Production.postman_environment.json`
3. Klik **"Import"**

### **Step 3: Set Environment**

1. Di dropdown kanan atas Postman, pilih **"SMART-EN Production Environment"**
2. Environment akan otomatis ter-set dengan:
   ```
   base_url: https://turnover-api-hd7ze.ondigitalocean.app
   username: testuser
   password: testpassword123
   ```

## 🔐 **Setup Authentication**

### **Option 1: Automatic (Recommended)**

Collection sudah memiliki **pre-request script** yang otomatis generate Basic Auth token.

### **Option 2: Manual**

1. Buat user dulu via registration endpoint
2. Generate Basic Auth token:
   ```javascript
   // Di browser console:
   btoa("username:password");
   ```
3. Set variable `auth_token` di environment

## 📚 **API Endpoints Categories**

### **🔐 1. Authentication (5 endpoints)**

- User Registration
- User Login
- Get User Profile
- Update User Profile
- Health Check

### **🏢 2. Departments (5 endpoints)**

- List All Departments
- Create Department
- Get Department Details
- Update Department
- Delete Department

### **👥 3. Employees (7 endpoints)**

- List All Employees
- Create Employee
- Get Employee Details
- Update Employee
- Delete Employee
- Search Employees
- Filter by Department

### **🤖 4. Turnover Predictions (7 endpoints)**

- Predict Single Employee
- Predict Custom Data
- Bulk Predict All
- Get Prediction History
- Get High Risk Employees
- Get Model Performance
- Train New Model

### **🎯 5. Performance Management (7 endpoints)**

- Dashboard Data
- Create Performance Review
- Get Performance Reviews
- Create Goal
- Get Employee Goals
- Create 360° Feedback
- Get 360° Feedback

### **📊 6. Analytics & Reports (4 endpoints)**

- Department Analytics
- Turnover Analytics
- Performance Trends
- Employee Satisfaction Report

### **🔧 7. System & Admin (4 endpoints)**

- API Root
- Admin Panel
- ML Models List
- Feature Importance

## 🧪 **Quick Testing Sequence**

### **Start Here (Test these first):**

1. **Health Check** - `GET /predictions/health/`
2. **User Registration** - `POST /api/auth/register/`
3. **List Departments** - `GET /api/departments/`
4. **List Employees** - `GET /api/employees/`

### **Core Features:**

5. **Create Department** - `POST /api/departments/`
6. **Create Employee** - `POST /api/employees/`
7. **Predict Turnover** - `POST /predictions/predict-custom/`
8. **Dashboard Data** - `GET /performance/api/dashboard/`

## 🐍 **Automated Testing dengan Python**

Jalankan automated test untuk semua endpoints:

```bash
cd /Users/dzikrirazzan/Documents/code/turnover_api
python test_all_apis.py
```

Script ini akan:

- ✅ Test semua 40+ endpoints
- ✅ Check response status
- ✅ Create sample data
- ✅ Verify authentication
- ✅ Generate test report

## 📝 **Sample Request Bodies**

### **Create Employee**

```json
{
  "employee_id": "EMP001",
  "name": "John Doe",
  "email": "john.doe@company.com",
  "department": 1,
  "hire_date": "2023-01-15",
  "satisfaction_level": 0.75,
  "last_evaluation": 0.8,
  "number_project": 5,
  "average_monthly_hours": 180,
  "time_spend_company": 2,
  "work_accident": false,
  "promotion_last_5years": false,
  "salary": "medium",
  "left": false
}
```

### **Predict Turnover**

```json
{
  "satisfaction_level": 0.38,
  "last_evaluation": 0.53,
  "number_project": 2,
  "average_monthly_hours": 157,
  "time_spend_company": 3,
  "work_accident": 0,
  "promotion_last_5years": 0,
  "department": "sales",
  "salary": "low"
}
```

### **Create Performance Review**

```json
{
  "employee": 1,
  "reviewer": 1,
  "review_period_start": "2024-01-01",
  "review_period_end": "2024-12-31",
  "overall_rating": 4,
  "goals_achievement": 85,
  "strengths": "Excellent communication skills",
  "areas_for_improvement": "Time management",
  "development_plan": "Attend time management workshop"
}
```

## 🔍 **Troubleshooting**

### **Authentication Errors (401)**

- Check username/password di environment
- Pastikan user sudah terdaftar via registration endpoint
- Verify auth_token ter-generate dengan benar

### **Server Errors (500)**

- Check apakah database migrations sudah dijalankan
- Verify app masih running di DigitalOcean
- Check logs di DigitalOcean console

### **Not Found Errors (404)**

- Check spelling endpoint URL
- Pastikan menggunakan base_url yang benar
- Verify API endpoint exists di server

### **Permission Errors (403)**

- Pastikan user memiliki permission yang tepat
- Check apakah user sudah login
- Verify authentication header format

## 🎯 **Expected Responses**

### **Success Response Example:**

```json
{
  "success": true,
  "data": {
    "employee_id": "EMP001",
    "name": "John Doe",
    "prediction_probability": 0.23,
    "prediction_result": false,
    "risk_level": "low"
  },
  "message": "Prediction completed successfully"
}
```

### **Error Response Example:**

```json
{
  "success": false,
  "error": "Employee not found",
  "details": "Employee with ID 'EMP999' does not exist"
}
```

## 📊 **Performance Expectations**

- **Health Check**: < 1 second
- **Simple GET requests**: < 2 seconds
- **CREATE/UPDATE operations**: < 3 seconds
- **ML Predictions**: < 5 seconds
- **Bulk operations**: < 10 seconds

## 🔗 **Links & Resources**

- **Production API**: https://turnover-api-hd7ze.ondigitalocean.app
- **Admin Panel**: https://turnover-api-hd7ze.ondigitalocean.app/admin/
- **API Root**: https://turnover-api-hd7ze.ondigitalocean.app/api/
- **Health Check**: https://turnover-api-hd7ze.ondigitalocean.app/predictions/health/

## 🎉 **Ready to Test!**

Sekarang kamu punya **complete API testing suite** untuk SMART-EN System!

1. **Import collections** ke Postman
2. **Set environment** ke production
3. **Start testing** dari Health Check
4. **Explore** semua 40+ endpoints
5. **Build** your frontend integration

Happy testing! 🚀
