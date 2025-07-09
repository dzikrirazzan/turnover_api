# 🚨 Postman CSRF Troubleshooting Guide

## 🔍 Masalah

Test script menunjukkan CSRF fix sudah bekerja, tapi Postman masih error:

```
"detail": "CSRF Failed: Referer checking failed - no Referer."
```

## 🛠️ Solusi Step-by-Step

### **Step 1: Clear Postman Cache**

1. **Close Postman completely**
2. **Clear browser cache** (jika menggunakan Postman web)
3. **Restart Postman**
4. **Clear collection cache**:
   - File → Settings → General
   - Scroll down to "Cache"
   - Click "Clear Cache"

### **Step 2: Check Postman Headers**

**Pastikan headers di Postman:**

```
Content-Type: application/json
User-Agent: PostmanRuntime/7.32.3
```

**JANGAN tambahkan header ini:**

- ❌ `X-CSRFToken`
- ❌ `Referer` (biarkan Postman set otomatis)
- ❌ `Origin` (biarkan Postman set otomatis)

### **Step 3: Test dengan Data Minimal**

**Gunakan data minimal dulu:**

```json
{
  "email": "test.minimal@smarten.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "Test",
  "last_name": "Minimal",
  "department": 1,
  "position": "Developer"
}
```

### **Step 4: Check Postman Version**

1. **Help → About Postman**
2. **Pastikan versi terbaru**
3. **Update jika perlu**

### **Step 5: Test dengan Different Postman Client**

**Jika menggunakan Postman Desktop:**

- Coba Postman Web: https://web.postman.com

**Jika menggunakan Postman Web:**

- Coba Postman Desktop

### **Step 6: Check Network Tab**

1. **Open Developer Tools** (F12)
2. **Network tab**
3. **Send request di Postman**
4. **Check request headers** yang dikirim
5. **Look for Referer header**

### **Step 7: Compare dengan Test Script**

**Test script yang bekerja:**

```python
headers = {
    "Content-Type": "application/json",
    "User-Agent": "PostmanRuntime/7.32.3"
}
```

**Pastikan Postman mengirim headers yang sama**

## 🔧 Advanced Troubleshooting

### **Step 8: Check Environment Variables**

**Pastikan di DigitalOcean:**

```
CSRF_TRUSTED_ORIGINS=https://smart-en-system.vercel.app,https://turnover-api-hd7ze.ondigitalocean.app,https://postman.com,https://www.postman.com,https://app.postman.com,http://localhost:3000,http://127.0.0.1:3000
```

### **Step 9: Force Deploy**

**Di DigitalOcean dashboard:**

1. Go to App Platform
2. Select turnover-api app
3. Click "Deploy" untuk force redeploy

### **Step 10: Check Deployment Status**

**Monitor deployment:**

- Check logs di DigitalOcean
- Wait 2-3 minutes setelah deploy
- Test lagi

## 🎯 Quick Fix Commands

### **Test API Status:**

```bash
python3 check_production_status.py
```

### **Test CSRF Fix:**

```bash
python3 test_correct_data.py
```

### **Debug Headers:**

```bash
python3 debug_postman_headers.py
```

## 📊 Expected Results

**Jika CSRF fix bekerja:**

- ✅ Status 201 (Created)
- ✅ Response: `{"success":true,"message":"Registrasi berhasil",...}`
- ❌ NO CSRF error

**Jika masih error:**

- ❌ Status 403 (Forbidden)
- ❌ Response: `{"detail": "CSRF Failed: Referer checking failed - no Referer."}`

## 🚨 Common Issues

### **Issue 1: Postman Cache**

- **Solution**: Clear cache dan restart Postman

### **Issue 2: Wrong Headers**

- **Solution**: Gunakan headers minimal saja

### **Issue 3: Environment Variables**

- **Solution**: Update CSRF_TRUSTED_ORIGINS di DigitalOcean

### **Issue 4: Deployment Not Complete**

- **Solution**: Wait 2-3 minutes dan test lagi

## 📞 Support

**Jika masih error:**

1. **Check Postman version**
2. **Clear all cache**
3. **Use minimal headers**
4. **Test dengan data minimal**
5. **Check DigitalOcean deployment status**

**Status**: 🔧 **NEEDS POSTMAN TROUBLESHOOTING**
