#!/bin/bash

# 🚀 SMART-EN Turnover API - Deployment Script untuk DigitalOcean
# Script ini akan update API dengan perubahan terbaru

echo "🚀 Starting deployment to DigitalOcean..."
echo "📅 $(date)"

# 1. Push to Git Repository
echo "📤 Pushing changes to Git repository..."
git add .
git status

echo "Enter commit message (or press Enter for default): "
read commit_message

if [ -z "$commit_message" ]; then
    commit_message="feat: improve API responses with complete data and token authentication

- Add EmployeeRegistrationResponseSerializer for complete registration data
- Add LoginResponseSerializer with token authentication  
- Update register_employee() to return full employee data + token
- Update login_employee() to return token
- Update user_profile() for consistency
- Add rest_framework.authtoken to INSTALLED_APPS
- Add TokenAuthentication to REST_FRAMEWORK settings
- Fix Postman Collection JSON errors
- Update all Bearer tokens to Token authentication

Breaking changes:
- Registration response now returns 'employee' object instead of flat fields
- Login and profile responses now include 'token' field
- All authenticated endpoints now support Token authentication"
fi

git commit -m "$commit_message"

echo "Push to repository? (y/n): "
read push_confirm

if [ "$push_confirm" = "y" ] || [ "$push_confirm" = "Y" ]; then
    git push origin main
    echo "✅ Changes pushed to Git repository"
else
    echo "⏸️  Skipping Git push"
fi

echo ""
echo "🔧 Next steps for DigitalOcean server:"
echo "================================================"
echo "1. SSH ke server:"
echo "   ssh root@your-server-ip"
echo ""
echo "2. Navigate ke project directory:"
echo "   cd /path/to/your/turnover_api"
echo ""
echo "3. Pull latest changes:"
echo "   git pull origin main"
echo ""
echo "4. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "5. Install/update dependencies:"
echo "   pip install -r requirements.txt"
echo ""
echo "6. Run migrations untuk token authentication:"
echo "   python manage.py migrate"
echo ""
echo "7. Create sample department (jika belum ada):"
echo "   python manage.py shell"
echo "   >>> from predictions.models import Department"
echo "   >>> Department.objects.get_or_create(id=1, defaults={'name': 'IT Department', 'description': 'Information Technology'})"
echo "   >>> exit()"
echo ""
echo "8. Collect static files:"
echo "   python manage.py collectstatic --noinput"
echo ""
echo "9. Restart services:"
echo "   sudo systemctl restart gunicorn"
echo "   sudo systemctl restart nginx"
echo ""
echo "10. Check status:"
echo "    sudo systemctl status gunicorn"
echo "    sudo systemctl status nginx"
echo ""
echo "11. Test API:"
echo "    curl https://your-domain.com/api/health/"
echo ""
echo "================================================"
echo "🎯 PERUBAHAN UTAMA:"
echo "✅ Response registrasi sekarang lengkap dengan token"
echo "✅ Response login sekarang include token authentication"  
echo "✅ User profile konsisten dengan login response"
echo "✅ Semua endpoint mendukung Token authentication"
echo "✅ Postman Collection sudah diperbaiki"
echo ""
echo "📝 FORMAT RESPONSE BARU:"
echo ""
echo "Registration:"
echo '{'
echo '    "message": "Registrasi berhasil",'
echo '    "employee": {'
echo '        "id": 1,'
echo '        "employee_id": "EMP20250003",'
echo '        "email": "user@example.com",'
echo '        "first_name": "John",'
echo '        "last_name": "Doe",'
echo '        "full_name": "John Doe",'
echo '        "phone_number": "+6281234567890",'
echo '        "department": 1,'
echo '        "department_name": "IT Department",'
echo '        "position": "Junior Staff",'
echo '        "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"'
echo '    }'
echo '}'
echo ""
echo "Login:"
echo '{'
echo '    "message": "Login berhasil",'
echo '    "user": {'
echo '        "id": 1,'
echo '        "employee_id": "EMP20250003",'
echo '        "email": "user@example.com",'
echo '        "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"'
echo '    }'
echo '}'
echo ""
echo "🔑 AUTHENTICATION HEADER:"
echo "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
echo ""
echo "🚀 Ready for deployment!"
