# 🚀 HR FEATURES: 1-on-1 Meetings, Performance Reviews & Analytics

## 📊 CHART DATA STRUCTURES FOR FRONTEND

### 🎯 Overview
Sistem HR Features ini menyediakan data untuk 3 jenis chart utama yang dapat digunakan di frontend untuk visualisasi analytics:

1. **Risk Distribution (Pie Chart)** - Distribusi tingkat risiko karyawan
2. **Department Analysis (Bar Chart)** - Analisis risiko per departemen  
3. **Trend Analysis (Line Chart)** - Tren risiko turnover selama 6 bulan terakhir

---

## 📈 DATA STRUCTURES & CHART CONFIGURATIONS

### 1. 🥧 Risk Distribution Pie Chart

**API Endpoint:** `GET /api/hr/analytics/charts/`

**Data Structure:**
```json
{
  "risk_distribution": {
    "chart_type": "pie",
    "title": "Employee Risk Distribution",
    "data": {
      "labels": ["Low Risk", "Medium Risk", "High Risk"],
      "datasets": [{
        "data": [15, 8, 3],
        "backgroundColor": ["#28a745", "#ffc107", "#dc3545"],
        "borderWidth": 2
      }]
    }
  }
}
```

**Frontend Chart.js Integration:**
```javascript
const riskChart = new Chart(ctx, {
  type: 'pie',
  data: chartData.risk_distribution.data,
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Employee Risk Distribution'
      },
      legend: {
        position: 'bottom'
      }
    }
  }
});
```

**X/Y Axis Data untuk Custom Charts:**
```javascript
const riskData = {
  x_axis: ["Low Risk", "Medium Risk", "High Risk"],
  y_axis: [15, 8, 3],
  colors: ["#28a745", "#ffc107", "#dc3545"],
  percentages: [57.7, 30.8, 11.5]
};
```

### 2. 📊 Department Analysis Bar Chart

**Data Structure:**
```json
{
  "department_analysis": {
    "chart_type": "bar",
    "title": "Risk Analysis by Department",
    "data": {
      "labels": ["Engineering", "Marketing", "HR", "Finance", "Sales"],
      "datasets": [{
        "label": "Average Risk Score (%)",
        "data": [45.2, 62.8, 38.1, 55.9, 71.3],
        "backgroundColor": "#4F46E5",
        "borderColor": "#3730A3",
        "borderWidth": 1
      }]
    }
  }
}
```

**Frontend Chart.js Integration:**
```javascript
const deptChart = new Chart(ctx, {
  type: 'bar',
  data: chartData.department_analysis.data,
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        title: {
          display: true,
          text: 'Risk Score (%)'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Department'
        }
      }
    }
  }
});
```

**X/Y Axis Data:**
```javascript
const departmentData = {
  x_axis: ["Engineering", "Marketing", "HR", "Finance", "Sales"],
  y_axis: [45.2, 62.8, 38.1, 55.9, 71.3],
  chart_config: {
    type: "bar",
    x_label: "Department",
    y_label: "Risk Score (%)",
    color: "#4F46E5",
    max_value: 100
  }
};
```

### 3. 📈 Trend Analysis Line Chart

**Data Structure:**
```json
{
  "trend_analysis": {
    "chart_type": "line",
    "title": "Turnover Risk Trend (Last 6 Months)",
    "data": {
      "labels": ["Jan 2025", "Feb 2025", "Mar 2025", "Apr 2025", "May 2025", "Jun 2025"],
      "datasets": [{
        "label": "Average Risk %",
        "data": [42.5, 38.2, 45.1, 52.8, 48.3, 46.7],
        "borderColor": "#EF4444",
        "backgroundColor": "rgba(239, 68, 68, 0.1)",
        "tension": 0.4,
        "fill": true
      }]
    }
  }
}
```

**Frontend Chart.js Integration:**
```javascript
const trendChart = new Chart(ctx, {
  type: 'line',
  data: chartData.trend_analysis.data,
  options: {
    responsive: true,
    interaction: {
      intersect: false,
    },
    plugins: {
      title: {
        display: true,
        text: 'Turnover Risk Trend (Last 6 Months)'
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        title: {
          display: true,
          text: 'Risk Percentage (%)'
        }
      }
    }
  }
});
```

**Time Series Data:**
```javascript
const trendData = {
  time_series: [
    { date: "Jan 2025", risk_percentage: 42.5 },
    { date: "Feb 2025", risk_percentage: 38.2 },
    { date: "Mar 2025", risk_percentage: 45.1 },
    { date: "Apr 2025", risk_percentage: 52.8 },
    { date: "May 2025", risk_percentage: 48.3 },
    { date: "Jun 2025", risk_percentage: 46.7 }
  ],
  x_axis: ["Jan 2025", "Feb 2025", "Mar 2025", "Apr 2025", "May 2025", "Jun 2025"],
  y_axis: [42.5, 38.2, 45.1, 52.8, 48.3, 46.7]
};
```

---

## 🔗 API ENDPOINTS SUMMARY

### 🤝 1-on-1 Meetings
| Method | Endpoint | Description | Access |
|--------|----------|-------------|---------|
| POST | `/api/hr/meetings/` | Create meeting | Admin only |
| GET | `/api/hr/meetings/` | Get all meetings | Admin: all, Employee: own |
| GET | `/api/hr/meetings/?employee={id}` | Filter by employee | Admin/Employee |
| PUT | `/api/hr/meetings/{id}/` | Update meeting | Admin only |
| DELETE | `/api/hr/meetings/{id}/` | Delete meeting | Admin only |

### ⭐ Performance Reviews
| Method | Endpoint | Description | Access |
|--------|----------|-------------|---------|
| POST | `/api/hr/reviews/` | Create review | Admin only |
| GET | `/api/hr/reviews/` | Get all reviews | Admin: all, Employee: own |
| GET | `/api/hr/reviews/?employee={id}` | Filter by employee | Admin/Employee |
| PUT | `/api/hr/reviews/{id}/` | Update review | Admin only |
| POST | `/api/hr/reviews/{id}/acknowledge/` | Acknowledge review | Employee only |
| GET | `/api/hr/reviews/summary/` | Get summary | Admin/Employee |

### 📊 Analytics & Charts
| Method | Endpoint | Description | Access |
|--------|----------|-------------|---------|
| GET | `/api/hr/analytics/dashboard/` | Complete dashboard | Admin only |
| GET | `/api/hr/analytics/charts/` | Chart data for frontend | Admin only |

---

## 💻 FRONTEND INTEGRATION EXAMPLES

### React + Chart.js Complete Component

```jsx
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
);

const HRAnalyticsDashboard = ({ adminToken }) => {
  const [chartData, setChartData] = useState(null);
  const [dashboardStats, setDashboardStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      const headers = {
        'Authorization': `Token ${adminToken}`,
        'Content-Type': 'application/json'
      };

      // Fetch chart data
      const chartsResponse = await fetch('/api/hr/analytics/charts/', { headers });
      const chartsData = await chartsResponse.json();

      // Fetch dashboard stats
      const dashboardResponse = await fetch('/api/hr/analytics/dashboard/', { headers });
      const dashboardData = await dashboardResponse.json();

      setChartData(chartsData.data);
      setDashboardStats(dashboardData.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching analytics data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading analytics...</div>;
  }

  return (
    <div className="hr-analytics-dashboard">
      {/* Dashboard Stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Predictions</h3>
          <p className="stat-number">{dashboardStats?.total_predictions || 0}</p>
        </div>
        <div className="stat-card">
          <h3>High Risk Employees</h3>
          <p className="stat-number danger">{dashboardStats?.high_risk_employees || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Total Meetings</h3>
          <p className="stat-number">{dashboardStats?.total_meetings || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Performance Reviews</h3>
          <p className="stat-number">{dashboardStats?.total_reviews || 0}</p>
        </div>
      </div>

      {/* Charts */}
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
                  legend: {
                    position: 'bottom'
                  }
                }
              }}
            />
          )}
        </div>

        {/* Department Analysis Bar Chart */}
        <div className="chart-container">
          <h3>Risk Analysis by Department</h3>
          {chartData?.department_analysis && (
            <Bar 
              data={chartData.department_analysis.data}
              options={{
                responsive: true,
                scales: {
                  y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                      display: true,
                      text: 'Risk Score (%)'
                    }
                  }
                }
              }}
            />
          )}
        </div>

        {/* Trend Analysis Line Chart */}
        <div className="chart-container large">
          <h3>Turnover Risk Trend (Last 6 Months)</h3>
          {chartData?.trend_analysis && (
            <Line 
              data={chartData.trend_analysis.data}
              options={{
                responsive: true,
                interaction: {
                  intersect: false,
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                      display: true,
                      text: 'Risk Percentage (%)'
                    }
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

export default HRAnalyticsDashboard;
```

### CSS Styles
```css
.hr-analytics-dashboard {
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

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  margin: 10px 0;
  color: #4F46E5;
}

.stat-number.danger {
  color: #dc3545;
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

.chart-container.large {
  grid-column: 1 / -1;
}

.chart-container h3 {
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 1.2rem;
  color: #666;
}
```

---

## 🔐 ROLE-BASED ACCESS CONTROL

### Admin/HR Access:
- ✅ Create, read, update, delete meetings
- ✅ Create, read, update performance reviews
- ✅ View all analytics and charts
- ✅ Access all employee data

### Employee Access:
- ✅ View own meetings (read-only)
- ✅ View own performance reviews (read-only)
- ✅ Acknowledge performance reviews
- ❌ Cannot create/edit meetings or reviews
- ❌ Cannot access analytics dashboard

---

## 🚀 TESTING & DEPLOYMENT

### 1. Import Postman Collection
Import `HR_FEATURES_COMPLETE_POSTMAN.json` untuk testing semua endpoints.

### 2. Run Test Script
```bash
python test_hr_features_complete.py
```

### 3. Database Migration
```bash
cd backend
python manage.py makemigrations hr_features
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

---

## 📋 SAMPLE DATA FOR TESTING

### Meeting Data
```json
{
  "employee": 1,
  "title": "Follow-up Meeting: High Turnover Risk",
  "meeting_type": "followup",
  "scheduled_date": "2025-07-15T14:00:00Z",
  "duration_minutes": 45,
  "meeting_link": "https://meet.google.com/abc-defg-hij",
  "agenda": "Discussion about career development and addressing concerns",
  "ml_probability": 0.85,
  "ml_risk_level": "high"
}
```

### Performance Review Data
```json
{
  "employee": 1,
  "review_period": "quarterly",
  "review_date": "2025-07-11",
  "period_start": "2025-04-01",
  "period_end": "2025-06-30",
  "overall_rating": 4,
  "technical_skills": 4,
  "communication": 3,
  "teamwork": 5,
  "leadership": 3,
  "initiative": 4,
  "problem_solving": 4,
  "strengths": "Excellent technical skills and strong collaboration",
  "areas_for_improvement": "Could improve communication skills",
  "goals_for_next_period": "Complete communication workshop, lead presentations"
}
```

---

## 🎯 NEXT STEPS

1. **Backend Deployment**
   - Run migrations untuk HR features
   - Test semua endpoints di production

2. **Frontend Integration** 
   - Implement chart components dengan Chart.js
   - Setup role-based routing
   - Add real-time data updates

3. **User Experience**
   - Add notifications untuk scheduled meetings
   - Email reminders untuk performance reviews
   - Dashboard widgets untuk quick insights

4. **Advanced Features**
   - Export charts sebagai PDF/PNG
   - Advanced filtering dan search
   - Bulk actions untuk meetings/reviews

🎉 **Semua fitur HR sudah siap untuk production!**
