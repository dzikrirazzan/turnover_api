# 🚀 Quick Fix: Next.js Auth Implementation (Simplified)

## 🎯 **Masalah yang Sering Terjadi:**
- ❌ Masuk halaman bentar, terus balik ke login lagi
- ❌ Token hilang setelah refresh
- ❌ Employee bisa akses fitur admin

## ✅ **Quick Solution (3 Steps):**

---

## **Step 1: Install Dependencies**
```bash
npm install axios js-cookie zustand
```

---

## **Step 2: Auth Store (Copy Paste)**
`src/store/authStore.js`
```javascript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import Cookies from 'js-cookie';

const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (credentials) => {
        set({ isLoading: true });
        try {
          const response = await fetch('https://turnover-api-hd7ze.ondigitalocean.app/api/login/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(credentials),
          });

          const data = await response.json();
          if (data.success && data.data?.user) {
            const { user } = data.data;
            set({ user, token: user.token, isAuthenticated: true, isLoading: false });
            Cookies.set('auth-token', user.token, { expires: 7 });
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
        try {
          await fetch('https://turnover-api-hd7ze.ondigitalocean.app/api/logout/', {
            method: 'POST',
            headers: { 'Authorization': `Token ${token}` },
          });
        } catch (error) {
          console.error('Logout failed:', error);
        }
        
        set({ user: null, token: null, isAuthenticated: false });
        Cookies.remove('auth-token');
      },

      initializeAuth: () => {
        const token = Cookies.get('auth-token');
        if (token) {
          fetch('https://turnover-api-hd7ze.ondigitalocean.app/api/profile/', {
            headers: { 'Authorization': `Token ${token}` },
          })
          .then(response => response.json())
          .then(data => {
            if (data.success && data.data) {
              set({ user: data.data, token, isAuthenticated: true });
            } else {
              Cookies.remove('auth-token');
            }
          })
          .catch(() => Cookies.remove('auth-token'));
        }
      },

      isAdmin: () => get().user?.role === 'admin' || get().user?.is_admin === true,
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ user: state.user, token: state.token, isAuthenticated: state.isAuthenticated }),
    }
  )
);

export default useAuthStore;
```

---

## **Step 3: Protected Route (Copy Paste)**
`src/components/ProtectedRoute.js`
```javascript
'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import useAuthStore from '@/store/authStore';

export default function ProtectedRoute({ children, adminOnly = false }) {
  const { isAuthenticated, token, initializeAuth, isAdmin } = useAuthStore();
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    initializeAuth();
    
    setTimeout(() => {
      setIsLoading(false);
      
      if (!isAuthenticated || !token) {
        router.replace('/auth/login');
        return;
      }
      
      if (adminOnly && !isAdmin()) {
        router.replace('/employee/dashboard');
        return;
      }
    }, 500);
  }, [isAuthenticated, token, router, initializeAuth, isAdmin, adminOnly]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated || (adminOnly && !isAdmin())) {
    return null;
  }

  return children;
}
```

---

## **Step 4: Login Page (Copy Paste)**
`src/app/auth/login/page.js`
```javascript
'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import useAuthStore from '@/store/authStore';

export default function LoginPage() {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const { login, isLoading, isAuthenticated, user } = useAuthStore();
  const router = useRouter();

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
      if (result.user.role === 'admin' || result.user.is_admin) {
        router.push('/admin/dashboard');
      } else {
        router.push('/employee/dashboard');
      }
    } else {
      setError(result.error);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full p-6 bg-white rounded-lg shadow">
        <h2 className="text-2xl font-bold text-center mb-6">Login to SMART-EN</h2>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
            required
          />
          
          <input
            type="password"
            placeholder="Password"
            value={formData.password}
            onChange={(e) => setFormData({...formData, password: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
            required
          />
          
          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {isLoading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        
        <div className="mt-4 text-sm text-gray-600">
          <p><strong>Admin:</strong> admin@company.com / AdminPass123!</p>
          <p><strong>Employee:</strong> bravely@gmail.com / user123</p>
        </div>
      </div>
    </div>
  );
}
```

---

## **Step 5: Dashboard Pages**

### **Admin Dashboard** `src/app/admin/dashboard/page.js`
```javascript
'use client';
import ProtectedRoute from '@/components/ProtectedRoute';
import useAuthStore from '@/store/authStore';

export default function AdminDashboard() {
  const { user, logout } = useAuthStore();

  return (
    <ProtectedRoute adminOnly={true}>
      <div className="p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">🛡️ Admin Dashboard</h1>
          <button 
            onClick={logout}
            className="bg-red-600 text-white px-4 py-2 rounded"
          >
            Logout
          </button>
        </div>
        
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
          ✅ Welcome Admin: {user?.full_name}! You have access to ML features.
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-bold mb-4">🤖 ML Features (Admin Only)</h3>
            <ul className="space-y-2">
              <li>• Employee Turnover Prediction</li>
              <li>• Performance Analytics</li>
              <li>• Risk Assessment</li>
              <li>• Advanced Reports</li>
            </ul>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-bold mb-4">👥 Admin Actions</h3>
            <ul className="space-y-2">
              <li>• Manage Employees</li>
              <li>• Manage Departments</li>
              <li>• View All Reports</li>
              <li>• System Configuration</li>
            </ul>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
```

### **Employee Dashboard** `src/app/employee/dashboard/page.js`
```javascript
'use client';
import ProtectedRoute from '@/components/ProtectedRoute';
import useAuthStore from '@/store/authStore';

export default function EmployeeDashboard() {
  const { user, logout } = useAuthStore();

  return (
    <ProtectedRoute>
      <div className="p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">👤 Employee Dashboard</h1>
          <button 
            onClick={logout}
            className="bg-red-600 text-white px-4 py-2 rounded"
          >
            Logout
          </button>
        </div>
        
        <div className="bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded mb-6">
          ✅ Welcome {user?.full_name}! You're logged in as an employee.
        </div>
        
        <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded mb-6">
          ⚠️ ML features are not available for employees. Admin access required.
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-bold mb-4">📊 Your Profile</h3>
            <ul className="space-y-2">
              <li>• Employee ID: {user?.employee_id}</li>
              <li>• Position: {user?.position}</li>
              <li>• Department: {user?.department_name}</li>
              <li>• Status: {user?.is_active ? 'Active' : 'Inactive'}</li>
            </ul>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-bold mb-4">🎯 Available Actions</h3>
            <ul className="space-y-2">
              <li>• Update Profile</li>
              <li>• View Performance</li>
              <li>• Submit Feedback</li>
              <li>• Request Leave</li>
            </ul>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
```

---

## **Step 6: Root Layout** `src/app/layout.js`
```javascript
'use client';
import { useEffect } from 'react';
import useAuthStore from '@/store/authStore';
import './globals.css';

export default function RootLayout({ children }) {
  const { initializeAuth } = useAuthStore();

  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

---

## **Step 7: CSS (Tailwind)** `src/app/globals.css`
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

## 🎯 **Testing Flow:**

### **Test Admin:**
1. Login dengan: `admin@company.com / AdminPass123!`
2. Harus redirect ke `/admin/dashboard`
3. Lihat "ML Features" section
4. Refresh page → tetap di dashboard (no redirect loop!)

### **Test Employee:**
1. Login dengan: `bravely@gmail.com / user123`
2. Harus redirect ke `/employee/dashboard`
3. Lihat warning "ML features not available"
4. Coba akses `/admin/dashboard` → redirect ke employee dashboard

### **Test Logout:**
1. Click logout
2. Harus redirect ke login page
3. Token invalidated di backend

---

## 🔧 **Quick Debug:**

### **Problem: Redirect Loop**
- Clear browser cookies
- Check console for errors
- Pastikan `setTimeout(500)` di ProtectedRoute

### **Problem: Token Hilang**
- Check localStorage di browser
- Check cookies di Application tab
- Pastikan `initializeAuth()` dipanggil

### **Problem: Role Access**
- Check `user.role` di console
- Pastikan `isAdmin()` function correct

---

## 🎉 **Expected Results:**

✅ **Admin**: Login → Admin Dashboard dengan ML access  
✅ **Employee**: Login → Employee Dashboard tanpa ML access  
✅ **Security**: Employee ga bisa akses admin features  
✅ **Persistence**: Token bertahan setelah refresh  
✅ **Logout**: Token di-invalidate properly  

**INI HARUSNYA SOLVE MASALAH REDIRECT LOOP DAN ROLE ACCESS! 🚀**
