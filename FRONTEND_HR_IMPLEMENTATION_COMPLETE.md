# 🎨 FRONTEND HR FEATURES IMPLEMENTATION GUIDE

Panduan lengkap untuk implementasi frontend HR Features dengan React/Next.js dan integrasi dengan SMART-EN Turnover API.

## 📋 Table of Contents
1. [Setup & Installation](#setup--installation)
2. [Project Structure](#project-structure)
3. [API Service Layer](#api-service-layer)
4. [Authentication & State Management](#authentication--state-management)
5. [Components Implementation](#components-implementation)
6. [Dashboard & Analytics](#dashboard--analytics)
7. [HR Features Pages](#hr-features-pages)
8. [Styling & UI](#styling--ui)
9. [Testing & Deployment](#testing--deployment)

---

## 1. Setup & Installation

### Next.js Setup
```bash
# Create new Next.js project
npx create-next-app@latest hr-dashboard --typescript --tailwind --eslint --app

# Navigate to project
cd hr-dashboard

# Install required dependencies
npm install axios @tanstack/react-query
npm install recharts lucide-react date-fns
npm install @headlessui/react @heroicons/react
npm install react-hook-form @hookform/resolvers yup
npm install react-hot-toast zustand
npm install @types/node @types/react @types/react-dom

# Optional: UI Libraries
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu
npm install class-variance-authority clsx tailwind-merge
```

### Environment Setup
```env
# .env.local
NEXT_PUBLIC_API_BASE_URL=https://turnover-api-hd7ze.ondigitalocean.app
NEXT_PUBLIC_APP_NAME=SMART-EN HR Dashboard
```

---

## 2. Project Structure

```
src/
├── app/                        # Next.js App Router
│   ├── globals.css
│   ├── layout.tsx
│   ├── page.tsx
│   ├── login/
│   │   └── page.tsx
│   ├── dashboard/
│   │   ├── page.tsx
│   │   ├── meetings/
│   │   │   ├── page.tsx
│   │   │   └── [id]/page.tsx
│   │   ├── reviews/
│   │   │   ├── page.tsx
│   │   │   └── [id]/page.tsx
│   │   └── analytics/
│   │       └── page.tsx
├── components/
│   ├── ui/                     # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Modal.tsx
│   │   ├── Table.tsx
│   │   └── Chart.tsx
│   ├── layout/                 # Layout components
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── Layout.tsx
│   ├── forms/                  # Form components
│   │   ├── LoginForm.tsx
│   │   ├── MeetingForm.tsx
│   │   └── ReviewForm.tsx
│   └── features/               # Feature-specific components
│       ├── meetings/
│       ├── reviews/
│       └── analytics/
├── lib/
│   ├── api.ts                  # API client
│   ├── auth.ts                 # Authentication utilities
│   ├── utils.ts                # General utilities
│   └── constants.ts            # Constants
├── hooks/                      # Custom React hooks
│   ├── useAuth.ts
│   ├── useMeetings.ts
│   └── useReviews.ts
├── store/                      # State management
│   ├── authStore.ts
│   └── appStore.ts
└── types/                      # TypeScript types
    ├── auth.ts
    ├── meetings.ts
    └── reviews.ts
```

---

## 3. API Service Layer

### API Client Setup
```typescript
// lib/api.ts
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://turnover-api-hd7ze.ondigitalocean.app';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    });

    // Request interceptor untuk menambahkan token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Token ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor untuk handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth methods
  async login(email: string, password: string) {
    const response = await this.client.post('/api/login/', { email, password });
    return response.data;
  }

  async logout() {
    const response = await this.client.post('/api/logout/');
    return response.data;
  }

  async getProfile() {
    const response = await this.client.get('/api/profile/');
    return response.data;
  }

  // Meetings methods
  async getMeetings() {
    const response = await this.client.get('/api/hr/meetings/');
    return response.data;
  }

  async createMeeting(data: any) {
    const response = await this.client.post('/api/hr/meetings/', data);
    return response.data;
  }

  async getMeeting(id: string) {
    const response = await this.client.get(`/api/hr/meetings/${id}/`);
    return response.data;
  }

  async updateMeeting(id: string, data: any) {
    const response = await this.client.put(`/api/hr/meetings/${id}/`, data);
    return response.data;
  }

  async deleteMeeting(id: string) {
    const response = await this.client.delete(`/api/hr/meetings/${id}/`);
    return response.data;
  }

  // Performance Reviews methods
  async getReviews() {
    const response = await this.client.get('/api/hr/reviews/');
    return response.data;
  }

  async createReview(data: any) {
    const response = await this.client.post('/api/hr/reviews/', data);
    return response.data;
  }

  async getReview(id: string) {
    const response = await this.client.get(`/api/hr/reviews/${id}/`);
    return response.data;
  }

  async updateReview(id: string, data: any) {
    const response = await this.client.put(`/api/hr/reviews/${id}/`, data);
    return response.data;
  }

  // Analytics methods
  async getAnalytics() {
    const response = await this.client.get('/api/hr/analytics/');
    return response.data;
  }

  // Employee methods
  async getEmployees() {
    const response = await this.client.get('/api/employees/');
    return response.data;
  }
}

export const apiClient = new ApiClient();
export default apiClient;
```

### TypeScript Types
```typescript
// types/auth.ts
export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  position?: string;
  department?: string;
}

export interface AuthResponse {
  data: {
    user: User & { token: string };
  };
  message: string;
}

// types/meetings.ts
export interface Meeting {
  id: number;
  title: string;
  description: string;
  employee: number;
  manager: number;
  scheduled_date: string;
  duration_minutes: number;
  meeting_type: 'one_on_one' | 'performance_review' | 'feedback' | 'career_development';
  status: 'scheduled' | 'completed' | 'cancelled';
  notes?: string;
  action_items?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateMeetingData {
  title: string;
  description: string;
  employee: number;
  scheduled_date: string;
  duration_minutes: number;
  meeting_type: string;
}

// types/reviews.ts
export interface PerformanceReview {
  id: number;
  employee: number;
  reviewer: number;
  review_period_start: string;
  review_period_end: string;
  overall_rating: number;
  goals_achievement: number;
  communication_skills: number;
  teamwork: number;
  initiative: number;
  strengths?: string;
  areas_for_improvement?: string;
  goals_next_period?: string;
  status: 'draft' | 'submitted' | 'approved';
  created_at: string;
  updated_at: string;
}

export interface CreateReviewData {
  employee: number;
  review_period_start: string;
  review_period_end: string;
  overall_rating: number;
  goals_achievement: number;
  communication_skills: number;
  teamwork: number;
  initiative: number;
  strengths?: string;
  areas_for_improvement?: string;
  goals_next_period?: string;
}
```

---

## 4. Authentication & State Management

### Auth Store (Zustand)
```typescript
// store/authStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User } from '@/types/auth';
import apiClient from '@/lib/api';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (email: string, password: string) => {
        set({ isLoading: true });
        try {
          const response = await apiClient.login(email, password);
          const { user, token } = response.data.user;
          
          localStorage.setItem('token', token);
          set({
            user,
            token,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      logout: async () => {
        try {
          await apiClient.logout();
        } catch (error) {
          console.error('Logout error:', error);
        } finally {
          localStorage.removeItem('token');
          set({
            user: null,
            token: null,
            isAuthenticated: false,
          });
        }
      },

      checkAuth: async () => {
        const token = localStorage.getItem('token');
        if (!token) {
          set({ isAuthenticated: false });
          return;
        }

        try {
          const response = await apiClient.getProfile();
          set({
            user: response.data,
            token,
            isAuthenticated: true,
          });
        } catch (error) {
          localStorage.removeItem('token');
          set({
            user: null,
            token: null,
            isAuthenticated: false,
          });
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ 
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated 
      }),
    }
  )
);
```

### Custom Hooks
```typescript
// hooks/useAuth.ts
import { useEffect } from 'react';
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';

export const useAuth = (requireAuth = false) => {
  const router = useRouter();
  const { user, isAuthenticated, isLoading, checkAuth } = useAuthStore();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  useEffect(() => {
    if (requireAuth && !isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [requireAuth, isLoading, isAuthenticated, router]);

  return { user, isAuthenticated, isLoading };
};

// hooks/useMeetings.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/lib/api';
import { Meeting, CreateMeetingData } from '@/types/meetings';

export const useMeetings = () => {
  return useQuery<Meeting[]>({
    queryKey: ['meetings'],
    queryFn: () => apiClient.getMeetings(),
  });
};

export const useCreateMeeting = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: CreateMeetingData) => apiClient.createMeeting(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['meetings'] });
    },
  });
};

export const useMeeting = (id: string) => {
  return useQuery<Meeting>({
    queryKey: ['meeting', id],
    queryFn: () => apiClient.getMeeting(id),
    enabled: !!id,
  });
};
```

---

## 5. Components Implementation

### UI Components
```typescript
// components/ui/Button.tsx
import React from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  className,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  children,
  disabled,
  ...props
}) => {
  const baseClasses = 'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none';
  
  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
    danger: 'bg-red-600 text-white hover:bg-red-700',
    outline: 'border border-gray-300 bg-white text-gray-700 hover:bg-gray-50',
  };

  const sizes = {
    sm: 'h-8 px-3 text-sm',
    md: 'h-10 px-4',
    lg: 'h-12 px-6 text-lg',
  };

  return (
    <button
      className={cn(
        baseClasses,
        variants[variant],
        sizes[size],
        className
      )}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && (
        <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
      )}
      {children}
    </button>
  );
};

// components/ui/Card.tsx
import React from 'react';
import { cn } from '@/lib/utils';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export const Card: React.FC<CardProps> = ({ className, children, ...props }) => (
  <div
    className={cn(
      'rounded-lg border border-gray-200 bg-white shadow-sm',
      className
    )}
    {...props}
  >
    {children}
  </div>
);

export const CardHeader: React.FC<CardProps> = ({ className, children, ...props }) => (
  <div className={cn('p-6 pb-4', className)} {...props}>
    {children}
  </div>
);

export const CardContent: React.FC<CardProps> = ({ className, children, ...props }) => (
  <div className={cn('p-6 pt-0', className)} {...props}>
    {children}
  </div>
);

export const CardTitle: React.FC<CardProps> = ({ className, children, ...props }) => (
  <h3 className={cn('text-lg font-semibold text-gray-900', className)} {...props}>
    {children}
  </h3>
);
```

### Layout Components
```typescript
// components/layout/Layout.tsx
'use client';

import React from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { useAuth } from '@/hooks/useAuth';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <>{children}</>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
};

// components/layout/Header.tsx
'use client';

import React from 'react';
import { useAuthStore } from '@/store/authStore';
import { Button } from '@/components/ui/Button';
import { User, LogOut, Bell } from 'lucide-react';

export const Header: React.FC = () => {
  const { user, logout } = useAuthStore();

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h1 className="text-xl font-bold text-gray-900">
            SMART-EN HR Dashboard
          </h1>
        </div>
        
        <div className="flex items-center space-x-4">
          <button className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-md">
            <Bell className="h-5 w-5" />
          </button>
          
          <div className="flex items-center space-x-2">
            <div className="h-8 w-8 bg-blue-600 rounded-full flex items-center justify-center">
              <User className="h-4 w-4 text-white" />
            </div>
            <span className="text-sm font-medium text-gray-700">
              {user?.first_name} {user?.last_name}
            </span>
          </div>
          
          <Button
            variant="outline"
            size="sm"
            onClick={logout}
            className="flex items-center space-x-1"
          >
            <LogOut className="h-4 w-4" />
            <span>Logout</span>
          </Button>
        </div>
      </div>
    </header>
  );
};

// components/layout/Sidebar.tsx
'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { 
  LayoutDashboard, 
  Users, 
  Calendar, 
  FileText, 
  BarChart3,
  Settings 
} from 'lucide-react';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: '1-on-1 Meetings', href: '/dashboard/meetings', icon: Calendar },
  { name: 'Performance Reviews', href: '/dashboard/reviews', icon: FileText },
  { name: 'Analytics', href: '/dashboard/analytics', icon: BarChart3 },
  { name: 'Employees', href: '/dashboard/employees', icon: Users },
  { name: 'Settings', href: '/dashboard/settings', icon: Settings },
];

export const Sidebar: React.FC = () => {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-white border-r border-gray-200 min-h-screen">
      <nav className="p-4 space-y-2">
        {navigation.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
          const Icon = item.icon;
          
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                'flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors',
                isActive
                  ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                  : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
              )}
            >
              <Icon className="h-5 w-5" />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
};
```

---

## 6. Dashboard & Analytics

### Dashboard Page
```typescript
// app/dashboard/page.tsx
'use client';

import React from 'react';
import { useAuth } from '@/hooks/useAuth';
import { Card, CardHeader, CardContent, CardTitle } from '@/components/ui/Card';
import { Calendar, FileText, Users, TrendingUp } from 'lucide-react';

export default function DashboardPage() {
  useAuth(true);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Meetings</p>
                <p className="text-3xl font-bold text-gray-900">24</p>
              </div>
              <Calendar className="h-8 w-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Pending Reviews</p>
                <p className="text-3xl font-bold text-gray-900">8</p>
              </div>
              <FileText className="h-8 w-8 text-orange-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Active Employees</p>
                <p className="text-3xl font-bold text-gray-900">142</p>
              </div>
              <Users className="h-8 w-8 text-green-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Avg Performance</p>
                <p className="text-3xl font-bold text-gray-900">4.2</p>
              </div>
              <TrendingUp className="h-8 w-8 text-purple-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Recent Meetings</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex items-center space-x-4 p-3 rounded-lg bg-gray-50">
                  <div className="h-2 w-2 bg-blue-600 rounded-full"></div>
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">1-on-1 with John Doe</p>
                    <p className="text-sm text-gray-600">Today at 2:00 PM</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Performance Overview</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { label: 'Goals Achievement', value: 85, color: 'bg-blue-600' },
                { label: 'Communication', value: 92, color: 'bg-green-600' },
                { label: 'Teamwork', value: 78, color: 'bg-purple-600' },
              ].map((item) => (
                <div key={item.label} className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium text-gray-700">{item.label}</span>
                    <span className="text-gray-600">{item.value}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${item.color}`}
                      style={{ width: `${item.value}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
```

### Analytics Page dengan Charts
```typescript
// app/dashboard/analytics/page.tsx
'use client';

import React from 'react';
import { useAuth } from '@/hooks/useAuth';
import { Card, CardHeader, CardContent, CardTitle } from '@/components/ui/Card';
import { 
  LineChart, 
  Line, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

const performanceData = [
  { month: 'Jan', average: 4.1, meetings: 12 },
  { month: 'Feb', average: 4.3, meetings: 15 },
  { month: 'Mar', average: 4.2, meetings: 18 },
  { month: 'Apr', average: 4.5, meetings: 20 },
  { month: 'May', average: 4.4, meetings: 22 },
  { month: 'Jun', average: 4.6, meetings: 25 },
];

const departmentData = [
  { name: 'Engineering', value: 35, color: '#3B82F6' },
  { name: 'Marketing', value: 25, color: '#10B981' },
  { name: 'Sales', value: 20, color: '#F59E0B' },
  { name: 'HR', value: 12, color: '#EF4444' },
  { name: 'Finance', value: 8, color: '#8B5CF6' },
];

export default function AnalyticsPage() {
  useAuth(true);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h1>
      </div>

      {/* Performance Trends */}
      <Card>
        <CardHeader>
          <CardTitle>Performance Trends</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="average" 
                stroke="#3B82F6" 
                strokeWidth={2}
                name="Average Rating"
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Meeting Frequency */}
        <Card>
          <CardHeader>
            <CardTitle>Meeting Frequency</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={performanceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="meetings" fill="#10B981" name="Meetings" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Department Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Department Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={departmentData}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}%`}
                >
                  {departmentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Performance Metrics */}
      <Card>
        <CardHeader>
          <CardTitle>Key Performance Metrics</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">4.4</div>
              <div className="text-sm text-gray-600">Average Performance Rating</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600">89%</div>
              <div className="text-sm text-gray-600">Goal Achievement Rate</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600">92%</div>
              <div className="text-sm text-gray-600">Employee Satisfaction</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
```

---

## 7. HR Features Pages

### Meetings Page
```typescript
// app/dashboard/meetings/page.tsx
'use client';

import React, { useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useMeetings, useCreateMeeting } from '@/hooks/useMeetings';
import { Card, CardHeader, CardContent, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Plus, Calendar, Clock, User } from 'lucide-react';
import { MeetingForm } from '@/components/forms/MeetingForm';
import { format } from 'date-fns';

export default function MeetingsPage() {
  useAuth(true);
  const [showForm, setShowForm] = useState(false);
  const { data: meetings, isLoading } = useMeetings();
  const createMeetingMutation = useCreateMeeting();

  const handleCreateMeeting = async (data: any) => {
    try {
      await createMeetingMutation.mutateAsync(data);
      setShowForm(false);
    } catch (error) {
      console.error('Error creating meeting:', error);
    }
  };

  if (isLoading) {
    return <div className="flex items-center justify-center p-8">Loading...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">1-on-1 Meetings</h1>
        <Button onClick={() => setShowForm(true)} className="flex items-center space-x-2">
          <Plus className="h-4 w-4" />
          <span>Schedule Meeting</span>
        </Button>
      </div>

      {/* Meetings Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {meetings?.map((meeting) => (
          <Card key={meeting.id} className="hover:shadow-md transition-shadow">
            <CardHeader>
              <CardTitle className="text-lg">{meeting.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Calendar className="h-4 w-4" />
                  <span>{format(new Date(meeting.scheduled_date), 'MMM dd, yyyy')}</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Clock className="h-4 w-4" />
                  <span>{meeting.duration_minutes} minutes</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <User className="h-4 w-4" />
                  <span>Employee ID: {meeting.employee}</span>
                </div>
                <div className="pt-2">
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                    meeting.status === 'completed' 
                      ? 'bg-green-100 text-green-800'
                      : meeting.status === 'scheduled'
                      ? 'bg-blue-100 text-blue-800'
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {meeting.status.charAt(0).toUpperCase() + meeting.status.slice(1)}
                  </span>
                </div>
                <p className="text-sm text-gray-700 line-clamp-2">
                  {meeting.description}
                </p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Meeting Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full">
            <MeetingForm
              onSubmit={handleCreateMeeting}
              onCancel={() => setShowForm(false)}
              isLoading={createMeetingMutation.isPending}
            />
          </div>
        </div>
      )}
    </div>
  );
}
```

### Meeting Form Component
```typescript
// components/forms/MeetingForm.tsx
'use client';

import React from 'react';
import { useForm } from 'react-hook-form';
import { Button } from '@/components/ui/Button';
import { CreateMeetingData } from '@/types/meetings';

interface MeetingFormProps {
  onSubmit: (data: CreateMeetingData) => void;
  onCancel: () => void;
  isLoading?: boolean;
}

export const MeetingForm: React.FC<MeetingFormProps> = ({
  onSubmit,
  onCancel,
  isLoading = false,
}) => {
  const { register, handleSubmit, formState: { errors } } = useForm<CreateMeetingData>();

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="p-6 space-y-4">
      <h3 className="text-lg font-semibold text-gray-900">Schedule New Meeting</h3>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Title
        </label>
        <input
          type="text"
          {...register('title', { required: 'Title is required' })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter meeting title"
        />
        {errors.title && (
          <p className="text-red-600 text-sm mt-1">{errors.title.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          {...register('description', { required: 'Description is required' })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows={3}
          placeholder="Meeting agenda and objectives"
        />
        {errors.description && (
          <p className="text-red-600 text-sm mt-1">{errors.description.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Employee ID
        </label>
        <input
          type="number"
          {...register('employee', { required: 'Employee ID is required' })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Employee ID"
        />
        {errors.employee && (
          <p className="text-red-600 text-sm mt-1">{errors.employee.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Scheduled Date & Time
        </label>
        <input
          type="datetime-local"
          {...register('scheduled_date', { required: 'Date is required' })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {errors.scheduled_date && (
          <p className="text-red-600 text-sm mt-1">{errors.scheduled_date.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Duration (minutes)
        </label>
        <input
          type="number"
          {...register('duration_minutes', { required: 'Duration is required' })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="30"
          defaultValue={30}
        />
        {errors.duration_minutes && (
          <p className="text-red-600 text-sm mt-1">{errors.duration_minutes.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Meeting Type
        </label>
        <select
          {...register('meeting_type', { required: 'Meeting type is required' })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Select meeting type</option>
          <option value="one_on_one">1-on-1</option>
          <option value="performance_review">Performance Review</option>
          <option value="feedback">Feedback Session</option>
          <option value="career_development">Career Development</option>
        </select>
        {errors.meeting_type && (
          <p className="text-red-600 text-sm mt-1">{errors.meeting_type.message}</p>
        )}
      </div>

      <div className="flex justify-end space-x-3 pt-4">
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit" isLoading={isLoading}>
          Schedule Meeting
        </Button>
      </div>
    </form>
  );
};
```

---

## 8. Styling & UI

### Global Styles
```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}

@layer utilities {
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
}
```

### Utility Functions
```typescript
// lib/utils.ts
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string | Date) {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(date));
}

export function formatDateTime(date: string | Date) {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(date));
}
```

---

## 9. Testing & Deployment

### Testing Setup
```typescript
// __tests__/components/Button.test.tsx
import { render, screen } from '@testing-library/react';
import { Button } from '@/components/ui/Button';

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('shows loading state', () => {
    render(<Button isLoading>Loading</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### Deployment
```bash
# Build untuk production
npm run build

# Deploy ke Vercel
npx vercel --prod

# Atau deploy ke Netlify
npm install -g netlify-cli
netlify deploy --prod --dir=out
```

---

## 🎯 Quick Start Summary

1. **Clone & Setup**:
   ```bash
   npx create-next-app@latest hr-dashboard --typescript --tailwind
   cd hr-dashboard
   npm install axios @tanstack/react-query recharts lucide-react
   ```

2. **Environment**:
   ```env
   NEXT_PUBLIC_API_BASE_URL=https://turnover-api-hd7ze.ondigitalocean.app
   ```

3. **Key Files**:
   - `lib/api.ts` - API client
   - `store/authStore.ts` - Authentication state
   - `components/layout/Layout.tsx` - Main layout
   - `app/dashboard/page.tsx` - Dashboard

4. **Features**:
   - ✅ Authentication & Authorization
   - ✅ Dashboard dengan Analytics
   - ✅ 1-on-1 Meetings Management
   - ✅ Performance Reviews
   - ✅ Real-time Charts & Metrics
   - ✅ Responsive Design
   - ✅ TypeScript Support

---

## 🚀 Next Steps

1. **Implement semua components** sesuai struktur di atas
2. **Test API integration** dengan backend yang sudah ada
3. **Add error handling** dan loading states
4. **Optimize performance** dengan React Query caching
5. **Add real-time updates** dengan WebSocket (optional)
6. **Deploy ke production** (Vercel/Netlify)

Frontend ini akan seamlessly integrate dengan backend API yang sudah ada dan memberikan user experience yang smooth untuk HR features! 🎨✨
