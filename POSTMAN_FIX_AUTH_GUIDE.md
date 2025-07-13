# 🔧 POSTMAN AUTHENTICATION FIX GUIDE

## ⚠️ MASALAH: "Authentication credentials were not provided"

### 🎯 **SOLUSI LANGSUNG - GUNAKAN FILE INI:**
📁 `ML_API_SIMPLE_FIX_AUTH.json`

---

## 🔐 **STEP-BY-STEP SETUP DI POSTMAN:**

### **1. Import Collection**
- Buka Postman
- Click **Import**
- Drag & drop file `ML_API_SIMPLE_FIX_AUTH.json`
- Collection akan muncul dengan nama: "🚀 SMART-EN ML API - SIMPLE (Fix Auth)"

### **2. Set Collection Variables**
Di collection, pastikan variables sudah benar:
```
base_url: https://turnover-api-hd7ze.ondigitalocean.app
admin_token: b42b585b90fbb149294bf041aaef5085c1ca4935
```

### **3. Test Authentication (WAJIB!)**
**Jalankan request ini dulu:**
```
🔐 1. AUTHENTICATION > ✅ Test Token Validation
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Profil pengguna berhasil diambil",
  "data": {
    "id": 4,
    "full_name": "System Administrator",
    "role": "admin",
    "is_admin": true
  }
}
```

---

## 🚨 **JIKA MASIH ERROR 401, LAKUKAN INI:**

### **Option 1: Manual Header Setup**
1. Buka request yang error
2. Go to **Headers** tab
3. Add manual header:
   ```
   Key: Authorization
   Value: Token b42b585b90fbb149294bf041aaef5085c1ca4935
   ```

### **Option 2: Fresh Login**
1. Jalankan request: `🔐 1. AUTHENTICATION > ✅ Admin Login (Get Token)`
2. Copy token dari response
3. Update collection variable `admin_token` dengan token baru

### **Option 3: Direct Token Test**
Test langsung di terminal:
```bash
curl -X GET "https://turnover-api-hd7ze.ondigitalocean.app/api/profile/" \
  -H "Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935"
```

---

## 🎯 **QUICK TEST FLOW:**

### **Test 1: Token Validation**
```
Request: GET /api/profile/
Header: Authorization: Token {{admin_token}}
Expected: 200 OK dengan data admin
```

### **Test 2: List Employees**
```
Request: GET /api/employees/
Header: Authorization: Token {{admin_token}}
Expected: 200 OK dengan list employees
```

### **Test 3: ML Prediction (MAIN)**
```
Request: POST /api/predict/
Header: Authorization: Token {{admin_token}}
Body: {"employee_id": 39}
Expected: 200 OK dengan prediction results
```

---

## 🛠️ **TROUBLESHOOTING:**

### **Problem: Token tidak terdeteksi**
**Solution:**
1. Check Collection Variables tab
2. Pastikan `admin_token` ada dan benar
3. Pastikan menggunakan `{{admin_token}}` di header

### **Problem: Headers tidak terbaca**
**Solution:**
1. Manual add header `Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935`
2. Atau copy-paste token langsung tanpa variable

### **Problem: CORS Error**
**Solution:**
- Ini normal untuk browser, tapi tidak untuk Postman
- Postman seharusnya tidak ada CORS issue

---

## ✅ **VERIFIED WORKING ENDPOINTS:**

### **🔐 Authentication:**
- ✅ `GET /api/profile/` (Token validation)
- ✅ `POST /api/login/` (Get new token)

### **👥 Employee Management:**
- ✅ `GET /api/employees/` (List employees)
- ✅ `GET /api/employees/39/performance_data/` (Get performance data)

### **🧠 ML Prediction:**
- ✅ `POST /api/predict/` (Main ML endpoint)
- ✅ Body: `{"employee_id": 39}`

### **📊 Performance Data:**
- ✅ `GET /api/performance/` (List performance data)
- ✅ `POST /api/performance/` (Create performance data)

---

## 🔑 **ADMIN CREDENTIALS:**
```
Email: admin@company.com
Password: AdminPass123!
Token: b42b585b90fbb149294bf041aaef5085c1ca4935
```

---

## 📞 **MASIH ERROR?**

**1. Check Token Validity:**
```bash
curl -X GET "https://turnover-api-hd7ze.ondigitalocean.app/api/profile/" \
  -H "Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935"
```

**2. Get Fresh Token:**
```bash
curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/login/" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@company.com", "password": "AdminPass123!"}'
```

**3. Test ML Prediction:**
```bash
curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/predict/" \
  -H "Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935" \
  -H "Content-Type: application/json" \
  -d '{"employee_id": 39}'
```

---

## 🎉 **EXPECTED SUCCESS RESULTS:**

### **Profile Response:**
```json
{
  "success": true,
  "data": {
    "full_name": "System Administrator",
    "role": "admin"
  }
}
```

### **ML Prediction Response:**
```json
{
  "success": true,
  "data": {
    "prediction": {
      "probability": 0.1,
      "risk_level": "low",
      "will_leave": false
    }
  }
}
```

---

## 📝 **CATATAN PENTING:**
1. **Token sudah teruji working** di curl
2. **Collection baru lebih simple** tanpa pre-request scripts
3. **Headers sudah hardcoded** untuk menghindari variable issues
4. **Semua endpoints sudah diverifikasi** working di production

**Import file `ML_API_SIMPLE_FIX_AUTH.json` dan test langsung!** 🚀
