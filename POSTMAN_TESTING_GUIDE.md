# 🚀 SMART-EN HR Analytics API - Postman Testing Guide

## 📋 Overview

This guide provides instructions for testing the SMART-EN HR Analytics Turnover Prediction API using the comprehensive Postman collections that have been created.

## 📁 Available Files

### 🔧 Postman Collections

1. **`SMART-EN-Complete-API-v2.postman_collection.json`** - Main collection with 12 comprehensive sections
2. **`Turnover_API_Collection_Clean.json`** - Clean, focused collection for core functionality

### 🌍 Environment Files

1. **`SMART-EN-Development.postman_environment.json`** - Development environment (localhost:8000)
2. **`SMART-EN-Environments.postman_environment.json`** - Production environment (DigitalOcean)
3. **`SMART-EN-Production.postman_environment.json`** - Production-specific settings

## 🎯 Testing Sections in Main Collection

### 1. 🔐 Authentication

- User Registration
- User Login (auto-saves auth token)

**Collection Version**: 2.0**API Version**: v2.0**Last Updated**: July 2024---✅ **Dashboard data** - Analytics endpoints return proper data✅ **Predictions received** - ML model returns turnover probabilities✅ **CSV uploaded** - File processed and predictions generated✅ **Employee created** - New employee record in system✅ **Login successful** - Auth token saved to environment## 🎉 Success Indicators4. Review error responses for detailed messages3. Ensure proper authentication token2. Verify your environment configuration1. Check the API status at the base URLIf you encounter any issues:## 📞 SupportYou can run the entire collection or specific folders using Postman's Collection Runner for automated testing.### Collection Runner:- Verify data consistency- Extract and save important values- Check response data structure- Validate response status codesEach request includes test scripts that:### Automated Testing Scripts:## 🔄 Continuous Testing- **500**: Server error- **404**: Not found- **403**: Forbidden (insufficient permissions)- **401**: Unauthorized (missing/invalid token)- **400**: Bad request (validation errors)- **201**: Created successfully- **200**: Success## 📊 Expected Response Codes- `password` - Your test password- `username` - Your test username- `base_url` - API base URL (localhost:8000 or production)### Manual Configuration:- `modelId` - Updated when training models- `userId` - Set after successful authentication- `authToken` - Auto-populated after login### Automatic Variables:## 🌐 Environment Variables- Test with various data sizes for bulk operations- Monitor response times for all endpoints### 4. Performance Testing- Check required fields and data format requirements- Use the validation tests to ensure data integrity### 3. Data Validation- Verify proper error responses and status codes- Check the "⚠️ Error Handling Examples" section for common error scenarios### 2. Error Handling- Token is valid for the session duration- All protected endpoints use this token automatically- The login request automatically saves the auth token to environment variables### 1. Authentication## 🔍 Testing Tips`Jane Smith,25,0.6,0.7,3,150,2,0,0,HR,highJohn Doe,30,0.7,0.8,4,160,3,0,0,IT,mediumname,age,satisfaction_level,last_evaluation,number_project,average_montly_hours,time_spend_company,work_accident,promotion_last_5years,department,salary`csv### Sample CSV Format:4. Set key as "file" and select your CSV file3. Attach your CSV file in the Body > form-data section2. Use "Upload CSV for Bulk Prediction" request1. Navigate to "📁 File Upload & Processing"### Using the File Upload Endpoints:## 📤 CSV Upload Testing4. **Analytics**: Verify dashboard and analytics endpoints3. **Performance Management**: Test performance review features2. **ML Predictions**: Upload CSV and get turnover predictions1. **Employee Management**: Create/manage employee records### Step 4: Test Core Functionality4. All subsequent requests will use the saved token3. Run "Login User" - this will automatically save the auth token2. Run "Register User" (if testing with new user)1. Go to "🔐 1. Authentication" folder### Step 3: Authentication Flow- **Production**: Import `SMART-EN-Environments.postman_environment.json`- **Development**: Import `SMART-EN-Development.postman_environment.json`Choose your testing environment:### Step 2: Set Up Environment4. Import the environment file for your testing scenario3. Select `SMART-EN-Complete-API-v2.postman_collection.json`2. Click "Import" button1. Open Postman### Step 1: Import Collections## 🚀 Quick Start Guide- Integration Tests- Performance Tests- API Response Validation- Data Validation Tests### 12. 🧪 Testing & Validation- Rate Limiting Examples- Permission Denied Cases- Authentication Errors- Invalid Data Scenarios### 11. ⚠️ Error Handling Examples- Chart Data- Real-time Updates- Widget Configuration- Dashboard Data### 10. 🎛️ Dashboard API- Batch Processing- Template Download- Excel File Processing- CSV File Upload### 9. 📁 File Upload & Processing- System Health Check- User Role Management- Data Export/Import- System Configuration### 8. 🔧 Admin Functions- Trend Analysis- Department Analytics- Performance Metrics- Turnover Analytics### 7. 📈 Analytics & Reporting- Career Planning- Learning & Development- Shoutouts System- Employee Recognition### 6. 🏆 Recognition & Development- Performance Analytics- 360° Feedback System- Performance Reviews- Goals & OKRs Management### 5. 📊 Performance Management- Prediction History- Model Status & Info- Bulk Prediction- Individual Prediction- Train Model with CSV Data### 4. 🤖 ML Model & Predictions- Bulk Employee Operations- Delete Employee- Update Employee- Get Employee Details- List Employees- Create Employee### 3. 🏢 Employee Management- User Preferences- List All Users (admin)- Update User Profile- Get Current User Profile- Token Refresh

- Logout

### 2. 👥 User Management
