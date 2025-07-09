# 🧠 SMART-EN ML Prediction API Documentation

## Overview
The ML Prediction API provides turnover risk assessment for employees using machine learning algorithms. This API is designed for admin/HR users to predict employee turnover probability and receive actionable recommendations.

## 🎯 Main Endpoint

### POST `/api/predict/`
**Predict Employee Turnover Risk**

**Access:** Admin/HR only (requires authentication + admin permission)

**Purpose:** Analyze employee performance data and predict turnover probability with risk level and recommendations.

---

## 📋 Request Format

### Headers
```
Authorization: Token YOUR_ADMIN_TOKEN
Content-Type: application/json
```

### Request Body
```json
{
    "employee_id": 123
}
```

### Parameters
- `employee_id` (required): The ID of the employee to analyze

---

## 📊 Response Format

### Success Response (200 OK)
```json
{
    "success": true,
    "message": "Turnover prediction completed for John Doe",
    "data": {
        "employee": {
            "id": 123,
            "name": "John Doe",
            "email": "john.doe@company.com",
            "department": "Engineering",
            "position": "Software Developer"
        },
        "prediction": {
            "probability": 0.342,
            "risk_level": "medium",
            "will_leave": false,
            "confidence_score": 0.85,
            "model_used": "RuleBasedModel"
        },
        "risk_analysis": {
            "overall_risk_score": 0.342,
            "risk_factors": {
                "satisfaction_level": {
                    "value": 0.65,
                    "risk": 0.1,
                    "weight": 0.25,
                    "contribution": 0.025
                },
                "last_evaluation": {
                    "value": 0.82,
                    "risk": 0.0,
                    "weight": 0.20,
                    "contribution": 0.0
                },
                "average_monthly_hours": {
                    "value": 185,
                    "risk": 0.1,
                    "weight": 0.15,
                    "contribution": 0.015
                },
                "time_spend_company": {
                    "value": 5,
                    "risk": 0.6,
                    "weight": 0.10,
                    "contribution": 0.06
                },
                "work_accident": {
                    "value": 0,
                    "risk": 0.0,
                    "weight": 0.05,
                    "contribution": 0.0
                },
                "promotion_last_5years": {
                    "value": 0,
                    "risk": 0.4,
                    "weight": 0.10,
                    "contribution": 0.04
                }
            }
        },
        "recommendations": [
            {
                "category": "Career Growth",
                "issue": "No promotion in the last 5 years",
                "recommendation": "Review career progression opportunities and create development plans",
                "priority": "medium"
            },
            {
                "category": "Workload",
                "issue": "Slightly elevated working hours",
                "recommendation": "Monitor workload and consider work-life balance improvements",
                "priority": "low"
            }
        ],
        "features_used": {
            "satisfaction_level": 0.65,
            "last_evaluation": 0.82,
            "number_project": 4,
            "average_monthly_hours": 185,
            "time_spend_company": 5,
            "work_accident": 0,
            "promotion_last_5years": 0
        },
        "prediction_id": 789,
        "created_at": "2024-01-15T10:30:00Z"
    }
}
```

### Error Responses

#### 400 Bad Request - Missing Employee ID
```json
{
    "success": false,
    "message": "Employee ID is required"
}
```

#### 404 Not Found - Employee Not Found
```json
{
    "success": false,
    "message": "Employee not found"
}
```

#### 404 Not Found - Performance Data Missing
```json
{
    "success": false,
    "message": "Performance data not found for this employee. Please add performance data first."
}
```

#### 401 Unauthorized - Invalid Token
```json
{
    "success": false,
    "message": "Authentication credentials were not provided."
}
```

#### 403 Forbidden - Not Admin
```json
{
    "success": false,
    "message": "Admin access required."
}
```

---

## 🎚️ Risk Levels

### Low Risk (< 30%)
- **Color:** Green
- **Description:** Employee is unlikely to leave
- **Action:** Continue current management approach

### Medium Risk (30-70%)
- **Color:** Yellow
- **Description:** Employee may leave if issues aren't addressed
- **Action:** Implement recommended interventions

### High Risk (> 70%)
- **Color:** Red
- **Description:** Employee is likely to leave soon
- **Action:** Immediate intervention required

---

## 🔧 Prerequisites

Before using the prediction API, ensure:

1. **Employee exists** in the system
2. **Performance data** has been added for the employee via `POST /api/performance/`
3. **Admin authentication** token is available
4. **Proper permissions** are set for the user

---

## 📝 Example Usage

### Step 1: Add Performance Data
```bash
curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/performance/" \
  -H "Authorization: Token YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 123,
    "satisfaction_level": 0.65,
    "last_evaluation": 0.82,
    "number_project": 4,
    "average_monthly_hours": 185,
    "time_spend_company": 5,
    "work_accident": 0,
    "promotion_last_5years": 0
  }'
```

### Step 2: Get Prediction
```bash
curl -X POST "https://turnover-api-hd7ze.ondigitalocean.app/api/predict/" \
  -H "Authorization: Token YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 123
  }'
```

---

## 🧮 ML Features Used

The prediction model uses these key features:

1. **satisfaction_level** (0-1): Employee satisfaction score
2. **last_evaluation** (0-1): Latest performance evaluation
3. **number_project** (int): Number of projects completed
4. **average_monthly_hours** (int): Average monthly working hours
5. **time_spend_company** (int): Years spent in company
6. **work_accident** (0/1): Whether employee had workplace accident
7. **promotion_last_5years** (0/1): Whether promoted in last 5 years

---

## 🎯 Recommendation Categories

### Employee Satisfaction
- **Issues:** Low satisfaction levels
- **Actions:** One-on-one meetings, environment improvements

### Performance
- **Issues:** Low evaluation scores
- **Actions:** Training, coaching, support

### Workload
- **Issues:** Excessive hours, burnout risk
- **Actions:** Workload redistribution, hiring

### Career Growth
- **Issues:** No promotions, stagnation
- **Actions:** Development plans, promotion paths

### Safety
- **Issues:** Work accidents
- **Actions:** Safety training, protocol review

---

## 🔄 Integration with Frontend

### React/Next.js Example
```javascript
const predictTurnover = async (employeeId) => {
  try {
    const response = await fetch('/api/predict/', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${adminToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        employee_id: employeeId
      })
    });
    
    const result = await response.json();
    
    if (result.success) {
      const { prediction, recommendations } = result.data;
      
      // Display risk level
      console.log(`Risk Level: ${prediction.risk_level}`);
      console.log(`Probability: ${prediction.probability}`);
      
      // Show recommendations
      recommendations.forEach(rec => {
        console.log(`${rec.category}: ${rec.recommendation}`);
      });
    } else {
      console.error('Prediction failed:', result.message);
    }
  } catch (error) {
    console.error('Error:', error);
  }
};
```

---

## 🚀 Production Considerations

### Performance
- Cache predictions for recently analyzed employees
- Implement batch prediction for multiple employees
- Use asynchronous processing for large datasets

### Security
- Validate all input parameters
- Log prediction requests for audit trails
- Implement rate limiting for prediction endpoints

### Monitoring
- Track prediction accuracy over time
- Monitor API response times
- Alert on high-risk predictions

---

## 📈 Future Enhancements

1. **Advanced ML Models**
   - Neural networks for complex patterns
   - Ensemble methods for better accuracy
   - Real-time model retraining

2. **Additional Features**
   - Seasonal patterns
   - Team dynamics
   - Company-wide trends

3. **Visualization**
   - Risk dashboards
   - Trend analysis
   - Predictive charts

4. **Notifications**
   - Real-time alerts for high-risk employees
   - Automated recommendation emails
   - Management dashboards

---

## 🛠️ Testing

### Unit Tests
```bash
python manage.py test predictions.tests.test_prediction_api
```

### Integration Tests
```bash
python manage.py test predictions.tests.test_ml_integration
```

### Load Testing
```bash
# Test with multiple concurrent predictions
ab -n 100 -c 10 -H "Authorization: Token YOUR_TOKEN" \
   -H "Content-Type: application/json" \
   -p prediction_data.json \
   https://turnover-api-hd7ze.ondigitalocean.app/api/predict/
```

---

## 📞 Support

For technical support or questions about the ML Prediction API:

- **Documentation:** This file
- **API Health:** `GET /api/health/`
- **System Info:** `GET /api/info/`
- **Error Logs:** Check Django admin panel

---

**Last Updated:** January 2024
**Version:** 1.0
**Status:** Production Ready
