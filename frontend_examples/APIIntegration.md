# 🔧 API Integration & State Management

Complete guide untuk API integration dan state management menggunakan React Query dan Zustand.

## API Service Layer dengan Error Handling

### Enhanced API Client
```typescript
// lib/apiClient.ts
import axios, { AxiosInstance, AxiosError } from 'axios';
import { toast } from 'react-hot-toast';

interface ApiResponse<T> {
  data: T;
  message: string;
  status: string;
}

class ApiClient {
  private client: AxiosInstance;
  private baseURL: string;

  constructor() {
    this.baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://turnover-api-hd7ze.ondigitalocean.app';
    
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getToken();
        if (token) {
          config.headers.Authorization = `Token ${token}`;
        }
        
        // Add request ID for debugging
        config.headers['X-Request-ID'] = this.generateRequestId();
        
        console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        console.error('❌ Request interceptor error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        console.log(`✅ API Response: ${response.status} ${response.config.url}`);
        return response;
      },
      (error: AxiosError) => {
        this.handleApiError(error);
        return Promise.reject(error);
      }
    );
  }

  private handleApiError(error: AxiosError) {
    console.error('❌ API Error:', error);

    if (error.response?.status === 401) {
      this.handleUnauthorized();
      return;
    }

    if (error.response?.status === 403) {
      toast.error('Access denied. You do not have permission for this action.');
      return;
    }

    if (error.response?.status === 404) {
      toast.error('Resource not found.');
      return;
    }

    if (error.response?.status >= 500) {
      toast.error('Server error. Please try again later.');
      return;
    }

    if (error.code === 'ECONNABORTED') {
      toast.error('Request timeout. Please check your connection.');
      return;
    }

    if (!error.response) {
      toast.error('Network error. Please check your internet connection.');
      return;
    }

    // Default error message
    const message = error.response?.data?.message || 'An unexpected error occurred.';
    toast.error(message);
  }

  private handleUnauthorized() {
    this.clearToken();
    toast.error('Session expired. Please login again.');
    window.location.href = '/login';
  }

  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('token');
    }
    return null;
  }

  private clearToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
  }

  private generateRequestId(): string {
    return Math.random().toString(36).substring(2, 15);
  }

  // Generic API methods
  async get<T>(url: string, params?: any): Promise<T> {
    const response = await this.client.get(url, { params });
    return response.data;
  }

  async post<T>(url: string, data?: any): Promise<T> {
    const response = await this.client.post(url, data);
    return response.data;
  }

  async put<T>(url: string, data?: any): Promise<T> {
    const response = await this.client.put(url, data);
    return response.data;
  }

  async delete<T>(url: string): Promise<T> {
    const response = await this.client.delete(url);
    return response.data;
  }

  // Authentication methods
  async login(email: string, password: string): Promise<ApiResponse<any>> {
    return this.post('/api/login/', { email, password });
  }

  async logout(): Promise<void> {
    await this.post('/api/logout/');
    this.clearToken();
  }

  async getProfile(): Promise<ApiResponse<any>> {
    return this.get('/api/profile/');
  }

  // HR Features methods
  async getMeetings(): Promise<ApiResponse<any[]>> {
    return this.get('/api/hr/meetings/');
  }

  async createMeeting(data: any): Promise<ApiResponse<any>> {
    return this.post('/api/hr/meetings/', data);
  }

  async getMeeting(id: string): Promise<ApiResponse<any>> {
    return this.get(`/api/hr/meetings/${id}/`);
  }

  async updateMeeting(id: string, data: any): Promise<ApiResponse<any>> {
    return this.put(`/api/hr/meetings/${id}/`, data);
  }

  async deleteMeeting(id: string): Promise<void> {
    return this.delete(`/api/hr/meetings/${id}/`);
  }

  // Performance Reviews methods
  async getReviews(): Promise<ApiResponse<any[]>> {
    return this.get('/api/hr/reviews/');
  }

  async createReview(data: any): Promise<ApiResponse<any>> {
    return this.post('/api/hr/reviews/', data);
  }

  async getReview(id: string): Promise<ApiResponse<any>> {
    return this.get(`/api/hr/reviews/${id}/`);
  }

  async updateReview(id: string, data: any): Promise<ApiResponse<any>> {
    return this.put(`/api/hr/reviews/${id}/`, data);
  }

  // Analytics methods
  async getAnalytics(): Promise<ApiResponse<any>> {
    return this.get('/api/hr/analytics/');
  }

  async getDepartmentAnalytics(department?: string): Promise<ApiResponse<any>> {
    const params = department ? { department } : {};
    return this.get('/api/hr/analytics/department/', params);
  }

  async getPerformanceTrends(timeRange?: string): Promise<ApiResponse<any>> {
    const params = timeRange ? { range: timeRange } : {};
    return this.get('/api/hr/analytics/trends/', params);
  }

  // Employee methods
  async getEmployees(): Promise<ApiResponse<any[]>> {
    return this.get('/api/employees/');
  }

  async getEmployee(id: string): Promise<ApiResponse<any>> {
    return this.get(`/api/employees/${id}/`);
  }
}

export const apiClient = new ApiClient();
export default apiClient;
```

## React Query Setup

### Query Client Configuration
```typescript
// lib/queryClient.ts
import { QueryClient, DefaultOptions } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';

const queryConfig: DefaultOptions = {
  queries: {
    retry: (failureCount, error: any) => {
      // Don't retry on 4xx errors except 408 (timeout)
      if (error?.response?.status >= 400 && error?.response?.status < 500 && error?.response?.status !== 408) {
        return false;
      }
      // Retry up to 3 times for other errors
      return failureCount < 3;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
    refetchOnWindowFocus: false,
    refetchOnReconnect: true,
  },
  mutations: {
    onError: (error: any) => {
      console.error('Mutation error:', error);
      if (!error?.response) {
        toast.error('Network error occurred');
      }
    },
  },
};

export const queryClient = new QueryClient({
  defaultOptions: queryConfig,
});
```

### Custom Hooks dengan React Query
```typescript
// hooks/useHRData.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import apiClient from '@/lib/apiClient';

// Query Keys
export const queryKeys = {
  meetings: ['meetings'] as const,
  meeting: (id: string) => ['meetings', id] as const,
  reviews: ['reviews'] as const,
  review: (id: string) => ['reviews', id] as const,
  analytics: ['analytics'] as const,
  employees: ['employees'] as const,
  profile: ['profile'] as const,
};

// Meetings Hooks
export const useMeetings = () => {
  return useQuery({
    queryKey: queryKeys.meetings,
    queryFn: () => apiClient.getMeetings(),
    select: (data) => data.data, // Extract data from API response wrapper
  });
};

export const useMeeting = (id: string) => {
  return useQuery({
    queryKey: queryKeys.meeting(id),
    queryFn: () => apiClient.getMeeting(id),
    select: (data) => data.data,
    enabled: !!id,
  });
};

export const useCreateMeeting = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: any) => apiClient.createMeeting(data),
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.meetings });
      toast.success(response.message || 'Meeting created successfully!');
    },
    onError: (error: any) => {
      console.error('Create meeting error:', error);
      // Error handling is done in API client interceptor
    },
  });
};

export const useUpdateMeeting = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: any }) => 
      apiClient.updateMeeting(id, data),
    onSuccess: (response, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.meetings });
      queryClient.invalidateQueries({ queryKey: queryKeys.meeting(id) });
      toast.success(response.message || 'Meeting updated successfully!');
    },
  });
};

export const useDeleteMeeting = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: string) => apiClient.deleteMeeting(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.meetings });
      toast.success('Meeting deleted successfully!');
    },
  });
};

// Performance Reviews Hooks
export const useReviews = () => {
  return useQuery({
    queryKey: queryKeys.reviews,
    queryFn: () => apiClient.getReviews(),
    select: (data) => data.data,
  });
};

export const useReview = (id: string) => {
  return useQuery({
    queryKey: queryKeys.review(id),
    queryFn: () => apiClient.getReview(id),
    select: (data) => data.data,
    enabled: !!id,
  });
};

export const useCreateReview = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: any) => apiClient.createReview(data),
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.reviews });
      toast.success(response.message || 'Performance review created successfully!');
    },
  });
};

export const useUpdateReview = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: any }) => 
      apiClient.updateReview(id, data),
    onSuccess: (response, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.reviews });
      queryClient.invalidateQueries({ queryKey: queryKeys.review(id) });
      toast.success(response.message || 'Review updated successfully!');
    },
  });
};

// Analytics Hooks
export const useAnalytics = () => {
  return useQuery({
    queryKey: queryKeys.analytics,
    queryFn: () => apiClient.getAnalytics(),
    select: (data) => data.data,
    staleTime: 2 * 60 * 1000, // 2 minutes for analytics
  });
};

export const useDepartmentAnalytics = (department?: string) => {
  return useQuery({
    queryKey: ['analytics', 'department', department],
    queryFn: () => apiClient.getDepartmentAnalytics(department),
    select: (data) => data.data,
    enabled: !!department,
  });
};

export const usePerformanceTrends = (timeRange: string = '6months') => {
  return useQuery({
    queryKey: ['analytics', 'trends', timeRange],
    queryFn: () => apiClient.getPerformanceTrends(timeRange),
    select: (data) => data.data,
  });
};

// Employee Hooks
export const useEmployees = () => {
  return useQuery({
    queryKey: queryKeys.employees,
    queryFn: () => apiClient.getEmployees(),
    select: (data) => data.data,
  });
};

export const useEmployee = (id: string) => {
  return useQuery({
    queryKey: ['employees', id],
    queryFn: () => apiClient.getEmployee(id),
    select: (data) => data.data,
    enabled: !!id,
  });
};
```

## Advanced State Management

### Enhanced Auth Store
```typescript
// store/authStore.ts
import { create } from 'zustand';
import { persist, devtools } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';
import apiClient from '@/lib/apiClient';

interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  position?: string;
  department?: string;
  role: 'admin' | 'manager' | 'employee';
  permissions: string[];
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  lastActivity: number;
  sessionTimeout: number;
}

interface AuthActions {
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
  refreshToken: () => Promise<void>;
  updateActivity: () => void;
  hasPermission: (permission: string) => boolean;
  isRole: (role: string) => boolean;
}

type AuthStore = AuthState & AuthActions;

export const useAuthStore = create<AuthStore>()(
  devtools(
    persist(
      immer((set, get) => ({
        // Initial state
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
        lastActivity: Date.now(),
        sessionTimeout: 30 * 60 * 1000, // 30 minutes

        // Actions
        login: async (email: string, password: string) => {
          set((state) => {
            state.isLoading = true;
          });

          try {
            const response = await apiClient.login(email, password);
            const { user, token } = response.data;

            if (typeof window !== 'undefined') {
              localStorage.setItem('token', token);
            }

            set((state) => {
              state.user = user;
              state.token = token;
              state.isAuthenticated = true;
              state.isLoading = false;
              state.lastActivity = Date.now();
            });
          } catch (error) {
            set((state) => {
              state.isLoading = false;
            });
            throw error;
          }
        },

        logout: async () => {
          try {
            await apiClient.logout();
          } catch (error) {
            console.error('Logout error:', error);
          } finally {
            if (typeof window !== 'undefined') {
              localStorage.removeItem('token');
            }

            set((state) => {
              state.user = null;
              state.token = null;
              state.isAuthenticated = false;
              state.lastActivity = 0;
            });
          }
        },

        checkAuth: async () => {
          const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
          
          if (!token) {
            set((state) => {
              state.isAuthenticated = false;
            });
            return;
          }

          // Check session timeout
          const { lastActivity, sessionTimeout } = get();
          if (Date.now() - lastActivity > sessionTimeout) {
            get().logout();
            return;
          }

          try {
            const response = await apiClient.getProfile();
            set((state) => {
              state.user = response.data;
              state.token = token;
              state.isAuthenticated = true;
              state.lastActivity = Date.now();
            });
          } catch (error) {
            console.error('Auth check failed:', error);
            get().logout();
          }
        },

        refreshToken: async () => {
          try {
            // Implement refresh token logic if available
            const response = await apiClient.getProfile();
            set((state) => {
              state.user = response.data;
              state.lastActivity = Date.now();
            });
          } catch (error) {
            console.error('Token refresh failed:', error);
            get().logout();
          }
        },

        updateActivity: () => {
          set((state) => {
            state.lastActivity = Date.now();
          });
        },

        hasPermission: (permission: string) => {
          const { user } = get();
          return user?.permissions?.includes(permission) || false;
        },

        isRole: (role: string) => {
          const { user } = get();
          return user?.role === role;
        },
      })),
      {
        name: 'auth-storage',
        partialize: (state) => ({
          token: state.token,
          user: state.user,
          isAuthenticated: state.isAuthenticated,
          lastActivity: state.lastActivity,
        }),
      }
    ),
    { name: 'AuthStore' }
  )
);

// Activity tracking hook
export const useActivityTracker = () => {
  const updateActivity = useAuthStore((state) => state.updateActivity);

  React.useEffect(() => {
    const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'];
    
    const resetTimer = () => {
      updateActivity();
    };

    events.forEach(event => {
      document.addEventListener(event, resetTimer, true);
    });

    return () => {
      events.forEach(event => {
        document.removeEventListener(event, resetTimer, true);
      });
    };
  }, [updateActivity]);
};
```

### Application Store
```typescript
// store/appStore.ts
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  duration?: number;
  timestamp: number;
}

interface AppState {
  sidebarOpen: boolean;
  notifications: Notification[];
  loading: Record<string, boolean>;
  filters: Record<string, any>;
  darkMode: boolean;
}

interface AppActions {
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp'>) => void;
  removeNotification: (id: string) => void;
  clearNotifications: () => void;
  setLoading: (key: string, loading: boolean) => void;
  setFilter: (key: string, value: any) => void;
  clearFilters: () => void;
  toggleDarkMode: () => void;
}

type AppStore = AppState & AppActions;

export const useAppStore = create<AppStore>()(
  devtools(
    immer((set, get) => ({
      // Initial state
      sidebarOpen: true,
      notifications: [],
      loading: {},
      filters: {},
      darkMode: false,

      // Actions
      toggleSidebar: () => {
        set((state) => {
          state.sidebarOpen = !state.sidebarOpen;
        });
      },

      setSidebarOpen: (open: boolean) => {
        set((state) => {
          state.sidebarOpen = open;
        });
      },

      addNotification: (notification) => {
        const id = Math.random().toString(36).substring(2, 15);
        const newNotification = {
          ...notification,
          id,
          timestamp: Date.now(),
        };

        set((state) => {
          state.notifications.push(newNotification);
        });

        // Auto-remove notification after duration
        if (notification.duration !== 0) {
          const duration = notification.duration || 5000;
          setTimeout(() => {
            get().removeNotification(id);
          }, duration);
        }
      },

      removeNotification: (id: string) => {
        set((state) => {
          state.notifications = state.notifications.filter(n => n.id !== id);
        });
      },

      clearNotifications: () => {
        set((state) => {
          state.notifications = [];
        });
      },

      setLoading: (key: string, loading: boolean) => {
        set((state) => {
          if (loading) {
            state.loading[key] = true;
          } else {
            delete state.loading[key];
          }
        });
      },

      setFilter: (key: string, value: any) => {
        set((state) => {
          state.filters[key] = value;
        });
      },

      clearFilters: () => {
        set((state) => {
          state.filters = {};
        });
      },

      toggleDarkMode: () => {
        set((state) => {
          state.darkMode = !state.darkMode;
        });
      },
    })),
    { name: 'AppStore' }
  )
);
```

## Error Boundary & Loading States

### Error Boundary Component
```typescript
// components/ErrorBoundary.tsx
import React from 'react';

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends React.Component<
  React.PropsWithChildren<{}>,
  ErrorBoundaryState
> {
  constructor(props: React.PropsWithChildren<{}>) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error Boundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-6">
            <div className="text-center">
              <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
                <svg className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </div>
              <div className="mt-3">
                <h3 className="text-lg font-medium text-gray-900">Something went wrong</h3>
                <div className="mt-2">
                  <p className="text-sm text-gray-500">
                    An unexpected error has occurred. Please refresh the page or contact support if the problem persists.
                  </p>
                </div>
              </div>
              <div className="mt-6">
                <button
                  type="button"
                  className="w-full inline-flex justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  onClick={() => window.location.reload()}
                >
                  Refresh Page
                </button>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
```

### Loading Components
```typescript
// components/ui/LoadingSpinner.tsx
export const LoadingSpinner = ({ size = 'md', className = '' }) => {
  const sizes = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8',
    xl: 'h-12 w-12',
  };

  return (
    <div className={`animate-spin rounded-full border-2 border-gray-300 border-t-blue-600 ${sizes[size]} ${className}`} />
  );
};

// components/ui/LoadingState.tsx
export const LoadingState = ({ message = 'Loading...' }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <LoadingSpinner size="lg" />
      <p className="mt-4 text-gray-600">{message}</p>
    </div>
  );
};

// components/ui/EmptyState.tsx
export const EmptyState = ({ 
  title = 'No data found', 
  description = 'There are no items to display.',
  action = null 
}) => {
  return (
    <div className="text-center py-12">
      <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
      </svg>
      <h3 className="mt-2 text-sm font-medium text-gray-900">{title}</h3>
      <p className="mt-1 text-sm text-gray-500">{description}</p>
      {action && <div className="mt-6">{action}</div>}
    </div>
  );
};
```

Ini adalah setup yang complete untuk API integration, state management, error handling, dan loading states yang akan membuat frontend aplikasi HR sangat robust dan professional! 🚀✨
