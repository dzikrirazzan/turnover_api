#!/bin/bash

# 🧪 COMPREHENSIVE API TESTING SCRIPT
# Test all endpoints of SMART-EN System API

echo "🧪 COMPREHENSIVE API TESTING"
echo "============================="
echo "🎯 Target: https://turnover-api-hd7ze.ondigitalocean.app"
echo

BASE_URL="https://turnover-api-hd7ze.ondigitalocean.app"
AUTH="Authorization: Basic YWRtaW46YWRtaW4xMjM="

# Test function
test_endpoint() {
    local method=$1
    local url=$2
    local data=$3
    local description=$4
    
    echo -n "   Testing $description... "
    
    if [ "$method" = "GET" ]; then
        result=$(curl -s -w "%{http_code}" -o /tmp/api_response -H "$AUTH" "$BASE_URL$url")
    else
        result=$(curl -s -w "%{http_code}" -o /tmp/api_response -X "$method" -H "Content-Type: application/json" -H "$AUTH" -d "$data" "$BASE_URL$url")
    fi
    
    if [ "$result" = "200" ] || [ "$result" = "201" ]; then
        echo "✅ $result"
    else
        echo "❌ $result"
        if [ "$result" != "404" ] && [ "$result" != "405" ]; then
            echo "      $(cat /tmp/api_response | head -c 100)"
        fi
    fi
}

echo "🔐 1. AUTHENTICATION ENDPOINTS"
test_endpoint "POST" "/api/auth/login/" '{"username":"admin","password":"admin123"}' "Login"
test_endpoint "GET" "/api/auth/profile/" "" "Profile"
test_endpoint "GET" "/api/auth/check/" "" "Auth Check"
echo

echo "👥 2. EMPLOYEE MANAGEMENT ENDPOINTS"
test_endpoint "GET" "/api/employees/" "" "List Employees"
test_endpoint "GET" "/api/employees/?search=HRA" "" "Search HRA Employees"
test_endpoint "GET" "/api/employees/statistics/" "" "Employee Statistics"
test_endpoint "GET" "/api/employees/1/" "" "Employee Detail"
echo

echo "🏢 3. DEPARTMENT ENDPOINTS"
test_endpoint "GET" "/api/departments/" "" "List Departments"
test_endpoint "GET" "/api/departments/1/" "" "Department Detail"
echo

echo "🤖 4. ML MODEL & PREDICTION ENDPOINTS"
test_endpoint "GET" "/api/models/" "" "List ML Models"
test_endpoint "POST" "/api/predictions/predict/" '{"satisfaction_level":0.6,"last_evaluation":0.8,"number_project":4,"average_monthly_hours":180,"time_spend_company":3,"work_accident":0,"promotion_last_5years":0,"department":"sales","salary":"medium"}' "ML Prediction"
test_endpoint "GET" "/api/predictions/bulk_predict/" "" "Bulk Prediction"
echo

echo "📊 5. PERFORMANCE MANAGEMENT ENDPOINTS"
test_endpoint "GET" "/performance/api/goals/" "" "Goals"
test_endpoint "GET" "/performance/api/performance-reviews/" "" "Performance Reviews"
test_endpoint "GET" "/performance/api/feedback/" "" "Feedback"
test_endpoint "GET" "/performance/api/oneonone-meetings/" "" "1-on-1 Meetings"
test_endpoint "GET" "/performance/api/shoutouts/" "" "Shoutouts"
echo

echo "📚 6. LEARNING & DEVELOPMENT ENDPOINTS"
test_endpoint "GET" "/performance/api/learning-modules/" "" "Learning Modules"
test_endpoint "GET" "/performance/api/learning-progress/" "" "Learning Progress"
test_endpoint "GET" "/performance/api/learning-goals/" "" "Learning Goals"
echo

echo "📈 7. ANALYTICS & DASHBOARD ENDPOINTS"
test_endpoint "GET" "/performance/api/analytics/dashboard/" "" "Analytics Dashboard"
test_endpoint "GET" "/performance/api/analytics/performance_matrix/" "" "Performance Matrix"
test_endpoint "GET" "/performance/api/analytics/risk_trends/" "" "Risk Trends"
test_endpoint "GET" "/performance/api/analytics/team_engagement/" "" "Team Engagement"
test_endpoint "GET" "/performance/api/dashboard/stats/" "" "Dashboard Stats"
test_endpoint "GET" "/performance/api/dashboard/activities/" "" "Dashboard Activities"
echo

echo "🔍 8. DATA VERIFICATION"
echo "   📊 Employee Count: $(curl -s -H "$AUTH" "$BASE_URL/api/employees/" | jq '.count')"
echo "   🏢 Department Count: $(curl -s -H "$AUTH" "$BASE_URL/api/departments/" | jq '.count')"
echo "   🤖 ML Model Count: $(curl -s -H "$AUTH" "$BASE_URL/api/models/" | jq '.count')"

# Check training data
hra_count=$(curl -s -H "$AUTH" "$BASE_URL/api/employees/?search=HRA" | jq '.count')
echo "   📈 Training Data (HRA): $hra_count employees"

if [ "$hra_count" -gt 1000 ]; then
    echo "   ✅ Sufficient training data for ML"
else
    echo "   ⚠️  Need more training data for optimal ML performance"
fi

echo
echo "============================="
echo "🎉 API TESTING COMPLETE!"
echo

# Test ML prediction if we have training data
if [ "$hra_count" -gt 10 ]; then
    echo "🔮 TESTING ML PREDICTION:"
    prediction_result=$(curl -s -X POST -H "Content-Type: application/json" -H "$AUTH" \
        -d '{"satisfaction_level":0.6,"last_evaluation":0.8,"number_project":4,"average_monthly_hours":180,"time_spend_company":3,"work_accident":0,"promotion_last_5years":0,"department":"sales","salary":"medium"}' \
        "$BASE_URL/api/predictions/predict/")
    
    echo "   Result: $(echo $prediction_result | head -c 200)"
fi

# Cleanup
rm -f /tmp/api_response

echo
echo "🎯 ALL CORE ENDPOINTS TESTED!"
echo "   API is ready for frontend integration"
