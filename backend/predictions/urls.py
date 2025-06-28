from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'departments', views.DepartmentViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'predictions', views.PredictionViewSet)
router.register(r'models', views.MLModelViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    
    # Authentication endpoints
    path('api/auth/register/', views.register_user, name='register_user'),
    path('api/auth/login/', views.login_user, name='login_user'),
    path('api/auth/logout/', views.logout_user, name='logout_user'),
    path('api/auth/profile/', views.user_profile, name='user_profile'),
    path('api/auth/profile/update/', views.update_profile, name='update_profile'),
    path('api/auth/change-password/', views.change_password, name='change_password'),
    path('api/auth/check/', views.check_auth, name='check_auth'),
    
    # CSV Training Data endpoints
    path('api/load-csv-data/', views.load_csv_training_data, name='load_csv_training_data'),
    path('api/csv-sample/', views.get_csv_sample, name='get_csv_sample'),
]
