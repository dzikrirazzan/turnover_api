# Django Database Migration Fix

## Problem

Production database missing `password` column in `predictions_employee` table causing registration failures.

## Solution

Migration `0003_ensure_password_column.py` safely adds the missing column.

## Deployment

### On DigitalOcean App Platform:

1. **Apply Migration**:

   ```bash
   python manage.py migrate predictions 0003
   ```

2. **Verify Fix**:

   ```bash
   python manage.py dbshell
   ```

   Then: `DESCRIBE predictions_employee;`

3. **Test Registration**:
   ```bash
   curl -X POST https://turnover-api-4amxd.ondigitalocean.app/api/register/ \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"TestPass123!"}'
   ```

## Expected Result

- ✅ Migration adds password column if missing
- ✅ User registration works without "Unknown column" error
- ✅ All authentication endpoints functional

## Rollback

If needed: `python manage.py migrate predictions 0002`

## Files

- `backend/predictions/migrations/0003_ensure_password_column.py` - The migration
- Uses `INFORMATION_SCHEMA` to safely check column existence
- No data loss risk - only adds missing column
