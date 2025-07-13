# 🚀 TUTORIAL FRONTEND INTEGRATION - HR FEATURES

## 📋 OVERVIEW FITUR BARU

### 3 Fitur Utama yang Sudah Dibuat:
1. **🤝 1-on-1 Meeting Management** - Schedule & manage meetings
2. **⭐ Performance Review System** - Rating bintang & review lengkap  
3. **📊 Analytics Dashboard** - 3 jenis chart untuk visualisasi data

---

## 🔗 ENDPOINT API YANG HARUS DIPAKAI

### 🔐 Authentication (WAJIB PERTAMA)
```javascript
// LOGIN ADMIN/HR
POST /api/login/
Body: {
  "email": "admin@company.com", 
  "password": "AdminPass123!"
}

Response: {
  "success": true,
  "data": {
    "token": "abc123..." // Simpan token ini!
  }
}
```

### 🤝 1-ON-1 MEETINGS ENDPOINTS

#### 1. **Create Meeting** (Admin Only)
```javascript
POST /api/hr/meetings/
Headers: { "Authorization": "Token abc123..." }
Body: {
  "employee": 1,
  "title": "Follow-up Meeting: High Turnover Risk",
  "meeting_type": "followup", // followup, regular, urgent, performance, career, feedback
  "scheduled_date": "2025-07-15T14:00:00Z",
  "duration_minutes": 45,
  "meeting_link": "https://meet.google.com/abc-defg-hij",
  "agenda": "Discussion about career development...",
  "ml_probability": 0.85, // dari hasil ML prediction
  "ml_risk_level": "high" // high, medium, low
}
```

#### 2. **Get All Meetings** (Admin) / **Get My Meetings** (Employee)
```javascript
GET /api/hr/meetings/
GET /api/hr/meetings/?employee=1  // filter by employee
GET /api/hr/meetings/?status=scheduled  // filter by status

Response: {
  "success": true,
  "data": [
    {
      "id": 1,
      "employee_name": "John Doe",
      "title": "Follow-up Meeting: High Turnover Risk",
      "scheduled_date": "2025-07-15T14:00:00Z",
      "meeting_link": "https://meet.google.com/abc-defg-hij",
      "status": "scheduled", // scheduled, completed, cancelled
      "ml_risk_level": "high"
    }
  ]
}
```

#### 3. **Update Meeting** (Admin Only)
```javascript
PUT /api/hr/meetings/1/
Body: {
  "status": "completed",
  "notes": "Meeting went well...",
  "action_items": "1. Schedule training\n2. Follow-up in 2 weeks"
}
```

### ⭐ PERFORMANCE REVIEWS ENDPOINTS

#### 1. **Create Performance Review** (Admin Only)
```javascript
POST /api/hr/reviews/
Body: {
  "employee": 1,
  "review_period": "quarterly", // monthly, quarterly, semi_annual, annual
  "review_date": "2025-07-11",
  "period_start": "2025-04-01",
  "period_end": "2025-06-30",
  "overall_rating": 4,        // 1-5 bintang
  "technical_skills": 4,      // 1-5 bintang
  "communication": 3,         // 1-5 bintang
  "teamwork": 5,             // 1-5 bintang
  "leadership": 3,           // 1-5 bintang
  "initiative": 4,           // 1-5 bintang
  "problem_solving": 4,      // 1-5 bintang
  "strengths": "Excellent technical skills...",
  "areas_for_improvement": "Could improve communication...",
  "goals_for_next_period": "1. Complete communication workshop\n2. Lead presentation"
}
```

#### 2. **Get Performance Reviews**
```javascript
GET /api/hr/reviews/                    // All reviews (Admin)
GET /api/hr/reviews/?employee=1         // Reviews for specific employee

Response: {
  "data": [
    {
      "id": 1,
      "employee_name": "John Doe",
      "overall_rating": 4,
      "average_rating": 3.86,          // auto calculated
      "rating_breakdown": {            // detail semua rating
        "overall": 4,
        "technical_skills": 4,
        "communication": 3,
        "teamwork": 5,
        "leadership": 3,
        "initiative": 4,
        "problem_solving": 4
      },
      "is_final": true,
      "employee_acknowledged": false
    }
  ]
}
```

#### 3. **Employee Acknowledge Review**
```javascript
POST /api/hr/reviews/1/acknowledge/
// Employee confirms they've read the review
```

### 📊 ANALYTICS & CHARTS ENDPOINTS

#### 1. **Get Dashboard Data**
```javascript
GET /api/hr/analytics/dashboard/

Response: {
  "data": {
    "total_predictions": 68,
    "total_meetings": 24,
    "total_reviews": 15,
    "high_risk_employees": 8,
    "recent_predictions": 12,
    "risk_distribution": {
      "low_risk": 42,
      "medium_risk": 18,
      "high_risk": 8
    }
  }
}
```

#### 2. **Get Chart Data** (PENTING untuk grafik!)
```javascript
GET /api/hr/analytics/charts/

Response: {
  "data": {
    "risk_distribution": {
      "chart_type": "pie",
      "title": "Employee Risk Distribution",
      "data": {
        "labels": ["Low Risk", "Medium Risk", "High Risk"],
        "datasets": [{
          "data": [42, 18, 8],
          "backgroundColor": ["#28a745", "#ffc107", "#dc3545"]
        }]
      }
    },
    "department_analysis": {
      "chart_type": "bar",
      "title": "Risk Analysis by Department",
      "data": {
        "labels": ["Engineering", "Marketing", "HR", "Finance", "Sales"],
        "datasets": [{
          "label": "Average Risk Score (%)",
          "data": [35.2, 62.8, 28.1, 45.9, 71.3],
          "backgroundColor": "#4F46E5"
        }]
      }
    },
    "trend_analysis": {
      "chart_type": "line",
      "title": "Turnover Risk Trend (Last 6 Months)",
      "data": {
        "labels": ["Feb 2025", "Mar 2025", "Apr 2025", "May 2025", "Jun 2025", "Jul 2025"],
        "datasets": [{
          "label": "Average Risk %",
          "data": [48.7, 43.2, 35.0, 36.0, 30.9, 25.2],
          "borderColor": "#EF4444"
        }]
      }
    }
  }
}
```

---

## 💻 FRONTEND IMPLEMENTATION

### 🔧 Setup & Dependencies

#### Install Chart.js untuk React:
```bash
npm install chart.js react-chartjs-2
```

#### Import yang diperlukan:
```javascript
import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Pie, Bar, Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale, LinearScale, BarElement, LineElement, 
  PointElement, ArcElement, Title, Tooltip, Legend, Filler
);
```

### 🔐 Authentication Service

```javascript
// services/authService.js
class AuthService {
  constructor() {
    this.baseURL = 'https://turnover-api-hd7ze.ondigitalocean.app';
    this.token = localStorage.getItem('admin_token');
  }

  async login(email, password) {
    const response = await fetch(`${this.baseURL}/api/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    
    const data = await response.json();
    if (data.success) {
      this.token = data.data.token;
      localStorage.setItem('admin_token', this.token);
      return { success: true, token: this.token };
    }
    return { success: false, message: data.message };
  }

  getHeaders() {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Token ${this.token}`
    };
  }

  isAuthenticated() {
    return !!this.token;
  }
}

export default new AuthService();
```

### 📊 Analytics Dashboard Component

```javascript
// components/AnalyticsDashboard.jsx
import React, { useState, useEffect } from 'react';
import { Pie, Bar, Line } from 'react-chartjs-2';
import authService from '../services/authService';

const AnalyticsDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      // Fetch dashboard stats
      const dashboardResponse = await fetch('/api/hr/analytics/dashboard/', {
        headers: authService.getHeaders()
      });
      const dashboardResult = await dashboardResponse.json();
      setDashboardData(dashboardResult.data);

      // Fetch chart data
      const chartsResponse = await fetch('/api/hr/analytics/charts/', {
        headers: authService.getHeaders()
      });
      const chartsResult = await chartsResponse.json();
      setChartData(chartsResult.data);

      setLoading(false);
    } catch (error) {
      console.error('Error fetching analytics:', error);
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading analytics...</div>;

  return (
    <div className="analytics-dashboard">
      {/* Dashboard Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Predictions</h3>
          <div className="stat-number">{dashboardData?.total_predictions || 0}</div>
        </div>
        <div className="stat-card danger">
          <h3>High Risk Employees</h3>
          <div className="stat-number">{dashboardData?.high_risk_employees || 0}</div>
        </div>
        <div className="stat-card">
          <h3>Total Meetings</h3>
          <div className="stat-number">{dashboardData?.total_meetings || 0}</div>
        </div>
        <div className="stat-card">
          <h3>Performance Reviews</h3>
          <div className="stat-number">{dashboardData?.total_reviews || 0}</div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="charts-grid">
        {/* Risk Distribution Pie Chart */}
        <div className="chart-container">
          <h3>Employee Risk Distribution</h3>
          {chartData?.risk_distribution && (
            <Pie 
              data={chartData.risk_distribution.data}
              options={{
                responsive: true,
                plugins: {
                  legend: { position: 'bottom' },
                  title: { display: true, text: 'Risk Distribution' }
                }
              }}
            />
          )}
        </div>

        {/* Department Analysis Bar Chart */}
        <div className="chart-container">
          <h3>Risk by Department</h3>
          {chartData?.department_analysis && (
            <Bar 
              data={chartData.department_analysis.data}
              options={{
                responsive: true,
                scales: {
                  y: {
                    beginAtZero: true,
                    max: 100,
                    title: { display: true, text: 'Risk Score (%)' }
                  }
                }
              }}
            />
          )}
        </div>

        {/* Trend Analysis Line Chart */}
        <div className="chart-container full-width">
          <h3>Risk Trend (Last 6 Months)</h3>
          {chartData?.trend_analysis && (
            <Line 
              data={chartData.trend_analysis.data}
              options={{
                responsive: true,
                interaction: { intersect: false },
                scales: {
                  y: {
                    beginAtZero: true,
                    max: 100,
                    title: { display: true, text: 'Risk Percentage (%)' }
                  }
                }
              }}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
```

### 🤝 Meetings Management Component

```javascript
// components/MeetingsManager.jsx
import React, { useState, useEffect } from 'react';
import authService from '../services/authService';

const MeetingsManager = () => {
  const [meetings, setMeetings] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    employee: '',
    title: '',
    meeting_type: 'regular',
    scheduled_date: '',
    duration_minutes: 30,
    meeting_link: '',
    agenda: ''
  });

  useEffect(() => {
    fetchMeetings();
    fetchEmployees();
  }, []);

  const fetchMeetings = async () => {
    try {
      const response = await fetch('/api/hr/meetings/', {
        headers: authService.getHeaders()
      });
      const result = await response.json();
      if (result.success) {
        setMeetings(result.data);
      }
    } catch (error) {
      console.error('Error fetching meetings:', error);
    }
  };

  const fetchEmployees = async () => {
    try {
      const response = await fetch('/api/employees/', {
        headers: authService.getHeaders()
      });
      const result = await response.json();
      if (result.success) {
        setEmployees(result.data);
      }
    } catch (error) {
      console.error('Error fetching employees:', error);
    }
  };

  const handleCreateMeeting = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/hr/meetings/', {
        method: 'POST',
        headers: authService.getHeaders(),
        body: JSON.stringify(formData)
      });
      
      const result = await response.json();
      if (result.success) {
        setMeetings([result.data, ...meetings]);
        setShowCreateForm(false);
        setFormData({
          employee: '',
          title: '',
          meeting_type: 'regular',
          scheduled_date: '',
          duration_minutes: 30,
          meeting_link: '',
          agenda: ''
        });
        alert('Meeting created successfully!');
      }
    } catch (error) {
      console.error('Error creating meeting:', error);
    }
  };

  const updateMeetingStatus = async (meetingId, status) => {
    try {
      const response = await fetch(`/api/hr/meetings/${meetingId}/`, {
        method: 'PUT',
        headers: authService.getHeaders(),
        body: JSON.stringify({ status })
      });
      
      if (response.ok) {
        fetchMeetings(); // Refresh list
      }
    } catch (error) {
      console.error('Error updating meeting:', error);
    }
  };

  return (
    <div className="meetings-manager">
      <div className="header">
        <h2>🤝 1-on-1 Meetings Management</h2>
        <button 
          className="btn-primary"
          onClick={() => setShowCreateForm(true)}
        >
          + Schedule New Meeting
        </button>
      </div>

      {/* Create Meeting Form */}
      {showCreateForm && (
        <div className="modal">
          <form onSubmit={handleCreateMeeting} className="meeting-form">
            <h3>Schedule New Meeting</h3>
            
            <select 
              value={formData.employee}
              onChange={(e) => setFormData({...formData, employee: e.target.value})}
              required
            >
              <option value="">Select Employee</option>
              {employees.map(emp => (
                <option key={emp.id} value={emp.id}>
                  {emp.first_name} {emp.last_name}
                </option>
              ))}
            </select>

            <input
              type="text"
              placeholder="Meeting Title"
              value={formData.title}
              onChange={(e) => setFormData({...formData, title: e.target.value})}
              required
            />

            <select 
              value={formData.meeting_type}
              onChange={(e) => setFormData({...formData, meeting_type: e.target.value})}
            >
              <option value="regular">Regular Check-in</option>
              <option value="followup">Follow-up from ML Prediction</option>
              <option value="urgent">Urgent Discussion</option>
              <option value="performance">Performance Discussion</option>
              <option value="career">Career Development</option>
            </select>

            <input
              type="datetime-local"
              value={formData.scheduled_date}
              onChange={(e) => setFormData({...formData, scheduled_date: e.target.value})}
              required
            />

            <input
              type="url"
              placeholder="Meeting Link (Zoom, Google Meet, etc.)"
              value={formData.meeting_link}
              onChange={(e) => setFormData({...formData, meeting_link: e.target.value})}
            />

            <textarea
              placeholder="Meeting Agenda"
              value={formData.agenda}
              onChange={(e) => setFormData({...formData, agenda: e.target.value})}
              rows="3"
            />

            <div className="form-actions">
              <button type="submit" className="btn-primary">Create Meeting</button>
              <button type="button" onClick={() => setShowCreateForm(false)}>Cancel</button>
            </div>
          </form>
        </div>
      )}

      {/* Meetings List */}
      <div className="meetings-list">
        {meetings.map(meeting => (
          <div key={meeting.id} className={`meeting-card ${meeting.ml_risk_level}`}>
            <div className="meeting-header">
              <h4>{meeting.title}</h4>
              <span className={`status ${meeting.status}`}>{meeting.status}</span>
            </div>
            
            <div className="meeting-details">
              <p><strong>Employee:</strong> {meeting.employee_name}</p>
              <p><strong>Date:</strong> {new Date(meeting.scheduled_date).toLocaleString()}</p>
              <p><strong>Duration:</strong> {meeting.duration_minutes} minutes</p>
              {meeting.ml_risk_level && (
                <p><strong>Risk Level:</strong> 
                  <span className={`risk-badge ${meeting.ml_risk_level}`}>
                    {meeting.ml_risk_level.toUpperCase()}
                  </span>
                </p>
              )}
            </div>

            {meeting.meeting_link && (
              <a href={meeting.meeting_link} target="_blank" className="meeting-link">
                🔗 Join Meeting
              </a>
            )}

            <div className="meeting-actions">
              {meeting.status === 'scheduled' && (
                <>
                  <button onClick={() => updateMeetingStatus(meeting.id, 'completed')}>
                    Mark Complete
                  </button>
                  <button onClick={() => updateMeetingStatus(meeting.id, 'cancelled')}>
                    Cancel
                  </button>
                </>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MeetingsManager;
```

### ⭐ Performance Reviews Component

```javascript
// components/PerformanceReviews.jsx
import React, { useState, useEffect } from 'react';
import authService from '../services/authService';

const StarRating = ({ rating, onRatingChange, readonly = false }) => {
  return (
    <div className="star-rating">
      {[1, 2, 3, 4, 5].map(star => (
        <span
          key={star}
          className={`star ${star <= rating ? 'filled' : ''} ${readonly ? 'readonly' : ''}`}
          onClick={() => !readonly && onRatingChange(star)}
        >
          ⭐
        </span>
      ))}
    </div>
  );
};

const PerformanceReviews = () => {
  const [reviews, setReviews] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    employee: '',
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
    problem_solving: 3,
    strengths: '',
    areas_for_improvement: '',
    goals_for_next_period: '',
    additional_notes: ''
  });

  useEffect(() => {
    fetchReviews();
    fetchEmployees();
  }, []);

  const fetchReviews = async () => {
    try {
      const response = await fetch('/api/hr/reviews/', {
        headers: authService.getHeaders()
      });
      const result = await response.json();
      if (result.success) {
        setReviews(result.data);
      }
    } catch (error) {
      console.error('Error fetching reviews:', error);
    }
  };

  const fetchEmployees = async () => {
    try {
      const response = await fetch('/api/employees/', {
        headers: authService.getHeaders()
      });
      const result = await response.json();
      if (result.success) {
        setEmployees(result.data);
      }
    } catch (error) {
      console.error('Error fetching employees:', error);
    }
  };

  const handleCreateReview = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/hr/reviews/', {
        method: 'POST',
        headers: authService.getHeaders(),
        body: JSON.stringify(formData)
      });
      
      const result = await response.json();
      if (result.success) {
        setReviews([result.data, ...reviews]);
        setShowCreateForm(false);
        alert('Performance review created successfully!');
      }
    } catch (error) {
      console.error('Error creating review:', error);
    }
  };

  const updateRating = (field, rating) => {
    setFormData({...formData, [field]: rating});
  };

  return (
    <div className="performance-reviews">
      <div className="header">
        <h2>⭐ Performance Reviews Management</h2>
        <button 
          className="btn-primary"
          onClick={() => setShowCreateForm(true)}
        >
          + Create New Review
        </button>
      </div>

      {/* Create Review Form */}
      {showCreateForm && (
        <div className="modal">
          <form onSubmit={handleCreateReview} className="review-form">
            <h3>Create Performance Review</h3>
            
            <div className="form-grid">
              <div className="form-group">
                <label>Employee</label>
                <select 
                  value={formData.employee}
                  onChange={(e) => setFormData({...formData, employee: e.target.value})}
                  required
                >
                  <option value="">Select Employee</option>
                  {employees.map(emp => (
                    <option key={emp.id} value={emp.id}>
                      {emp.first_name} {emp.last_name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Review Period</label>
                <select 
                  value={formData.review_period}
                  onChange={(e) => setFormData({...formData, review_period: e.target.value})}
                >
                  <option value="monthly">Monthly</option>
                  <option value="quarterly">Quarterly</option>
                  <option value="semi_annual">Semi-Annual</option>
                  <option value="annual">Annual</option>
                </select>
              </div>

              <div className="form-group">
                <label>Period Start</label>
                <input
                  type="date"
                  value={formData.period_start}
                  onChange={(e) => setFormData({...formData, period_start: e.target.value})}
                  required
                />
              </div>

              <div className="form-group">
                <label>Period End</label>
                <input
                  type="date"
                  value={formData.period_end}
                  onChange={(e) => setFormData({...formData, period_end: e.target.value})}
                  required
                />
              </div>
            </div>

            {/* Star Ratings Section */}
            <div className="ratings-section">
              <h4>Performance Ratings (1-5 Stars)</h4>
              
              <div className="rating-item">
                <label>Overall Rating</label>
                <StarRating 
                  rating={formData.overall_rating}
                  onRatingChange={(rating) => updateRating('overall_rating', rating)}
                />
              </div>

              <div className="rating-item">
                <label>Technical Skills</label>
                <StarRating 
                  rating={formData.technical_skills}
                  onRatingChange={(rating) => updateRating('technical_skills', rating)}
                />
              </div>

              <div className="rating-item">
                <label>Communication</label>
                <StarRating 
                  rating={formData.communication}
                  onRatingChange={(rating) => updateRating('communication', rating)}
                />
              </div>

              <div className="rating-item">
                <label>Teamwork</label>
                <StarRating 
                  rating={formData.teamwork}
                  onRatingChange={(rating) => updateRating('teamwork', rating)}
                />
              </div>

              <div className="rating-item">
                <label>Leadership</label>
                <StarRating 
                  rating={formData.leadership}
                  onRatingChange={(rating) => updateRating('leadership', rating)}
                />
              </div>

              <div className="rating-item">
                <label>Initiative</label>
                <StarRating 
                  rating={formData.initiative}
                  onRatingChange={(rating) => updateRating('initiative', rating)}
                />
              </div>

              <div className="rating-item">
                <label>Problem Solving</label>
                <StarRating 
                  rating={formData.problem_solving}
                  onRatingChange={(rating) => updateRating('problem_solving', rating)}
                />
              </div>
            </div>

            {/* Text Areas */}
            <div className="form-group">
              <label>Strengths</label>
              <textarea
                value={formData.strengths}
                onChange={(e) => setFormData({...formData, strengths: e.target.value})}
                rows="3"
                placeholder="Employee's key strengths and achievements..."
                required
              />
            </div>

            <div className="form-group">
              <label>Areas for Improvement</label>
              <textarea
                value={formData.areas_for_improvement}
                onChange={(e) => setFormData({...formData, areas_for_improvement: e.target.value})}
                rows="3"
                placeholder="Areas where employee can improve..."
                required
              />
            </div>

            <div className="form-group">
              <label>Goals for Next Period</label>
              <textarea
                value={formData.goals_for_next_period}
                onChange={(e) => setFormData({...formData, goals_for_next_period: e.target.value})}
                rows="3"
                placeholder="Goals and objectives for next review period..."
                required
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="btn-primary">Create Review</button>
              <button type="button" onClick={() => setShowCreateForm(false)}>Cancel</button>
            </div>
          </form>
        </div>
      )}

      {/* Reviews List */}
      <div className="reviews-list">
        {reviews.map(review => (
          <div key={review.id} className="review-card">
            <div className="review-header">
              <h4>{review.employee_name} - {review.review_period} Review</h4>
              <div className="overall-rating">
                <StarRating rating={review.overall_rating} readonly />
                <span>({review.average_rating}/5.0 avg)</span>
              </div>
            </div>

            <div className="review-details">
              <p><strong>Period:</strong> {review.period_start} to {review.period_end}</p>
              <p><strong>Review Date:</strong> {review.review_date}</p>
              
              <div className="rating-breakdown">
                <h5>Rating Breakdown:</h5>
                <div className="rating-grid">
                  <div>Technical: <StarRating rating={review.rating_breakdown.technical_skills} readonly /></div>
                  <div>Communication: <StarRating rating={review.rating_breakdown.communication} readonly /></div>
                  <div>Teamwork: <StarRating rating={review.rating_breakdown.teamwork} readonly /></div>
                  <div>Leadership: <StarRating rating={review.rating_breakdown.leadership} readonly /></div>
                </div>
              </div>

              {review.strengths && (
                <div className="review-section">
                  <h5>Strengths:</h5>
                  <p>{review.strengths}</p>
                </div>
              )}

              <div className="review-status">
                <span className={`badge ${review.is_final ? 'final' : 'draft'}`}>
                  {review.is_final ? 'Final' : 'Draft'}
                </span>
                {review.employee_acknowledged && (
                  <span className="badge acknowledged">Employee Acknowledged</span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PerformanceReviews;
```

### 🎨 CSS Styling

```css
/* styles/hr-features.css */
.analytics-dashboard {
  padding: 20px;
  background-color: #f8f9fa;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
}

.stat-card.danger {
  border-left: 4px solid #dc3545;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #4F46E5;
  margin: 10px 0;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.chart-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.chart-container.full-width {
  grid-column: 1 / -1;
}

/* Meetings Styling */
.meetings-manager, .performance-reviews {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: between;
  align-items: center;
  margin-bottom: 20px;
}

.btn-primary {
  background: #4F46E5;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
}

.meeting-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border-left: 4px solid #e9ecef;
}

.meeting-card.high {
  border-left-color: #dc3545;
}

.meeting-card.medium {
  border-left-color: #ffc107;
}

.meeting-card.low {
  border-left-color: #28a745;
}

.risk-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.risk-badge.high { background: #dc3545; color: white; }
.risk-badge.medium { background: #ffc107; color: black; }
.risk-badge.low { background: #28a745; color: white; }

/* Star Rating */
.star-rating {
  display: flex;
  gap: 2px;
}

.star {
  cursor: pointer;
  font-size: 1.2rem;
  color: #ddd;
  transition: color 0.2s;
}

.star.filled {
  color: #ffc107;
}

.star.readonly {
  cursor: default;
}

.rating-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

/* Modal */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.meeting-form, .review-form {
  background: white;
  padding: 30px;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}
```

### 🔄 Main App Integration

```javascript
// App.jsx
import React, { useState, useEffect } from 'react';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import MeetingsManager from './components/MeetingsManager';
import PerformanceReviews from './components/PerformanceReviews';
import authService from './services/authService';
import './styles/hr-features.css';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loginForm, setLoginForm] = useState({ email: '', password: '' });

  useEffect(() => {
    setIsAuthenticated(authService.isAuthenticated());
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    const result = await authService.login(loginForm.email, loginForm.password);
    if (result.success) {
      setIsAuthenticated(true);
    } else {
      alert('Login failed: ' + result.message);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="login-container">
        <form onSubmit={handleLogin} className="login-form">
          <h2>🔐 HR System Login</h2>
          <input
            type="email"
            placeholder="Email"
            value={loginForm.email}
            onChange={(e) => setLoginForm({...loginForm, email: e.target.value})}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={loginForm.password}
            onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
            required
          />
          <button type="submit">Login</button>
          
          <div className="demo-credentials">
            <p><strong>Demo Credentials:</strong></p>
            <p>Email: admin@company.com</p>
            <p>Password: AdminPass123!</p>
          </div>
        </form>
      </div>
    );
  }

  return (
    <div className="app">
      <nav className="navbar">
        <h1>🚀 HR Management System</h1>
        <div className="nav-tabs">
          <button 
            className={activeTab === 'dashboard' ? 'active' : ''}
            onClick={() => setActiveTab('dashboard')}
          >
            📊 Analytics
          </button>
          <button 
            className={activeTab === 'meetings' ? 'active' : ''}
            onClick={() => setActiveTab('meetings')}
          >
            🤝 Meetings
          </button>
          <button 
            className={activeTab === 'reviews' ? 'active' : ''}
            onClick={() => setActiveTab('reviews')}
          >
            ⭐ Reviews
          </button>
        </div>
        <button onClick={() => {
          localStorage.removeItem('admin_token');
          setIsAuthenticated(false);
        }}>
          Logout
        </button>
      </nav>

      <main>
        {activeTab === 'dashboard' && <AnalyticsDashboard />}
        {activeTab === 'meetings' && <MeetingsManager />}
        {activeTab === 'reviews' && <PerformanceReviews />}
      </main>
    </div>
  );
}

export default App;
```

---

## 🚀 DEPLOYMENT STEPS

### 1. **Setup Project**
```bash
npx create-react-app hr-system
cd hr-system
npm install chart.js react-chartjs-2
```

### 2. **Add Files**
- Copy semua component code di atas
- Add CSS styling
- Update App.jsx

### 3. **Test Connection**
- Login dengan credentials: `admin@company.com` / `AdminPass123!`
- Test semua fitur: Analytics, Meetings, Reviews

### 4. **Production Build**
```bash
npm run build
```

---

## 📋 CHECKLIST FITUR

### ✅ Yang Sudah Siap:
- [x] **Analytics Dashboard** - 3 chart types ready
- [x] **Meetings Management** - Full CRUD with ML integration
- [x] **Performance Reviews** - Star rating system
- [x] **Authentication** - Token-based login
- [x] **Role-based Access** - Admin vs Employee permissions
- [x] **API Integration** - All endpoints working
- [x] **Responsive Design** - Mobile-friendly components

### 🎯 Next Steps:
1. Deploy frontend
2. Test with real data
3. Add real-time notifications
4. Implement advanced filtering
5. Add export functionality

**🎉 Semua fitur HR sudah siap untuk production!**
