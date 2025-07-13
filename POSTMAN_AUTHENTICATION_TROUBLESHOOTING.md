# 🔧 TROUBLESHOOTING AUTHENTICATION POSTMAN

## ❌ Problem: "Authentication credentials were not provided"

### 🔍 Kemungkinan Penyebab:
1. **Token tidak ada atau salah**
2. **Header Authorization tidak diset**
3. **Format token salah**
4. **Token expired atau invalid**

### ✅ Solusi Step-by-Step:

#### 1. **Import Collection Baru**
```
File: ML_ENDPOINTS_POSTMAN_COMPLETE.json
```

#### 2. **Pastikan Variables Collection Diset**
- `base_url`: `https://turnover-api-hd7ze.ondigitalocean.app`
- `admin_token`: `b42b585b90fbb149294bf041aaef5085c1ca4935`
- `admin_email`: `admin@company.com`
- `admin_password`: `AdminPass123!`

#### 3. **Langkah Testing yang Benar:**

**Step 1: Login Admin**
```
POST /api/login/
Body: {
  "email": "admin@company.com",
  "password": "AdminPass123!"
}
```

**Step 2: Verify Token**
```
GET /api/profile/
Headers: Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935
```

**Step 3: Test ML Prediction**
```
POST /api/predict/
Headers: Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935
Body: {
  "employee_id": 39
}
```

### 🛠️ Manual Header Setup (jika automation gagal):

1. **Buka Postman Request**
2. **Go to Headers tab**
3. **Add header:**
   - Key: `Authorization`
   - Value: `Token b42b585b90fbb149294bf041aaef5085c1ca4935`
4. **Add header:**
   - Key: `Content-Type`
   - Value: `application/json`

### 🔄 Token Validation Commands:

```bash
# Test token manual
curl -X GET "https://turnover-api-hd7ze.ondigitalocean.app/api/profile/" \
  -H "Authorization: Token b42b585b90fbb149294bf041aaef5085c1ca4935"

# Test login manual
curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/login/" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@company.com", "password": "AdminPass123!"}'
```

### 🎯 Quick Fix Checklist:

- [ ] Collection variables diset dengan benar
- [ ] Token format: `Token <token_value>` (bukan `Bearer`)
- [ ] Header Authorization ada di setiap request
- [ ] Admin user exists dan aktif
- [ ] API server running di DigitalOcean
- [ ] No typos dalam token atau email

### 📋 Collection Features:

1. **Auto-token management** - Token otomatis disimpan setelah login
2. **Error handling** - Pesan error yang jelas
3. **Pre-request scripts** - Token otomatis ditambahkan ke header
4. **Validation tests** - Test authentication dan input validation
5. **Scenario testing** - Low, medium, high risk scenarios
6. **Comprehensive logging** - Detailed console output

### 🚀 Ready-to-Use Endpoints:

1. **🔐 Authentication** - Login dan token validation
2. **🏥 Health Check** - API status dan info
3. **👥 Employee Management** - List employees, statistics
4. **📊 Performance Data** - CRUD operations untuk ML data
5. **🧠 ML Prediction** - Main prediction endpoint
6. **🔬 Testing** - Validation dan error handling
7. **📈 Scenarios** - Low/medium/high risk testing

### 💡 Pro Tips:

- Run "Admin Login" first untuk setup token
- Use "List All Employees" untuk auto-set test employee ID
- Create performance data sebelum prediction
- Check console logs untuk detailed hasil
- Use scenarios untuk testing different risk levels

**🎯 Collection Status: READY FOR TESTING!**
