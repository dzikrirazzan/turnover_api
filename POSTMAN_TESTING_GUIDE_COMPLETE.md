# 🔥 SMART-EN API - Complete CRUD Testing Guide

## 🎯 **STATUS: 100% SUCCESS - ALL 12 FEATURES WORKING!**

**Production URL**: `https://turnover-api-hd7ze.ondigitalocean.app`  
**Authentication**: Token-based (NO CSRF cookies needed!)  
**Last Tested**: July 14, 2025  

---

## 📥 **IMPORT POSTMAN COLLECTION**

1. **Download**: `SMART_EN_CRUD_COMPLETE_POSTMAN.json`
2. **Import ke Postman**: File > Import > Select file
3. **Ready to test!** - Semua variable udah auto-configured

---

## 🔄 **TESTING SEQUENCE (Run in Order)**

### **Step 1: Admin Authentication**
```
🔐 1. ADMIN LOGIN
- Method: POST
- URL: /api/login/
- Body: admin@company.com / AdminPass123!
- Expected: 200 + Token auto-saved
```

### **Step 2: Department Management**
```
🏢 2. CREATE DEPARTMENT  
- Method: POST /api/departments/
- Auth: Admin token (auto-added)
- Expected: 201 + Department ID auto-saved

✏️ 5. ADMIN UPDATE DEPARTMENT
- Method: PUT /api/departments/{id}/
- Auth: Admin token
- Expected: 200 + Updated data

🏢 11. HARD DELETE DEPARTMENT
- Method: DELETE /api/departments/{id}/
- Auth: Admin token  
- Expected: 200 + "berhasil dihapus"
```

### **Step 3: Employee Management**
```
👤 3. ADMIN ACCESS EMPLOYEE DETAILS
- Method: GET /api/employees/27/
- Auth: Admin token
- Expected: 200 + Employee details

📝 6. ADMIN UPDATE EMPLOYEE DATA
- Method: PATCH /api/employees/27/
- Auth: Admin token
- Expected: 200 + "Data berhasil diperbarui"

🗑️ 10. SOFT DELETE EMPLOYEE
- Method: DELETE /api/employees/27/
- Auth: Admin token
- Expected: 200 + "berhasil dinonaktifkan"
```

### **Step 4: Profile Access**
```
🎯 4. ADMIN PROFILE ACCESS
- Method: GET /api/profile/
- Auth: Admin token
- Expected: 200 + Admin profile data
```

### **Step 5: Employee Authentication & Self-Management**
```
👨‍💼 7. EMPLOYEE LOGIN
- Method: POST /api/login/
- Body: bravely@gmail.com / user123
- Expected: 200 + Employee token auto-saved

👤 8. EMPLOYEE PROFILE ACCESS  
- Method: GET /api/profile/
- Auth: Employee token
- Expected: 200 + Employee profile

🔄 9. EMPLOYEE SELF-UPDATE
- Method: PATCH /api/profile/update/
- Auth: Employee token
- Expected: 200 + "Profil berhasil diupdate"
```

### **Step 6: Token Invalidation (Security)**
```
🚪 12A. EMPLOYEE LOGOUT
- Method: POST /api/logout/
- Auth: Employee token
- Expected: 200 + "Logout berhasil"

✅ 12B. VERIFY EMPLOYEE TOKEN INVALIDATED
- Method: GET /api/profile/
- Auth: Employee token (should be invalid)
- Expected: 401 + "Invalid token"

🚪 12C. ADMIN LOGOUT  
- Method: POST /api/logout/
- Auth: Admin token
- Expected: 200 + "Logout berhasil"

✅ 12D. VERIFY ADMIN TOKEN INVALIDATED
- Method: GET /api/profile/ 
- Auth: Admin token (should be invalid)
- Expected: 401 + "Invalid token"
```

---

## ✅ **SUCCESS CRITERIA**

### **Expected Results:**
- ✅ **12/12 requests successful**
- ✅ **All status codes 200/201 (except verification steps = 401)**
- ✅ **Tokens auto-saved between requests**
- ✅ **Department ID auto-captured and used**
- ✅ **Employee soft delete (is_active=false)**
- ✅ **Department hard delete (completely removed)**
- ✅ **Token invalidation working**

---

## 🔧 **MANUAL TESTING (Alternative)**

### **Admin Credentials:**
```
Email: admin@company.com
Password: AdminPass123!
```

### **Employee Credentials:**
```
Email: bravely@gmail.com  
Password: user123
```

### **Key Endpoints:**
```bash
# Authentication
POST /api/login/

# Department CRUD
POST   /api/departments/         # Create (Admin)
GET    /api/departments/{id}/    # Read details
PUT    /api/departments/{id}/    # Update (Admin)
DELETE /api/departments/{id}/    # Hard delete (Admin)

# Employee CRUD  
GET    /api/employees/{id}/      # Read details (Admin)
PATCH  /api/employees/{id}/      # Update (Admin)
DELETE /api/employees/{id}/      # Soft delete (Admin)

# Profile Management
GET    /api/profile/             # Get own profile
PATCH  /api/profile/update/      # Employee self-update

# Security
POST   /api/logout/              # Invalidate token
```

---

## 🚀 **NO CSRF ISSUES!**

### **Why This Works:**
✅ **Token-based authentication** - No cookies needed  
✅ **CORS properly configured** - Cross-origin requests allowed  
✅ **No CSRF tokens required** - Django REST Framework handles it  
✅ **Clean JSON responses** - Consistent API format  
✅ **Proper error handling** - Clear error messages  

### **Headers You Need:**
```
Content-Type: application/json
Authorization: Token {your_token_here}
```

**That's it! No cookies, no CSRF, just clean token auth!** 🔥

---

## 🎉 **PRODUCTION READY!**

**All 12 CRUD features working perfectly:**
1. ✅ Admin login
2. ✅ Create department  
3. ✅ Admin access employee details
4. ✅ Admin profile access
5. ✅ Admin update department
6. ✅ Admin update employee data
7. ✅ Employee login
8. ✅ Employee profile access  
9. ✅ Employee self-update
10. ✅ Soft delete employee
11. ✅ Hard delete department
12. ✅ Token invalidation (logout)

**MANTAP BROOO! API SIAP DIPAKE! 🚀🔥**
