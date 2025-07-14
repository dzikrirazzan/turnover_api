# serializers.py - Django REST Framework serializers

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Meeting, HRPerformanceReview, MLPredictionHistory
from django.utils import timezone

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user info for nested serialization"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email']


class MeetingSerializer(serializers.ModelSerializer):
    """Meeting serializer with full CRUD support"""
    employee_info = UserBasicSerializer(source='employee', read_only=True)
    scheduled_by_info = UserBasicSerializer(source='scheduled_by', read_only=True)
    is_high_priority = serializers.ReadOnlyField()
    
    class Meta:
        model = Meeting
        fields = [
            'id', 'employee', 'employee_info', 'scheduled_by', 'scheduled_by_info',
            'title', 'meeting_type', 'scheduled_date', 'duration_minutes',
            'meeting_link', 'agenda', 'notes', 'action_items',
            'prediction_id', 'ml_probability', 'ml_risk_level',
            'status', 'reminder_sent', 'is_high_priority',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'employee_info', 'scheduled_by_info']
    
    def validate_scheduled_date(self, value):
        """Ensure meeting is scheduled in the future"""
        if value <= timezone.now():
            raise serializers.ValidationError("Meeting must be scheduled in the future")
        return value
    
    def validate_duration_minutes(self, value):
        """Validate meeting duration"""
        if value < 15 or value > 240:
            raise serializers.ValidationError("Meeting duration must be between 15 and 240 minutes")
        return value


class MeetingCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating meetings"""
    
    class Meta:
        model = Meeting
        fields = [
            'employee', 'title', 'meeting_type', 'scheduled_date', 
            'duration_minutes', 'meeting_link', 'agenda',
            'prediction_id', 'ml_probability', 'ml_risk_level'
        ]
    
    def create(self, validated_data):
        """Auto-set scheduled_by to current user"""
        validated_data['scheduled_by'] = self.context['request'].user
        return super().create(validated_data)


class PerformanceReviewSerializer(serializers.ModelSerializer):
    """Performance review serializer with star ratings"""
    employee_info = UserBasicSerializer(source='employee', read_only=True)
    reviewer_info = UserBasicSerializer(source='reviewer', read_only=True)
    average_rating = serializers.ReadOnlyField()
    rating_breakdown = serializers.ReadOnlyField()
    
    class Meta:
        model = HRPerformanceReview
        fields = [
            'id', 'employee', 'employee_info', 'reviewer', 'reviewer_info',
            'review_period', 'review_date', 'period_start', 'period_end',
            'overall_rating', 'technical_skills', 'communication', 'teamwork',
            'leadership', 'initiative', 'problem_solving',
            'strengths', 'areas_for_improvement', 'goals_for_next_period',
            'additional_notes', 'triggered_by_ml', 'ml_prediction_id',
            'is_final', 'employee_acknowledged', 'acknowledged_date',
            'average_rating', 'rating_breakdown',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'employee_info', 'reviewer_info',
            'average_rating', 'rating_breakdown'
        ]
    
    def validate_review_date(self, value):
        """Ensure review date is not in the future"""
        if value > timezone.now().date():
            raise serializers.ValidationError("Review date cannot be in the future")
        return value
    
    def validate(self, data):
        """Validate period dates"""
        if data.get('period_start') and data.get('period_end'):
            if data['period_start'] >= data['period_end']:
                raise serializers.ValidationError("Period start must be before period end")
        return data


class PerformanceReviewCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating performance reviews with defaults"""
    
    class Meta:
        model = HRPerformanceReview
        fields = [
            'employee', 'review_period', 'review_date',
            'period_start', 'period_end', 'overall_rating',
            'technical_skills', 'communication', 'teamwork',
            'leadership', 'initiative', 'problem_solving',
            'strengths', 'areas_for_improvement', 'goals_for_next_period',
            'additional_notes'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields optional with default values
        self.fields['technical_skills'].required = False
        self.fields['communication'].required = False
        self.fields['teamwork'].required = False
        self.fields['leadership'].required = False
        self.fields['initiative'].required = False
        self.fields['problem_solving'].required = False
        self.fields['strengths'].required = False
        self.fields['areas_for_improvement'].required = False
        self.fields['goals_for_next_period'].required = False
        
    def create(self, validated_data):
        """Auto-set reviewer and provide defaults for missing fields"""
        validated_data['reviewer'] = self.context['request'].user
        
        # Set default values for rating fields if not provided
        rating_fields = ['technical_skills', 'communication', 'teamwork', 
                        'leadership', 'initiative', 'problem_solving']
        for field in rating_fields:
            if field not in validated_data:
                validated_data[field] = validated_data.get('overall_rating', 3)
        
        # Set default text fields if not provided
        text_defaults = {
            'strengths': 'To be updated in future reviews',
            'areas_for_improvement': 'To be identified and documented',
            'goals_for_next_period': 'Goals will be set during review discussion'
        }
        
        for field, default_value in text_defaults.items():
            if field not in validated_data or not validated_data[field]:
                validated_data[field] = default_value
                
        return super().create(validated_data)


class MLPredictionHistorySerializer(serializers.ModelSerializer):
    """ML prediction history for analytics"""
    employee_info = UserBasicSerializer(source='employee', read_only=True)
    
    class Meta:
        model = MLPredictionHistory
        fields = [
            'id', 'employee', 'employee_info', 'prediction_id',
            'probability', 'risk_level', 'confidence_score',
            'satisfaction_level', 'last_evaluation', 'number_project',
            'average_monthly_hours', 'time_spend_company',
            'work_accident', 'promotion_last_5years',
            'model_used', 'overall_risk_score', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'employee_info']


# Chart Data Serializers
class ChartDataSerializer(serializers.Serializer):
    """Base serializer for chart data"""
    chart_type = serializers.CharField()
    title = serializers.CharField()
    data = serializers.DictField()
    options = serializers.DictField(required=False)


class RiskDistributionSerializer(serializers.Serializer):
    """Risk distribution pie chart data"""
    low_risk = serializers.IntegerField()
    medium_risk = serializers.IntegerField()
    high_risk = serializers.IntegerField()
    total_employees = serializers.IntegerField()


class DepartmentAnalysisSerializer(serializers.Serializer):
    """Department-wise risk analysis"""
    department = serializers.CharField()
    employee_count = serializers.IntegerField()
    average_risk = serializers.FloatField()
    high_risk_count = serializers.IntegerField()


class TrendAnalysisSerializer(serializers.Serializer):
    """Trend analysis over time"""
    month = serializers.CharField()
    average_risk = serializers.FloatField()
    prediction_count = serializers.IntegerField()


class AnalyticsSummarySerializer(serializers.Serializer):
    """Complete analytics summary"""
    total_predictions = serializers.IntegerField()
    total_meetings = serializers.IntegerField()
    total_reviews = serializers.IntegerField()
    high_risk_employees = serializers.IntegerField()
    recent_predictions = serializers.IntegerField()
    
    risk_distribution = RiskDistributionSerializer()
    department_analysis = DepartmentAnalysisSerializer(many=True)
    trend_analysis = TrendAnalysisSerializer(many=True)
    
    chart_data = serializers.DictField()
