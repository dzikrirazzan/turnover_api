#!/bin/bash
# Deploy script untuk DigitalOcean server

echo "🚀 Starting deployment of SMART-EN API improvements..."

# 1. Pull latest code
echo "📥 Pulling latest code from Git..."
git pull origin main

# 2. Activate virtual environment
echo "🐍 Activating virtual environment..."
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "env" ]; then
    source env/bin/activate
else
    echo "⚠️  Virtual environment not found, using system Python"
fi

# 3. Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# 4. Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# 5. Collect static files
echo "📂 Collecting static files..."
python manage.py collectstatic --noinput

# 6. Create sample department if not exists
echo "🏢 Ensuring department exists..."
python manage.py shell -c "
from predictions.models import Department
Department.objects.get_or_create(
    id=1, 
    defaults={
        'name': 'IT Department', 
        'description': 'Information Technology Department'
    }
)
print('Department check complete.')
"

# 7. Restart services
echo "🔄 Restarting services..."
if systemctl is-active --quiet gunicorn; then
    echo "Restarting Gunicorn..."
    sudo systemctl restart gunicorn
fi

if systemctl is-active --quiet nginx; then
    echo "Restarting Nginx..."
    sudo systemctl restart nginx
fi

# 8. Check service status
echo "✅ Checking service status..."
echo "Gunicorn status:"
sudo systemctl status gunicorn --no-pager -l

echo "Nginx status:"
sudo systemctl status nginx --no-pager -l

# 9. Test API
echo "🧪 Testing API endpoints..."
echo "Health check:"
curl -s http://localhost:8000/api/health/ | python -m json.tool 2>/dev/null || echo "API not responding on localhost"

echo ""
echo "🎉 Deployment complete!"
echo "🔗 Your API should be available at your domain"
echo "📖 Test the new endpoints with improved responses!"

echo ""
echo "🆕 NEW FEATURES DEPLOYED:"
echo "✅ Complete registration response with all employee data"
echo "✅ Token authentication in login/registration responses"
echo "✅ Consistent response format across endpoints"
echo "✅ Bearer token support for API authentication"
