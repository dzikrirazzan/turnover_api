#!/bin/bash
# Deploy the AbstractUser columns fix to production

echo "🔧 Applying AbstractUser Columns Fix Migration"
echo "=============================================="
echo ""
echo "❌ CONFIRMED: Registration failing with 'Unknown column last_login' error"
echo "🔍 Database schema is missing essential AbstractUser columns"
echo ""
echo "📋 This migration will add missing AbstractUser columns:"
echo "   - last_login (DATETIME)"
echo "   - is_superuser (BOOLEAN)"
echo "   - is_staff (BOOLEAN)" 
echo "   - is_active (BOOLEAN)"
echo "   - date_joined (DATETIME)"
echo "   - password (if still missing)"
echo ""
echo "🚀 REQUIRED ACTION - Run this command on DigitalOcean App Platform:"
echo ""
echo "   python manage.py migrate predictions 0004"
echo ""
echo "📊 This should resolve the 'Unknown column last_login' error"
echo "   and ensure full user registration functionality."
echo ""
echo "✅ After migration, test registration with:"
echo '   curl -X POST https://turnover-api-hd7ze.ondigitalocean.app/api/auth/register/ \'
echo '     -H "Content-Type: application/json" \'
echo '     -d "{\"email\":\"test@example.com\",\"password\":\"TestPass123!\",\"password_confirm\":\"TestPass123!\",\"first_name\":\"Test\",\"last_name\":\"User\"}"'
echo ""
echo "🔧 Test with comprehensive data:"
echo '   curl -X POST https://turnover-api-hd7ze.ondigitalocean.app/api/auth/register/ \'
echo '     -H "Content-Type: application/json" \'
echo '     -d "{\"email\":\"comprehensive@test.com\",\"password\":\"TestPass123!\",\"password_confirm\":\"TestPass123!\",\"first_name\":\"John\",\"last_name\":\"Doe\",\"phone_number\":\"+1234567890\",\"address\":\"123 Main St, City, State\",\"position\":\"Software Engineer\"}"'
echo ""
echo "🆘 If issues persist, check database user permissions for ALTER TABLE operations."
