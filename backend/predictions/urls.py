from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet, EmployeeViewSet, PredictionViewSet, MLModelViewSet,
    register_user, login_user, logout_user, user_profile, update_profile,
    change_password, check_auth, upload_csv_and_predict, get_csv_template,
    update_employee_ml_data
)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'predictions', PredictionViewSet)
router.register(r'models', MLModelViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    
    # Authentication endpoints
    path('api/auth/register/', register_user, name='register_user'),
    path('api/auth/login/', login_user, name='login_user'),
    path('api/auth/logout/', logout_user, name='logout_user'),
    path('api/auth/profile/', user_profile, name='user_profile'),
    path('api/auth/profile/update/', update_profile, name='update_profile'),
    path('api/auth/change-password/', change_password, name='change_password'),
    path('api/auth/check/', check_auth, name='check_auth'),
    
    # CSV Upload and Batch Prediction endpoints
    path('api/predictions/upload-csv/', upload_csv_and_predict, name='upload_csv_predict'),
    path('api/predictions/csv-template/', get_csv_template, name='csv_template'),
    
    # Admin ML Data Management
    path('api/admin/employees/<str:employee_id>/ml-data/', update_employee_ml_data, name='update_employee_ml_data'),
]
