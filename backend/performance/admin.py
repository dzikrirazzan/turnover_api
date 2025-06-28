from django.contrib import admin
from .models import (
    Goal, KeyResult, Feedback, PerformanceReview, OneOnOneMeeting,
    Shoutout, ShoutoutLike, LearningModule, LearningProgress, LearningGoal,
    AnalyticsMetric, DashboardActivity
)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'priority', 'status', 'progress_percentage', 'due_date']
    list_filter = ['status', 'priority', 'owner__department']
    search_fields = ['title', 'owner__name']
    date_hierarchy = 'created_at'

@admin.register(KeyResult)
class KeyResultAdmin(admin.ModelAdmin):
    list_display = ['title', 'goal', 'is_completed', 'order']
    list_filter = ['is_completed', 'goal__status']
    search_fields = ['title', 'goal__title']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['from_employee', 'to_employee', 'feedback_type', 'rating', 'created_at']
    list_filter = ['feedback_type', 'rating', 'created_at']
    search_fields = ['from_employee__name', 'to_employee__name', 'content']

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ['employee', 'reviewer', 'status', 'overall_rating', 'review_period_start']
    list_filter = ['status', 'review_period_start', 'overall_rating']
    search_fields = ['employee__name', 'reviewer__name']

@admin.register(OneOnOneMeeting)
class OneOnOneMeetingAdmin(admin.ModelAdmin):
    list_display = ['employee', 'manager', 'meeting_date', 'status', 'satisfaction_rating']
    list_filter = ['status', 'meeting_date', 'satisfaction_rating']
    search_fields = ['employee__name', 'manager__name', 'topic']

@admin.register(Shoutout)
class ShoutoutAdmin(admin.ModelAdmin):
    list_display = ['from_employee', 'to_employee', 'to_team', 'likes_count', 'created_at']
    list_filter = ['values', 'is_public', 'created_at']
    search_fields = ['from_employee__name', 'to_employee__name', 'title', 'message']

@admin.register(LearningModule)
class LearningModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'category', 'duration_minutes', 'helpful_count']
    list_filter = ['content_type', 'category', 'is_active']
    search_fields = ['title', 'description']

@admin.register(LearningProgress)
class LearningProgressAdmin(admin.ModelAdmin):
    list_display = ['employee', 'module', 'is_completed', 'completion_date', 'rating']
    list_filter = ['is_completed', 'rating', 'module__category']
    search_fields = ['employee__name', 'module__title']

@admin.register(LearningGoal)
class LearningGoalAdmin(admin.ModelAdmin):
    list_display = ['employee', 'title', 'current_value', 'target_value', 'is_completed']
    list_filter = ['is_completed', 'week_start']
    search_fields = ['employee__name', 'title']

@admin.register(AnalyticsMetric)
class AnalyticsMetricAdmin(admin.ModelAdmin):
    list_display = ['employee', 'department', 'metric_type', 'value', 'date']
    list_filter = ['metric_type', 'date']
    search_fields = ['employee__name', 'department__name']

@admin.register(DashboardActivity)
class DashboardActivityAdmin(admin.ModelAdmin):
    list_display = ['employee', 'activity_type', 'title', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['employee__name', 'title', 'description']
