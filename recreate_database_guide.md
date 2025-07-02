# Recreate DigitalOcean Managed Database - Panduan Lengkap

## Mengapa Recreate Database?

- Local development berjalan normal, production error karena schema mismatch
- Production database missing AbstractUser columns (last_login, is_superuser, etc.)
- Belum ada data penting yang akan hilang
- Migration AbstractUser di production seringkali bermasalah

## Langkah 1: Backup Data (Opsional)

Jika ada data yang ingin disimpan:

```bash
# Backup dari production (jika diperlukan)
pg_dump -h your-db-host -U your-username -d your-database > backup.sql
```

## Langkah 2: Recreate Database di DigitalOcean

### A. Via DigitalOcean Control Panel:

1. Login ke DigitalOcean dashboard
2. Go to Databases → Your Database Cluster
3. Settings → Destroy Database
4. Create new database cluster dengan nama yang sama
5. Update connection string jika berubah

### B. Via DigitalOcean CLI (doctl):

```bash
# List existing databases
doctl databases list

# Delete existing database
doctl databases delete <database-id>

# Create new database
doctl databases create <name> --engine postgres --version 14 --region nyc1 --size db-s-1vcpu-1gb
```

## Langkah 3: Update Environment Variables

Check dan update DATABASE_URL di App Platform jika berubah:

```bash
# Check current environment
doctl apps list
doctl apps spec get <app-id>
```

## Langkah 4: Deploy dengan Fresh Database

```bash
# Push ke production untuk trigger deploy
git add .
git commit -m "Deploy with fresh database schema"
git push origin main

# Monitor deployment
doctl apps list
```

## Langkah 5: Verify Schema

Test registration endpoint:

```bash
curl -X POST https://turnover-api-hd7ze.ondigitalocean.app/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

## Expected Result:

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User"
  }
}
```

## Keuntungan Recreate Database:

✅ **Schema konsisten**: Database baru akan match dengan model Django
✅ **Tidak ada legacy issues**: Bersih dari masalah migration sebelumnya  
✅ **Waktu lebih cepat**: Daripada debug migration kompleks
✅ **Risk rendah**: Tidak ada data penting yang hilang
✅ **Future-proof**: Foundation yang solid untuk development selanjutnya

## Jika Ada Masalah:

1. **Connection string berubah**: Update di App Platform environment
2. **Deploy gagal**: Check logs dengan `doctl apps logs <app-id>`
3. **Schema masih error**: Re-run migrations manual

## Alternative: Manual Migration (Tidak Disarankan)

Jika tetap ingin pakai database existing:

```bash
# Login ke production database
psql "postgresql://username:password@host:port/database"

# Manual add columns
ALTER TABLE predictions_employee ADD COLUMN last_login timestamp;
ALTER TABLE predictions_employee ADD COLUMN is_superuser boolean DEFAULT false;
# ... dll
```

**Tapi recreate database jauh lebih aman dan efisien!**
