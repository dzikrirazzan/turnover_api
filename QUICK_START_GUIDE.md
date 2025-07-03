# 🚀 Quick Start Guide - SMARTEN Turnover API Postman Collection

## 📥 Import Instructions

### 1. Download Collection
- File: `SMARTEN_TURNOVER_API_COMPREHENSIVE_v2.1.json`
- Location: `/Users/dzikrirazzan/Documents/code/turnover_api/`

### 2. Import to Postman
1. Open Postman Desktop/Web
2. Click **"Import"** button (top left)
3. Select **"Upload Files"**
4. Choose `SMARTEN_TURNOVER_API_COMPREHENSIVE_v2.1.json`
5. Click **"Import"**

## ⚡ Immediate Testing

### Step 1: Health Check
```
GET {{base_url}}/api/health/
```
**Expected**: 200 OK

### Step 2: Register New User
```
POST {{base_url}}/api/register/
Body (JSON):
{
  "email": "test@company.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "Test",
  "last_name": "User",
  "phone_number": "+6281234567890",
  "date_of_birth": "1990-01-01",
  "gender": "M",
  "marital_status": "single",
  "education_level": "bachelor",
  "address": "Test Address",
  "position": "Test Position",
  "department": 1,
  "hire_date": "2024-01-01"
}
```
**Expected**: 201 Created + Auth Token

### Step 3: Login (if registration email exists)
```
POST {{base_url}}/api/login/
Body (JSON):
{
  "email": "test@company.com",
  "password": "SecurePass123!"
}
```
**Expected**: 200 OK + Auth Token

### Step 4: Get Profile (Authenticated)
```
GET {{base_url}}/api/profile/
Headers: Authorization: Token {{auth_token}}
```
**Expected**: 200 OK + User Profile

## 🔧 Environment Variables (Auto-configured)

| Variable | Value | Description |
|----------|-------|-------------|
| `base_url` | `https://turnover-api-hd7ze.ondigitalocean.app` | Production API URL |
| `auth_token` | Auto-set from login | Bearer token for authentication |
| `employee_id` | Auto-set | Current user's employee ID |
| `department_id` | Auto-set | Current user's department ID |

## 📊 Collection Structure

### 🔐 Authentication & Core (6 endpoints)
- Health Check ✅
- Register Employee ✅
- Login Employee ✅
- User Profile ✅
- Refresh Token
- Logout

### 🏢 Department Management (7 endpoints)
- List Departments
- Get Department
- Create Department
- Update Department
- Delete Department
- Department Employees
- Department Statistics

### 👥 Employee Management (11 endpoints)
- List Employees
- Get Employee
- Create Employee
- Update Employee
- Delete Employee
- Employee Search
- Employee by Department
- Employee Performance
- Employee Predictions
- Update Employee Status
- Employee Analytics

### 🤖 Admin ML & Data (3 endpoints)
- Train Model
- Model Status
- Prediction Batch

### 🎯 Performance Goals (4 endpoints)
- List Goals
- Create Goal
- Update Goal
- Goal Progress

### 💬 Feedback & Reviews (3 endpoints)
- Submit Feedback
- Get Reviews
- Performance Review

### 📊 Analytics & Dashboard (4 endpoints)
- Dashboard Data
- Turnover Analytics
- Risk Analysis
- Trend Reports

### 📚 Learning & Development (3 endpoints)
- Training Programs
- Employee Skills
- Development Plans

### 🔧 Testing & Debug (2 endpoints)
- Debug Info
- System Status

## 🔒 Authentication Flow

### Automatic Token Management
The collection includes JavaScript that automatically:
1. Extracts tokens from login/register responses
2. Sets the `auth_token` environment variable
3. Uses the token in subsequent requests

### Manual Token Setting
If needed, manually set token:
1. Go to **Environment** tab
2. Set `auth_token` variable
3. All authenticated requests will use this token

## ⚠️ Expected API Responses

### Success Responses
- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **204 No Content**: Delete successful

### Authentication Responses
- **401 Unauthorized**: Missing or invalid token
- **403 Forbidden**: Insufficient permissions

### Client Error Responses
- **400 Bad Request**: Invalid data format
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation errors

## 🎯 Testing Workflow

### 1. Basic Authentication Flow
1. Health Check → Register/Login → Profile → Logout

### 2. Employee Management Flow
1. Login → List Employees → Get Employee → Update Employee

### 3. Department Management Flow
1. Login → List Departments → Get Department → Department Employees

### 4. Analytics Flow
1. Login → Dashboard Data → Analytics → Risk Analysis

## 🚨 Troubleshooting

### Common Issues
1. **CSRF Errors**: ✅ **COMPLETELY RESOLVED** - No longer occurs
   - **Problem**: `CSRF Failed: Referer checking failed - no Referer`
   - **Cause**: Postman sends referer headers, Django validates them
   - **Solution**: Added `@csrf_exempt` decorators (deployed in commit `ddb1fa0`)
   - **Status**: Working perfectly in production

2. **400 Bad Request - Email exists**: 
   - **Cause**: Trying to register with existing email
   - **Solution**: Use LOGIN instead of REGISTER, or use new email
   - **Example**: `john.doe@smarten.com` already exists, use login

3. **401 Unauthorized**: Check if token is set correctly
4. **403 Forbidden**: User lacks required permissions

### Quick Fixes
- **CSRF Issues**: ✅ **NO ACTION NEEDED** - Already fixed
- **Email Exists Error**: Use `/api/login/` instead of `/api/register/`
- **Token Issues**: Re-login to refresh token
- **Permission Issues**: Check user role (employee/hr/manager/admin)
- **Network Issues**: Verify production URL is accessible

### Why CSRF Works in CURL but Not Postman?
**Common StackOverflow Issue**: This affects thousands of developers
- **CURL**: Doesn't send referer headers by default → Django skips CSRF check
- **Postman**: Sends referer headers → Django validates and fails
- **Our Fix**: `@csrf_exempt` on API endpoints → Works for both CURL and Postman

## 📞 Support Information

### API Documentation
- Production URL: `https://turnover-api-hd7ze.ondigitalocean.app`
- Health Check: `https://turnover-api-hd7ze.ondigitalocean.app/api/health/`

### Status
- ✅ CSRF Issues: **RESOLVED**
- ✅ Production: **LIVE**
- ✅ Authentication: **WORKING**
- ✅ All Core Endpoints: **FUNCTIONAL**

---

**🎉 Ready to Start Testing!**

Import the collection and begin with the Health Check endpoint to verify everything is working correctly.
