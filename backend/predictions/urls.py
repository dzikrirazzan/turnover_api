from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'departments', views.DepartmentViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'predictions', views.PredictionViewSet)
router.register(r'models', views.MLModelViewSet)

urlpatterns = [
    
    # Authentication endpoints
    path('api/auth/register/', views.register_employee, name='register_employee'),
    path('api/auth/login/', views.login_user, name='login_user'),
    path('api/auth/logout/', views.logout_user, name='logout_user'),
    path('api/auth/profile/', views.user_profile, name='user_profile'),
    path('api/auth/change-password/', views.change_password, name='change_password'),
    path('api/auth/check/', views.check_auth, name='check_auth'),
    
    # CSV Upload and Batch Prediction endpoints
    path('api/predictions/upload-csv/', views.upload_csv_and_predict, name='upload_csv_predict'),
    path('api/predictions/csv-template/', views.get_csv_template, name='csv_template'),

    path('api/', include(router.urls)),
]
