from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from predictions.models import Employee, Department

class Goal(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='owned_goals')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_started')
    progress_percentage = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.owner.name}"

class KeyResult(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='key_results')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.goal.title} - {self.title}"

class Feedback(models.Model):
    FEEDBACK_TYPE_CHOICES = [
        ('peer', 'Peer Review'),
        ('manager', 'Manager Review'),
        ('self', 'Self Assessment'),
        ('360', '360 Feedback'),
    ]
    
    from_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='feedback_given')
    to_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='feedback_received')
    feedback_type = models.CharField(max_length=10, choices=FEEDBACK_TYPE_CHOICES)
    project = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    is_helpful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback from {self.from_employee.name} to {self.to_employee.name}"

class PerformanceReview(models.Model):
    REVIEW_STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('self_assessment', 'Self Assessment'),
        ('peer_review', 'Peer Review'),
        ('manager_review', 'Manager Review'),
        ('calibration', 'Calibration'),
        ('completed', 'Completed'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_reviews')
    reviewer = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reviews_conducted')
    review_period_start = models.DateField()
    review_period_end = models.DateField()
    status = models.CharField(max_length=20, choices=REVIEW_STATUS_CHOICES, default='not_started')
    overall_rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        null=True, blank=True
    )
    self_assessment_progress = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    peer_reviews_received = models.IntegerField(default=0)
    peer_reviews_target = models.IntegerField(default=5)
    manager_review_completed = models.BooleanField(default=False)
    calibration_completed = models.BooleanField(default=False)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.employee.name} - {self.review_period_start.year} Review"

class OneOnOneMeeting(models.Model):
    MEETING_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='oneonone_meetings')
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='oneonone_managed')
    meeting_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=45)
    topic = models.CharField(max_length=200)
    agenda = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=MEETING_STATUS_CHOICES, default='scheduled')
    satisfaction_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.employee.name} - {self.manager.name} ({self.meeting_date.date()})"

class Shoutout(models.Model):
    VALUE_CHOICES = [
        ('excellence', 'Excellence'),
        ('collaboration', 'Collaboration'),
        ('innovation', 'Innovation'),
        ('customer_focus', 'Customer Focus'),
        ('teamwork', 'Teamwork'),
        ('leadership', 'Leadership'),
    ]
    
    from_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='shoutouts_given')
    to_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='shoutouts_received', null=True, blank=True)
    to_team = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    values = models.JSONField(default=list)  # Store multiple values
    likes_count = models.IntegerField(default=0)
    is_public = models.BooleanField(default=True)
    shared_to_slack = models.BooleanField(default=False)
    shared_to_teams = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        target = self.to_employee.name if self.to_employee else self.to_team.name
        return f"Shoutout from {self.from_employee.name} to {target}"

class ShoutoutLike(models.Model):
    shoutout = models.ForeignKey(Shoutout, on_delete=models.CASCADE, related_name='likes')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['shoutout', 'employee']

class LearningModule(models.Model):
    TYPE_CHOICES = [
        ('micro-learning', 'Micro Learning'),
        ('article', 'Article'),
        ('course', 'Course'),
        ('video', 'Video'),
    ]
    
    CATEGORY_CHOICES = [
        ('leadership', 'Leadership'),
        ('technical', 'Technical Skills'),
        ('communication', 'Communication'),
        ('project_management', 'Project Management'),
        ('personal_development', 'Personal Development'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    content_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    duration_minutes = models.IntegerField()
    url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class LearningProgress(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='learning_progress')
    module = models.ForeignKey(LearningModule, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    time_spent_minutes = models.IntegerField(default=0)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    is_helpful = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['employee', 'module']
    
    def __str__(self):
        return f"{self.employee.name} - {self.module.title}"

class LearningGoal(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='learning_goals')
    title = models.CharField(max_length=200)
    target_value = models.IntegerField()
    current_value = models.IntegerField(default=0)
    unit = models.CharField(max_length=50)  # e.g., "modules", "minutes", "items"
    week_start = models.DateField()
    is_completed = models.BooleanField(default=False)
    
    @property
    def progress_percentage(self):
        if self.target_value == 0:
            return 0
        return min(100, (self.current_value / self.target_value) * 100)
    
    def __str__(self):
        return f"{self.employee.name} - {self.title}"

class AnalyticsMetric(models.Model):
    METRIC_TYPE_CHOICES = [
        ('team_engagement', 'Team Engagement'),
        ('stress_level', 'Stress Level'),
        ('risk_score', 'Risk Score'),
        ('performance_score', 'Performance Score'),
        ('goal_completion', 'Goal Completion'),
        ('feedback_count', 'Feedback Count'),
        ('learning_hours', 'Learning Hours'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='analytics_metrics', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    metric_type = models.CharField(max_length=30, choices=METRIC_TYPE_CHOICES)
    value = models.FloatField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['employee', 'department', 'metric_type', 'date']
    
    def __str__(self):
        target = self.employee.name if self.employee else self.department.name
        return f"{target} - {self.metric_type} ({self.date})"

class DashboardActivity(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    related_object_type = models.CharField(max_length=50, blank=True)  # goal, feedback, learning, etc.
    related_object_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee.name} - {self.title}"
