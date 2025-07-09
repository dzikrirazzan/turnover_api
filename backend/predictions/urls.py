from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # ViewSets
    DepartmentViewSet, EmployeeViewSet,
    # Function-based views
    health_check, api_info, register_employee,
    login_employee, logout_employee, user_profile, manage_performance_data,
    list_employees, list_departments, data_separation_stats, predict_turnover
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='departments')
router.register(r'employees', EmployeeViewSet, basename='employees')

urlpatterns = [
    # Include router URLs for CRUD operations
    path('api/', include(router.urls)),
    
    # Existing function-based views
    path('api/health/', health_check, name='health_check'),
    path('api/info/', api_info, name='api_info'),
    path('', api_info, name='api_root'),
    path('api/register/', register_employee, name='register_employee'),
    path('api/login/', login_employee, name='login_employee'),
    path('api/logout/', logout_employee, name='logout_employee'),
    path('api/profile/', user_profile, name='user_profile'),
    
    # Legacy endpoints (will be replaced by ViewSets)
    path('api/departments-list/', list_departments, name='list_departments_legacy'),
    path('api/employees-list/', list_employees, name='list_employees_legacy'),
    
    path('api/performance/', manage_performance_data, name='manage_performance_data'),
    path('api/stats/', data_separation_stats, name='data_separation_stats'),
    path('api/predict/', predict_turnover, name='predict_turnover'),
]