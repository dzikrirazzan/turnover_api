# 🚀 NEW FEATURES: 1-on-1 Meeting, Performance Review & Analytics

## 📋 Feature Overview

### 1. 🤝 1-on-1 Meeting Management
- **HR/Admin**: Schedule meetings berdasarkan hasil ML prediction
- **Employee**: View meeting schedule dan join links
- **Features**: Scheduling, meeting links, notes, history

### 2. ⭐ Performance Review System  
- **HR/Admin**: Create/update performance reviews dengan rating
- **Employee**: View own performance reviews (read-only)
- **Features**: Star ratings, detailed notes, CRUD operations

### 3. 📊 Analytics & Charts
- **Data visualization** dari hasil ML prediction
- **Trend analysis** untuk turnover risk over time
- **Department-wise analytics**

---

## 🔗 API ENDPOINTS

### 📅 1-on-1 Meeting Endpoints

#### **Create Meeting Schedule**
```
POST /api/meetings/
```

#### **Get All Meetings (Admin)**
```
GET /api/meetings/
```

#### **Get Employee Meetings**
```
GET /api/meetings/employee/{employee_id}/
```

#### **Update Meeting**
```
PUT /api/meetings/{meeting_id}/
```

#### **Delete Meeting**
```
DELETE /api/meetings/{meeting_id}/
```

### ⭐ Performance Review Endpoints

#### **Create Performance Review**
```
POST /api/reviews/
```

#### **Get All Reviews (Admin)**
```
GET /api/reviews/
```

#### **Get Employee Reviews**
```
GET /api/reviews/employee/{employee_id}/
```

#### **Update Review**
```
PUT /api/reviews/{review_id}/
```

#### **Delete Review**
```
DELETE /api/reviews/{review_id}/
```

### 📊 Analytics Endpoints

#### **ML Prediction Analytics**
```
GET /api/analytics/predictions/
```

#### **Department Risk Analysis**
```
GET /api/analytics/departments/
```

#### **Turnover Trend Analysis**
```
GET /api/analytics/trends/
```

#### **Chart Data for Frontend**
```
GET /api/analytics/charts/
```

---

## 📊 CHART DATA STRUCTURE FOR FRONTEND

### **1. Risk Distribution Chart (Pie Chart)**
```json
{
  "chart_type": "pie",
  "title": "Employee Risk Distribution",
  "data": {
    "labels": ["Low Risk", "Medium Risk", "High Risk"],
    "datasets": [{
      "data": [65, 25, 10],
      "backgroundColor": ["#28a745", "#ffc107", "#dc3545"],
      "borderWidth": 2
    }]
  }
}
```

### **2. Department Risk Analysis (Bar Chart)**
```json
{
  "chart_type": "bar",
  "title": "Risk Analysis by Department",
  "data": {
    "labels": ["Engineering", "Marketing", "HR", "Finance"],
    "datasets": [{
      "label": "Average Risk Score (%)",
      "data": [15, 32, 8, 28],
      "backgroundColor": "#4F46E5",
      "borderColor": "#3730A3",
      "borderWidth": 1
    }]
  }
}
```

### **3. Turnover Probability Trend (Line Chart)**
```json
{
  "chart_type": "line",
  "title": "Turnover Risk Trend (Last 6 Months)",
  "data": {
    "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "datasets": [{
      "label": "Average Risk %",
      "data": [12, 15, 18, 22, 19, 16],
      "borderColor": "#EF4444",
      "backgroundColor": "rgba(239, 68, 68, 0.1)",
      "tension": 0.4,
      "fill": true
    }]
  }
}
```

### **4. Risk Factors Impact (Horizontal Bar)**
```json
{
  "chart_type": "horizontalBar",
  "title": "Risk Factors Impact Analysis",
  "data": {
    "labels": [
      "Satisfaction Level",
      "Last Evaluation", 
      "Working Hours",
      "Number of Projects",
      "Promotion History",
      "Work Accidents"
    ],
    "datasets": [{
      "label": "Average Impact (%)",
      "data": [35, 28, 18, 12, 5, 2],
      "backgroundColor": [
        "#EF4444", "#F97316", "#EAB308", 
        "#22C55E", "#3B82F6", "#8B5CF6"
      ]
    }]
  }
}
```

### **5. Employee Risk Scatter Plot**
```json
{
  "chart_type": "scatter",
  "title": "Satisfaction vs Performance Risk",
  "data": {
    "datasets": [{
      "label": "Employees",
      "data": [
        {"x": 65, "y": 82, "employee": "John Doe", "risk": "low"},
        {"x": 30, "y": 45, "employee": "Jane Smith", "risk": "high"},
        {"x": 75, "y": 88, "employee": "Bob Wilson", "risk": "low"}
      ],
      "backgroundColor": "#4F46E5",
      "pointRadius": 8,
      "pointHoverRadius": 12
    }]
  },
  "options": {
    "scales": {
      "x": {"title": {"display": true, "text": "Satisfaction Level (%)"}},
      "y": {"title": {"display": true, "text": "Last Evaluation (%)"}}
    },
    "plugins": {
      "tooltip": {
        "callbacks": {
          "label": "function(context) { return context.raw.employee + ': ' + context.raw.risk + ' risk'; }"
        }
      }
    }
  }
}
```

---

## 🗄️ DATABASE MODELS

### **Meeting Model**
```python
class Meeting(models.Model):
    MEETING_STATUS = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled')
    ]
    
    MEETING_TYPE = [
        ('followup', 'Follow-up from ML Prediction'),
        ('regular', 'Regular Check-in'),
        ('urgent', 'Urgent Discussion'),
        ('performance', 'Performance Discussion')
    ]
    
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meetings')
    scheduled_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scheduled_meetings')
    
    # Meeting Details
    title = models.CharField(max_length=200)
    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPE, default='followup')
    scheduled_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=30)
    
    # Meeting Links & Notes
    meeting_link = models.URLField(blank=True, null=True)
    agenda = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # ML Prediction Context
    prediction_id = models.CharField(max_length=100, blank=True, null=True)
    ml_probability = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    ml_risk_level = models.CharField(max_length=10, blank=True, null=True)
    
    # Status & Tracking
    status = models.CharField(max_length=20, choices=MEETING_STATUS, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_date']
```

### **Performance Review Model**
```python
class PerformanceReview(models.Model):
    RATING_CHOICES = [
        (1, '1 Star - Poor'),
        (2, '2 Stars - Below Average'),
        (3, '3 Stars - Average'),
        (4, '4 Stars - Good'),
        (5, '5 Stars - Excellent')
    ]
    
    REVIEW_PERIOD = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annual', 'Semi-Annual'),
        ('annual', 'Annual'),
        ('adhoc', 'Ad-hoc')
    ]
    
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='performance_reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conducted_reviews')
    
    # Review Details
    review_period = models.CharField(max_length=20, choices=REVIEW_PERIOD)
    review_date = models.DateField()
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Ratings
    overall_rating = models.IntegerField(choices=RATING_CHOICES)
    technical_skills = models.IntegerField(choices=RATING_CHOICES)
    communication = models.IntegerField(choices=RATING_CHOICES)
    teamwork = models.IntegerField(choices=RATING_CHOICES)
    leadership = models.IntegerField(choices=RATING_CHOICES)
    initiative = models.IntegerField(choices=RATING_CHOICES)
    
    # Notes & Feedback
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    goals_for_next_period = models.TextField()
    additional_notes = models.TextField(blank=True)
    
    # ML Context (if review triggered by prediction)
    triggered_by_ml = models.BooleanField(default=False)
    ml_prediction_id = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-review_date']
        unique_together = ['employee', 'review_date', 'review_period']
```

---

## 📱 FRONTEND INTEGRATION EXAMPLES

### **Chart.js Integration**
```jsx
// components/AnalyticsDashboard.jsx
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, LineElement, PointElement } from 'chart.js';
import { Pie, Bar, Line, Scatter } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, LineElement, PointElement);

function AnalyticsDashboard() {
  const [chartData, setChartData] = useState(null);
  
  useEffect(() => {
    fetchAnalyticsData();
  }, []);
  
  const fetchAnalyticsData = async () => {
    const response = await fetch('/api/analytics/charts/', {
      headers: { 'Authorization': `Token ${token}` }
    });
    const data = await response.json();
    setChartData(data);
  };
  
  if (!chartData) return <div>Loading charts...</div>;
  
  return (
    <div className="analytics-dashboard">
      <div className="chart-grid">
        
        {/* Risk Distribution */}
        <div className="chart-container">
          <h3>Risk Distribution</h3>
          <Pie data={chartData.risk_distribution.data} />
        </div>
        
        {/* Department Analysis */}
        <div className="chart-container">
          <h3>Department Risk Analysis</h3>
          <Bar data={chartData.department_analysis.data} />
        </div>
        
        {/* Trend Analysis */}
        <div className="chart-container">
          <h3>Risk Trend (6 Months)</h3>
          <Line data={chartData.trend_analysis.data} />
        </div>
        
        {/* Scatter Plot */}
        <div className="chart-container">
          <h3>Satisfaction vs Performance</h3>
          <Scatter data={chartData.satisfaction_performance.data} />
        </div>
        
      </div>
    </div>
  );
}
```

### **Meeting Scheduler Component**
```jsx
// components/MeetingScheduler.jsx
import { useState } from 'react';

function MeetingScheduler({ employeeId, mlPrediction }) {
  const [meeting, setMeeting] = useState({
    title: '',
    scheduled_date: '',
    meeting_link: '',
    agenda: '',
    meeting_type: 'followup'
  });
  
  const handleScheduleMeeting = async () => {
    const meetingData = {
      employee: employeeId,
      ...meeting,
      prediction_id: mlPrediction.prediction_id,
      ml_probability: mlPrediction.prediction.probability,
      ml_risk_level: mlPrediction.prediction.risk_level
    };
    
    const response = await fetch('/api/meetings/', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(meetingData)
    });
    
    if (response.ok) {
      alert('Meeting scheduled successfully!');
    }
  };
  
  return (
    <div className="meeting-scheduler">
      <h3>Schedule 1-on-1 Meeting</h3>
      
      <div className="ml-context">
        <p>Employee Risk: {Math.round(mlPrediction.prediction.probability * 100)}%</p>
        <p>Risk Level: {mlPrediction.prediction.risk_level.toUpperCase()}</p>
      </div>
      
      <form onSubmit={handleScheduleMeeting}>
        <input
          type="text"
          placeholder="Meeting Title"
          value={meeting.title}
          onChange={(e) => setMeeting({...meeting, title: e.target.value})}
        />
        
        <input
          type="datetime-local"
          value={meeting.scheduled_date}
          onChange={(e) => setMeeting({...meeting, scheduled_date: e.target.value})}
        />
        
        <input
          type="url"
          placeholder="Meeting Link (Zoom, Google Meet, etc.)"
          value={meeting.meeting_link}
          onChange={(e) => setMeeting({...meeting, meeting_link: e.target.value})}
        />
        
        <select
          value={meeting.meeting_type}
          onChange={(e) => setMeeting({...meeting, meeting_type: e.target.value})}
        >
          <option value="followup">Follow-up from ML Prediction</option>
          <option value="urgent">Urgent Discussion</option>
          <option value="performance">Performance Discussion</option>
        </select>
        
        <textarea
          placeholder="Meeting Agenda"
          value={meeting.agenda}
          onChange={(e) => setMeeting({...meeting, agenda: e.target.value})}
        />
        
        <button type="submit">Schedule Meeting</button>
      </form>
    </div>
  );
}
```

### **Performance Review Component**
```jsx
// components/PerformanceReview.jsx
import { useState } from 'react';

function PerformanceReviewForm({ employeeId }) {
  const [review, setReview] = useState({
    review_period: 'quarterly',
    review_date: new Date().toISOString().split('T')[0],
    period_start: '',
    period_end: '',
    overall_rating: 3,
    technical_skills: 3,
    communication: 3,
    teamwork: 3,
    leadership: 3,
    initiative: 3,
    strengths: '',
    areas_for_improvement: '',
    goals_for_next_period: '',
    additional_notes: ''
  });
  
  const StarRating = ({ rating, onChange, label }) => (
    <div className="star-rating">
      <label>{label}</label>
      <div className="stars">
        {[1, 2, 3, 4, 5].map(star => (
          <span
            key={star}
            className={`star ${star <= rating ? 'filled' : ''}`}
            onClick={() => onChange(star)}
          >
            ⭐
          </span>
        ))}
      </div>
    </div>
  );
  
  const handleSubmit = async () => {
    const response = await fetch('/api/reviews/', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        employee: employeeId,
        ...review
      })
    });
    
    if (response.ok) {
      alert('Performance review saved successfully!');
    }
  };
  
  return (
    <div className="performance-review-form">
      <h3>Performance Review</h3>
      
      <div className="review-period">
        <select
          value={review.review_period}
          onChange={(e) => setReview({...review, review_period: e.target.value})}
        >
          <option value="monthly">Monthly</option>
          <option value="quarterly">Quarterly</option>
          <option value="semi_annual">Semi-Annual</option>
          <option value="annual">Annual</option>
          <option value="adhoc">Ad-hoc</option>
        </select>
      </div>
      
      <div className="ratings-section">
        <h4>Ratings</h4>
        
        <StarRating 
          rating={review.overall_rating}
          onChange={(rating) => setReview({...review, overall_rating: rating})}
          label="Overall Performance"
        />
        
        <StarRating 
          rating={review.technical_skills}
          onChange={(rating) => setReview({...review, technical_skills: rating})}
          label="Technical Skills"
        />
        
        <StarRating 
          rating={review.communication}
          onChange={(rating) => setReview({...review, communication: rating})}
          label="Communication"
        />
        
        <StarRating 
          rating={review.teamwork}
          onChange={(rating) => setReview({...review, teamwork: rating})}
          label="Teamwork"
        />
        
        <StarRating 
          rating={review.leadership}
          onChange={(rating) => setReview({...review, leadership: rating})}
          label="Leadership"
        />
        
        <StarRating 
          rating={review.initiative}
          onChange={(rating) => setReview({...review, initiative: rating})}
          label="Initiative"
        />
      </div>
      
      <div className="feedback-section">
        <h4>Feedback</h4>
        
        <textarea
          placeholder="Strengths"
          value={review.strengths}
          onChange={(e) => setReview({...review, strengths: e.target.value})}
        />
        
        <textarea
          placeholder="Areas for Improvement"
          value={review.areas_for_improvement}
          onChange={(e) => setReview({...review, areas_for_improvement: e.target.value})}
        />
        
        <textarea
          placeholder="Goals for Next Period"
          value={review.goals_for_next_period}
          onChange={(e) => setReview({...review, goals_for_next_period: e.target.value})}
        />
        
        <textarea
          placeholder="Additional Notes"
          value={review.additional_notes}
          onChange={(e) => setReview({...review, additional_notes: e.target.value})}
        />
      </div>
      
      <button onClick={handleSubmit}>Save Performance Review</button>
    </div>
  );
}
```

---

## 🔐 ROLE-BASED ACCESS CONTROL

### **Admin/HR Permissions:**
- ✅ Create/Read/Update/Delete meetings
- ✅ Create/Read/Update/Delete performance reviews
- ✅ View all analytics and charts
- ✅ Schedule meetings based on ML predictions
- ✅ Access all employee data

### **Employee Permissions:**
- ✅ View own meetings (read-only)
- ✅ View own performance reviews (read-only) 
- ✅ View basic analytics (own data only)
- ❌ Cannot create/edit meetings
- ❌ Cannot create/edit performance reviews
- ❌ Cannot access other employees' data

---

## 🚀 NEXT STEPS

1. **Implement Backend APIs** - Create Django views for all endpoints
2. **Setup Database Migrations** - Add Meeting and PerformanceReview models
3. **Create Frontend Components** - Build React components for UI
4. **Integrate Chart.js** - Add data visualization
5. **Test with Postman** - Validate all API endpoints
6. **Deploy & Monitor** - Deploy to production with monitoring

This comprehensive feature set will provide HR teams with powerful tools to act on ML predictions through structured 1-on-1 meetings, systematic performance reviews, and insightful analytics dashboards! 🎯
