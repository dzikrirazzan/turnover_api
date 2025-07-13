# admin.py
from django.contrib import admin
from .models import Meeting, HRPerformanceReview, MLPredictionHistory

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['title', 'employee', 'scheduled_by', 'scheduled_date', 'status', 'meeting_type']
    list_filter = ['status', 'meeting_type', 'scheduled_date']
    search_fields = ['title', 'employee__first_name', 'employee__last_name']
    date_hierarchy = 'scheduled_date'

@admin.register(HRPerformanceReview)
class HRPerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ['employee', 'reviewer', 'review_date', 'overall_rating', 'average_rating', 'is_final']
    list_filter = ['review_period', 'overall_rating', 'is_final', 'review_date']
    search_fields = ['employee__first_name', 'employee__last_name']
    date_hierarchy = 'review_date'

@admin.register(MLPredictionHistory)
class MLPredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ['employee', 'risk_level', 'probability', 'confidence_score', 'created_at']
    list_filter = ['risk_level', 'created_at']
    search_fields = ['employee__first_name', 'employee__last_name']
    date_hierarchy = 'created_at'
