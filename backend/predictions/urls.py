from django.urls import path
from .views import (
    health_check, api_info, list_departments, register_employee,
    login_employee, logout_employee, user_profile, manage_performance_data,
    list_employees, data_separation_stats
)

urlpatterns = [
    path('api/health/', health_check, name='health_check'),
    path('api/info/', api_info, name='api_info'),
    path('', api_info, name='api_root'),
    path('api/register/', register_employee, name='register_employee'),
    path('api/login/', login_employee, name='login_employee'),
    path('api/logout/', logout_employee, name='logout_employee'),
    path('api/profile/', user_profile, name='user_profile'),
    path('api/departments/', list_departments, name='list_departments'),
    path('api/employees/', list_employees, name='list_employees'),
    path('api/performance/', manage_performance_data, name='manage_performance_data'),
    path('api/stats/', data_separation_stats, name='data_separation_stats'),
]