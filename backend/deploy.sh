#!/bin/bash

# DigitalOcean App Platform deployment script
echo "🚀 Starting SMART-EN System deployment..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files (if not disabled)
if [ "$DISABLE_COLLECTSTATIC" != "1" ]; then
    echo "📁 Collecting static files..."
    python manage.py collectstatic --noinput
else
    echo "⚠️ Skipping collectstatic (disabled)"
fi

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Create superuser (only if doesn't exist)
echo "👤 Creating admin user..."
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@company.com', 'admin123')
    print('✅ Admin user created')
else:
    print('ℹ️ Admin user already exists')
EOF

# Load sample data (optional, for testing)
echo "📊 Loading sample data..."
python load_csv_data.py || echo "⚠️ Sample data loading skipped (optional)"

echo "✅ Deployment setup completed!"
echo "🔗 Access your API at: https://[your-app-name].ondigitalocean.app"
echo "🔐 Admin credentials: admin / admin123"
