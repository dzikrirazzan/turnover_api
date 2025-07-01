#!/bin/bash
# Script to deploy the database fix to DigitalOcean
set -e

echo "🚀 Deploying database fix to DigitalOcean..."
echo "=" * 50

# Check if git is clean
if [[ `git status --porcelain` ]]; then
    echo "📝 Adding changes to git..."
    git add .
    git commit -m "Add production database fix script"
else
    echo "✅ Git repository is clean"
fi

echo "📤 Pushing to main branch to trigger deployment..."
git push origin main

echo "⏳ Waiting for deployment to complete (this may take a few minutes)..."
sleep 30

echo "🔧 Testing if the fix worked..."
echo "Testing registration endpoint..."

# Test the registration endpoint
curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test_deploy_fix@example.com",
    "first_name": "Deploy",
    "last_name": "Test",
    "employee_id": "EMP_DEPLOY_001",
    "phone_number": "08123456789",
    "password": "testpassword123",
    "password_confirm": "testpassword123"
  }'

echo ""
echo "=" * 50
echo "🎉 Deployment completed!"
echo ""
echo "If you still see the database error, you may need to:"
echo "1. Check DigitalOcean App Platform logs"
echo "2. Manually trigger the release command"
echo "3. Or contact DigitalOcean support to run migrations"
echo ""
echo "The fix script is now deployed and can be run via:"
echo "python fix_production_db.py"
