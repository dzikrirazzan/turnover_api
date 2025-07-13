# 🚀 Tutorial Frontend: HR Features API Integration

## 📋 Daftar Isi
1. [Overview Fitur Baru](#overview-fitur-baru)
2. [Authentication & Setup](#authentication--setup)
3. [1-on-1 Meetings Feature](#1-on-1-meetings-feature)
4. [Performance Reviews Feature](#performance-reviews-feature)
5. [Analytics & Charts Feature](#analytics--charts-feature)
6. [Contoh Implementasi React](#contoh-implementasi-react)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)

---

## 🎯 Overview Fitur Baru

### Fitur yang Tersedia:
1. **1-on-1 Meetings** - Scheduling dan tracking meeting dengan ML context
2. **Performance Reviews** - CRUD performance review dengan star ratings
3. **Analytics Dashboard** - Charts dan visualisasi data untuk dashboard
4. **ML Integration** - Integrasi dengan ML prediction untuk turnover risk

### Base URL & Authentication:
```javascript
const BASE_URL = 'https://turnover-api-hd7ze.ondigitalocean.app';
const API_BASE = `${BASE_URL}/api`;

// Headers untuk semua request
const getHeaders = (token) => ({
  'Content-Type': 'application/json',
  'Authorization': `Token ${token}`
});
```

---

## 🔐 Authentication & Setup

### 1. Login Admin/HR
```javascript
// Login untuk mendapatkan token
const loginAdmin = async () => {
  try {
    const response = await fetch(`${API_BASE}/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'admin@company.com',
        password: 'AdminPass123!'
      })
    });
    
    const data = await response.json();
    if (data.success) {
      localStorage.setItem('admin_token', data.data.token);
      return data.data.token;
    }
  } catch (error) {
    console.error('Login failed:', error);
  }
};
```

### 2. Check User Role
```javascript
const checkUserRole = async (token) => {
  try {
    const response = await fetch(`${API_BASE}/employees/me/`, {
      headers: getHeaders(token)
    });
    const userData = await response.json();
    return userData.role; // 'admin', 'hr', 'employee'
  } catch (error) {
    console.error('Failed to check user role:', error);
  }
};
```

---

## 🤝 1-on-1 Meetings Feature

### API Endpoints:
- `GET /api/hr/meetings/` - Get all meetings
- `POST /api/hr/meetings/` - Create new meeting
- `PUT /api/hr/meetings/{id}/` - Update meeting
- `POST /api/hr/meetings/{id}/complete/` - Mark meeting as complete

### 1. Get Meetings List
```javascript
const getMeetings = async (token, filters = {}) => {
  const queryParams = new URLSearchParams(filters).toString();
  const url = `${API_BASE}/hr/meetings/${queryParams ? '?' + queryParams : ''}`;
  
  try {
    const response = await fetch(url, {
      headers: getHeaders(token)
    });
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch meetings:', error);
  }
};

// Contoh penggunaan dengan filter
const upcomingMeetings = await getMeetings(token, { 
  status: 'scheduled',
  employee: '1' 
});
```

### 2. Create New Meeting
```javascript
const createMeeting = async (token, meetingData) => {
  try {
    const response = await fetch(`${API_BASE}/hr/meetings/`, {
      method: 'POST',
      headers: getHeaders(token),
      body: JSON.stringify({
        employee: meetingData.employeeId,
        title: meetingData.title,
        meeting_type: 'followup', // 'regular', 'followup', 'performance'
        scheduled_date: meetingData.scheduledDate,
        duration_minutes: meetingData.duration,
        meeting_link: meetingData.meetingLink,
        agenda: meetingData.agenda,
        ml_probability: meetingData.mlProbability,
        ml_risk_level: meetingData.riskLevel // 'low', 'medium', 'high'
      })
    });
    
    return await response.json();
  } catch (error) {
    console.error('Failed to create meeting:', error);
  }
};
```

### 3. React Component Example - Meeting Scheduler
```jsx
import React, { useState, useEffect } from 'react';

const MeetingScheduler = () => {
  const [meetings, setMeetings] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [formData, setFormData] = useState({
    employeeId: '',
    title: '',
    scheduledDate: '',
    duration: 30,
    meetingLink: '',
    agenda: ''
  });

  useEffect(() => {
    loadMeetings();
    loadEmployees();
  }, []);

  const loadMeetings = async () => {
    const token = localStorage.getItem('admin_token');
    const data = await getMeetings(token);
    setMeetings(data);
  };

  const loadEmployees = async () => {
    const token = localStorage.getItem('admin_token');
    const response = await fetch(`${API_BASE}/employees/`, {
      headers: getHeaders(token)
    });
    const data = await response.json();
    setEmployees(data);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('admin_token');
    
    await createMeeting(token, formData);
    loadMeetings(); // Refresh list
    
    // Reset form
    setFormData({
      employeeId: '',
      title: '',
      scheduledDate: '',
      duration: 30,
      meetingLink: '',
      agenda: ''
    });
  };

  return (
    <div className="meeting-scheduler">
      <h2>Schedule 1-on-1 Meeting</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Employee:</label>
          <select 
            value={formData.employeeId}
            onChange={(e) => setFormData({...formData, employeeId: e.target.value})}
          >
            <option value="">Select Employee</option>
            {employees.map(emp => (
              <option key={emp.id} value={emp.id}>
                {emp.first_name} {emp.last_name} - {emp.department}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Meeting Title:</label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => setFormData({...formData, title: e.target.value})}
            placeholder="e.g., Follow-up Meeting: High Turnover Risk"
          />
        </div>

        <div className="form-group">
          <label>Date & Time:</label>
          <input
            type="datetime-local"
            value={formData.scheduledDate}
            onChange={(e) => setFormData({...formData, scheduledDate: e.target.value})}
          />
        </div>

        <div className="form-group">
          <label>Duration (minutes):</label>
          <select 
            value={formData.duration}
            onChange={(e) => setFormData({...formData, duration: parseInt(e.target.value)})}
          >
            <option value={30}>30 minutes</option>
            <option value={45}>45 minutes</option>
            <option value={60}>60 minutes</option>
          </select>
        </div>

        <div className="form-group">
          <label>Meeting Link:</label>
          <input
            type="url"
            value={formData.meetingLink}
            onChange={(e) => setFormData({...formData, meetingLink: e.target.value})}
            placeholder="https://meet.google.com/..."
          />
        </div>

        <div className="form-group">
          <label>Agenda:</label>
          <textarea
            value={formData.agenda}
            onChange={(e) => setFormData({...formData, agenda: e.target.value})}
            placeholder="Discussion points and meeting objectives..."
          />
        </div>

        <button type="submit">Schedule Meeting</button>
      </form>

      {/* Meetings List */}
      <div className="meetings-list">
        <h3>Upcoming Meetings</h3>
        {meetings.map(meeting => (
          <div key={meeting.id} className="meeting-card">
            <h4>{meeting.title}</h4>
            <p>Employee: {meeting.employee_name}</p>
            <p>Date: {new Date(meeting.scheduled_date).toLocaleString()}</p>
            <p>Status: <span className={`status ${meeting.status}`}>{meeting.status}</span></p>
            {meeting.ml_risk_level && (
              <p>Risk Level: <span className={`risk ${meeting.ml_risk_level}`}>
                {meeting.ml_risk_level}
              </span></p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
```

---

## ⭐ Performance Reviews Feature

### API Endpoints:
- `GET /api/hr/reviews/` - Get all reviews
- `POST /api/hr/reviews/` - Create new review
- `PUT /api/hr/reviews/{id}/` - Update review
- `POST /api/hr/reviews/{id}/acknowledge/` - Employee acknowledge review

### 1. Get Performance Reviews
```javascript
const getPerformanceReviews = async (token, filters = {}) => {
  const queryParams = new URLSearchParams(filters).toString();
  const url = `${API_BASE}/hr/reviews/${queryParams ? '?' + queryParams : ''}`;
  
  try {
    const response = await fetch(url, {
      headers: getHeaders(token)
    });
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch reviews:', error);
  }
};
```

### 2. Create Performance Review
```javascript
const createPerformanceReview = async (token, reviewData) => {
  try {
    const response = await fetch(`${API_BASE}/hr/reviews/`, {
      method: 'POST',
      headers: getHeaders(token),
      body: JSON.stringify({
        employee: reviewData.employeeId,
        review_period: reviewData.period, // 'quarterly', 'annual'
        review_date: reviewData.reviewDate,
        period_start: reviewData.periodStart,
        period_end: reviewData.periodEnd,
        overall_rating: reviewData.overallRating, // 1-5 stars
        technical_skills: reviewData.technicalSkills,
        communication: reviewData.communication,
        teamwork: reviewData.teamwork,
        leadership: reviewData.leadership,
        initiative: reviewData.initiative,
        problem_solving: reviewData.problemSolving,
        strengths: reviewData.strengths,
        areas_for_improvement: reviewData.areasForImprovement,
        goals_for_next_period: reviewData.goals,
        additional_notes: reviewData.notes
      })
    });
    
    return await response.json();
  } catch (error) {
    console.error('Failed to create review:', error);
  }
};
```

### 3. React Component - Performance Review Form
```jsx
import React, { useState } from 'react';

const StarRating = ({ rating, onRatingChange, label }) => {
  return (
    <div className="star-rating">
      <label>{label}:</label>
      <div className="stars">
        {[1, 2, 3, 4, 5].map(star => (
          <span
            key={star}
            className={`star ${star <= rating ? 'filled' : ''}`}
            onClick={() => onRatingChange(star)}
          >
            ⭐
          </span>
        ))}
      </div>
      <span className="rating-text">({rating}/5)</span>
    </div>
  );
};

const PerformanceReviewForm = ({ employeeId, onSubmit }) => {
  const [reviewData, setReviewData] = useState({
    employeeId: employeeId,
    period: 'quarterly',
    reviewDate: new Date().toISOString().split('T')[0],
    periodStart: '',
    periodEnd: '',
    overallRating: 3,
    technicalSkills: 3,
    communication: 3,
    teamwork: 3,
    leadership: 3,
    initiative: 3,
    problemSolving: 3,
    strengths: '',
    areasForImprovement: '',
    goals: '',
    notes: ''
  });

  const handleRatingChange = (field, value) => {
    setReviewData({...reviewData, [field]: value});
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('admin_token');
    const result = await createPerformanceReview(token, reviewData);
    
    if (result && result.id) {
      onSubmit(result);
      alert('Performance review created successfully!');
    }
  };

  return (
    <div className="performance-review-form">
      <h2>Performance Review</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="form-group">
            <label>Review Period:</label>
            <select 
              value={reviewData.period}
              onChange={(e) => setReviewData({...reviewData, period: e.target.value})}
            >
              <option value="quarterly">Quarterly</option>
              <option value="annual">Annual</option>
            </select>
          </div>

          <div className="form-group">
            <label>Review Date:</label>
            <input
              type="date"
              value={reviewData.reviewDate}
              onChange={(e) => setReviewData({...reviewData, reviewDate: e.target.value})}
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Period Start:</label>
            <input
              type="date"
              value={reviewData.periodStart}
              onChange={(e) => setReviewData({...reviewData, periodStart: e.target.value})}
            />
          </div>

          <div className="form-group">
            <label>Period End:</label>
            <input
              type="date"
              value={reviewData.periodEnd}
              onChange={(e) => setReviewData({...reviewData, periodEnd: e.target.value})}
            />
          </div>
        </div>

        {/* Star Ratings */}
        <div className="ratings-section">
          <h3>Performance Ratings</h3>
          
          <StarRating
            rating={reviewData.overallRating}
            onRatingChange={(value) => handleRatingChange('overallRating', value)}
            label="Overall Performance"
          />
          
          <StarRating
            rating={reviewData.technicalSkills}
            onRatingChange={(value) => handleRatingChange('technicalSkills', value)}
            label="Technical Skills"
          />
          
          <StarRating
            rating={reviewData.communication}
            onRatingChange={(value) => handleRatingChange('communication', value)}
            label="Communication"
          />
          
          <StarRating
            rating={reviewData.teamwork}
            onRatingChange={(value) => handleRatingChange('teamwork', value)}
            label="Teamwork"
          />
          
          <StarRating
            rating={reviewData.leadership}
            onRatingChange={(value) => handleRatingChange('leadership', value)}
            label="Leadership"
          />
          
          <StarRating
            rating={reviewData.initiative}
            onRatingChange={(value) => handleRatingChange('initiative', value)}
            label="Initiative"
          />
          
          <StarRating
            rating={reviewData.problemSolving}
            onRatingChange={(value) => handleRatingChange('problemSolving', value)}
            label="Problem Solving"
          />
        </div>

        {/* Text Areas */}
        <div className="form-group">
          <label>Strengths:</label>
          <textarea
            value={reviewData.strengths}
            onChange={(e) => setReviewData({...reviewData, strengths: e.target.value})}
            placeholder="Employee's key strengths and accomplishments..."
          />
        </div>

        <div className="form-group">
          <label>Areas for Improvement:</label>
          <textarea
            value={reviewData.areasForImprovement}
            onChange={(e) => setReviewData({...reviewData, areasForImprovement: e.target.value})}
            placeholder="Areas where employee can improve..."
          />
        </div>

        <div className="form-group">
          <label>Goals for Next Period:</label>
          <textarea
            value={reviewData.goals}
            onChange={(e) => setReviewData({...reviewData, goals: e.target.value})}
            placeholder="SMART goals for the next review period..."
          />
        </div>

        <div className="form-group">
          <label>Additional Notes:</label>
          <textarea
            value={reviewData.notes}
            onChange={(e) => setReviewData({...reviewData, notes: e.target.value})}
            placeholder="Any additional observations or notes..."
          />
        </div>

        <button type="submit" className="submit-btn">
          Create Performance Review
        </button>
      </form>
    </div>
  );
};
```

---

## 📊 Analytics & Charts Feature

### API Endpoints:
- `GET /api/hr/analytics/dashboard/` - Complete dashboard data
- `GET /api/hr/analytics/charts/` - Chart data for frontend

### 1. Get Analytics Data
```javascript
const getAnalyticsData = async (token) => {
  try {
    const response = await fetch(`${API_BASE}/hr/analytics/dashboard/`, {
      headers: getHeaders(token)
    });
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch analytics:', error);
  }
};

const getChartData = async (token) => {
  try {
    const response = await fetch(`${API_BASE}/hr/analytics/charts/`, {
      headers: getHeaders(token)
    });
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch chart data:', error);
  }
};
```

### 2. React Component - Analytics Dashboard
```jsx
import React, { useState, useEffect } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, PointElement, LineElement } from 'chart.js';
import { Pie, Bar, Line, Scatter } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, PointElement, LineElement);

const AnalyticsDashboard = () => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalyticsData();
  }, []);

  const loadAnalyticsData = async () => {
    setLoading(true);
    const token = localStorage.getItem('admin_token');
    
    try {
      const [analytics, charts] = await Promise.all([
        getAnalyticsData(token),
        getChartData(token)
      ]);
      
      setAnalyticsData(analytics);
      setChartData(charts);
    } catch (error) {
      console.error('Failed to load analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading analytics...</div>;

  // Risk Distribution Pie Chart
  const riskDistributionData = {
    labels: ['Low Risk', 'Medium Risk', 'High Risk'],
    datasets: [{
      data: [
        chartData?.risk_distribution?.low || 0,
        chartData?.risk_distribution?.medium || 0,
        chartData?.risk_distribution?.high || 0
      ],
      backgroundColor: ['#4CAF50', '#FF9800', '#F44336'],
      borderWidth: 2
    }]
  };

  // Department Risk Bar Chart
  const departmentRiskData = {
    labels: chartData?.department_risk?.map(d => d.department) || [],
    datasets: [{
      label: 'Average Risk Score',
      data: chartData?.department_risk?.map(d => d.avg_risk) || [],
      backgroundColor: '#2196F3',
      borderColor: '#1976D2',
      borderWidth: 1
    }]
  };

  // Performance Trend Line Chart
  const performanceTrendData = {
    labels: chartData?.performance_trends?.map(t => t.month) || [],
    datasets: [{
      label: 'Average Performance Rating',
      data: chartData?.performance_trends?.map(t => t.avg_rating) || [],
      borderColor: '#4CAF50',
      backgroundColor: 'rgba(76, 175, 80, 0.1)',
      tension: 0.4
    }]
  };

  return (
    <div className="analytics-dashboard">
      <h1>HR Analytics Dashboard</h1>
      
      {/* Summary Cards */}
      <div className="summary-cards">
        <div className="card">
          <h3>Total Employees</h3>
          <div className="value">{analyticsData?.total_employees || 0}</div>
        </div>
        
        <div className="card">
          <h3>High Risk Employees</h3>
          <div className="value danger">{analyticsData?.high_risk_count || 0}</div>
        </div>
        
        <div className="card">
          <h3>Avg Performance Rating</h3>
          <div className="value">{analyticsData?.avg_performance?.toFixed(1) || 'N/A'}</div>
        </div>
        
        <div className="card">
          <h3>Pending Reviews</h3>
          <div className="value warning">{analyticsData?.pending_reviews || 0}</div>
        </div>
      </div>

      {/* Charts */}
      <div className="charts-grid">
        <div className="chart-container">
          <h3>Turnover Risk Distribution</h3>
          <Pie 
            data={riskDistributionData}
            options={{
              responsive: true,
              plugins: {
                legend: {
                  position: 'bottom'
                }
              }
            }}
          />
        </div>

        <div className="chart-container">
          <h3>Risk by Department</h3>
          <Bar 
            data={departmentRiskData}
            options={{
              responsive: true,
              scales: {
                y: {
                  beginAtZero: true,
                  max: 1
                }
              }
            }}
          />
        </div>

        <div className="chart-container">
          <h3>Performance Trends</h3>
          <Line 
            data={performanceTrendData}
            options={{
              responsive: true,
              scales: {
                y: {
                  beginAtZero: true,
                  max: 5
                }
              }
            }}
          />
        </div>
      </div>

      {/* Recent Activities */}
      <div className="recent-activities">
        <h3>Recent Activities</h3>
        <div className="activities-list">
          {analyticsData?.recent_meetings?.map(meeting => (
            <div key={meeting.id} className="activity-item">
              <span className="activity-type">📅 Meeting</span>
              <span className="activity-desc">
                {meeting.title} with {meeting.employee_name}
              </span>
              <span className="activity-date">
                {new Date(meeting.created_at).toLocaleDateString()}
              </span>
            </div>
          ))}
          
          {analyticsData?.recent_reviews?.map(review => (
            <div key={review.id} className="activity-item">
              <span className="activity-type">⭐ Review</span>
              <span className="activity-desc">
                Performance review for {review.employee_name} 
                (Rating: {review.overall_rating}/5)
              </span>
              <span className="activity-date">
                {new Date(review.created_at).toLocaleDateString()}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
```

---

## 🎨 CSS Styling

```css
/* Analytics Dashboard Styles */
.analytics-dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
}

.card h3 {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 14px;
  font-weight: 500;
}

.card .value {
  font-size: 32px;
  font-weight: bold;
  color: #333;
}

.card .value.danger { color: #F44336; }
.card .value.warning { color: #FF9800; }

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-bottom: 30px;
}

.chart-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.chart-container h3 {
  margin: 0 0 20px 0;
  color: #333;
  text-align: center;
}

/* Meeting Scheduler Styles */
.meeting-scheduler {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

.meetings-list {
  margin-top: 40px;
}

.meeting-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 15px;
}

.meeting-card h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
}

.status.scheduled { background: #E3F2FD; color: #1976D2; }
.status.completed { background: #E8F5E8; color: #388E3C; }
.status.cancelled { background: #FFEBEE; color: #D32F2F; }

.risk.high { color: #F44336; font-weight: bold; }
.risk.medium { color: #FF9800; font-weight: bold; }
.risk.low { color: #4CAF50; font-weight: bold; }

/* Performance Review Styles */
.performance-review-form {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.ratings-section {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin: 20px 0;
}

.star-rating {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  gap: 10px;
}

.star-rating label {
  min-width: 150px;
  margin-bottom: 0;
}

.stars {
  display: flex;
  gap: 5px;
}

.star {
  font-size: 20px;
  cursor: pointer;
  filter: grayscale(100%);
  transition: all 0.2s;
}

.star.filled {
  filter: grayscale(0%);
}

.star:hover {
  transform: scale(1.1);
}

.rating-text {
  font-size: 14px;
  color: #666;
  margin-left: 10px;
}

.submit-btn {
  background: #2196F3;
  color: white;
  padding: 12px 30px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.2s;
}

.submit-btn:hover {
  background: #1976D2;
}

/* Recent Activities */
.recent-activities {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.activities-list {
  max-height: 400px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
  gap: 15px;
}

.activity-type {
  font-size: 16px;
  min-width: 80px;
}

.activity-desc {
  flex: 1;
  color: #333;
}

.activity-date {
  color: #666;
  font-size: 12px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .summary-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .activity-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
}
```

---

## 🚨 Error Handling

```javascript
// Error handling utility
const handleApiError = (error, response) => {
  if (response?.status === 401) {
    // Token expired or invalid
    localStorage.removeItem('admin_token');
    window.location.href = '/login';
    return;
  }
  
  if (response?.status === 403) {
    alert('You do not have permission to perform this action.');
    return;
  }
  
  if (response?.status >= 500) {
    alert('Server error. Please try again later.');
    return;
  }
  
  console.error('API Error:', error);
  alert('An error occurred. Please check the console for details.');
};

// Enhanced fetch wrapper
const apiRequest = async (url, options = {}) => {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    });
    
    if (!response.ok) {
      handleApiError(new Error(`HTTP ${response.status}`), response);
      return null;
    }
    
    return await response.json();
  } catch (error) {
    handleApiError(error);
    return null;
  }
};
```

---

## 💡 Best Practices

### 1. State Management
```javascript
// Menggunakan Context untuk global state
import React, { createContext, useContext, useReducer } from 'react';

const HRContext = createContext();

const hrReducer = (state, action) => {
  switch (action.type) {
    case 'SET_MEETINGS':
      return { ...state, meetings: action.payload };
    case 'ADD_MEETING':
      return { ...state, meetings: [...state.meetings, action.payload] };
    case 'SET_REVIEWS':
      return { ...state, reviews: action.payload };
    case 'SET_ANALYTICS':
      return { ...state, analytics: action.payload };
    default:
      return state;
  }
};

export const HRProvider = ({ children }) => {
  const [state, dispatch] = useReducer(hrReducer, {
    meetings: [],
    reviews: [],
    analytics: null
  });

  return (
    <HRContext.Provider value={{ state, dispatch }}>
      {children}
    </HRContext.Provider>
  );
};

export const useHR = () => useContext(HRContext);
```

### 2. Custom Hooks
```javascript
// Custom hook untuk meetings
import { useState, useEffect } from 'react';

export const useMeetings = () => {
  const [meetings, setMeetings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchMeetings = async (filters = {}) => {
    setLoading(true);
    setError(null);
    
    try {
      const token = localStorage.getItem('admin_token');
      const data = await getMeetings(token, filters);
      setMeetings(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const createMeeting = async (meetingData) => {
    try {
      const token = localStorage.getItem('admin_token');
      const newMeeting = await createMeeting(token, meetingData);
      setMeetings(prev => [...prev, newMeeting]);
      return newMeeting;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  useEffect(() => {
    fetchMeetings();
  }, []);

  return {
    meetings,
    loading,
    error,
    fetchMeetings,
    createMeeting
  };
};
```

### 3. Data Validation
```javascript
// Validation schemas
const meetingValidation = {
  employeeId: (value) => value ? null : 'Employee is required',
  title: (value) => value?.length >= 3 ? null : 'Title must be at least 3 characters',
  scheduledDate: (value) => {
    const date = new Date(value);
    const now = new Date();
    return date > now ? null : 'Meeting date must be in the future';
  },
  duration: (value) => value >= 15 ? null : 'Duration must be at least 15 minutes'
};

const validateForm = (data, schema) => {
  const errors = {};
  
  Object.keys(schema).forEach(field => {
    const error = schema[field](data[field]);
    if (error) errors[field] = error;
  });
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};
```

---

## 🚀 Quick Start Example

```javascript
// App.js - Main application setup
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { HRProvider } from './contexts/HRContext';
import Dashboard from './pages/Dashboard';
import Meetings from './pages/Meetings';
import Reviews from './pages/Reviews';
import Analytics from './pages/Analytics';

function App() {
  return (
    <HRProvider>
      <Router>
        <div className="app">
          <nav>
            <a href="/dashboard">Dashboard</a>
            <a href="/meetings">Meetings</a>
            <a href="/reviews">Reviews</a>
            <a href="/analytics">Analytics</a>
          </nav>
          
          <main>
            <Routes>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/meetings" element={<Meetings />} />
              <Route path="/reviews" element={<Reviews />} />
              <Route path="/analytics" element={<Analytics />} />
            </Routes>
          </main>
        </div>
      </Router>
    </HRProvider>
  );
}

export default App;
```

## 📝 Testing dengan Postman

1. **Import Collection**: Import file `HR_FEATURES_COMPLETE_POSTMAN.json`
2. **Set Variables**: 
   - `base_url`: `https://turnover-api-hd7ze.ondigitalocean.app`
   - `admin_token`: Will be set automatically after login
3. **Run Authentication**: Execute "Admin Login" request first
4. **Test Endpoints**: Run other requests in sequence

## 🔧 Deployment Notes

Pastikan backend sudah ter-deploy dengan:
- Models sudah di-migrate
- Endpoint sudah aktif 
- CORS sudah dikonfigurasi untuk domain frontend
- Authentication sudah berjalan

---

Dengan tutorial ini, frontend developer dapat mengintegrasikan semua HR Features dengan mudah dan efisien! 🎉
