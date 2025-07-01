#!/bin/bash

# Script to fix trailing slash issues in Postman collection

echo "🔧 Fixing trailing slash issues in Postman collection..."

# File path
COLLECTION_FILE="/Users/dzikrirazzan/Documents/code/turnover_api/SMART-EN-Complete-API-v2.postman_collection.json"

# Create backup
cp "$COLLECTION_FILE" "$COLLECTION_FILE.backup"

# Fix all URLs that are missing trailing slashes
sed -i '' 's|"{{base_url}}/api/auth/register"|"{{base_url}}/api/auth/register/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/api/auth/login"|"{{base_url}}/api/auth/login/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/api/auth/profile"|"{{base_url}}/api/auth/profile/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/api/auth/profile/update"|"{{base_url}}/api/auth/profile/update/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/api/auth/change-password"|"{{base_url}}/api/auth/change-password/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/api/auth/check"|"{{base_url}}/api/auth/check/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/api/auth/logout"|"{{base_url}}/api/auth/logout/"|g' "$COLLECTION_FILE"

# Fix departments URLs
sed -i '' 's|"{{base_url}}/api/departments"|"{{base_url}}/api/departments/"|g' "$COLLECTION_FILE"

# Fix employees URLs
sed -i '' 's|"{{base_url}}/api/employees"|"{{base_url}}/api/employees/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/api/employees/statistics"|"{{base_url}}/api/employees/statistics/"|g' "$COLLECTION_FILE"

# Fix models URLs
sed -i '' 's|"{{base_url}}/api/models"|"{{base_url}}/api/models/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/api/models/active"|"{{base_url}}/api/models/active/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/api/models/train"|"{{base_url}}/api/models/train/"|g' "$COLLECTION_FILE"

# Fix predictions URLs
sed -i '' 's|"{{base_url}}/api/predictions"|"{{base_url}}/api/predictions/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/api/predictions/predict"|"{{base_url}}/api/predictions/predict/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/api/predictions/bulk_predict"|"{{base_url}}/api/predictions/bulk_predict/"|g' "$COLLECTION_FILE"

# Fix performance URLs
sed -i '' 's|"{{base_url}}/performance/api/goals"|"{{base_url}}/performance/api/goals/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/goals/statistics"|"{{base_url}}/performance/api/goals/statistics/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/goals/sample_goals"|"{{base_url}}/performance/api/goals/sample_goals/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/key-results"|"{{base_url}}/performance/api/key-results/"|g' "$COLLECTION_FILE"

# Fix feedback URLs
sed -i '' 's|"{{base_url}}/performance/api/feedback"|"{{base_url}}/performance/api/feedback/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/feedback/received"|"{{base_url}}/performance/api/feedback/received/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/feedback/sent"|"{{base_url}}/performance/api/feedback/sent/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/feedback/sample_feedback"|"{{base_url}}/performance/api/feedback/sample_feedback/"|g' "$COLLECTION_FILE"

# Fix performance reviews URLs
sed -i '' 's|"{{base_url}}/performance/api/performance-reviews"|"{{base_url}}/performance/api/performance-reviews/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/performance-reviews/current_review"|"{{base_url}}/performance/api/performance-reviews/current_review/"|g' "$COLLECTION_FILE"

# Fix meetings URLs
sed -i '' 's|"{{base_url}}/performance/api/oneonone-meetings"|"{{base_url}}/performance/api/oneonone-meetings/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/oneonone-meetings/statistics"|"{{base_url}}/performance/api/oneonone-meetings/statistics/"|g' "$COLLECTION_FILE"

# Fix shoutouts URLs
sed -i '' 's|"{{base_url}}/performance/api/shoutouts"|"{{base_url}}/performance/api/shoutouts/"|g' "$COLLECTION_FILE"

# Fix learning URLs
sed -i '' 's|"{{base_url}}/performance/api/learning-modules"|"{{base_url}}/performance/api/learning-modules/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/learning-modules/categories"|"{{base_url}}/performance/api/learning-modules/categories/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/learning-modules/recommendations"|"{{base_url}}/performance/api/learning-modules/recommendations/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/learning-progress"|"{{base_url}}/performance/api/learning-progress/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/learning-progress/statistics"|"{{base_url}}/performance/api/learning-progress/statistics/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/learning-goals"|"{{base_url}}/performance/api/learning-goals/"|g' "$COLLECTION_FILE"

# Fix analytics URLs
sed -i '' 's|"{{base_url}}/performance/api/analytics/dashboard"|"{{base_url}}/performance/api/analytics/dashboard/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/analytics/team_engagement"|"{{base_url}}/performance/api/analytics/team_engagement/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/analytics/risk_trends"|"{{base_url}}/performance/api/analytics/risk_trends/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/analytics/performance_matrix"|"{{base_url}}/performance/api/analytics/performance_matrix/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/dashboard/stats"|"{{base_url}}/performance/api/dashboard/stats/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/dashboard/activities"|"{{base_url}}/performance/api/dashboard/activities/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api/dashboard/user_info"|"{{base_url}}/performance/api/dashboard/user_info/"|g' "$COLLECTION_FILE"

# Fix system URLs
sed -i '' 's|"{{base_url}}/api"|"{{base_url}}/api/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/performance/api"|"{{base_url}}/performance/api/"|g' "$COLLECTION_FILE"
sed -i '' 's|"{{base_url}}/admin"|"{{base_url}}/admin/"|g' "$COLLECTION_FILE"

echo "✅ Fixed trailing slash issues in Postman collection"
echo "📁 Backup created: $COLLECTION_FILE.backup"
echo "🔧 Updated file: $COLLECTION_FILE"
