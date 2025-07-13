# urls.py - URL routing for HR features

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'meetings', views.MeetingViewSet, basename='meeting')
router.register(r'reviews', views.PerformanceReviewViewSet, basename='performancereview')
router.register(r'analytics', views.AnalyticsViewSet, basename='analytics')

urlpatterns = [
    # Include all router URLs (no 'api/' prefix since main urls.py already has it)
    path('', include(router.urls)),
    
    # Additional custom endpoints
    path('meetings/employee/<int:employee_id>/', 
         views.MeetingViewSet.as_view({'get': 'list'}), 
         name='employee-meetings'),
    
    path('reviews/employee/<int:employee_id>/', 
         views.PerformanceReviewViewSet.as_view({'get': 'list'}), 
         name='employee-reviews'),
]

# API Endpoints Documentation:
"""
🔗 HR FEATURES API ENDPOINTS

📅 MEETING MANAGEMENT:
- GET    /api/meetings/                    # List all meetings (admin) or user's meetings
- POST   /api/meetings/                    # Create new meeting (admin only)
- GET    /api/meetings/{id}/               # Get specific meeting
- PUT    /api/meetings/{id}/               # Update meeting (admin only)
- DELETE /api/meetings/{id}/               # Delete meeting (admin only)
- GET    /api/meetings/upcoming/           # Get upcoming meetings
- POST   /api/meetings/{id}/complete/      # Mark meeting as completed

⭐ PERFORMANCE REVIEW:
- GET    /api/reviews/                     # List all reviews (admin) or user's reviews
- POST   /api/reviews/                     # Create new review (admin only)
- GET    /api/reviews/{id}/                # Get specific review
- PUT    /api/reviews/{id}/                # Update review (admin only)
- DELETE /api/reviews/{id}/                # Delete review (admin only)
- POST   /api/reviews/{id}/acknowledge/    # Employee acknowledges review
- GET    /api/reviews/summary/             # Get review summary for employee

📊 ANALYTICS:
- GET    /api/analytics/dashboard/         # Complete analytics dashboard
- GET    /api/analytics/charts/            # Chart data for frontend

🔍 FILTERING & SEARCH:
All list endpoints support query parameters:
- employee={id}        # Filter by employee
- status={status}      # Filter by status
- period={period}      # Filter by review period
- year={year}          # Filter by year
- start_date={date}    # Filter by date range
- end_date={date}      # Filter by date range

🔐 PERMISSIONS:
- Admin/HR: Full CRUD access to all features
- Employee: Read-only access to own data only
"""
