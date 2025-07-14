# 📊 Frontend HR Analytics Dashboard

Advanced analytics components for HR features dengan real-time charts dan metrics.

## Chart Components

### Performance Trends Chart
```typescript
// components/charts/PerformanceTrendsChart.tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { month: 'Jan', performance: 4.1, meetings: 12, reviews: 8 },
  { month: 'Feb', performance: 4.3, meetings: 15, reviews: 10 },
  { month: 'Mar', performance: 4.2, meetings: 18, reviews: 12 },
  { month: 'Apr', performance: 4.5, meetings: 20, reviews: 15 },
  { month: 'May', performance: 4.4, meetings: 22, reviews: 18 },
  { month: 'Jun', performance: 4.6, meetings: 25, reviews: 20 },
];

export const PerformanceTrendsChart = () => {
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Performance Trends</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis domain={[3.5, 5]} />
          <Tooltip 
            formatter={(value, name) => [value, name === 'performance' ? 'Avg Rating' : name]}
          />
          <Line 
            type="monotone" 
            dataKey="performance" 
            stroke="#3B82F6" 
            strokeWidth={3}
            dot={{ fill: '#3B82F6', strokeWidth: 2, r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};
```

### Department Performance Comparison
```typescript
// components/charts/DepartmentChart.tsx
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const departmentData = [
  { department: 'Engineering', avgRating: 4.5, employeeCount: 35 },
  { department: 'Marketing', avgRating: 4.2, employeeCount: 25 },
  { department: 'Sales', avgRating: 4.3, employeeCount: 20 },
  { department: 'HR', avgRating: 4.6, employeeCount: 12 },
  { department: 'Finance', avgRating: 4.1, employeeCount: 8 },
];

export const DepartmentChart = () => {
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Department Performance</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={departmentData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="department" />
          <YAxis domain={[3.5, 5]} />
          <Tooltip />
          <Bar 
            dataKey="avgRating" 
            fill="#10B981" 
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
```

### Employee Engagement Metrics
```typescript
// components/charts/EngagementMetrics.tsx
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

const engagementData = [
  { name: 'Highly Engaged', value: 45, color: '#10B981' },
  { name: 'Engaged', value: 35, color: '#3B82F6' },
  { name: 'Neutral', value: 15, color: '#F59E0B' },
  { name: 'Disengaged', value: 5, color: '#EF4444' },
];

export const EngagementMetrics = () => {
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Employee Engagement</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={engagementData}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={100}
            dataKey="value"
            label={({ name, value }) => `${name}: ${value}%`}
          >
            {engagementData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};
```

## Analytics Dashboard Layout

### Main Analytics Page
```typescript
// app/dashboard/analytics/page.tsx
export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">HR Analytics Dashboard</h1>
        <div className="flex space-x-2">
          <select className="px-3 py-2 border border-gray-300 rounded-md">
            <option>Last 6 months</option>
            <option>Last year</option>
            <option>All time</option>
          </select>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
            Export Report
          </button>
        </div>
      </div>

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricCard
          title="Average Performance"
          value="4.4"
          change="+0.2"
          trend="up"
          icon="star"
        />
        <MetricCard
          title="Employee Satisfaction"
          value="87%"
          change="+5%"
          trend="up"
          icon="smile"
        />
        <MetricCard
          title="1-on-1 Completion"
          value="92%"
          change="+3%"
          trend="up"
          icon="calendar"
        />
        <MetricCard
          title="Goal Achievement"
          value="78%"
          change="-2%"
          trend="down"
          icon="target"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PerformanceTrendsChart />
        <DepartmentChart />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <EngagementMetrics />
        <MeetingFrequencyChart />
        <SkillsRadarChart />
      </div>

      {/* Detailed Tables */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TopPerformersTable />
        <UpcomingReviewsTable />
      </div>
    </div>
  );
}

// Metric Card Component
const MetricCard = ({ title, value, change, trend, icon }) => {
  const icons = {
    star: '⭐',
    smile: '😊',
    calendar: '📅',
    target: '🎯',
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
        <div className="text-2xl">{icons[icon]}</div>
      </div>
      <div className="mt-2">
        <span className={`text-sm font-medium ${
          trend === 'up' ? 'text-green-600' : 'text-red-600'
        }`}>
          {change} from last period
        </span>
      </div>
    </div>
  );
};
```

## Real-time Features

### Live Data Updates
```typescript
// hooks/useRealTimeAnalytics.ts
import { useState, useEffect } from 'react';

export const useRealTimeAnalytics = () => {
  const [metrics, setMetrics] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Fetch initial data
    fetchAnalytics();

    // Set up real-time updates (polling every 30 seconds)
    const interval = setInterval(fetchAnalytics, 30000);

    return () => clearInterval(interval);
  }, []);

  const fetchAnalytics = async () => {
    try {
      const response = await fetch('/api/hr/analytics/');
      const data = await response.json();
      setMetrics(data);
      setIsLoading(false);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
      setIsLoading(false);
    }
  };

  return { metrics, isLoading, refresh: fetchAnalytics };
};
```

### Notification System
```typescript
// components/notifications/NotificationBell.tsx
import { useState, useEffect } from 'react';
import { Bell } from 'lucide-react';

export const NotificationBell = () => {
  const [notifications, setNotifications] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);

  useEffect(() => {
    // Fetch notifications
    fetchNotifications();
    
    // Set up real-time notifications
    const interval = setInterval(fetchNotifications, 60000);
    
    return () => clearInterval(interval);
  }, []);

  const fetchNotifications = async () => {
    try {
      const response = await fetch('/api/notifications/');
      const data = await response.json();
      setNotifications(data);
    } catch (error) {
      console.error('Failed to fetch notifications:', error);
    }
  };

  return (
    <div className="relative">
      <button
        onClick={() => setShowDropdown(!showDropdown)}
        className="relative p-2 text-gray-600 hover:text-gray-900"
      >
        <Bell className="h-6 w-6" />
        {notifications.length > 0 && (
          <span className="absolute top-0 right-0 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
            {notifications.length}
          </span>
        )}
      </button>

      {showDropdown && (
        <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
          <div className="p-4 border-b border-gray-200">
            <h3 className="font-semibold text-gray-900">Notifications</h3>
          </div>
          <div className="max-h-96 overflow-y-auto">
            {notifications.map((notification) => (
              <div key={notification.id} className="p-4 border-b border-gray-100 hover:bg-gray-50">
                <p className="text-sm font-medium text-gray-900">{notification.title}</p>
                <p className="text-sm text-gray-600">{notification.message}</p>
                <p className="text-xs text-gray-500 mt-1">{notification.created_at}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
```

## Advanced Features

### Data Export
```typescript
// utils/exportData.ts
export const exportToCSV = (data, filename) => {
  const csv = convertToCSV(data);
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = window.URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.href = url;
  a.download = `${filename}-${new Date().toISOString().split('T')[0]}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
};

const convertToCSV = (data) => {
  const headers = Object.keys(data[0]).join(',');
  const rows = data.map(row => 
    Object.values(row).map(value => 
      typeof value === 'string' ? `"${value}"` : value
    ).join(',')
  ).join('\n');
  
  return `${headers}\n${rows}`;
};

// Export Performance Report
export const exportPerformanceReport = async () => {
  try {
    const response = await fetch('/api/hr/analytics/export/');
    const data = await response.json();
    exportToCSV(data.performance_data, 'performance-report');
  } catch (error) {
    console.error('Export failed:', error);
  }
};
```

### Filter & Search
```typescript
// components/filters/AnalyticsFilters.tsx
export const AnalyticsFilters = ({ onFilterChange }) => {
  const [filters, setFilters] = useState({
    department: '',
    dateRange: '6months',
    performanceRange: '',
    employeeType: '',
  });

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow mb-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Department
          </label>
          <select
            value={filters.department}
            onChange={(e) => handleFilterChange('department', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md"
          >
            <option value="">All Departments</option>
            <option value="engineering">Engineering</option>
            <option value="marketing">Marketing</option>
            <option value="sales">Sales</option>
            <option value="hr">HR</option>
            <option value="finance">Finance</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Date Range
          </label>
          <select
            value={filters.dateRange}
            onChange={(e) => handleFilterChange('dateRange', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md"
          >
            <option value="1month">Last Month</option>
            <option value="3months">Last 3 Months</option>
            <option value="6months">Last 6 Months</option>
            <option value="1year">Last Year</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Performance Range
          </label>
          <select
            value={filters.performanceRange}
            onChange={(e) => handleFilterChange('performanceRange', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md"
          >
            <option value="">All Ratings</option>
            <option value="4-5">High (4.0-5.0)</option>
            <option value="3-4">Medium (3.0-4.0)</option>
            <option value="1-3">Low (1.0-3.0)</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Employee Type
          </label>
          <select
            value={filters.employeeType}
            onChange={(e) => handleFilterChange('employeeType', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md"
          >
            <option value="">All Types</option>
            <option value="full-time">Full-time</option>
            <option value="part-time">Part-time</option>
            <option value="contractor">Contractor</option>
          </select>
        </div>
      </div>
    </div>
  );
};
```

Ini adalah implementasi frontend yang advanced dengan fitur analytics yang comprehensive, real-time updates, export functionality, dan filtering yang powerful untuk HR dashboard! 📊✨
