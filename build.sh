#!/bin/bash

# DigitalOcean Build Script
echo "🚀 Starting SMART-EN System build..."

# Change to backend directory
cd backend

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Build completed successfully!"
