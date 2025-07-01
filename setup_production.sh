#!/bin/bash
# Script to manually run migrations and seed data on DigitalOcean
# Use this if the automatic release command doesn't work

echo "Setting up environment..."
export DJANGO_SETTINGS_MODULE=backend.turnover_prediction.settings
export PYTHONPATH=$PYTHONPATH:./backend

echo "Running database migrations..."
python manage.py migrate

echo "Creating superuser if needed..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser(
        email='admin@example.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"

echo "Seeding department data..."
python manage.py seed_data

echo "Database setup completed!"
