#!/bin/bash

# DigitalOcean Build Script
echo "🚀 Starting SMART-EN System build..."

# Change to backend directory
cd backend

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Setup static files
echo "🎨 Setting up static files..."
python setup_static.py

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "✅ Build completed successfully!"
