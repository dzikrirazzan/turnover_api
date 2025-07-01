# 🚀 POSTMAN TESTING GUIDE - Django Turnover Prediction API

## 📁 Files Created

1. **`COMPLETE_API_ENDPOINTS_LIST.md`** - Full documentation dengan semua endpoint
2. **`Django_Turnover_API_Complete.postman_collection.json`** - Postman collection (30 endpoints)
3. **`Django_Turnover_API_Environment.postman_environment.json`** - Environment variables

---

## 🎯 QUICK START (5 Menit)

### 1. **Import ke Postman**

```
1. Buka Postman
2. Click "Import" → pilih file:
   - Django_Turnover_API_Complete.postman_collection.json
   - Django_Turnover_API_Environment.postman_environment.json
3. Set environment ke "Django Turnover API Environment"
```

### 2. **Start Django Server**

```bash
cd /Users/dzikrirazzan/Documents/code/turnover_api/backend
source venv/bin/activate
python manage.py runserver 8000
```

### 3. **Test Login (WAJIB PERTAMA!)**

```
Request: 🔐 Authentication → 2. User Login
Method: POST
URL: http://127.0.0.1:8000/api/auth/login/
Body: {
  "username": "admin",
  "password": "admin123"
}

✅ Pastikan dapat response dengan auth_token!
```

### 4. **Test Core Endpoints**

```
1. 📊 Employee Statistics: GET /api/employees/statistics/
2. 🤖 ML Prediction: POST /api/predictions/predict/
3. 👥 List Employees: GET /api/employees/
4. 🧠 Active Model: GET /api/models/active/
```

---

## 🎯 TESTING PRIORITIES

### **🔥 MUST TEST (Critical)**

1. ✅ **User Login** - Get auth token
2. ✅ **Employee Statistics** - Dashboard metrics
3. ✅ **Single Prediction** - Core ML functionality
4. ✅ **List Employees** - Data access
5. ✅ **Active Model** - ML system status

### **⚡ SHOULD TEST (Important)**

6. ✅ **Bulk Predictions** - Batch processing
7. ✅ **Employee Detail** - Individual records
8. ✅ **Departments** - Organization structure
9. ✅ **Profile Management** - User operations
10. ✅ **Model Management** - ML operations

### **🔧 NICE TO TEST (Enhancement)**

11. ✅ **CRUD Operations** - Create/Update/Delete
12. ✅ **Authentication Flow** - Full auth cycle
13. ✅ **Error Handling** - Edge cases

---

## 📊 EXPECTED RESULTS

### **1. Login Response**

```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User",
    "is_staff": true
  },
  "auth_token": "YWRtaW46YWRtaW4xMjM=",
  "auth_header": "Basic YWRtaW46YWRtaW4xMjM="
}
```

### **2. Employee Statistics**

```json
{
  "total_employees": 15001,
  "total_left": 3570,
  "turnover_rate": 23.8,
  "avg_satisfaction": 0.613,
  "avg_monthly_hours": 201.5,
  "department_stats": {
    "IT": { "total": 1500, "left": 300, "turnover_rate": 20.0 },
    "Sales": { "total": 2000, "left": 600, "turnover_rate": 30.0 }
  },
  "salary_distribution": {
    "low": 7500,
    "medium": 6000,
    "high": 1501
  }
}
```

### **3. ML Prediction Response**

```json
{
  "prediction": true,
  "probability": 0.87,
  "confidence": 0.74,
  "risk_level": "High",
  "recommendations": ["Consider conducting a satisfaction survey and addressing concerns", "Employee may be overworked - consider workload redistribution", "Review compensation package"]
}
```

### **4. Active Model Info**

```json
{
  "id": 1,
  "name": "csv_model_v1",
  "model_type": "RandomForest",
  "accuracy": 0.991,
  "is_active": true,
  "created_at": "2025-06-23T10:30:00Z"
}
```

---

## 🧪 TESTING SCENARIOS

### **Scenario 1: HR Dashboard Load**

```
1. Login → Get auth token
2. Employee Statistics → Dashboard overview
3. List Employees → Employee data
4. List Departments → Organization structure
5. Active Model → ML system status
```

### **Scenario 2: ML Prediction Workflow**

```
1. Single Prediction (High Risk) → Test high-risk employee
2. Single Prediction (Low Risk) → Test low-risk employee
3. Bulk Predictions → Test batch processing
4. Prediction History → View past predictions
```

### **Scenario 3: Employee Management**

```
1. List Employees → View all employees
2. Get Specific Employee → Individual details
3. Create Employee → Add new record
4. Update Employee → Modify record
5. Predict Turnover → Individual prediction
```

### **Scenario 4: System Administration**

```
1. List ML Models → View available models
2. Train New Model → Create new ML model
3. Activate Model → Switch active model
4. User Profile → Manage user account
```

---

## 🔍 DEBUGGING TIPS

### **Common Issues:**

#### **1. 401 Unauthorized**

```
Problem: Missing atau invalid auth token
Solution:
- Test login endpoint dulu
- Copy auth_token dari response
- Pastikan format: "Basic [token]"
```

#### **2. 404 Not Found**

```
Problem: Wrong endpoint URL
Solution:
- Check base_url: http://127.0.0.1:8000
- Ensure server running: python manage.py runserver 8000
- Check endpoint path di documentation
```

#### **3. 400 Bad Request**

```
Problem: Invalid request body
Solution:
- Check JSON format
- Verify required fields
- Check field data types (string vs number)
```

#### **4. 500 Internal Server Error**

```
Problem: Server error
Solution:
- Check Django server logs
- Verify ML model is active
- Check database connection
```

---

## 📈 SUCCESS METRICS

### **✅ Passing Criteria:**

- **Authentication**: 100% success (7/7 endpoints)
- **Employee Management**: 90%+ success (12/14 endpoints)
- **ML Predictions**: 100% success (5/5 endpoints)
- **Model Management**: 100% success (5/5 endpoints)

### **🎯 Expected Results:**

- **Total Endpoints**: 30
- **Success Rate**: 90%+
- **Critical Endpoints**: 100% working
- **Response Time**: < 2 seconds
- **Data Quality**: Complete and accurate

---

## 🚀 PRODUCTION CHECKLIST

### **Before Go-Live:**

- [ ] All critical endpoints working
- [ ] Authentication system secure
- [ ] ML model accuracy > 99%
- [ ] Data validation working
- [ ] Error handling proper
- [ ] Performance acceptable
- [ ] Documentation complete

### **Production URLs:**

```
Development: http://127.0.0.1:8000
Staging: https://staging-api.company.com
Production: https://api.company.com
```

---

## 📞 SUPPORT

### **If Issues:**

1. Check server status: `python manage.py runserver 8000`
2. Check logs: `tail -f logs/django.log`
3. Test basic connectivity: `curl http://127.0.0.1:8000/admin/`
4. Verify database: `python manage.py shell`

### **Quick Fixes:**

```bash
# Restart server
python manage.py runserver 8000

# Check model status
python manage.py shell
>>> from predictions.models import MLModel
>>> MLModel.objects.filter(is_active=True)

# Activate model if needed
python -c "
from predictions.models import MLModel
model = MLModel.objects.first()
if model: model.is_active = True; model.save()
"
```

---

**🎯 Total: 30 Endpoints | Expected Success: 90%+ | Ready for Production!**

**Happy Testing! 🚀**
