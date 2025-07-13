# 🧠 SMART-EN Turnover API - ML Endpoints Documentation

## 📋 Daftar Isi

- [1. Authentication](#1-authentication)
- [2. System Health Check](#2-system-health-check)
- [3. Employee Management](#3-employee-management)
- [4. Performance Data Management](#4-performance-data-management)
- [5. ML Prediction Engine](#5-ml-prediction-engine)
- [6. Statistics & Analytics](#6-statistics--analytics)
- [7. Error Codes](#7-error-codes)
- [8. Quick Start Guide](#8-quick-start-guide)

---

## 🔐 1. Authentication

### Login Admin

**Endpoint:** `POST /api/login/`  
**Auth Required:** No  
**Description:** Login sebagai admin dan dapatkan token untuk akses ML endpoints

#### Request Body:

```json
{
  "email": "admin@company.com",
  "password": "AdminPass123!"
}
```

#### Response Success (200):

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1,
      "email": "admin@company.com",
      "full_name": "System Administrator",
      "role": "admin",
      "department_name": "IT",
      "position": "System Admin",
      "is_admin": true,
      "token": "b42b585b90fbb149294bf041aaef5085c1ca4935"
    }
  }
}
```

#### Response Error (401):

```json
{
  "success": false,
  "message": "Invalid credentials",
  "errors": {
    "non_field_errors": ["Invalid email or password"]
  }
}
```

### Test Token Validation

**Endpoint:** `GET /api/profile/`  
**Auth Required:** Yes (Token)  
**Headers:** `Authorization: Token {your_token}`

#### Response Success (200):

```json
{
  "success": true,
  "message": "Profile retrieved successfully",
  "data": {
    "id": 1,
    "email": "admin@company.com",
    "full_name": "System Administrator",
    "role": "admin",
    "department_name": "IT",
    "position": "System Admin",
    "is_admin": true,
    "created_at": "2025-01-15T10:00:00Z"
  }
}
```

---

## 🏥 2. System Health Check

### API Health Check

**Endpoint:** `GET /api/health/`  
**Auth Required:** No

#### Response Success (200):

```json
{
  "success": true,
  "message": "API is healthy",
  "data": {
    "status": "healthy",
    "version": "1.0.0",
    "timestamp": "2025-01-15T10:00:00Z"
  }
}
```

### API Information

**Endpoint:** `GET /api/info/`  
**Auth Required:** No

#### Response Success (200):

```json
{
  "success": true,
  "message": "API information retrieved",
  "data": {
    "api_name": "SMART-EN Turnover Prediction API",
    "version": "1.0.0",
    "description": "Machine Learning API untuk prediksi turnover karyawan",
    "features": ["Employee Management", "Performance Data Tracking", "ML Turnover Prediction", "Risk Analysis", "Recommendations Engine"]
  }
}
```

---

## 👥 3. Employee Management

### List All Employees

**Endpoint:** `GET /api/employees/`  
**Auth Required:** Yes (Admin Token)  
**Headers:** `Authorization: Token {your_token}`

#### Query Parameters (Optional):

- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `department`: Filter by department
- `search`: Search by name or email

#### Response Success (200):

```json
{
  "success": true,
  "message": "Employees retrieved successfully",
  "count": 50,
  "next": "http://api.example.com/api/employees/?page=2",
  "previous": null,
  "results": [
    {
      "id": 39,
      "email": "john.doe@company.com",
      "full_name": "John Doe",
      "department_name": "Engineering",
      "position": "Software Engineer",
      "role": "employee",
      "hire_date": "2023-01-15",
      "is_active": true,
      "has_performance_data": true
    },
    {
      "id": 38,
      "email": "jane.smith@company.com",
      "full_name": "Jane Smith",
      "department_name": "Marketing",
      "position": "Marketing Manager",
      "role": "employee",
      "hire_date": "2022-06-10",
      "is_active": true,
      "has_performance_data": false
    }
  ]
}
```

### Get Employee Performance Data

**Endpoint:** `GET /api/employees/{employee_id}/performance_data/`  
**Auth Required:** Yes (Admin Token)  
**Headers:** `Authorization: Token {your_token}`

#### Response Success (200):

```json
{
  "success": true,
  "message": "Performance data retrieved successfully",
  "data": {
    "id": 15,
    "employee": 39,
    "employee_name": "John Doe",
    "satisfaction_level": 0.75,
    "last_evaluation": 0.88,
    "number_project": 5,
    "average_monthly_hours": 170,
    "time_spend_company": 4,
    "work_accident": false,
    "promotion_last_5years": true,
    "left": false,
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-15T10:00:00Z"
  }
}
```

#### Response Not Found (404):

```json
{
  "success": false,
  "message": "Performance data not found for this employee",
  "error_code": "PERFORMANCE_DATA_NOT_FOUND"
}
```

### Employee Statistics

**Endpoint:** `GET /api/employees/statistics/`  
**Auth Required:** Yes (Admin Token)  
**Headers:** `Authorization: Token {your_token}`

#### Response Success (200):

```json
{
  "success": true,
  "message": "Employee statistics retrieved successfully",
  "data": {
    "total_employees": 50,
    "with_performance_data": 35,
    "without_performance_data": 15,
    "coverage_percentage": 70.0,
    "by_department": {
      "Engineering": 20,
      "Marketing": 15,
      "HR": 8,
      "Finance": 7
    },
    "active_employees": 48,
    "inactive_employees": 2
  }
}
```

---

## 📊 4. Performance Data Management

### List All Performance Data

**Endpoint:** `GET /api/performance/`  
**Auth Required:** Yes (Admin Token)  
**Headers:** `Authorization: Token {your_token}`

#### Query Parameters (Optional):

- `page`: Page number
- `employee`: Filter by employee ID
- `satisfaction_level__gte`: Min satisfaction level
- `satisfaction_level__lte`: Max satisfaction level

#### Response Success (200):

```json
{
  "success": true,
  "message": "Performance data retrieved successfully",
  "data": [
    {
      "id": 15,
      "employee": 39,
      "employee_name": "John Doe",
      "satisfaction_level": 0.75,
      "last_evaluation": 0.88,
      "number_project": 5,
      "average_monthly_hours": 170,
      "time_spend_company": 4,
      "work_accident": false,
      "promotion_last_5years": true,
      "left": false,
      "created_at": "2025-01-15T10:00:00Z"
    }
  ]
}
```

### Create Performance Data

**Endpoint:** `POST /api/performance/`  
**Auth Required:** Yes (Admin Token)  
**Headers:**

- `Authorization: Token {your_token}`
- `Content-Type: application/json`

#### Request Body:

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

#### Field Descriptions:

- `employee` (integer, required): Employee ID
- `satisfaction_level` (float, 0.0-1.0): Tingkat kepuasan karyawan
- `last_evaluation` (float, 0.0-1.0): Skor evaluasi terakhir
- `number_project` (integer): Jumlah proyek yang dikerjakan
- `average_monthly_hours` (integer): Rata-rata jam kerja per bulan
- `time_spend_company` (integer): Lama bekerja di perusahaan (tahun)
- `work_accident` (boolean): Pernah mengalami kecelakaan kerja
- `promotion_last_5years` (boolean): Promosi dalam 5 tahun terakhir
- `left` (boolean): Sudah resign atau tidak

#### Response Success (201):

```json
{
  "success": true,
  "message": "Performance data created successfully",
  "data": {
    "id": 16,
    "employee": 39,
    "employee_name": "John Doe",
    "satisfaction_level": 0.75,
    "last_evaluation": 0.88,
    "number_project": 5,
    "average_monthly_hours": 170,
    "time_spend_company": 4,
    "work_accident": false,
    "promotion_last_5years": true,
    "left": false,
    "created_at": "2025-01-15T10:00:00Z"
  }
}
```

#### Response Validation Error (400):

```json
{
  "success": false,
  "message": "Validation errors",
  "errors": {
    "satisfaction_level": ["Ensure this value is between 0.0 and 1.0"],
    "number_project": ["This field is required"]
  }
}
```

### Update Performance Data

**Endpoint:** `PUT /api/performance/{performance_id}/`  
**Auth Required:** Yes (Admin Token)

#### Request Body: (Same as Create)

### Delete Performance Data

**Endpoint:** `DELETE /api/performance/{performance_id}/`  
**Auth Required:** Yes (Admin Token)

#### Response Success (204): No Content

---

## 🧠 5. ML Prediction Engine (MAIN FEATURE)

### Predict Turnover Risk

**Endpoint:** `POST /api/predict/`  
**Auth Required:** Yes (Admin Token)  
**Headers:**

- `Authorization: Token {your_token}`
- `Content-Type: application/json`

#### Request Body:

```json
{
  "employee_id": 39
}
```

#### Response Success (200):

```json
{
  "success": true,
  "message": "Prediction completed successfully",
  "data": {
    "prediction_id": "pred_20250115_123456",
    "employee": {
      "id": 39,
      "name": "John Doe",
      "email": "john.doe@company.com",
      "department": "Engineering",
      "position": "Software Engineer"
    },
    "prediction": {
      "will_leave": false,
      "probability": 0.23,
      "risk_level": "low",
      "confidence_score": 0.89,
      "model_used": "RandomForestClassifier",
      "prediction_date": "2025-01-15T10:00:00Z"
    },
    "risk_analysis": {
      "risk_factors": {
        "satisfaction_level": {
          "value": 0.75,
          "risk": 0,
          "description": "Good satisfaction level"
        },
        "last_evaluation": {
          "value": 0.88,
          "risk": 0,
          "description": "Excellent evaluation score"
        },
        "average_monthly_hours": {
          "value": 170,
          "risk": 0,
          "description": "Normal working hours"
        },
        "time_spend_company": {
          "value": 4,
          "risk": 0,
          "description": "Stable tenure"
        },
        "work_accident": {
          "value": false,
          "risk": 0,
          "description": "No work accidents"
        },
        "promotion_last_5years": {
          "value": true,
          "risk": 0,
          "description": "Recent promotion"
        }
      },
      "total_risk_score": 0.23
    },
    "recommendations": [
      {
        "category": "Career Development",
        "recommendation": "Continue providing growth opportunities and challenging projects",
        "priority": "low",
        "impact": "medium"
      },
      {
        "category": "Work-Life Balance",
        "recommendation": "Maintain current work-life balance practices",
        "priority": "low",
        "impact": "low"
      }
    ]
  }
}
```

#### Response Errors:

**Employee Not Found (404):**

```json
{
  "success": false,
  "message": "Employee not found",
  "error_code": "EMPLOYEE_NOT_FOUND"
}
```

**Performance Data Not Found (404):**

```json
{
  "success": false,
  "message": "Performance data not found for this employee",
  "error_code": "PERFORMANCE_DATA_NOT_FOUND",
  "details": {
    "employee_id": 39,
    "suggestion": "Create performance data first using POST /api/performance/"
  }
}
```

**Missing Employee ID (400):**

```json
{
  "success": false,
  "message": "employee_id is required",
  "error_code": "MISSING_EMPLOYEE_ID"
}
```

**Authentication Error (401):**

```json
{
  "success": false,
  "message": "Authentication credentials were not provided",
  "error_code": "AUTHENTICATION_FAILED"
}
```

---

## 📈 6. Statistics & Analytics

### Data Separation Statistics

**Endpoint:** `GET /api/stats/`  
**Auth Required:** Yes (Admin Token)  
**Headers:** `Authorization: Token {your_token}`

#### Response Success (200):

```json
{
  "success": true,
  "message": "Statistics retrieved successfully",
  "data": {
    "registration_count": 50,
    "ml_data_count": 35,
    "overlap_count": 35,
    "coverage_percentage": 70.0,
    "missing_ml_data": 15,
    "department_breakdown": {
      "Engineering": {
        "total_employees": 20,
        "ml_data": 18,
        "coverage": 90.0
      },
      "Marketing": {
        "total_employees": 15,
        "ml_data": 10,
        "coverage": 66.7
      },
      "HR": {
        "total_employees": 8,
        "ml_data": 5,
        "coverage": 62.5
      },
      "Finance": {
        "total_employees": 7,
        "ml_data": 2,
        "coverage": 28.6
      }
    },
    "last_updated": "2025-01-15T10:00:00Z"
  }
}
```

## 📝 Notes

### Risk Level Classification:

- **Low Risk** (0.0 - 0.3): probability ≤ 30%
- **Medium Risk** (0.3 - 0.7): 30% < probability ≤ 70%
- **High Risk** (0.7 - 1.0): probability > 70%

### Performance Data Guidelines:

- `satisfaction_level`: 0.0 (very unsatisfied) - 1.0 (very satisfied)
- `last_evaluation`: 0.0 (poor) - 1.0 (excellent)
- `number_project`: Typical range 1-10 projects
- `average_monthly_hours`: Typical range 80-350 hours
- `time_spend_company`: Years at company (0-20+)

### Base URL:

```
Production: https://turnover-api-hd7ze.ondigitalocean.app
```

### Authentication:

Semua ML endpoints memerlukan authentication dengan format:

```
Authorization: Token {your_token_here}
```

---

## 🧪 7. HASIL TEST ML PREDICTION (LIVE RESULTS)

### Hasil Test Employee ID 39 (LOW RISK)

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
      "probability": 0.1, // 10% kemungkinan resign
      "risk_level": "low", // Level risiko rendah
      "will_leave": false, // Prediksi tidak akan resign
      "confidence_score": 0.85, // 85% confidence dari model
      "model_used": "RuleBasedModel"
    },
    "risk_analysis": {
      "overall_risk_score": 0.04, // 4% total risk score
      "risk_factors": {
        "satisfaction_level": {
          "value": 0.65, // 65% satisfaction
          "risk": 0.0, // No risk (good)
          "weight": 0.25, // 25% importance
          "contribution": 0.0 // 0% contribution to risk
        },
        "last_evaluation": {
          "value": 0.82, // 82% evaluation score
          "risk": 0.0,
          "weight": 0.2,
          "contribution": 0.0
        },
        "number_project": {
          "value": 4, // 4 projects (normal)
          "risk": 0.0,
          "weight": 0.15,
          "contribution": 0.0
        },
        "average_monthly_hours": {
          "value": 185, // 185 hours/month (normal)
          "risk": 0.0,
          "weight": 0.15,
          "contribution": 0.0
        },
        "promotion_last_5years": {
          "value": false, // No promotion ⚠️
          "risk": 0.4, // 40% risk factor
          "weight": 0.1,
          "contribution": 0.04 // 4% contribution to risk
        }
      }
    },
    "recommendations": [
      {
        "category": "Career Growth",
        "issue": "No promotion in the last 5 years",
        "recommendation": "Review career progression opportunities and create development plans",
        "priority": "medium"
      }
    ]
  }
}
```

### Hasil Test Employee ID 38 (HIGH RISK)

```json
{
  "success": true,
  "message": "Turnover prediction completed for Bravely Dirgayuska",
  "data": {
    "employee": {
      "id": 38,
      "name": "Bravely Dirgayuska",
      "department": "IT Department",
      "position": "Software Developer"
    },
    "prediction": {
      "probability": 1.0, // 100% kemungkinan resign ⚠️
      "risk_level": "high", // Level risiko TINGGI
      "will_leave": true, // Prediksi AKAN resign
      "confidence_score": 0.85, // 85% confidence
      "model_used": "RuleBasedModel"
    },
    "risk_analysis": {
      "overall_risk_score": 0.63, // 63% total risk score
      "risk_factors": {
        "satisfaction_level": {
          "value": 0.3, // 30% satisfaction (LOW!) ⚠️
          "risk": 1.0, // 100% risk factor
          "weight": 0.25,
          "contribution": 0.25 // 25% contribution to risk
        },
        "last_evaluation": {
          "value": 0.4, // 40% evaluation (POOR!) ⚠️
          "risk": 0.5, // 50% risk factor
          "weight": 0.2,
          "contribution": 0.1 // 10% contribution
        },
        "number_project": {
          "value": 7, // 7 projects (HIGH!) ⚠️
          "risk": 0.7, // 70% risk factor
          "weight": 0.15,
          "contribution": 0.105 // 10.5% contribution
        },
        "average_monthly_hours": {
          "value": 280, // 280 hours/month (EXCESSIVE!) ⚠️
          "risk": 0.8, // 80% risk factor
          "weight": 0.15,
          "contribution": 0.12 // 12% contribution
        },
        "work_accident": {
          "value": true, // Work accident occurred ⚠️
          "risk": 0.3, // 30% risk factor
          "weight": 0.05,
          "contribution": 0.015 // 1.5% contribution
        }
      }
    },
    "recommendations": [
      {
        "category": "Employee Satisfaction",
        "issue": "Low satisfaction level detected",
        "recommendation": "Conduct one-on-one meetings to understand concerns",
        "priority": "high" // HIGH priority action needed!
      },
      {
        "category": "Workload",
        "issue": "Excessive working hours detected",
        "recommendation": "Review workload distribution and consider hiring additional staff",
        "priority": "medium"
      },
      {
        "category": "Safety",
        "issue": "Work accident recorded",
        "recommendation": "Review safety protocols and provide additional training",
        "priority": "medium"
      }
    ]
  }
}
```

### Summary Persentase dan Analisis:

#### 📊 **Probability Scores:**

- **Low Risk**: 10% probability (Employee ID 39)
- **High Risk**: 100% probability (Employee ID 38)

#### 🎯 **Risk Level Classification:**

- **Low**: 0-30% probability
- **Medium**: 31-70% probability
- **High**: 71-100% probability

#### ⚖️ **Weight Distribution:**

1. **Satisfaction Level**: 25% (highest impact)
2. **Last Evaluation**: 20%
3. **Number Projects**: 15%
4. **Monthly Hours**: 15%
5. **Time in Company**: 10%
6. **Promotion History**: 10%
7. **Work Accident**: 5%

#### 🚨 **Critical Risk Factors:**

- Satisfaction < 50% = HIGH RISK
- Monthly hours > 250 = HIGH RISK
- Evaluation < 60% = MEDIUM-HIGH RISK
- No promotion + low satisfaction = COMBINED HIGH RISK

#### 💡 **Recommendation Priorities:**

- **High**: Immediate action required (1-2 weeks)
- **Medium**: Action needed (1-2 months)
- **Low**: Monitor and improve (3-6 months)

---

## 📊 PENJELASAN FORMAT HASIL ML PREDICTION

### 🔢 **Format Hasil: Decimal (0.0-1.0), BUKAN Persen**

#### **Yang Dikembalikan API:**
```json
{
  "probability": 0.1,        // Decimal: 0.1
  "confidence_score": 0.85,  // Decimal: 0.85
  "overall_risk_score": 0.04 // Decimal: 0.04
}
```

#### **Konversi ke Persen:**
```javascript
// Untuk Frontend/Display
probability_percent = probability * 100;     // 0.1 * 100 = 10%
confidence_percent = confidence_score * 100; // 0.85 * 100 = 85%
risk_percent = overall_risk_score * 100;     // 0.04 * 100 = 4%
```

### 📈 **Contoh Konversi Real:**

#### **Employee ID 39 (Low Risk):**
- API: `"probability": 0.1` → **Display: 10%**
- API: `"confidence_score": 0.85` → **Display: 85%**
- API: `"overall_risk_score": 0.04` → **Display: 4%**

#### **Employee ID 38 (High Risk):**
- API: `"probability": 1.0` → **Display: 100%**
- API: `"confidence_score": 0.85` → **Display: 85%**
- API: `"overall_risk_score": 0.63` → **Display: 63%**

### 🎯 **Cara Baca Hasil:**

#### **Probability (Kemungkinan Resign):**
```
0.0 = 0%   (Tidak akan resign)
0.3 = 30%  (Low risk)
0.5 = 50%  (Medium risk)
0.8 = 80%  (High risk)
1.0 = 100% (Sangat tinggi akan resign)
```

#### **Confidence Score (Kepercayaan Model):**
```
0.50 = 50% (Model kurang yakin)
0.70 = 70% (Model cukup yakin)
0.85 = 85% (Model sangat yakin)
0.95 = 95% (Model hampir pasti)
```

#### **Risk Factors (Per Faktor):**
```json
"satisfaction_level": {
  "value": 0.65,        // 65% satisfaction (input data)
  "risk": 0.0,          // 0% risk dari faktor ini
  "weight": 0.25,       // 25% importance dalam model
  "contribution": 0.0   // 0% kontribusi ke total risk
}
```

### 💡 **Untuk Frontend Development:**

#### **JavaScript Conversion:**
```javascript
function convertToPercent(decimal) {
  return Math.round(decimal * 100);
}

// Usage:
const probability = 0.1;
const probabilityPercent = convertToPercent(probability); // 10

// Display:
`${probabilityPercent}% kemungkinan resign`
```

#### **React Component Example:**
```jsx
function PredictionResult({ prediction }) {
  const probabilityPercent = Math.round(prediction.probability * 100);
  const confidencePercent = Math.round(prediction.confidence_score * 100);
  
  return (
    <div>
      <h3>Turnover Risk: {probabilityPercent}%</h3>
      <p>Confidence: {confidencePercent}%</p>
      <p>Risk Level: {prediction.risk_level.toUpperCase()}</p>
    </div>
  );
}
```

### 🚨 **PENTING:**
- **API selalu return decimal** (0.0-1.0)
- **Frontend harus konversi** ke persen untuk display
- **Threshold tetap pakai decimal** dalam logic:
  ```javascript
  if (probability <= 0.3) {
    riskLevel = "LOW";
  } else if (probability <= 0.7) {
    riskLevel = "MEDIUM";
  } else {
    riskLevel = "HIGH";
  }
  ```

---

## 🎯 MAPPING VARIABEL RESPONSE ML PREDICTION UNTUK FRONTEND

### 📊 **VARIABEL UTAMA YANG WAJIB DITAMPILKAN**

#### **1. 🚨 PRIMARY INDICATORS (Wajib di Header/Dashboard)**
```javascript
// Dari response.data.prediction
{
  probability: 0.1,           // → Convert: 10% (Kemungkinan Resign)
  risk_level: "low",          // → Display: LOW RISK badge
  will_leave: false,          // → Show: "✅ Likely to Stay" atau "⚠️ Likely to Leave"
  confidence_score: 0.85      // → Convert: 85% (Kepercayaan Model)
}
```

**Frontend Display:**
```jsx
<div className="main-dashboard">
  <div className="risk-percentage">{Math.round(probability * 100)}%</div>
  <div className={`risk-badge ${risk_level}`}>{risk_level.toUpperCase()} RISK</div>
  <div className="prediction-status">
    {will_leave ? "⚠️ Likely to Leave" : "✅ Likely to Stay"}
  </div>
  <div className="confidence">Model Confidence: {Math.round(confidence_score * 100)}%</div>
</div>
```

#### **2. 👤 EMPLOYEE INFO (Context Header)**
```javascript
// Dari response.data.employee
{
  id: 39,
  name: "Bravely Dirgayuska",
  email: "bravely@company.com",
  department: "Information Technology",
  position: "Sales Representative"
}
```

**Frontend Display:**
```jsx
<div className="employee-header">
  <h2>{employee.name}</h2>
  <p>{employee.position} - {employee.department}</p>
  <span className="employee-id">ID: {employee.id}</span>
</div>
```

#### **3. 📈 RISK ANALYSIS BREAKDOWN (Detail Section)**
```javascript
// Dari response.data.risk_analysis
{
  overall_risk_score: 0.04,  // → Convert: 4% Total Risk Score
  risk_factors: {
    satisfaction_level: {
      value: 0.65,            // → Convert: 65% Satisfaction
      risk: 0.0,              // → Convert: 0% Risk dari faktor ini
      weight: 0.25,           // → Convert: 25% Importance
      contribution: 0.0       // → Convert: 0% Contribution to total risk
    },
    last_evaluation: {
      value: 0.82,            // → Convert: 82% Evaluation Score
      risk: 0.0,
      weight: 0.2,
      contribution: 0.0
    }
    // ... dst untuk semua factors
  }
}
```

**Frontend Display:**
```jsx
<div className="risk-breakdown">
  <h3>Overall Risk Score: {Math.round(overall_risk_score * 100)}%</h3>
  
  {Object.entries(risk_factors).map(([factor, data]) => (
    <div key={factor} className="factor-item">
      <div className="factor-name">
        {factor.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
      </div>
      <div className="factor-metrics">
        <span>Value: {Math.round(data.value * 100)}%</span>
        <span>Risk: {Math.round(data.risk * 100)}%</span>
        <span>Contributes: {Math.round(data.contribution * 100)}%</span>
      </div>
      <div className="progress-bar">
        <div 
          className={`fill ${data.risk > 0.7 ? 'high' : data.risk > 0.3 ? 'medium' : 'low'}`}
          style={{width: `${data.risk * 100}%`}}
        />
      </div>
    </div>
  ))}
</div>
```

#### **4. 💡 RECOMMENDATIONS (Action Items)**
```javascript
// Dari response.data.recommendations
[
  {
    category: "Career Growth",
    issue: "No promotion in the last 5 years",
    recommendation: "Review career progression opportunities and create development plans",
    priority: "medium"
  }
]
```

**Frontend Display:**
```jsx
<div className="recommendations">
  <h3>Action Items</h3>
  {recommendations.map((rec, index) => (
    <div key={index} className={`recommendation priority-${rec.priority}`}>
      <div className="priority-badge">{rec.priority.toUpperCase()}</div>
      <div className="category">{rec.category}</div>
      <div className="issue">Issue: {rec.issue}</div>
      <div className="action">Action: {rec.recommendation}</div>
    </div>
  ))}
</div>
```

### 🔍 PERBEDAAN CONFIDENCE SCORE vs PROBABILITY vs OVERALL RISK SCORE

### 📊 **DEFINISI DAN PERBEDAAN**

#### **1. 🎯 PROBABILITY (Kemungkinan Resign)**
```json
"probability": 0.1  // 10% kemungkinan akan resign
```

**Apa itu:**
- **Hasil prediksi utama** dari model ML
- **Probabilitas karyawan akan resign** (0.0 = tidak resign, 1.0 = pasti resign)
- **Output langsung** dari algoritma machine learning

**Contoh Interpretasi:**
```javascript
probability: 0.1   // → 10% kemungkinan resign (LOW RISK)
probability: 0.5   // → 50% kemungkinan resign (MEDIUM RISK)  
probability: 0.9   // → 90% kemungkinan resign (HIGH RISK)
```

**Frontend Display:**
```jsx
<div className="main-prediction">
  {Math.round(probability * 100)}% chance of leaving
</div>
```

---

#### **2. 🎲 CONFIDENCE SCORE (Kepercayaan Model)**
```json
"confidence_score": 0.85  // 85% model yakin dengan prediksinya
```

**Apa itu:**
- **Seberapa yakin model** dengan prediksi yang dibuat
- **Ukuran reliability** dari hasil prediksi
- **Tidak berkaitan langsung** dengan hasil prediksi, tapi dengan kualitas prediksi

**Contoh Interpretasi:**
```javascript
// Skenario 1: Prediksi Yakin
probability: 0.1,          // 10% kemungkinan resign
confidence_score: 0.95     // 95% model yakin → RELIABLE prediction

// Skenario 2: Prediksi Tidak Yakin  
probability: 0.1,          // 10% kemungkinan resign
confidence_score: 0.45     // 45% model yakin → UNRELIABLE prediction

// Skenario 3: High Risk Yakin
probability: 0.9,          // 90% kemungkinan resign
confidence_score: 0.88     // 88% model yakin → RELIABLE high risk

// Skenario 4: High Risk Tidak Yakin
probability: 0.9,          // 90% kemungkinan resign  
confidence_score: 0.52     // 52% model yakin → UNRELIABLE, perlu data lebih
```

**Frontend Display:**
```jsx
<div className="confidence-indicator">
  <div className="confidence-bar">
    <div style={{width: `${confidence_score * 100}%`}} 
         className={confidence_score >= 0.8 ? 'high-confidence' : 'low-confidence'}>
    </div>
  </div>
  <span>{Math.round(confidence_score * 100)}% model confidence</span>
  {confidence_score < 0.7 && (
    <div className="warning">⚠️ Low confidence - Consider adding more data</div>
  )}
</div>
```

---

#### **3. 📈 OVERALL RISK SCORE (Total Risk Score)**
```json
"overall_risk_score": 0.04  // 4% total risk berdasarkan semua faktor
```

**Apa itu:**
- **Agregasi semua risk factors** yang berkontribusi ke prediksi
- **Sum of weighted contributions** dari setiap faktor risiko
- **Breakdown detail** dari mana probability berasal

**Contoh Perhitungan:**
```javascript
// Breakdown Risk Factors:
risk_factors: {
  satisfaction_level: {
    value: 0.65,           // 65% satisfaction
    risk: 0.0,             // 0% risk dari faktor ini
    weight: 0.25,          // 25% importance
    contribution: 0.0      // 0% × 25% = 0% contribution
  },
  last_evaluation: {
    value: 0.82,           // 82% evaluation
    risk: 0.0,             // 0% risk
    weight: 0.2,           // 20% importance  
    contribution: 0.0      // 0% × 20% = 0% contribution
  },
  promotion_last_5years: {
    value: false,          // No promotion
    risk: 0.4,             // 40% risk dari faktor ini
    weight: 0.1,           // 10% importance
    contribution: 0.04     // 40% × 10% = 4% contribution
  }
  // ... faktor lain
}

// Total Overall Risk Score:
overall_risk_score = sum(all contributions) = 0.04 (4%)
```

**Frontend Display:**
```jsx
<div className="risk-breakdown">
  <h3>Overall Risk Score: {Math.round(overall_risk_score * 100)}%</h3>
  
  <div className="factor-contributions">
    {Object.entries(risk_factors).map(([factor, data]) => (
      <div key={factor} className="factor-item">
        <span className="factor-name">{formatFactorName(factor)}</span>
        <div className="contribution-bar">
          <div 
            style={{width: `${(data.contribution / overall_risk_score) * 100}%`}}
            className="contribution-fill"
          />
        </div>
        <span>{Math.round(data.contribution * 100)}% contribution</span>
      </div>
    ))}
  </div>
</div>
```

---

### 🔄 **HUBUNGAN ANTARA KETIGANYA**

#### **Relationship Model:**
```
Input Data → ML Model → Probability (Main Result)
                   ↓
            Confidence Score (Model certainty)
                   ↓  
         Overall Risk Score (Factor breakdown)
```

#### **Contoh Real Case:**

**Case 1: LOW RISK Employee**
```json
{
  "probability": 0.1,           // 10% kemungkinan resign
  "confidence_score": 0.85,     // 85% model yakin
  "overall_risk_score": 0.04,   // 4% total risk dari semua faktor
  
  // Interpretasi: Model sangat yakin (85%) bahwa karyawan ini hanya 
  // punya 10% kemungkinan resign, dengan total risk score 4%
}
```

**Case 2: HIGH RISK Employee**
```json
{
  "probability": 1.0,           // 100% kemungkinan resign
  "confidence_score": 0.85,     // 85% model yakin  
  "overall_risk_score": 0.63,   // 63% total risk dari semua faktor
  
  // Interpretasi: Model sangat yakin (85%) bahwa karyawan ini akan 
  // resign (100%), dengan banyak faktor risiko (63% total)
}
```

**Case 3: UNCERTAIN Prediction**
```json
{
  "probability": 0.5,           // 50% kemungkinan resign (MEDIUM)
  "confidence_score": 0.45,     // 45% model tidak yakin (LOW!)
  "overall_risk_score": 0.3,    // 30% total risk
  
  // Interpretasi: Model tidak yakin (45%) dengan prediksi 50%, 
  // perlu data tambahan untuk prediksi yang lebih akurat
}
```

---

### 🎯 **KAPAN MENGGUNAKAN MASING-MASING**

#### **1. Probability → MAIN DECISION MAKING**
```jsx
// Primary action berdasarkan probability
if (probability >= 0.7) {
  return <HighRiskAlert employee={employee} />
} else if (probability >= 0.3) {
  return <MediumRiskWarning employee={employee} />
} else {
  return <LowRiskStatus employee={employee} />
}
```

#### **2. Confidence Score → RELIABILITY INDICATOR**
```jsx
// Warning jika confidence rendah
function PredictionReliability({ confidence_score }) {
  if (confidence_score < 0.6) {
    return (
      <div className="low-confidence-warning">
        ⚠️ Low model confidence ({Math.round(confidence_score * 100)}%)
        <p>Consider collecting more performance data for better accuracy</p>
      </div>
    )
  }
  
  return (
    <div className="high-confidence">
      ✅ High confidence prediction ({Math.round(confidence_score * 100)}%)
    </div>
  )
}
```

#### **3. Overall Risk Score → DETAILED ANALYSIS**
```jsx
// Drill-down analysis untuk HR team
function RiskFactorAnalysis({ overall_risk_score, risk_factors }) {
  const sortedFactors = Object.entries(risk_factors)
    .sort((a, b) => b[1].contribution - a[1].contribution)
  
  return (
    <div className="detailed-analysis">
      <h3>Risk Factor Analysis (Total: {Math.round(overall_risk_score * 100)}%)</h3>
      
      {sortedFactors.map(([factor, data]) => (
        <div key={factor} className="factor-detail">
          <span>{formatFactorName(factor)}</span>
          <span>Contributes: {Math.round(data.contribution * 100)}%</span>
          
          {data.contribution > 0.1 && (
            <div className="high-impact-factor">
              🚨 High impact factor - needs attention
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
```

---

### 📊 **DASHBOARD LAYOUT RECOMMENDATIONS**

#### **Visual Hierarchy:**
```jsx
function MLPredictionDashboard({ prediction, risk_analysis }) {
  return (
    <div className="ml-dashboard">
      
      {/* 1. PRIMARY: Probability (Biggest Display) */}
      <div className="primary-result">
        <div className="probability-circle">
          {Math.round(prediction.probability * 100)}%
        </div>
        <div className="risk-level">
          {prediction.risk_level.toUpperCase()} RISK
        </div>
      </div>
      
      {/* 2. SECONDARY: Confidence (Quality Indicator) */}
      <div className="confidence-section">
        <div className="confidence-bar">
          <div style={{width: `${prediction.confidence_score * 100}%`}} />
        </div>
        <span>Model Confidence: {Math.round(prediction.confidence_score * 100)}%</span>
      </div>
      
      {/* 3. TERTIARY: Overall Risk (Detailed Breakdown) */}
      <div className="risk-breakdown">
        <h3>Risk Analysis ({Math.round(risk_analysis.overall_risk_score * 100)}%)</h3>
        {/* Factor details... */}
      </div>
      
    </div>
  )
}
```

---

### 🚨 **INTERPRETASI UNTUK HR TEAM**

#### **Action Matrix:**
```
┌─────────────────┬──────────────────┬────────────────────┐
│ Probability     │ Confidence       │ Recommended Action │
├─────────────────┼──────────────────┼────────────────────┤
│ HIGH (>70%)     │ HIGH (>80%)      │ 🚨 IMMEDIATE ACTION│
│ HIGH (>70%)     │ LOW (<60%)       │ ⚠️ COLLECT MORE DATA│
│ MEDIUM (30-70%) │ HIGH (>80%)      │ 📊 MONITOR CLOSELY │
│ MEDIUM (30-70%) │ LOW (<60%)       │ 📝 REVIEW FACTORS  │
│ LOW (<30%)      │ HIGH (>80%)      │ ✅ MAINTAIN STATUS │
│ LOW (<30%)      │ LOW (<60%)       │ 🔄 UPDATE DATA     │
└─────────────────┴──────────────────┴────────────────────┘
```

#### **Business Logic Example:**
```javascript
function getActionRecommendation(probability, confidence_score) {
  const prob = probability
  const conf = confidence_score
  
  if (prob >= 0.7 && conf >= 0.8) {
    return {
      urgency: "CRITICAL",
      action: "Schedule immediate retention meeting",
      timeline: "Within 1 week"
    }
  }
  
  if (prob >= 0.7 && conf < 0.6) {
    return {
      urgency: "HIGH", 
      action: "Collect more performance data before action",
      timeline: "Within 2 weeks"
    }
  }
  
  if (prob < 0.3 && conf >= 0.8) {
    return {
      urgency: "LOW",
      action: "Continue current management approach", 
      timeline: "Regular review"
    }
  }
  
  // ... other combinations
}
```

Dengan pemahaman ini, frontend developer dan HR team bisa menggunakan setiap metric untuk tujuan yang tepat:

- **Probability** = Keputusan utama
- **Confidence Score** = Validasi kualitas prediksi  
- **Overall Risk Score** = Analisis mendalam untuk action plan
