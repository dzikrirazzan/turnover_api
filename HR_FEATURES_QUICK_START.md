# 🚀 HR Features Quick Start Guide

## 📋 Yang Perlu Anda Ketahui

### 🎯 3 Fitur Utama HR:
1. **1-on-1 Meetings** - Schedule & track meetings dengan ML context
2. **Performance Reviews** - CRUD reviews dengan star ratings  
3. **Analytics Dashboard** - Charts & visualisasi data

### 🔐 Authentication
```javascript
// Base setup
const BASE_URL = 'https://turnover-api-hd7ze.ondigitalocean.app';
const API_BASE = `${BASE_URL}/api`;

// Login admin untuk mendapatkan token
const token = await loginAdmin(); // Lihat tutorial lengkap untuk implementasi
```

---

## ⚡ Quick Implementation Examples

### 1. Get Meetings List
```javascript
const meetings = await fetch(`${API_BASE}/hr/meetings/`, {
  headers: { 'Authorization': `Token ${token}` }
}).then(res => res.json());
```

### 2. Create Performance Review
```javascript
const review = await fetch(`${API_BASE}/hr/reviews/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${token}`
  },
  body: JSON.stringify({
    employee: 1,
    overall_rating: 4,
    technical_skills: 4,
    communication: 5,
    // ... other fields
  })
});
```

### 3. Get Analytics Data
```javascript
const analytics = await fetch(`${API_BASE}/hr/analytics/dashboard/`, {
  headers: { 'Authorization': `Token ${token}` }
}).then(res => res.json());
```

---

## 📊 Data Structures

### Meeting Object
```javascript
{
  "id": 1,
  "employee": 1,
  "employee_name": "John Doe",
  "title": "Follow-up Meeting",
  "meeting_type": "followup",
  "scheduled_date": "2024-01-15T10:00:00Z",
  "status": "scheduled",
  "duration_minutes": 30,
  "meeting_link": "https://meet.google.com/abc-def-ghi",
  "agenda": "Discuss career development",
  "ml_probability": 0.75,
  "ml_risk_level": "high"
}
```

### Performance Review Object
```javascript
{
  "id": 1,
  "employee": 1,
  "employee_name": "John Doe",
  "review_period": "quarterly",
  "overall_rating": 4,
  "technical_skills": 4,
  "communication": 5,
  "teamwork": 4,
  "leadership": 3,
  "initiative": 4,
  "problem_solving": 4,
  "strengths": "Excellent communication skills",
  "areas_for_improvement": "Leadership development",
  "goals_for_next_period": "Lead a project team"
}
```

### Analytics Dashboard Data
```javascript
{
  "total_employees": 50,
  "high_risk_count": 8,
  "avg_performance": 3.8,
  "pending_reviews": 5,
  "recent_meetings": [...],
  "recent_reviews": [...]
}
```

---

## 🎨 Essential CSS Classes

```css
/* Key classes untuk styling */
.meeting-card { /* Meeting list items */ }
.star-rating { /* Star rating components */ }
.chart-container { /* Chart wrappers */ }
.summary-cards { /* Dashboard summary grid */ }
.status.scheduled { /* Meeting status badges */ }
.risk.high { /* Risk level indicators */ }
```

---

## 🔧 Environment Setup

### 1. Install Dependencies
```bash
npm install react-chartjs-2 chart.js
```

### 2. Import Chart Components
```javascript
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie, Bar, Line } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);
```

### 3. Environment Variables
```javascript
// .env
REACT_APP_API_BASE_URL=https://turnover-api-hd7ze.ondigitalocean.app/api
REACT_APP_ADMIN_EMAIL=admin@company.com
```

---

## 🧪 Testing dengan Postman

1. **Import**: `HR_FEATURES_COMPLETE_POSTMAN.json`
2. **Login**: Run "Admin Login" dulu untuk dapat token
3. **Test**: Semua endpoint sudah siap dengan sample data

---

## 📱 Mobile Responsive

All components sudah include responsive CSS:
- Grid layouts menggunakan `grid-template-columns: repeat(auto-fit, minmax(...))`
- Mobile breakpoint di 768px
- Flex layouts untuk mobile optimization

---

## 🚨 Common Issues & Solutions

### 1. CORS Error
```javascript
// Pastikan backend CORS settings include frontend domain
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://your-frontend-domain.com'
]
```

### 2. Authentication Error
```javascript
// Check token expiry dan format
if (response.status === 401) {
  localStorage.removeItem('admin_token');
  window.location.href = '/login';
}
```

### 3. Chart Not Rendering
```javascript
// Pastikan Chart.js dependencies registered
import { Chart as ChartJS, CategoryScale, LinearScale } from 'chart.js';
ChartJS.register(CategoryScale, LinearScale);
```

---

## 📚 File Structure Recommendation

```
src/
├── components/
│   ├── meetings/
│   │   ├── MeetingScheduler.jsx
│   │   ├── MeetingList.jsx
│   │   └── MeetingCard.jsx
│   ├── reviews/
│   │   ├── PerformanceReviewForm.jsx
│   │   ├── StarRating.jsx
│   │   └── ReviewsList.jsx
│   ├── analytics/
│   │   ├── AnalyticsDashboard.jsx
│   │   ├── SummaryCards.jsx
│   │   └── ChartComponents.jsx
│   └── common/
│       ├── ErrorBoundary.jsx
│       └── LoadingSpinner.jsx
├── hooks/
│   ├── useMeetings.js
│   ├── useReviews.js
│   └── useAnalytics.js
├── utils/
│   ├── api.js
│   ├── validation.js
│   └── errorHandling.js
├── contexts/
│   └── HRContext.js
└── styles/
    ├── meetings.css
    ├── reviews.css
    ├── analytics.css
    └── common.css
```

---

## 🎯 Next Steps

1. **Review Tutorial Lengkap**: Baca `FRONTEND_HR_FEATURES_TUTORIAL_COMPLETE.md`
2. **Import Postman Collection**: Test semua endpoints
3. **Setup Development Environment**: Install dependencies
4. **Start dengan Dashboard**: Implement analytics dashboard dulu
5. **Test dengan Real Data**: Connect ke backend API

---

## 💬 Support

Jika ada pertanyaan atau butuh bantuan:
1. Check tutorial lengkap untuk detail implementation
2. Test endpoint dengan Postman collection yang disediakan
3. Review demo script `demo_hr_features_complete.py` untuk sample data

Happy coding! 🚀
