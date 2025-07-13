# 🧠 SMART-EN ML Prediction API - Complete Documentation

## 📋 Overview
Dokumentasi lengkap untuk semua endpoint Machine Learning dalam SMART-EN Turnover Prediction API. API ini menggunakan Token Authentication dan dirancang khusus untuk admin/HR dalam memprediksi risiko turnover karyawan.

## 🔐 Authentication
Semua endpoint ML memerlukan token authentication:
```
Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935
```

## 📊 Base URL
```
https://turnover-api-hd7ze.ondigitalocean.app
```

---

## 🎯 1. AUTHENTICATION ENDPOINTS

### 1.1 Admin Login
**Endpoint:** `POST /api/login/`  
**Access:** Public  
**Purpose:** Login sebagai admin untuk mendapatkan token authentication

#### Request Body:
```json
{
  "email": "admin@company.com",
  "password": "AdminPass123!"
}
```

#### Success Response (200):
```json
{
  "success": true,
  "message": "Login berhasil",
  "data": {
    "user": {
      "id": 4,
      "employee_id": "EMP20250004",
      "email": "admin@company.com",
      "first_name": "System",
      "last_name": "Administrator",
      "full_name": "System Administrator",
      "phone_number": null,
      "date_of_birth": null,
      "gender": null,
      "marital_status": null,
      "education_level": null,
      "address": null,
      "position": "System Administrator",
      "department": 5,
      "department_name": "Human Resources",
      "hire_date": null,
      "role": "admin",
      "is_admin": true,
      "is_manager": true,
      "is_hr": false,
      "is_active": true,
      "created_at": "2025-07-03T11:00:33.391099",
      "token": "b42b585b90fbb149294bf041aaef5085c1ca4935"
    }
  }
}
```

#### Error Response (401):
```json
{
  "success": false,
  "message": "Email atau password salah",
  "data": null
}
```

### 1.2 Token Validation
**Endpoint:** `GET /api/profile/`  
**Access:** Admin Only  
**Purpose:** Validasi apakah token masih valid

#### Headers:
```
Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935
```

#### Success Response (200):
```json
{
  "success": true,
  "message": "Profil pengguna berhasil diambil",
  "data": {
    "id": 4,
    "employee_id": "EMP20250004",
    "email": "admin@company.com",
    "full_name": "System Administrator",
    "role": "admin",
    "is_admin": true,
    "is_manager": true,
    "department_name": "Human Resources",
    "token": "b42b585b90fbb149294bf041aaef5085c1ca4935"
  }
}
```

---

## 🏥 2. SYSTEM HEALTH ENDPOINTS

### 2.1 API Health Check
**Endpoint:** `GET /api/health/`  
**Access:** Public  
**Purpose:** Check status kesehatan API

#### Success Response (200):
```json
{
  "success": true,
  "message": "SMART-EN Turnover Prediction API berjalan",
  "data": {
    "status": "healthy",
    "version": "2.0.0"
  }
}
```

### 2.2 API Information
**Endpoint:** `GET /api/info/`  
**Access:** Public  
**Purpose:** Informasi lengkap tentang API dan fitur ML

#### Success Response (200):
```json
{
  "success": true,
  "message": "Informasi API berhasil diambil",
  "data": {
    "api_name": "SMART-EN Turnover Prediction API",
    "version": "2.0.0",
    "description": "Sistem prediksi turnover karyawan dengan role-based access",
    "features": [
      "Registrasi dan manajemen karyawan",
      "Role-based access control (Employee/Manager/HR/Admin)",
      "Manajemen department",
      "Data performance tracking (hanya admin)",
      "Prediksi turnover berbasis ML (hanya admin)",
      "Kategorisasi risiko dan alert"
    ],
    "data_separation": {
      "registration_data": "Data basic karyawan untuk admin info",
      "ml_data": "Data terpisah untuk machine learning (hanya admin)",
      "shared_data": "Department digunakan di kedua sistem"
    }
  }
}
```

---

## 👥 3. EMPLOYEE MANAGEMENT ENDPOINTS

### 3.1 List All Employees
**Endpoint:** `GET /api/employees/`  
**Access:** Admin Only  
**Purpose:** Daftar semua karyawan untuk keperluan ML

#### Headers:
```
Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935
```

#### Success Response (200):
```json
{
  "count": 35,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 39,
      "employee_id": "EMP20250039",
      "email": "bravely@company.com",
      "full_name": "Bravely Dirgayuska",
      "first_name": "Bravely",
      "last_name": "Dirgayuska",
      "position": "Sales Representative",
      "department": 2,
      "department_name": "Information Technology",
      "role": "employee",
      "is_admin": false,
      "is_manager": false,
      "is_hr": false,
      "is_active": true,
      "created_at": "2025-07-03T11:03:22.123456"
    }
  ]
}
```

### 3.2 Get Employee Performance Data
**Endpoint:** `GET /api/employees/{employee_id}/performance_data/`  
**Access:** Admin Only  
**Purpose:** Mendapatkan data performance ML untuk employee tertentu

#### Headers:
```
Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935
```

#### Success Response (200):
```json
{
  "success": true,
  "message": "Performance data ditemukan",
  "data": {
    "id": 1,
    "employee": 39,
    "employee_name": "Bravely Dirgayuska",
    "satisfaction_level": 0.65,
    "last_evaluation": 0.82,
    "number_project": 4,
    "average_monthly_hours": 185,
    "time_spend_company": 3,
    "work_accident": false,
    "promotion_last_5years": false,
    "left": false,
    "created_at": "2025-07-09T11:45:12.123456"
  }
}
```

#### Error Response (404):
```json
{
  "success": false,
  "message": "Performance data tidak ditemukan untuk employee ini",
  "data": null
}
```

### 3.3 Employee Statistics
**Endpoint:** `GET /api/employees/statistics/`  
**Access:** Admin Only  
**Purpose:** Statistik karyawan termasuk coverage data ML

#### Headers:
```
Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935
```

#### Success Response (200):
```json
{
  "success": true,
  "message": "Statistik employee berhasil diambil",
  "data": {
    "total_employees": 35,
    "with_performance_data": 15,
    "without_performance_data": 20,
    "coverage_percentage": 42.9,
    "by_department": {
      "Human Resources": 8,
      "Information Technology": 12,
      "Sales": 10,
      "Marketing": 5
    }
  }
}
```

---

## 📊 4. PERFORMANCE DATA MANAGEMENT ENDPOINTS

### 4.1 List All Performance Data
**Endpoint:** `GET /api/performance/`  
**Access:** Admin Only  
**Purpose:** Daftar semua data performance ML

#### Headers:
```
Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935
```

#### Success Response (200):
```json
{
  "success": true,
  "message": "Performance data berhasil diambil",
  "data": [
    {
      "id": 1,
      "employee": 39,
      "employee_name": "Bravely Dirgayuska",
      "satisfaction_level": 0.65,
      "last_evaluation": 0.82,
      "number_project": 4,
      "average_monthly_hours": 185,
      "time_spend_company": 3,
      "work_accident": false,
      "promotion_last_5years": false,
      "left": false,
      "created_at": "2025-07-09T11:45:12.123456"
    },
    {
      "id": 2,
      "employee": 38,
      "employee_name": "John Doe",
      "satisfaction_level": 0.85,
      "last_evaluation": 0.92,
      "number_project": 3,
      "average_monthly_hours": 160,
      "time_spend_company": 2,
      "work_accident": false,
      "promotion_last_5years": true,
      "left": false,
      "created_at": "2025-07-09T12:30:45.123456"
    }
  ]
}
```

### 4.2 Create Performance Data
**Endpoint:** `POST /api/performance/`  
**Access:** Admin Only  
**Purpose:** Membuat data performance baru untuk ML prediction

#### Headers:
```
Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935
Content-Type: application/json
```

#### Request Body (Normal Risk):
```json
{
  "employee": 39,
  "satisfaction_level": 0.75,
  "last_evaluation": 0.88,
  "number_project": 5,
  "average_monthly_hours": 170,
  "time_spend_company": 4,
  "work_accident": false,
  "promotion_last_5years": true,
  "left": false
}
```

#### Request Body (High Risk):
```json
{
  "employee": 39,
  "satisfaction_level": 0.25,
  "last_evaluation": 0.35,
  "number_project": 7,
  "average_monthly_hours": 280,
  "time_spend_company": 6,
  "work_accident": true,
  "promotion_last_5years": false,
  "left": false
}
```

#### Field Descriptions:
- `employee` (integer): ID karyawan
- `satisfaction_level` (float): Level kepuasan (0.0 - 1.0)
- `last_evaluation` (float): Evaluasi terakhir (0.0 - 1.0)
- `number_project` (integer): Jumlah project yang dikerjakan
- `average_monthly_hours` (integer): Rata-rata jam kerja per bulan
- `time_spend_company` (integer): Lama bekerja di perusahaan (tahun)
- `work_accident` (boolean): Apakah pernah mengalami kecelakaan kerja
- `promotion_last_5years` (boolean): Apakah mendapat promosi dalam 5 tahun terakhir
- `left` (boolean): Apakah sudah keluar dari perusahaan

#### Success Response (201):
```json
{
  "success": true,
  "message": "Performance data berhasil dibuat",
  "data": {
    "id": 3,
    "employee": 39,
    "employee_name": "Bravely Dirgayuska",
    "satisfaction_level": 0.75,
    "last_evaluation": 0.88,
    "number_project": 5,
    "average_monthly_hours": 170,
    "time_spend_company": 4,
    "work_accident": false,
    "promotion_last_5years": true,
    "left": false,
    "created_at": "2025-07-09T14:22:33.123456"
  }
}
```

#### Error Response (400):
```json
{
  "success": false,
  "message": "Data tidak valid",
  "data": {
    "employee": ["Employee dengan ID ini tidak ditemukan"],
    "satisfaction_level": ["Nilai harus antara 0.0 dan 1.0"]
  }
}
```

### 4.3 Data Separation Statistics
**Endpoint:** `GET /api/stats/`  
**Access:** Admin Only  
**Purpose:** Statistik pemisahan data ML vs registrasi

#### Headers:
```
Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935
```

#### Success Response (200):
```json
{
  "success": true,
  "message": "Statistik data separation berhasil diambil",
  "data": {
    "registration_count": 35,
    "ml_data_count": 15,
    "overlap_count": 15,
    "coverage_percentage": 42.9,
    "department_breakdown": {
      "Human Resources": {
        "total_employees": 8,
        "ml_data": 5,
        "coverage": 62.5
      },
      "Information Technology": {
        "total_employees": 12,
        "ml_data": 6,
        "coverage": 50.0
      },
      "Sales": {
        "total_employees": 10,
        "ml_data": 3,
        "coverage": 30.0
      },
      "Marketing": {
        "total_employees": 5,
        "ml_data": 1,
        "coverage": 20.0
      }
    }
  }
}
```

---

## 🧠 5. ML PREDICTION ENGINE (MAIN ENDPOINTS)

### 5.1 Predict Turnover Risk (MAIN ENDPOINT)
**Endpoint:** `POST /api/predict/`  
**Access:** Admin Only  
**Purpose:** Prediksi risiko turnover karyawan menggunakan ML model

#### Headers:
```
Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935
Content-Type: application/json
```

#### Request Body:
```json
{
  "employee_id": 39
}
```

#### Success Response (200):
```json
{
  "success": true,
  "message": "Turnover prediction completed for Bravely Dirgayuska",
  "data": {
    "employee": {
      "id": 39,
      "name": "Bravely Dirgayuska",
      "email": "bravely@company.com",
      "department": "Information Technology",
      "position": "Sales Representative"
    },
    "prediction": {
      "probability": 0.342,
      "risk_level": "medium",
      "will_leave": false,
      "confidence_score": 0.85,
      "model_used": "RuleBasedModel"
    },
    "risk_analysis": {
      "overall_risk_score": 0.342,
      "risk_factors": {
        "satisfaction_level": {
          "value": 0.65,
          "risk": 0.1,
          "weight": 0.25,
          "contribution": 0.025
        },
        "last_evaluation": {
          "value": 0.82,
          "risk": 0.0,
          "weight": 0.2,
          "contribution": 0.0
        },
        "number_project": {
          "value": 4,
          "risk": 0.0,
          "weight": 0.15,
          "contribution": 0.0
        },
        "average_monthly_hours": {
          "value": 185,
          "risk": 0.1,
          "weight": 0.15,
          "contribution": 0.015
        },
        "time_spend_company": {
          "value": 3,
          "risk": 0.0,
          "weight": 0.1,
          "contribution": 0.0
        },
        "work_accident": {
          "value": false,
          "risk": 0.0,
          "weight": 0.05,
          "contribution": 0.0
        },
        "promotion_last_5years": {
          "value": false,
          "risk": 0.2,
          "weight": 0.1,
          "contribution": 0.02
        }
      }
    },
    "recommendations": [
      {
        "category": "Career Growth",
        "issue": "No promotion in the last 5 years",
        "recommendation": "Review career progression opportunities and create development plans",
        "priority": "medium"
      },
      {
        "category": "Workload",
        "issue": "Slightly elevated working hours",
        "recommendation": "Monitor workload and consider work-life balance improvements",
        "priority": "low"
      }
    ],
    "features_used": {
      "satisfaction_level": 0.65,
      "last_evaluation": 0.82,
      "number_project": 4,
      "average_monthly_hours": 185,
      "time_spend_company": 3,
      "work_accident": 0,
      "promotion_last_5years": 0
    },
    "prediction_id": 2,
    "created_at": "2025-07-09T11:50:21.241246"
  }
}
```

#### Risk Level Classifications:
- **Low Risk** (probability < 0.3): Employee kemungkinan kecil untuk resign
- **Medium Risk** (probability 0.3 - 0.7): Employee perlu monitoring dan intervensi
- **High Risk** (probability > 0.7): Employee berisiko tinggi resign, perlu tindakan segera

#### Error Responses:

**Employee not found (404):**
```json
{
  "success": false,
  "message": "Employee not found",
  "data": null
}
```

**Performance data not found (404):**
```json
{
  "success": false,
  "message": "Performance data not found for this employee. Please add performance data first.",
  "data": null
}
```

**Missing employee_id (400):**
```json
{
  "success": false,
  "message": "Employee ID is required",
  "data": null
}
```

**Authentication required (401):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Permission denied (403):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## 🔬 6. TESTING & VALIDATION ENDPOINTS

### 6.1 Test Authentication
**Purpose:** Validasi bahwa endpoint memerlukan authentication

#### Test Without Token:
```bash
curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/predict/" \
  -H "Content-Type: application/json" \
  -d '{"employee_id": 39}'
```

**Expected Response (401):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 6.2 Test Input Validation
**Purpose:** Validasi input yang required

#### Test Without employee_id:
```bash
curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/predict/" \
  -H "Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935" \
  -H "Content-Type: application/json" \
  -d '{"invalid_field": "test"}'
```

**Expected Response (400):**
```json
{
  "success": false,
  "message": "Employee ID is required",
  "data": null
}
```

### 6.3 Test Non-existent Employee
**Purpose:** Validasi employee yang tidak ada

#### Test Invalid employee_id:
```bash
curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/predict/" \
  -H "Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935" \
  -H "Content-Type: application/json" \
  -d '{"employee_id": 999999}'
```

**Expected Response (404):**
```json
{
  "success": false,
  "message": "Employee not found",
  "data": null
}
```

---

## 📈 7. TESTING SCENARIOS

### 7.1 Low Risk Employee Scenario
**Purpose:** Test prediction untuk employee dengan risk rendah

#### Step 1 - Create Low Risk Performance Data:
```bash
curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/performance/" \
  -H "Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935" \
  -H "Content-Type: application/json" \
  -d '{
    "employee": 39,
    "satisfaction_level": 0.85,
    "last_evaluation": 0.90,
    "number_project": 3,
    "average_monthly_hours": 160,
    "time_spend_company": 2,
    "work_accident": false,
    "promotion_last_5years": true,
    "left": false
  }'
```

#### Step 2 - Predict:
```bash
curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/predict/" \
  -H "Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935" \
  -H "Content-Type: application/json" \
  -d '{"employee_id": 39}'
```

**Expected:** `risk_level: "low"`, `probability < 0.3`

### 7.2 High Risk Employee Scenario
**Purpose:** Test prediction untuk employee dengan risk tinggi

#### Step 1 - Create High Risk Performance Data:
```bash
curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/performance/" \
  -H "Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935" \
  -H "Content-Type: application/json" \
  -d '{
    "employee": 39,
    "satisfaction_level": 0.20,
    "last_evaluation": 0.30,
    "number_project": 8,
    "average_monthly_hours": 300,
    "time_spend_company": 7,
    "work_accident": true,
    "promotion_last_5years": false,
    "left": false
  }'
```

#### Step 2 - Predict:
```bash
curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/predict/" \
  -H "Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935" \
  -H "Content-Type: application/json" \
  -d '{"employee_id": 39}'
```

**Expected:** `risk_level: "high"`, `probability > 0.7`

### 7.3 Medium Risk Employee Scenario
**Purpose:** Test prediction untuk employee dengan risk medium

#### Step 1 - Create Medium Risk Performance Data:
```bash
curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/performance/" \
  -H "Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935" \
  -H "Content-Type: application/json" \
  -d '{
    "employee": 39,
    "satisfaction_level": 0.55,
    "last_evaluation": 0.65,
    "number_project": 5,
    "average_monthly_hours": 220,
    "time_spend_company": 4,
    "work_accident": false,
    "promotion_last_5years": false,
    "left": false
  }'
```

#### Step 2 - Predict:
```bash
curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/predict/" \
  -H "Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935" \
  -H "Content-Type: application/json" \
  -d '{"employee_id": 39}'
```

**Expected:** `risk_level: "medium"`, `probability 0.3-0.7`

---

## 🛠️ Implementation Guide

### Step-by-Step Testing Flow:

1. **Authentication Setup:**
   ```bash
   # Get admin token
   curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/login/" \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@company.com", "password": "AdminPass123!"}'
   ```

2. **Check API Health:**
   ```bash
   curl -X GET "https://turnover-api-hd7ze.ondigitalocean.app/api/health/"
   ```

3. **List Employees:**
   ```bash
   curl -X GET "https://turnover-api-hd7ze.ondigitalocean.app/api/employees/" \
     -H "Authorization: Token YOUR_TOKEN"
   ```

4. **Create Performance Data:**
   ```bash
   curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/performance/" \
     -H "Authorization: Token YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"employee": EMPLOYEE_ID, "satisfaction_level": 0.75, ...}'
   ```

5. **Predict Turnover:**
   ```bash
   curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/predict/" \
     -H "Authorization: Token YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"employee_id": EMPLOYEE_ID}'
   ```

### Postman Collection:
Import file `ML_ENDPOINTS_POSTMAN_COMPLETE.json` untuk testing yang lebih mudah dengan:
- Auto token management
- Pre-configured requests
- Test scenarios
- Detailed logging

---

## 📋 Error Codes Reference

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request berhasil |
| 201 | Created | Data berhasil dibuat |
| 400 | Bad Request | Input tidak valid |
| 401 | Unauthorized | Token tidak ada/invalid |
| 403 | Forbidden | Tidak memiliki permission |
| 404 | Not Found | Data tidak ditemukan |
| 500 | Internal Server Error | Error server |

---

## 🔒 Security Notes

1. **Token Security:** Jangan share token di public repositories
2. **Admin Only:** Semua ML endpoints hanya untuk admin
3. **Data Privacy:** Performance data bersifat sensitive
4. **Rate Limiting:** API mungkin memiliki rate limiting
5. **HTTPS Only:** Selalu gunakan HTTPS untuk production

---

## 📞 Support

- **Documentation:** File ini
- **Postman Collection:** `ML_ENDPOINTS_POSTMAN_COMPLETE.json`
- **Troubleshooting:** `POSTMAN_AUTHENTICATION_TROUBLESHOOTING.md`
- **API Status:** `GET /api/health/`

**Last Updated:** July 11, 2025  
**Version:** 2.0.0  
**Status:** Production Ready ✅
