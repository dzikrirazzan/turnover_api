from rest_framework import serializers
from .models import (
    Goal, KeyResult, Feedback, PerformanceReview, OneOnOneMeeting,
    Shoutout, ShoutoutLike, LearningModule, LearningProgress, LearningGoal,
    AnalyticsMetric, DashboardActivity
)
from predictions.models import Employee, Department

class KeyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyResult
        fields = ['id', 'title', 'description', 'is_completed', 'order']

class GoalSerializer(serializers.ModelSerializer):
    key_results = KeyResultSerializer(many=True, read_only=True)
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    
    class Meta:
        model = Goal
        fields = ['id', 'title', 'description', 'owner', 'owner_name', 'priority', 
                 'status', 'progress_percentage', 'due_date', 'created_at', 
                 'updated_at', 'key_results']

class GoalCreateSerializer(serializers.ModelSerializer):
    key_results = KeyResultSerializer(many=True, required=False)
    
    class Meta:
        model = Goal
        fields = ['title', 'description', 'owner', 'priority', 'status', 
                 'progress_percentage', 'due_date', 'key_results']
    
    def create(self, validated_data):
        key_results_data = validated_data.pop('key_results', [])
        goal = Goal.objects.create(**validated_data)
        
        for kr_data in key_results_data:
            KeyResult.objects.create(goal=goal, **kr_data)
        
        return goal

class FeedbackSerializer(serializers.ModelSerializer):
    from_employee_name = serializers.CharField(source='from_employee.name', read_only=True)
    to_employee_name = serializers.CharField(source='to_employee.name', read_only=True)
    
    class Meta:
        model = Feedback
        fields = ['id', 'from_employee', 'from_employee_name', 'to_employee', 
                 'to_employee_name', 'feedback_type', 'project', 'content', 
                 'rating', 'is_helpful', 'created_at']

class PerformanceReviewSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.name', read_only=True)
    peer_reviews_progress = serializers.SerializerMethodField()
    
    class Meta:
        model = PerformanceReview
        fields = ['id', 'employee', 'employee_name', 'reviewer', 'reviewer_name',
                 'review_period_start', 'review_period_end', 'status', 'overall_rating',
                 'self_assessment_progress', 'peer_reviews_received', 'peer_reviews_target',
                 'peer_reviews_progress', 'manager_review_completed', 'calibration_completed',
                 'comments', 'created_at', 'updated_at']
    
    def get_peer_reviews_progress(self, obj):
        if obj.peer_reviews_target == 0:
            return 100
        return min(100, (obj.peer_reviews_received / obj.peer_reviews_target) * 100)

class OneOnOneMeetingSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    manager_name = serializers.CharField(source='manager.name', read_only=True)
    
    class Meta:
        model = OneOnOneMeeting
        fields = ['id', 'employee', 'employee_name', 'manager', 'manager_name',
                 'meeting_date', 'duration_minutes', 'topic', 'agenda', 'notes',
                 'status', 'satisfaction_rating', 'created_at', 'updated_at']

class ShoutoutSerializer(serializers.ModelSerializer):
    from_employee_name = serializers.CharField(source='from_employee.name', read_only=True)
    from_employee_initials = serializers.SerializerMethodField()
    to_employee_name = serializers.CharField(source='to_employee.name', read_only=True)
    to_team_name = serializers.CharField(source='to_team.name', read_only=True)
    
    class Meta:
        model = Shoutout
        fields = ['id', 'from_employee', 'from_employee_name', 'from_employee_initials',
                 'to_employee', 'to_employee_name', 'to_team', 'to_team_name',
                 'title', 'message', 'values', 'likes_count', 'is_public',
                 'shared_to_slack', 'shared_to_teams', 'created_at']
    
    def get_from_employee_initials(self, obj):
        name_parts = obj.from_employee.name.split()
        if len(name_parts) >= 2:
            return f"{name_parts[0][0]}{name_parts[1][0]}"
        return name_parts[0][:2] if name_parts else "??"

class LearningModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningModule
        fields = ['id', 'title', 'description', 'content_type', 'category',
                 'duration_minutes', 'url', 'is_active', 'helpful_count', 'created_at']

class LearningProgressSerializer(serializers.ModelSerializer):
    module_title = serializers.CharField(source='module.title', read_only=True)
    module_duration = serializers.IntegerField(source='module.duration_minutes', read_only=True)
    module_type = serializers.CharField(source='module.content_type', read_only=True)
    
    class Meta:
        model = LearningProgress
        fields = ['id', 'employee', 'module', 'module_title', 'module_duration',
                 'module_type', 'is_completed', 'completion_date', 'time_spent_minutes',
                 'rating', 'is_helpful', 'feedback', 'created_at']

class LearningGoalSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = LearningGoal
        fields = ['id', 'employee', 'title', 'target_value', 'current_value',
                 'unit', 'week_start', 'is_completed', 'progress_percentage']

class AnalyticsMetricSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = AnalyticsMetric
        fields = ['id', 'employee', 'employee_name', 'department', 'department_name',
                 'metric_type', 'value', 'date', 'created_at']

class DashboardActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardActivity
        fields = ['id', 'employee', 'activity_type', 'title', 'description',
                 'related_object_type', 'related_object_id', 'created_at']

class DashboardStatsSerializer(serializers.Serializer):
    goals_completed = serializers.IntegerField()
    goals_total = serializers.IntegerField()
    goals_completion_rate = serializers.FloatField()
    feedback_received = serializers.IntegerField()
    learning_hours = serializers.IntegerField()
    performance_score = serializers.FloatField()

class TeamEngagementSerializer(serializers.Serializer):
    date = serializers.DateField()
    engagement_score = serializers.FloatField()
    stress_level = serializers.FloatField()

class IndividualPerformanceSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    employee_name = serializers.CharField()
    employee_initials = serializers.CharField()
    role = serializers.CharField()
    performance_score = serializers.FloatField()
    engagement_score = serializers.FloatField()
    goal_completion = serializers.FloatField()
    risk_level = serializers.CharField()

class AnalyticsDashboardSerializer(serializers.Serializer):
    team_engagement = serializers.FloatField()
    team_engagement_change = serializers.FloatField()
    active_employees = serializers.IntegerField()
    participation_rate = serializers.FloatField()
    at_risk_count = serializers.IntegerField()
    at_risk_percentage = serializers.FloatField()
    goal_completion = serializers.FloatField()
    goal_target_met = serializers.BooleanField()
    engagement_trends = TeamEngagementSerializer(many=True)
    risk_trends = serializers.ListField(child=serializers.DictField())
    individual_performance = IndividualPerformanceSerializer(many=True)
