# Complete Smart Employee Management System API Documentation

## 🎯 Overview
Comprehensive API documentation for the Smart Employee Management System that supports all frontend features including performance management, goals & OKRs, feedback systems, analytics, learning modules, and more.

This API extends the original turnover prediction system with full performance management capabilities to match the frontend at: https://smart-en-system.vercel.app/

---

## 🔐 Authentication
All endpoints require Basic Authentication:
- **Username:** admin
- **Password:** admin123

---

## 📊 API Endpoints Summary

### **Core Employee & Turnover APIs (30 endpoints)**
- 🔐 Authentication: 7 endpoints
- 👥 Employee Management: 14 endpoints  
- 🏢 Department Management: 5 endpoints
- 🤖 ML Predictions: 5 endpoints
- 🧠 Model Management: 5 endpoints

### **Performance Management APIs (45 endpoints)**
- 🎯 Goals & OKRs: 8 endpoints
- 💬 Feedback System: 6 endpoints
- 📈 Performance Reviews: 5 endpoints
- 🤝 1-on-1 Meetings: 6 endpoints
- 🌟 Shoutouts & Recognition: 6 endpoints
- 📚 Learning & Development: 9 endpoints
- 📊 Analytics & Dashboard: 5 endpoints

**Total: 75 API Endpoints**

---

## 🎯 Goals & OKRs Management

### Get All Goals
```http
GET /performance/api/goals/
```
**Query Parameters:**
- `employee` - Filter by employee ID
- `status` - Filter by status (not_started, in_progress, completed, cancelled)

**Response Example:**
```json
[
    {
        "id": 1,
        "title": "Improve Team Collaboration",
        "description": "Enhance cross-functional team communication...",
        "owner": 1000,
        "owner_name": "Bravely Dirgayuska",
        "priority": "high",
        "status": "in_progress",
        "progress_percentage": 85,
        "due_date": "2024-12-31",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-06-15T14:20:00Z",
        "key_results": [
            {
                "id": 1,
                "title": "Implement new project management tool",
                "description": "",
                "is_completed": true,
                "order": 0
            },
            {
                "id": 2,
                "title": "Conduct team collaboration workshops",
                "description": "",
                "is_completed": true,
                "order": 1
            },
            {
                "id": 3,
                "title": "Establish weekly cross-team sync meetings",
                "description": "",
                "is_completed": false,
                "order": 2
            }
        ]
    }
]
```

### Create New Goal
```http
POST /performance/api/goals/
```
**Request Body:**
```json
{
    "title": "Revenue Growth Strategy",
    "description": "Develop and execute strategies to increase revenue by 25%",
    "owner": 1001,
    "priority": "high",
    "status": "not_started",
    "progress_percentage": 0,
    "due_date": "2024-12-31",
    "key_results": [
        {
            "title": "Identify three new market segments",
            "description": "Research and document potential markets",
            "order": 0
        },
        {
            "title": "Launch two new product lines",
            "description": "Develop and launch new products",
            "order": 1
        }
    ]
}
```

### Update Goal
```http
PUT /performance/api/goals/{id}/
PATCH /performance/api/goals/{id}/
```

### Delete Goal
```http
DELETE /performance/api/goals/{id}/
```

### Get Goal Statistics
```http
GET /performance/api/goals/statistics/
```
**Query Parameters:**
- `employee` - Get stats for specific employee

**Response:**
```json
{
    "total_goals": 12,
    "completed_goals": 8,
    "in_progress_goals": 3,
    "completion_rate": 66.7,
    "achievement_rate": 85
}
```

### Get Key Results for Goal
```http
GET /performance/api/key-results/?goal={goal_id}
```

### Create Key Result
```http
POST /performance/api/key-results/
```

### Update Key Result
```http
PUT /performance/api/key-results/{id}/
PATCH /performance/api/key-results/{id}/
```

### Delete Key Result
```http
DELETE /performance/api/key-results/{id}/
```

---

## 💬 Feedback System

### Get All Feedback
```http
GET /performance/api/feedback/
```
**Query Parameters:**
- `employee` - Filter by employee ID (sent or received)
- `type` - Filter by type (peer, manager, self, 360)

### Get Received Feedback
```http
GET /performance/api/feedback/received/?employee={employee_id}
```

### Get Sent Feedback
```http
GET /performance/api/feedback/sent/?employee={employee_id}
```

### Create Feedback
```http
POST /performance/api/feedback/
```
**Request Body:**
```json
{
    "from_employee": 1000,
    "to_employee": 1001,
    "feedback_type": "peer",
    "project": "Q4 Product Launch",
    "content": "Great collaboration on the user interface design. Your attention to detail really made a difference.",
    "rating": 5,
    "is_helpful": true
}
```

**Response Example:**
```json
{
    "id": 1,
    "from_employee": 1000,
    "from_employee_name": "Bravely Dirgayuska",
    "to_employee": 1001,
    "to_employee_name": "Tasya Salsabila",
    "feedback_type": "peer",
    "project": "Q4 Product Launch",
    "content": "Great collaboration on the user interface design...",
    "rating": 5,
    "is_helpful": true,
    "created_at": "2024-01-15T10:30:00Z"
}
```

### Update Feedback
```http
PUT /performance/api/feedback/{id}/
PATCH /performance/api/feedback/{id}/
```

### Delete Feedback
```http
DELETE /performance/api/feedback/{id}/
```

---

## 📈 Performance Reviews

### Get Performance Reviews
```http
GET /performance/api/performance-reviews/
```
**Query Parameters:**
- `employee` - Filter by employee ID

**Response Example:**
```json
[
    {
        "id": 1,
        "employee": 1001,
        "employee_name": "Tasya Salsabila",
        "reviewer": 1000,
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
        "comments": "",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-06-15T14:20:00Z"
    }
]
```

### Create Performance Review
```http
POST /performance/api/performance-reviews/
```

### Update Review Progress
```http
POST /performance/api/performance-reviews/{id}/update_progress/
```
**Request Body:**
```json
{
    "type": "self_assessment",
    "value": 90
}
```
**Types:** `self_assessment`, `peer_review`, `manager_review`, `calibration`, `overall_rating`

### Update Performance Review
```http
PUT /performance/api/performance-reviews/{id}/
PATCH /performance/api/performance-reviews/{id}/
```

### Delete Performance Review
```http
DELETE /performance/api/performance-reviews/{id}/
```

---

## 🤝 1-on-1 Meetings

### Get 1-on-1 Meetings
```http
GET /performance/api/oneonone-meetings/
```
**Query Parameters:**
- `employee` - Filter by employee ID
- `status` - Filter by status (scheduled, upcoming, completed, cancelled)

**Response Example:**
```json
[
    {
        "id": 1,
        "employee": 1001,
        "employee_name": "Tasya Salsabila",
        "manager": 1000,
        "manager_name": "Bravely Dirgayuska",
        "meeting_date": "2024-01-20T10:00:00Z",
        "duration_minutes": 45,
        "topic": "Career development",
        "agenda": "Discuss promotion timeline and skill development plan",
        "notes": "",
        "status": "upcoming",
        "satisfaction_rating": null,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
]
```

### Schedule 1-on-1 Meeting
```http
POST /performance/api/oneonone-meetings/
```
**Request Body:**
```json
{
    "employee": 1001,
    "manager": 1000,
    "meeting_date": "2024-01-25T15:00:00Z",
    "duration_minutes": 45,
    "topic": "Project feedback",
    "agenda": "Review Q4 project performance and plan Q1 goals",
    "status": "scheduled"
}
```

### Get Meeting Statistics
```http
GET /performance/api/oneonone-meetings/statistics/
```
**Query Parameters:**
- `employee` - Get stats for specific employee

**Response:**
```json
{
    "total_meetings": 24,
    "this_month": 8,
    "avg_duration_minutes": 45,
    "satisfaction_percentage": 96
}
```

### Update 1-on-1 Meeting
```http
PUT /performance/api/oneonone-meetings/{id}/
PATCH /performance/api/oneonone-meetings/{id}/
```

### Delete 1-on-1 Meeting
```http
DELETE /performance/api/oneonone-meetings/{id}/
```

---

## 🌟 Shoutouts & Recognition

### Get Public Shoutouts
```http
GET /performance/api/shoutouts/
```
**Query Parameters:**
- `employee` - Filter by employee ID
- `public` - Filter public shoutouts (default: true)

**Response Example:**
```json
[
    {
        "id": 1,
        "from_employee": 1004,
        "from_employee_name": "Putri Aulia Simanjuntak",
        "from_employee_initials": "PA",
        "to_employee": 1001,
        "to_employee_name": "Tasya Salsabila",
        "to_team": null,
        "to_team_name": null,
        "title": "🌟 Amazing work on the client presentation!",
        "message": "Your research was thorough and the delivery was flawless.",
        "values": ["excellence", "collaboration"],
        "likes_count": 12,
        "is_public": true,
        "shared_to_slack": false,
        "shared_to_teams": false,
        "created_at": "2024-01-15T10:30:00Z"
    }
]
```

### Give Shoutout
```http
POST /performance/api/shoutouts/
```
**Request Body:**
```json
{
    "from_employee": 1000,
    "to_employee": 1001,
    "title": "🚀 Excellent problem solving!",
    "message": "Your innovative approach to the technical challenge saved us hours of work.",
    "values": ["innovation", "excellence"],
    "is_public": true,
    "shared_to_slack": true,
    "shared_to_teams": false
}
```

### Like/Unlike Shoutout
```http
POST /performance/api/shoutouts/{id}/like/
```
**Request Body:**
```json
{
    "employee_id": 1000
}
```

**Response:**
```json
{
    "liked": true,
    "likes_count": 13
}
```

### Get Shoutout Statistics
```http
GET /performance/api/shoutouts/statistics/
```
**Query Parameters:**
- `employee` - Get stats for specific employee

**Response:**
```json
{
    "shoutouts_given": 48,
    "shoutouts_received": 32,
    "total_likes": 156,
    "team_participation_percentage": 89
}
```

### Update Shoutout
```http
PUT /performance/api/shoutouts/{id}/
PATCH /performance/api/shoutouts/{id}/
```

### Delete Shoutout
```http
DELETE /performance/api/shoutouts/{id}/
```

---

## 📚 Learning & Development

### Get Learning Modules
```http
GET /performance/api/learning-modules/
```
**Query Parameters:**
- `category` - Filter by category (leadership, technical, communication, project_management, personal_development)
- `type` - Filter by type (micro-learning, article, course, video)

**Response Example:**
```json
[
    {
        "id": 1,
        "title": "Effective Remote Leadership",
        "description": "Learn key strategies for leading distributed teams effectively in the modern workplace...",
        "content_type": "micro-learning",
        "category": "leadership",
        "duration_minutes": 5,
        "url": "",
        "is_active": true,
        "helpful_count": 8,
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```

### Get Learning Recommendations
```http
GET /performance/api/learning-modules/recommendations/?employee={employee_id}
```

### Get Learning Categories
```http
GET /performance/api/learning-modules/categories/
```

**Response:**
```json
[
    {
        "category": "leadership",
        "count": 12
    },
    {
        "category": "technical",
        "count": 18
    },
    {
        "category": "communication",
        "count": 8
    },
    {
        "category": "project_management",
        "count": 15
    }
]
```

### Create Learning Module
```http
POST /performance/api/learning-modules/
```

### Get Learning Progress
```http
GET /performance/api/learning-progress/?employee={employee_id}
```

**Response Example:**
```json
[
    {
        "id": 1,
        "employee": 1001,
        "module": 1,
        "module_title": "Effective Remote Leadership",
        "module_duration": 5,
        "module_type": "micro-learning",
        "is_completed": true,
        "completion_date": "2024-01-10T15:30:00Z",
        "time_spent_minutes": 7,
        "rating": 5,
        "is_helpful": true,
        "feedback": "Very practical tips!",
        "created_at": "2024-01-10T15:00:00Z"
    }
]
```

### Record Learning Progress
```http
POST /performance/api/learning-progress/
```
**Request Body:**
```json
{
    "employee": 1001,
    "module": 1,
    "is_completed": true,
    "time_spent_minutes": 7,
    "rating": 5,
    "is_helpful": true,
    "feedback": "Very practical and applicable to my daily work"
}
```

### Get Learning Statistics
```http
GET /performance/api/learning-progress/statistics/?employee={employee_id}
```

**Response:**
```json
{
    "completed_this_week": 4,
    "time_spent_minutes": 23,
    "streak_days": 7,
    "total_completed": 15
}
```

### Get Learning Goals
```http
GET /performance/api/learning-goals/?employee={employee_id}&current_week=true
```

**Response Example:**
```json
[
    {
        "id": 1,
        "employee": 1001,
        "title": "Complete 5 micro-learning modules",
        "target_value": 5,
        "current_value": 4,
        "unit": "modules",
        "week_start": "2024-01-15",
        "is_completed": false,
        "progress_percentage": 80
    }
]
```

### Create Learning Goal
```http
POST /performance/api/learning-goals/
```

### Update Learning Goal Progress
```http
PATCH /performance/api/learning-goals/{id}/
```

---

## 📊 Analytics & Dashboard

### Get Analytics Dashboard
```http
GET /performance/api/analytics/dashboard/
```

**Response Example:**
```json
{
    "team_engagement": 8.2,
    "team_engagement_change": 0.3,
    "active_employees": 247,
    "participation_rate": 98.4,
    "at_risk_count": 23,
    "at_risk_percentage": 9.3,
    "goal_completion": 76.0,
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
            "employee_id": 1000,
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

### Get Dashboard Statistics
```http
GET /performance/api/dashboard/stats/?employee={employee_id}
```

**Response Example:**
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

### Get Dashboard Activities
```http
GET /performance/api/dashboard/activities/?employee={employee_id}
```

**Response Example:**
```json
[
    {
        "id": 1,
        "employee": 1001,
        "activity_type": "goal_completed",
        "title": "Completed goal: Improve team collaboration",
        "description": "",
        "related_object_type": "goal",
        "related_object_id": 1,
        "created_at": "2024-01-15T08:30:00Z"
    },
    {
        "id": 2,
        "employee": 1001,
        "activity_type": "feedback_received",
        "title": "Received feedback from Bravely Dirgayuska",
        "description": "",
        "related_object_type": "feedback",
        "related_object_id": 1,
        "created_at": "2024-01-14T10:20:00Z"
    }
]
```

---

## 🧪 Testing the APIs

### Test Dashboard Endpoints
```bash
# Get dashboard stats for employee
curl -u admin:admin123 "http://localhost:8000/performance/api/dashboard/stats/?employee=1001"

# Get recent activities
curl -u admin:admin123 "http://localhost:8000/performance/api/dashboard/activities/?employee=1001"

# Get analytics dashboard
curl -u admin:admin123 "http://localhost:8000/performance/api/analytics/dashboard/"
```

### Test Goals & OKRs
```bash
# Get all goals
curl -u admin:admin123 "http://localhost:8000/performance/api/goals/"

# Get goals for specific employee
curl -u admin:admin123 "http://localhost:8000/performance/api/goals/?employee=1000"

# Get goal statistics
curl -u admin:admin123 "http://localhost:8000/performance/api/goals/statistics/?employee=1000"
```

### Test Feedback System
```bash
# Get received feedback
curl -u admin:admin123 "http://localhost:8000/performance/api/feedback/received/?employee=1001"

# Get sent feedback
curl -u admin:admin123 "http://localhost:8000/performance/api/feedback/sent/?employee=1000"
```

### Test Learning System
```bash
# Get learning recommendations
curl -u admin:admin123 "http://localhost:8000/performance/api/learning-modules/recommendations/?employee=1001"

# Get learning statistics
curl -u admin:admin123 "http://localhost:8000/performance/api/learning-progress/statistics/?employee=1001"

# Get current week learning goals
curl -u admin:admin123 "http://localhost:8000/performance/api/learning-goals/?employee=1001&current_week=true"
```

---

## 📋 Complete API Endpoints List

### **Core System (30 endpoints)**
1. `POST /api/auth/register/` - Register new user
2. `POST /api/auth/login/` - User login
3. `GET /api/auth/profile/` - Get user profile
4. `PUT /api/auth/profile/` - Update user profile
5. `POST /api/auth/logout/` - User logout
6. `POST /api/auth/change-password/` - Change password
7. `POST /api/auth/reset-password/` - Reset password
8. `GET /api/employees/` - List all employees
9. `POST /api/employees/` - Create new employee
10. `GET /api/employees/{id}/` - Get employee details
11. `PUT /api/employees/{id}/` - Update employee
12. `DELETE /api/employees/{id}/` - Delete employee
13. `GET /api/employees/statistics/` - Employee statistics
14. `GET /api/employees/{id}/predict/` - Get individual prediction
15. `POST /api/employees/bulk-create/` - Bulk create employees
16. `GET /api/employees/export/` - Export employees
17. `POST /api/employees/import/` - Import employees
18. `GET /api/employees/search/` - Search employees
19. `GET /api/employees/by-department/` - Group by department
20. `GET /api/employees/at-risk/` - Get at-risk employees
21. `GET /api/departments/` - List departments
22. `POST /api/departments/` - Create department
23. `GET /api/departments/{id}/` - Get department
24. `PUT /api/departments/{id}/` - Update department
25. `DELETE /api/departments/{id}/` - Delete department
26. `POST /api/predictions/predict/` - Single prediction
27. `POST /api/predictions/bulk-predict/` - Bulk predictions
28. `GET /api/predictions/history/` - Prediction history
29. `GET /api/predictions/` - List predictions
30. `POST /api/predictions/` - Create prediction

### **Performance Management (45 endpoints)**
31. `GET /performance/api/goals/` - List goals
32. `POST /performance/api/goals/` - Create goal
33. `GET /performance/api/goals/{id}/` - Get goal
34. `PUT /performance/api/goals/{id}/` - Update goal
35. `DELETE /performance/api/goals/{id}/` - Delete goal
36. `GET /performance/api/goals/statistics/` - Goal statistics
37. `GET /performance/api/key-results/` - List key results
38. `POST /performance/api/key-results/` - Create key result
39. `GET /performance/api/feedback/` - List feedback
40. `POST /performance/api/feedback/` - Create feedback
41. `GET /performance/api/feedback/received/` - Received feedback
42. `GET /performance/api/feedback/sent/` - Sent feedback
43. `PUT /performance/api/feedback/{id}/` - Update feedback
44. `DELETE /performance/api/feedback/{id}/` - Delete feedback
45. `GET /performance/api/performance-reviews/` - List reviews
46. `POST /performance/api/performance-reviews/` - Create review
47. `POST /performance/api/performance-reviews/{id}/update_progress/` - Update progress
48. `PUT /performance/api/performance-reviews/{id}/` - Update review
49. `DELETE /performance/api/performance-reviews/{id}/` - Delete review
50. `GET /performance/api/oneonone-meetings/` - List meetings
51. `POST /performance/api/oneonone-meetings/` - Schedule meeting
52. `GET /performance/api/oneonone-meetings/statistics/` - Meeting stats
53. `PUT /performance/api/oneonone-meetings/{id}/` - Update meeting
54. `DELETE /performance/api/oneonone-meetings/{id}/` - Delete meeting
55. `GET /performance/api/shoutouts/` - List shoutouts
56. `POST /performance/api/shoutouts/` - Give shoutout
57. `POST /performance/api/shoutouts/{id}/like/` - Like shoutout
58. `GET /performance/api/shoutouts/statistics/` - Shoutout stats
59. `PUT /performance/api/shoutouts/{id}/` - Update shoutout
60. `DELETE /performance/api/shoutouts/{id}/` - Delete shoutout
61. `GET /performance/api/learning-modules/` - List modules
62. `POST /performance/api/learning-modules/` - Create module
63. `GET /performance/api/learning-modules/recommendations/` - Get recommendations
64. `GET /performance/api/learning-modules/categories/` - List categories
65. `GET /performance/api/learning-progress/` - List progress
66. `POST /performance/api/learning-progress/` - Record progress
67. `GET /performance/api/learning-progress/statistics/` - Learning stats
68. `GET /performance/api/learning-goals/` - List learning goals
69. `POST /performance/api/learning-goals/` - Create learning goal
70. `GET /performance/api/analytics/dashboard/` - Analytics dashboard
71. `GET /performance/api/dashboard/stats/` - Dashboard statistics
72. `GET /performance/api/dashboard/activities/` - Dashboard activities
73. `PUT /performance/api/key-results/{id}/` - Update key result
74. `DELETE /performance/api/key-results/{id}/` - Delete key result
75. `PATCH /performance/api/learning-goals/{id}/` - Update learning goal

---

## 🚀 Getting Started

1. **Start the server:**
   ```bash
   cd backend
   source venv/bin/activate
   python manage.py runserver
   ```

2. **Populate sample data:**
   ```bash
   python manage.py seed_performance_data
   ```

3. **Test the APIs:**
   - Use the provided curl commands
   - Import the Postman collection
   - Use the frontend at https://smart-en-system.vercel.app/

4. **Authentication:**
   - All requests require Basic Auth
   - Username: `admin`
   - Password: `admin123`

---

## 📈 Frontend Integration

The API is designed to fully support the frontend features:

- **Dashboard**: Real-time performance metrics and activity feeds
- **Analytics**: Team engagement trends and individual performance matrix
- **Goals & OKRs**: Complete goal management with key results tracking
- **Feedback**: 360° feedback system with peer and manager reviews
- **Performance Reviews**: Annual review cycles with progress tracking
- **1-on-1 Meetings**: Meeting scheduling and note management
- **Shoutouts**: Peer recognition with social features
- **Learning**: Personalized learning recommendations and progress tracking
- **Profile**: Complete employee profile management

This comprehensive API provides all the data structures and endpoints needed to power the Smart Employee Management System frontend.
