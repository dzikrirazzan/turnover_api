# SMART-EN SYSTEM API DOCUMENTATION

## Complete Backend API Endpoints for Frontend Integration

This document provides all API endpoints needed to power the Smart-en System frontend at https://smart-en-system.vercel.app/

## Base URL

```
http://localhost:8001
```

## Authentication

All endpoints require Basic Authentication:

- Username: `admin`
- Password: `admin123`

---

## 🏠 DASHBOARD APIs

### 1. Get Dashboard Statistics

```http
GET /performance/api/dashboard/stats/?employee=1
```

**Response (matches frontend exactly):**

```json
{
  "goals_completed": 8,
  "goals_total": 12,
  "goals_completion_rate": 67,
  "feedback_received": 15,
  "learning_hours": 24,
  "performance_score": 4.2
}
```

### 2. Get Recent Activities

```http
GET /performance/api/dashboard/activities/?employee=1
```

**Response:**

```json
[
  {
    "id": 1,
    "activity_type": "goal_completed",
    "title": "Completed goal: Improve team collaboration",
    "description": "",
    "created_at": "2024-01-15T10:00:00Z"
  },
  {
    "id": 2,
    "activity_type": "feedback_received",
    "title": "Received feedback from Bravely Dirgayuska",
    "description": "",
    "created_at": "2024-01-14T15:30:00Z"
  }
]
```

### 3. Get User Info

```http
GET /performance/api/dashboard/user_info/?employee=1
```

**Response:**

```json
{
  "name": "Tasya Salsabila",
  "initials": "TS",
  "role": "Senior Developer",
  "department": "Engineering",
  "employee_id": "EMP001"
}
```

---

## 📊 ANALYTICS APIs

### 4. Get Analytics Dashboard

```http
GET /performance/api/analytics/dashboard/
```

**Response (matches frontend analytics page):**

```json
{
  "team_engagement": 8.2,
  "team_engagement_change": 0.3,
  "active_employees": 247,
  "participation_rate": 98.4,
  "at_risk_count": 23,
  "at_risk_percentage": 9.3,
  "goal_completion": 76,
  "goal_target_met": true,
  "engagement_trends": [
    {
      "date": "2024-01-01",
      "engagement_score": 8.0,
      "stress_level": 3.2
    }
  ],
  "risk_trends": [
    {
      "date": "2024-01-01",
      "value": 25
    }
  ],
  "individual_performance": [
    {
      "employee_id": 1,
      "employee_name": "Bravely Dirgayuska",
      "employee_initials": "BD",
      "role": "Team Member",
      "performance_score": 9.2,
      "engagement_score": 8.8,
      "goal_completion": 9.1,
      "risk_level": "LOW"
    }
  ]
}
```

### 5. Get Team Engagement Data

```http
GET /performance/api/analytics/team_engagement/?days=30
```

### 6. Get Risk Trends

```http
GET /performance/api/analytics/risk_trends/?months=12
```

### 7. Get Performance Matrix

```http
GET /performance/api/analytics/performance_matrix/
```

---

## 🎯 GOALS & OKRs APIs

### 8. Get Goals Statistics

```http
GET /performance/api/goals/statistics/?employee=1
```

**Response:**

```json
{
  "total_goals": 12,
  "completed_goals": 8,
  "in_progress_goals": 3,
  "completion_rate": 67,
  "achievement_rate": 85
}
```

### 9. Get Sample Goals (matches frontend exactly)

```http
GET /performance/api/goals/sample_goals/
```

**Response:**

```json
[
  {
    "id": 1,
    "title": "Improve Team Collaboration",
    "description": "Enhance cross-functional team communication and collaboration through better tools and processes.",
    "owner_name": "Bravely Dirgayuska",
    "priority": "high",
    "status": "in_progress",
    "progress_percentage": 85,
    "due_date": "2024-12-31",
    "key_results": [
      {
        "id": 1,
        "title": "Implement new project management tool",
        "is_completed": true
      },
      {
        "id": 2,
        "title": "Conduct team collaboration workshops",
        "is_completed": true
      },
      {
        "id": 3,
        "title": "Establish weekly cross-team sync meetings",
        "is_completed": false
      }
    ]
  }
]
```

### 10. CRUD Goals

```http
GET    /performance/api/goals/                    # List all goals
POST   /performance/api/goals/                    # Create new goal
GET    /performance/api/goals/{id}/               # Get specific goal
PUT    /performance/api/goals/{id}/               # Update goal
DELETE /performance/api/goals/{id}/               # Delete goal
```

### 11. CRUD Key Results

```http
GET    /performance/api/key-results/              # List key results
POST   /performance/api/key-results/              # Create key result
PUT    /performance/api/key-results/{id}/         # Update key result
DELETE /performance/api/key-results/{id}/         # Delete key result
```

---

## 💬 FEEDBACK APIs

### 12. Get Sample Feedback (matches frontend)

```http
GET /performance/api/feedback/sample_feedback/
```

**Response:**

```json
[
  {
    "id": 1,
    "from_employee_name": "Dzikri Razzan Athallah",
    "to_employee_name": "Tasya Salsabila",
    "feedback_type": "peer",
    "project": "Q4 Product Launch",
    "content": "Great collaboration on the user interface design. Your attention to detail really made a difference.",
    "rating": 5,
    "is_helpful": true,
    "created_at": "2024-01-15T00:00:00Z"
  },
  {
    "id": 2,
    "from_employee_name": "Bravely Dirgayuska",
    "to_employee_name": "Tasya Salsabila",
    "feedback_type": "manager",
    "project": "Team Leadership",
    "content": "Excellent job mentoring new team members. Your leadership skills have grown significantly.",
    "rating": 5,
    "is_helpful": true,
    "created_at": "2024-01-12T00:00:00Z"
  }
]
```

### 13. Feedback Statistics

```http
GET /performance/api/feedback/stats/?employee=1
```

**Response:**

```json
{
  "received": 2,
  "sent": 1
}
```

### 14. CRUD Feedback

```http
GET    /performance/api/feedback/                 # List all feedback
POST   /performance/api/feedback/                 # Give feedback
GET    /performance/api/feedback/received/?employee=1  # Received feedback
GET    /performance/api/feedback/sent/?employee=1      # Sent feedback
```

---

## 📋 PERFORMANCE REVIEW APIs

### 15. Get Current Review (matches frontend)

```http
GET /performance/api/performance-reviews/current_review/?employee=1
```

**Response:**

```json
{
  "id": 1,
  "employee_name": "Tasya Salsabila",
  "reviewer_name": "Bravely Dirgayuska",
  "review_period_start": "2024-01-01",
  "review_period_end": "2024-12-31",
  "status": "manager_review",
  "overall_rating": 4.2,
  "self_assessment_progress": 85,
  "peer_reviews_received": 3,
  "peer_reviews_target": 5,
  "peer_reviews_progress": 60,
  "manager_review_completed": false,
  "calibration_completed": false,
  "comments": "2024 Annual Review in progress"
}
```

### 16. Update Review Progress

```http
POST /performance/api/performance-reviews/{id}/update_progress/
```

**Body:**

```json
{
  "type": "self_assessment",
  "value": 90
}
```

### 17. CRUD Performance Reviews

```http
GET    /performance/api/performance-reviews/      # List reviews
GET    /performance/api/performance-reviews/history/?employee=1  # Review history
```

---

## 🤝 1-ON-1 MEETINGS APIs

### 18. Meeting Statistics

```http
GET /performance/api/oneonone-meetings/statistics/?employee=1
```

**Response:**

```json
{
  "total_meetings": 24,
  "this_month": 8,
  "avg_duration_minutes": 45,
  "satisfaction_percentage": 96
}
```

### 19. CRUD 1-on-1 Meetings

```http
GET    /performance/api/oneonone-meetings/        # List meetings
POST   /performance/api/oneonone-meetings/        # Schedule meeting
PUT    /performance/api/oneonone-meetings/{id}/   # Update meeting
```

---

## 🎉 SHOUTOUTS APIs

### 20. Shoutout Statistics

```http
GET /performance/api/shoutouts/statistics/?employee=1
```

**Response:**

```json
{
  "shoutouts_given": 48,
  "shoutouts_received": 32,
  "total_likes": 156,
  "team_participation_percentage": 89
}
```

### 21. Like/Unlike Shoutout

```http
POST /performance/api/shoutouts/{id}/like/
```

**Body:**

```json
{
  "employee_id": 1
}
```

### 22. CRUD Shoutouts

```http
GET    /performance/api/shoutouts/               # List shoutouts
POST   /performance/api/shoutouts/               # Create shoutout
```

---

## 🎓 LEARNING APIs

### 23. Learning Recommendations

```http
GET /performance/api/learning-modules/recommendations/?employee=1
```

### 24. Learning Categories

```http
GET /performance/api/learning-modules/categories/
```

### 25. Learning Statistics

```http
GET /performance/api/learning-progress/statistics/?employee=1
```

**Response:**

```json
{
  "completed_this_week": 7,
  "time_spent_minutes": 1380,
  "streak_days": 7,
  "total_completed": 45
}
```

### 26. CRUD Learning

```http
GET    /performance/api/learning-modules/        # List modules
GET    /performance/api/learning-progress/       # Learning progress
GET    /performance/api/learning-goals/          # Learning goals
```

---

## 👥 EMPLOYEE APIs (from existing predictions app)

### 27. List Employees

```http
GET /api/employees/
```

### 28. Employee Statistics

```http
GET /api/employees/statistics/
```

### 29. Employee Details

```http
GET /api/employees/{id}/
```

---

## 🏢 DEPARTMENT APIs

### 30. List Departments

```http
GET /api/departments/
```

---

## 🔮 PREDICTION APIs (existing)

### 31. Predict Turnover

```http
POST /api/predict/
```

### 32. Bulk Predict

```http
POST /api/bulk-predict/
```

---

## Testing with Frontend

To test with the frontend at https://smart-en-system.vercel.app/:

1. **Start the backend server:**

   ```bash
   cd /Users/dzikrirazzan/Documents/code/turnover_api/backend
   python manage.py runserver 8001
   ```

2. **Update frontend API base URL to:**

   ```
   http://localhost:8001
   ```

3. **Use these employee IDs for testing:**

   - Employee ID 1: Tasya Salsabila (TS)
   - Employee ID 2: Bravely Dirgayuska (BD)
   - Employee ID 3: Dzikri Razzan Athallah (DRA)

4. **Test key endpoints:**
   - Dashboard: `/performance/api/dashboard/stats/?employee=1`
   - Analytics: `/performance/api/analytics/dashboard/`
   - Goals: `/performance/api/goals/sample_goals/`
   - Feedback: `/performance/api/feedback/sample_feedback/`

All endpoints return data that exactly matches the frontend requirements!
