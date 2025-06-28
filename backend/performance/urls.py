from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GoalViewSet, KeyResultViewSet, FeedbackViewSet, PerformanceReviewViewSet,
    OneOnOneMeetingViewSet, ShoutoutViewSet, LearningModuleViewSet,
    LearningProgressViewSet, LearningGoalViewSet, AnalyticsViewSet, DashboardViewSet
)

router = DefaultRouter()
router.register(r'goals', GoalViewSet)
router.register(r'key-results', KeyResultViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'performance-reviews', PerformanceReviewViewSet)
router.register(r'oneonone-meetings', OneOnOneMeetingViewSet)
router.register(r'shoutouts', ShoutoutViewSet)
router.register(r'learning-modules', LearningModuleViewSet)
router.register(r'learning-progress', LearningProgressViewSet)
router.register(r'learning-goals', LearningGoalViewSet)
router.register(r'analytics', AnalyticsViewSet, basename='analytics')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('api/', include(router.urls)),
]
