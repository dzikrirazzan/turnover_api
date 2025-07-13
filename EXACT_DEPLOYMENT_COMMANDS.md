# 🚀 DEPLOYMENT COMMANDS - DIGITALOCEAN CONSOLE

## ✅ COMMAND SEQUENCE YANG BENAR

**Copy-paste commands ini satu per satu ke console DigitalOcean:**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run database migrations
python manage.py migrate

# 3. Collect static files
python manage.py collectstatic --noinput

# 4. Train ML model from CSV (FIXED!)
python manage.py train_model_from_csv

# 5. Setup production environment
python manage.py setup_production

# 6. Restart the service (IMPORTANT!)
sudo systemctl restart turnover_api
```

## 🔧 FIXED THE ML TRAINING ERROR!

**Problem:** CSV file had column name mismatches:
- CSV: `average_montly_hours` (typo)
- Code expected: `average_monthly_hours`
- CSV: `Work_accident` (capital W)
- Code expected: `work_accident`

**Solution:** Updated `ml_utils.py` to automatically map column names.

---

## 📋 PENJELASAN SETIAP COMMAND

### 1. `pip install -r requirements.txt`
- ✅ Install semua Python packages yang dibutuhkan
- Termasuk: Django, Django REST Framework, scikit-learn, pandas, dll.

### 2. `python manage.py migrate`
- ✅ Membuat dan update database tables
- Menjalankan migrations untuk predictions app dan performance app

### 3. `python manage.py collectstatic --noinput`
- ✅ Mengumpulkan static files (CSS, JS, images)
- `--noinput` = tidak ada prompt interaktif

### 4. `python manage.py train_model_from_csv`
- ✅ Melatih ML model menggunakan data CSV
- Membaca file `ml_data/training_data.csv`
- Menyimpan trained model untuk prediction

### 5. `python manage.py setup_production`
- ✅ Setup environment production
- Membuat admin user dan sample data
- Konfigurasi production settings

### 6. `sudo systemctl restart turnover_api`
- ✅ Restart service untuk apply semua perubahan
- **PENTING**: Tanpa ini, perubahan tidak akan aktif!

---

## 🔧 ADDITIONAL COMMANDS (Optional)

### Check Status Commands:
```bash
# Check if everything is working
python manage.py check

# Check database status
python manage.py showmigrations

# Check available commands
python manage.py help

# Check service status
sudo systemctl status turnover_api
```

### If There Are Issues:
```bash
# Check logs
sudo journalctl -u turnover_api -f

# Check error logs
tail -f /var/log/turnover_api/error.log

# Force restart
sudo systemctl stop turnover_api
sudo systemctl start turnover_api
```

---

## 🎯 QUICK TEST AFTER DEPLOYMENT

Setelah menjalankan semua commands, test endpoints ini:

```bash
# 1. Health check
curl https://turnover-api-hd7ze.ondigitalocean.app/api/health/

# 2. API info
curl https://turnover-api-hd7ze.ondigitalocean.app/api/info/

# 3. Test login (use admin credentials from setup_production)
curl -X POST https://turnover-api-hd7ze.ondigitalocean.app/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@company.com", "password": "AdminPass123!"}'
```

---

## 🚨 TROUBLESHOOTING

### Jika ada error pada command tertentu:

**Error pada `pip install`:**
```bash
# Update pip first
pip install --upgrade pip
pip install -r requirements.txt
```

**Error pada `migrate`:**
```bash
# Check database connection
python manage.py dbshell
# Or reset migrations (CAREFUL!)
python manage.py migrate predictions zero
python manage.py migrate
```

**Error pada `collectstatic`:**
```bash
# Check static files settings
python manage.py collectstatic --dry-run
# Force collect
python manage.py collectstatic --noinput --clear
```

**Error pada `train_model_from_csv`:**
```bash
# Check if CSV file exists
ls -la ml_data/training_data.csv
# Check command details
python manage.py train_model_from_csv --help
```

**Error pada `setup_production`:**
```bash
# Check command details
python manage.py setup_production --help
# Or run individual setup commands
python manage.py seed_data
```

---

## 🎉 EXPECTED RESULTS

Setelah menjalankan semua commands, Anda akan mendapatkan:

1. ✅ **Database** dengan semua tables
2. ✅ **ML Model** yang sudah dilatih
3. ✅ **Admin user** dengan kredensial:
   - Email: `admin@company.com`
   - Password: `AdminPass123!`
4. ✅ **Sample departments** dan data
5. ✅ **Static files** untuk production
6. ✅ **All API endpoints** berfungsi termasuk:
   - `/api/health/`
   - `/api/login/`
   - `/api/register/`
   - `/api/predict/` (NEW!)
   - `/api/performance/`

---

## 🌟 FINAL VERIFICATION

**Run this command untuk memastikan semua OK:**

```bash
# Check all endpoints
curl https://turnover-api-hd7ze.ondigitalocean.app/api/health/ && echo "✅ Health OK"
curl https://turnover-api-hd7ze.ondigitalocean.app/api/info/ && echo "✅ API Info OK"
```

**Commands Anda 100% BENAR!** 🎯

Copy-paste satu per satu dan tunggu sampai selesai sebelum menjalankan yang berikutnya.
