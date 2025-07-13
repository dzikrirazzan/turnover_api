# 🚀 DEPLOYMENT COMMANDS FOR DIGITALOCEAN

## ✅ CORRECT DEPLOYMENT SEQUENCE

Jalankan commands ini **berurutan** di console DigitalOcean:

### 1. Setup Environment
```bash
# Navigate to backend directory
cd /var/www/turnover_api/backend

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser (optional - only if needed)
python manage.py createsuperuser
```

### 3. Static Files
```bash
# Collect static files
python manage.py collectstatic --noinput
```

### 4. ML Model Training
```bash
# Train ML model from CSV data
python manage.py train_model_from_csv
```

### 5. Production Setup
```bash
# Setup production data and configurations
python manage.py setup_production
```

### 6. Restart Service
```bash
# Restart the application
sudo systemctl restart turnover_api
# or
sudo service turnover_api restart
```

---

## 📋 DETAILED EXPLANATION

### Command 1: `pip install -r requirements.txt`
- ✅ **Correct** - Installs all Python dependencies
- Pastikan file `requirements.txt` ada di backend directory

### Command 2: `python manage.py migrate`
- ✅ **Correct** - Runs database migrations
- Creates all necessary tables in database

### Command 3: `python manage.py collectstatic --noinput`
- ✅ **Correct** - Collects static files for production
- `--noinput` prevents interactive prompts

### Command 4: `python manage.py train_model_from_csv`
- ✅ **Correct** - This command exists in your codebase
- Trains ML model using CSV data from `ml_data/training_data.csv`

### Command 5: `python manage.py setup_production`
- ✅ **Correct** - This command exists in your codebase
- Sets up production environment and seed data

---

## 🔧 ADDITIONAL COMMANDS (Optional)

### Check Status
```bash
# Check if manage.py is working
python manage.py check

# Check available commands
python manage.py help
```

### Seed Data (if needed)
```bash
# Create sample departments and users
python manage.py seed_data
```

### Fix Database Issues (if any)
```bash
# Fix production database issues
python manage.py fix_production_db
```

---

## 🌍 ENVIRONMENT VARIABLES

Make sure these are set in your DigitalOcean environment:

```bash
# Check current environment
echo $DJANGO_SETTINGS_MODULE
echo $DEBUG
echo $DATABASE_URL
```

---

## 🚨 TROUBLESHOOTING

### If Migration Fails:
```bash
# Check migration status
python manage.py showmigrations

# Reset migrations (DANGER - only if needed)
python manage.py migrate predictions zero
python manage.py migrate
```

### If Static Files Fail:
```bash
# Check static files settings
python manage.py collectstatic --dry-run

# Force collect static files
python manage.py collectstatic --noinput --clear
```

### If ML Training Fails:
```bash
# Check if CSV file exists
ls -la ml_data/training_data.csv

# Check ML training command
python manage.py train_model_from_csv --help
```

---

## ✅ FINAL CHECK

After running all commands, test the endpoints:

```bash
# Test health check
curl https://turnover-api-hd7ze.ondigitalocean.app/api/health/

# Test API info
curl https://turnover-api-hd7ze.ondigitalocean.app/api/info/

# Test ML prediction (with auth)
curl -X POST https://turnover-api-hd7ze.ondigitalocean.app/api/predict/ \
  -H "Authorization: Token YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"employee_id": 1}'
```

---

## 🎯 SUMMARY

**Your commands are CORRECT!** Here's the exact sequence:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py train_model_from_csv
python manage.py setup_production
```

**Plus restart the service:**
```bash
sudo systemctl restart turnover_api
```

**All commands exist and will work perfectly!** 🎉
