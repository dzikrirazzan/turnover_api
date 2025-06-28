# DigitalOcean App Platform Alternative Configuration

## If app.yaml doesn't work, use Manual Configuration:

### 1. **Don't use app.yaml** - Let DigitalOcean auto-detect

### 2. **Manual App Creation:**

**Service Configuration:**
- **Name**: smart-en-backend
- **Source**: GitHub - dzikrirazzan/turnover_api
- **Branch**: main  
- **Source Directory**: `backend`
- **Autodeploy**: Yes

**Build & Run Settings:**
- **Build Command**: `pip install -r requirements.txt`
- **Run Command**: `gunicorn --worker-tmp-dir /dev/shm turnover_prediction.wsgi:application`
- **HTTP Port**: 8080

**Environment Variables:**
```
DEBUG=False
SECRET_KEY=your-32-char-secret-key
ALLOWED_HOSTS=${APP_DOMAIN}
DATABASE_URL=${DATABASE_URL}
CORS_ALLOWED_ORIGINS=https://your-domain.com
```

### 3. **Database Configuration:**
- **Engine**: MySQL
- **Version**: 8
- **Size**: Basic ($15/month)
- **Name**: smart-en-db

### 4. **Alternative: Skip app.yaml entirely**
Delete the `.do/app.yaml` file and let DigitalOcean auto-detect the Python Django project.

This often works better than YAML configuration.
