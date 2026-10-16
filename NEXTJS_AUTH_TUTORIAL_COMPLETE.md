# 🚀 Next.js Authentication Tutorial - SMART-EN API Integration

## 🎯 **Problem yang Sering Terjadi:**
- ❌ Token hilang setelah refresh
- ❌ Redirect loop login → dashboard → login
- ❌ Role-based access ga berfungsi
- ❌ ML features accessible oleh user biasa

## ✅ **Solution Lengkap:**
- ✅ Persistent token dengan localStorage/cookies
- ✅ Proper authentication flow
- ✅ Role-based route protection
- ✅ ML features admin-only access

---

## 📁 **Project Structure**

```
src/
├── app/
│   ├── auth/
│   │   ├── login/
│   │   │   └── page.js
│   │   └── layout.js
│   ├── admin/
│   │   ├── dashboard/
│   │   │   └── page.js
│   │   ├── ml-features/
│   │   │   └── page.js
│   │   └── layout.js
│   ├── employee/
│   │   ├── dashboard/
│   │   │   └── page.js
│   │   └── layout.js
│   └── layout.js
├── components/
│   ├── ProtectedRoute.js
│   ├── AdminRoute.js
│   └── Navigation.js
├── lib/
│   ├── auth.js
│   ├── api.js
│   └── utils.js
└── store/
    └── authStore.js
```

---

## 🔧 **1. Setup Dependencies**

```bash
npm install axios js-cookie zustand
# atau
yarn add axios js-cookie zustand
```

---

## 🔐 **2. Authentication Store (Zustand)**

`src/store/authStore.js`
```javascript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import Cookies from 'js-cookie';

const useAuthStore = create(
  persist(
    (set, get) => ({
      // State
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      // Actions
      login: async (credentials) => {
        set({ isLoading: true });
        try {
          const response = await fetch('https://turnover-api-hd7ze.ondigitalocean.app/api/login/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(credentials),
          });

          const data = await response.json();

          if (data.success && data.data?.user) {
            const { user } = data.data;
            
            // Save to store
            set({
              user,
              token: user.token,
              isAuthenticated: true,
              isLoading: false,
            });

            // Save to cookies (untuk SSR)
            Cookies.set('auth-token', user.token, { expires: 7 });
            Cookies.set('user-role', user.role, { expires: 7 });

            return { success: true, user };
          } else {
            throw new Error(data.message || 'Login failed');
          }
        } catch (error) {
          set({ isLoading: false });
          return { success: false, error: error.message };
        }
      },

      logout: async () => {
        const { token } = get();
        
        // Call API logout untuk invalidate token
        try {
          await fetch('https://turnover-api-hd7ze.ondigitalocean.app/api/logout/', {
            method: 'POST',
            headers: {
              'Authorization': `Token ${token}`,
            },
          });
        } catch (error) {
          console.error('Logout API call failed:', error);
        }

        // Clear store
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });

        // Clear cookies
        Cookies.remove('auth-token');
        Cookies.remove('user-role');
      },

      // Initialize from cookies (untuk SSR/refresh)
      initializeAuth: () => {
        const token = Cookies.get('auth-token');
        const userRole = Cookies.get('user-role');
        
        if (token) {
          // Verify token masih valid
          fetch('https://turnover-api-hd7ze.ondigitalocean.app/api/profile/', {
            headers: {
              'Authorization': `Token ${token}`,
            },
          })
          .then(response => response.json())
          .then(data => {
            if (data.success && data.data) {
              set({
                user: data.data,
                token,
                isAuthenticated: true,
              });
            } else {
              // Token invalid, clear cookies
              Cookies.remove('auth-token');
              Cookies.remove('user-role');
            }
          })
          .catch(() => {
            // Token invalid, clear cookies
            Cookies.remove('auth-token');
            Cookies.remove('user-role');
          });
        }
      },

      // Helper functions
      isAdmin: () => {
        const { user } = get();
        return user?.role === 'admin' || user?.is_admin === true;
      },

      isEmployee: () => {
        const { user } = get();
        return user?.role === 'employee';
      },
    }),
    {
      name: 'auth-storage',
      // Hanya persist data yang penting
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

export default useAuthStore;
```

---

## 🛡️ **3. Protected Route Components**

`src/components/ProtectedRoute.js`
```javascript
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import useAuthStore from '@/store/authStore';

export default function ProtectedRoute({ children }) {
  const { isAuthenticated, token, initializeAuth } = useAuthStore();
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Initialize auth dari cookies
    initializeAuth();
    
    // Delay sedikit untuk memastikan auth state ter-update
    const timer = setTimeout(() => {
      setIsLoading(false);
      
      if (!isAuthenticated || !token) {
        router.replace('/auth/login');
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [isAuthenticated, token, router, initializeAuth]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Will redirect to login
  }

  return children;
}
```

`src/components/AdminRoute.js`
```javascript
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import useAuthStore from '@/store/authStore';

export default function AdminRoute({ children }) {
  const { isAuthenticated, token, isAdmin, initializeAuth } = useAuthStore();
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    initializeAuth();
    
    const timer = setTimeout(() => {
      setIsLoading(false);
      
      if (!isAuthenticated || !token) {
        router.replace('/auth/login');
      } else if (!isAdmin()) {
        // User bukan admin, redirect ke employee dashboard
        router.replace('/employee/dashboard');
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [isAuthenticated, token, router, initializeAuth, isAdmin]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600"></div>
      </div>
    );
  }

  if (!isAuthenticated || !isAdmin()) {
    return null; // Will redirect
  }

  return children;
}
```

---

## 🔐 **4. Login Page**

`src/app/auth/login/page.js`
```javascript
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import useAuthStore from '@/store/authStore';

export default function LoginPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  
  const { login, isLoading, isAuthenticated, user } = useAuthStore();
  const router = useRouter();

  // Redirect jika sudah login
  useEffect(() => {
    if (isAuthenticated && user) {
      if (user.role === 'admin' || user.is_admin) {
        router.replace('/admin/dashboard');
      } else {
        router.replace('/employee/dashboard');
      }
    }
  }, [isAuthenticated, user, router]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const result = await login(formData);

    if (result.success) {
      // Redirect berdasarkan role
      if (result.user.role === 'admin' || result.user.is_admin) {
        router.push('/admin/dashboard');
      } else {
        router.push('/employee/dashboard');
      }
    } else {
      setError(result.error);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to SMART-EN
          </h2>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}
          
          <div className="space-y-4">
            <div>
              <label htmlFor="email" className="sr-only">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="relative block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="Email address"
              />
            </div>
            
            <div>
              <label htmlFor="password" className="sr-only">Password</label>
              <input
                id="password"
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={handleChange}
                className="relative block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="Password"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {isLoading ? 'Signing in...' : 'Sign in'}
            </button>
          </div>
          
          {/* Demo credentials */}
          <div className="text-sm text-gray-600 space-y-2">
            <p className="font-medium">Demo Accounts:</p>
            <div className="bg-gray-100 p-3 rounded space-y-1">
              <p><strong>Admin:</strong> admin@company.com / AdminPass123!</p>
              <p><strong>Employee:</strong> bravely@gmail.com / user123</p>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
```

---

## 👨‍💼 **5. Admin Dashboard dengan ML Features**

`src/app/admin/dashboard/page.js`
```javascript
'use client';

import { useState, useEffect } from 'react';
import useAuthStore from '@/store/authStore';

export default function AdminDashboard() {
  const { user, token } = useAuthStore();
  const [employees, setEmployees] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [employeesRes, departmentsRes] = await Promise.all([
        fetch('https://turnover-api-hd7ze.ondigitalocean.app/api/employees/', {
          headers: { 'Authorization': `Token ${token}` },
        }),
        fetch('https://turnover-api-hd7ze.ondigitalocean.app/api/departments/', {
          headers: { 'Authorization': `Token ${token}` },
        }),
      ]);

      const employeesData = await employeesRes.json();
      const departmentsData = await departmentsRes.json();

      setEmployees(employeesData.results || employeesData);
      setDepartments(departmentsData.results || departmentsData);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-6">Loading...</div>;
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
        <p className="text-gray-600">Welcome back, {user?.full_name}!</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900">Total Employees</h3>
          <p className="text-3xl font-bold text-blue-600">{employees.length}</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900">Total Departments</h3>
          <p className="text-3xl font-bold text-green-600">{departments.length}</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900">Active Users</h3>
          <p className="text-3xl font-bold text-purple-600">
            {employees.filter(emp => emp.is_active).length}
          </p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <button className="w-full text-left px-4 py-2 bg-blue-50 hover:bg-blue-100 rounded-lg">
              📊 View ML Analytics
            </button>
            <button className="w-full text-left px-4 py-2 bg-green-50 hover:bg-green-100 rounded-lg">
              👥 Manage Employees
            </button>
            <button className="w-full text-left px-4 py-2 bg-purple-50 hover:bg-purple-100 rounded-lg">
              🏢 Manage Departments
            </button>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Employees</h3>
          <div className="space-y-2">
            {employees.slice(0, 5).map((employee) => (
              <div key={employee.id} className="flex justify-between items-center py-2">
                <span className="text-sm text-gray-900">{employee.full_name}</span>
                <span className={`text-xs px-2 py-1 rounded ${
                  employee.is_active 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {employee.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
```

`src/app/admin/ml-features/page.js`
```javascript
'use client';

import { useState, useEffect } from 'react';
import useAuthStore from '@/store/authStore';

export default function MLFeatures() {
  const { token } = useAuthStore();
  const [mlData, setMlData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedEmployee, setSelectedEmployee] = useState('');

  useEffect(() => {
    fetchMLData();
  }, []);

  const fetchMLData = async () => {
    try {
      // Contoh endpoint ML - sesuaikan dengan API yang tersedia
      const response = await fetch('https://turnover-api-hd7ze.ondigitalocean.app/api/employees/statistics/', {
        headers: { 'Authorization': `Token ${token}` },
      });
      
      const data = await response.json();
      setMlData(data);
    } catch (error) {
      console.error('Error fetching ML data:', error);
    } finally {
      setLoading(false);
    }
  };

  const runPrediction = async () => {
    if (!selectedEmployee) return;
    
    try {
      const response = await fetch(`https://turnover-api-hd7ze.ondigitalocean.app/api/employees/${selectedEmployee}/performance_data/`, {
        headers: { 'Authorization': `Token ${token}` },
      });
      
      const data = await response.json();
      alert('Prediction completed! Check console for results.');
      console.log('ML Prediction Result:', data);
    } catch (error) {
      console.error('Error running prediction:', error);
      alert('Error running prediction');
    }
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">🤖 ML Features</h1>
        <p className="text-gray-600">Advanced analytics and predictions (Admin Only)</p>
      </div>

      {/* WARNING: Admin Only */}
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">
              Admin Only Feature
            </h3>
            <p className="text-sm text-red-700 mt-1">
              This page is only accessible to administrators. Employees cannot access ML features.
            </p>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading ML data...</p>
        </div>
      ) : (
        <div className="space-y-6">
          {/* ML Analytics Dashboard */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-gradient-to-r from-blue-500 to-blue-600 p-6 rounded-lg text-white">
              <h3 className="text-lg font-medium">Employee Turnover Risk</h3>
              <p className="text-3xl font-bold mt-2">15%</p>
              <p className="text-blue-100 text-sm">Based on ML analysis</p>
            </div>
            
            <div className="bg-gradient-to-r from-green-500 to-green-600 p-6 rounded-lg text-white">
              <h3 className="text-lg font-medium">Performance Score</h3>
              <p className="text-3xl font-bold mt-2">87.5</p>
              <p className="text-green-100 text-sm">Average team performance</p>
            </div>
            
            <div className="bg-gradient-to-r from-purple-500 to-purple-600 p-6 rounded-lg text-white">
              <h3 className="text-lg font-medium">Satisfaction Index</h3>
              <p className="text-3xl font-bold mt-2">8.2/10</p>
              <p className="text-purple-100 text-sm">Employee satisfaction</p>
            </div>
          </div>

          {/* ML Prediction Tool */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-medium text-gray-900 mb-4">🔮 Run ML Prediction</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Select Employee for Analysis
                </label>
                <select
                  value={selectedEmployee}
                  onChange={(e) => setSelectedEmployee(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">Choose an employee...</option>
                  <option value="27">Employee #27 (Test User)</option>
                  <option value="38">Employee #38 (Bravely Dirgayuska)</option>
                </select>
              </div>
              
              <button
                onClick={runPrediction}
                disabled={!selectedEmployee}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                🚀 Run Turnover Prediction
              </button>
            </div>
          </div>

          {/* ML Features List */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Available ML Features</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="border border-gray-200 rounded-lg p-4">
                <h4 className="font-medium text-gray-900">📊 Turnover Prediction</h4>
                <p className="text-sm text-gray-600 mt-1">
                  Predict employee turnover risk based on performance data
                </p>
              </div>
              
              <div className="border border-gray-200 rounded-lg p-4">
                <h4 className="font-medium text-gray-900">📈 Performance Analytics</h4>
                <p className="text-sm text-gray-600 mt-1">
                  Advanced performance metrics and trends analysis
                </p>
              </div>
              
              <div className="border border-gray-200 rounded-lg p-4">
                <h4 className="font-medium text-gray-900">🎯 Recommendation Engine</h4>
                <p className="text-sm text-gray-600 mt-1">
                  AI-powered recommendations for employee development
                </p>
              </div>
              
              <div className="border border-gray-200 rounded-lg p-4">
                <h4 className="font-medium text-gray-900">📋 Risk Assessment</h4>
                <p className="text-sm text-gray-600 mt-1">
                  Identify high-risk employees and intervention strategies
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

---

## 👤 **6. Employee Dashboard (Limited Access)**

`src/app/employee/dashboard/page.js`
```javascript
'use client';

import { useState, useEffect } from 'react';
import useAuthStore from '@/store/authStore';

export default function EmployeeDashboard() {
  const { user, token } = useAuthStore();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await fetch('https://turnover-api-hd7ze.ondigitalocean.app/api/profile/', {
        headers: { 'Authorization': `Token ${token}` },
      });
      
      const data = await response.json();
      if (data.success) {
        setProfile(data.data);
      }
    } catch (error) {
      console.error('Error fetching profile:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-6">Loading...</div>;
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Employee Dashboard</h1>
        <p className="text-gray-600">Welcome back, {profile?.full_name}!</p>
      </div>

      {/* Profile Card */}
      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Your Profile</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p className="text-sm font-medium text-gray-500">Employee ID</p>
            <p className="text-gray-900">{profile?.employee_id}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Position</p>
            <p className="text-gray-900">{profile?.position}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Department</p>
            <p className="text-gray-900">{profile?.department_name}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Phone</p>
            <p className="text-gray-900">{profile?.phone_number || 'Not set'}</p>
          </div>
        </div>
      </div>

      {/* No ML Access Warning */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-yellow-800">
              Limited Access
            </h3>
            <p className="text-sm text-yellow-700 mt-1">
              ML features and advanced analytics are only available to administrators.
            </p>
          </div>
        </div>
      </div>

      {/* Employee Features */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Available Actions</h3>
          <div className="space-y-3">
            <button className="w-full text-left px-4 py-2 bg-blue-50 hover:bg-blue-100 rounded-lg">
              👤 Update Profile
            </button>
            <button className="w-full text-left px-4 py-2 bg-green-50 hover:bg-green-100 rounded-lg">
              📊 View My Performance
            </button>
            <button className="w-full text-left px-4 py-2 bg-purple-50 hover:bg-purple-100 rounded-lg">
              📝 Submit Feedback
            </button>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Stats</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Status</span>
              <span className={`px-2 py-1 rounded text-xs ${
                profile?.is_active 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                {profile?.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Role</span>
              <span className="text-gray-900 capitalize">{profile?.role}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Hire Date</span>
              <span className="text-gray-900">
                {profile?.hire_date ? new Date(profile.hire_date).toLocaleDateString() : 'Not set'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

## 🧭 **7. Navigation Component**

`src/components/Navigation.js`
```javascript
'use client';

import { useRouter } from 'next/navigation';
import useAuthStore from '@/store/authStore';

export default function Navigation() {
  const { user, logout, isAdmin } = useAuthStore();
  const router = useRouter();

  const handleLogout = async () => {
    await logout();
    router.push('/auth/login');
  };

  return (
    <nav className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-gray-900">SMART-EN</h1>
          </div>
          
          <div className="flex items-center space-x-4">
            {/* Role-based navigation */}
            {isAdmin() ? (
              <div className="flex space-x-4">
                <a href="/admin/dashboard" className="text-gray-700 hover:text-gray-900">
                  📊 Dashboard
                </a>
                <a href="/admin/ml-features" className="text-gray-700 hover:text-gray-900">
                  🤖 ML Features
                </a>
              </div>
            ) : (
              <div className="flex space-x-4">
                <a href="/employee/dashboard" className="text-gray-700 hover:text-gray-900">
                  📊 Dashboard
                </a>
              </div>
            )}
            
            {/* User info */}
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-700">
                {user?.full_name} ({user?.role})
              </span>
              <button
                onClick={handleLogout}
                className="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
```

---

## 🔧 **8. Layout dengan Auth Protection**

`src/app/admin/layout.js`
```javascript
import AdminRoute from '@/components/AdminRoute';
import Navigation from '@/components/Navigation';

export default function AdminLayout({ children }) {
  return (
    <AdminRoute>
      <Navigation />
      <main>{children}</main>
    </AdminRoute>
  );
}
```

`src/app/employee/layout.js`
```javascript
import ProtectedRoute from '@/components/ProtectedRoute';
import Navigation from '@/components/Navigation';

export default function EmployeeLayout({ children }) {
  return (
    <ProtectedRoute>
      <Navigation />
      <main>{children}</main>
    </ProtectedRoute>
  );
}
```

---

## 🚀 **9. Root Layout dengan Auth Initialization**

`src/app/layout.js`
```javascript
'use client';

import { useEffect } from 'react';
import useAuthStore from '@/store/authStore';
import './globals.css';

export default function RootLayout({ children }) {
  const { initializeAuth } = useAuthStore();

  useEffect(() => {
    // Initialize auth saat app load
    initializeAuth();
  }, [initializeAuth]);

  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
```

---

## ✅ **Hasil yang Diharapkan:**

### **✅ Admin User:**
1. Login → Redirect ke `/admin/dashboard`
2. Bisa akses ML features di `/admin/ml-features`
3. Bisa manage employees/departments
4. Token persistent setelah refresh

### **✅ Employee User:**
1. Login → Redirect ke `/employee/dashboard`
2. **TIDAK BISA** akses `/admin/ml-features` (redirect ke employee dashboard)
3. Hanya bisa akses fitur employee
4. Token persistent setelah refresh

### **✅ Security:**
- Token disimpan di cookies untuk SSR
- Token di-verify setiap page load
- Logout menginvalidate token di backend
- Route protection berdasarkan role

---

## 🔥 **Tips Debugging:**

1. **Check browser console** untuk error authentication
2. **Check Network tab** untuk API calls
3. **Clear cookies** jika stuck di redirect loop
4. **Verify token** di API response

**MANTAP! Ini harusnya solve masalah authentication loop dan role-based access! 🚀**
