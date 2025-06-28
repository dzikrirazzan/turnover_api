# 🔗 FRONTEND-BACKEND CONNECTION GUIDE

## 🎯 Frontend: https://smart-en-system.vercel.app/
## 🚀 Backend: https://octopus-app.ondigitalocean.app/

## ✅ UPDATED ENVIRONMENT VARIABLES FOR DIGITALOCEAN:

### **CORS Configuration (CRITICAL!):**
```bash
CORS_ALLOWED_ORIGINS=https://smart-en-system.vercel.app,https://octopus-app.ondigitalocean.app,http://localhost:3000
```

### **Complete Environment Variables for DigitalOcean:**
```bash
DEBUG=False
SECRET_KEY=django-insecure-production-smarten-2025-change-this-32chars
ALLOWED_HOSTS=octopus-app.ondigitalocean.app,*.ondigitalocean.app

MYSQL_DATABASE=defaultdb
MYSQL_USER=doadmin
MYSQL_PASSWORD=YOUR_DATABASE_PASSWORD
MYSQL_HOST=YOUR_DATABASE_HOST
MYSQL_PORT=25060

DATABASE_URL=mysql://doadmin:YOUR_PASSWORD@YOUR_HOST:25060/defaultdb?ssl-mode=REQUIRED

CORS_ALLOWED_ORIGINS=https://smart-en-system.vercel.app,https://octopus-app.ondigitalocean.app,http://localhost:3000

STATIC_URL=/static/
STATIC_ROOT=staticfiles
LOG_LEVEL=INFO
MYSQL_SSL_MODE=REQUIRED
```

## 🔧 FRONTEND CONFIGURATION UPDATE NEEDED:

### **Update API Base URL di Frontend:**
Ganti dari localhost ke:
```javascript
const API_BASE_URL = "https://octopus-app.ondigitalocean.app"
```

### **Authentication Headers:**
```javascript
const auth = {
  username: "admin",
  password: "admin123"
}

// Untuk fetch requests:
headers: {
  'Authorization': 'Basic ' + btoa('admin:admin123'),
  'Content-Type': 'application/json'
}
```

## 🎯 ENDPOINT EXAMPLES FOR FRONTEND:

### **Dashboard API:**
```javascript
// Dashboard stats
GET https://octopus-app.ondigitalocean.app/performance/api/dashboard/stats/?employee=45002

// Analytics dashboard
GET https://octopus-app.ondigitalocean.app/performance/api/analytics/dashboard/

// Goals statistics
GET https://octopus-app.ondigitalocean.app/performance/api/goals/statistics/?employee=45002
```

### **Authentication Test:**
```javascript
fetch('https://octopus-app.ondigitalocean.app/api/employees/', {
  headers: {
    'Authorization': 'Basic ' + btoa('admin:admin123')
  }
})
```

## 🚀 DEPLOYMENT CHECKLIST:

### **1. DigitalOcean Backend:**
- ✅ Set CORS_ALLOWED_ORIGINS dengan smart-en-system.vercel.app
- ✅ Deploy dengan database MySQL cluster
- ✅ Test endpoints dengan curl

### **2. Vercel Frontend:**
- ✅ Update API_BASE_URL ke octopus-app.ondigitalocean.app
- ✅ Test connection ke backend
- ✅ Verify authentication works

### **3. Test End-to-End:**
```bash
# Backend test
curl -u admin:admin123 https://octopus-app.ondigitalocean.app/api/employees/

# Frontend access
https://smart-en-system.vercel.app/
```

## 📊 PRODUCTION SYSTEM ARCHITECTURE:

```
Frontend (Vercel)
https://smart-en-system.vercel.app/
         ↓ API Calls
Backend (DigitalOcean)
https://octopus-app.ondigitalocean.app/
         ↓ Database Connection
MySQL Cluster (DigitalOcean)
turnover-db-do-user-22843561-0.d.db.ondigitalocean.com:25060
```

## 🎉 FULL STACK SMART-EN SYSTEM:

**Frontend**: React/Next.js di Vercel
**Backend**: Django REST API di DigitalOcean  
**Database**: MySQL Cluster di DigitalOcean
**Features**: 30+ APIs, ML Prediction, 15K+ employees

**Ready for production! 🚀**
