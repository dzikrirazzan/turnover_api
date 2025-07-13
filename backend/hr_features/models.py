# models.py - Add these models to your Django app

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Meeting(models.Model):
    """1-on-1 Meeting Model for HR follow-ups based on ML predictions"""
    
    MEETING_STATUS = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled')
    ]
    
    MEETING_TYPE = [
        ('followup', 'Follow-up from ML Prediction'),
        ('regular', 'Regular Check-in'),
        ('urgent', 'Urgent Discussion'),
        ('performance', 'Performance Discussion'),
        ('career', 'Career Development'),
        ('feedback', 'Feedback Session')
    ]
    
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='meetings')
    scheduled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scheduled_meetings')
    
    # Meeting Details
    title = models.CharField(max_length=200)
    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPE, default='followup')
    scheduled_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=30, validators=[MinValueValidator(15), MaxValueValidator(240)])
    
    # Meeting Links & Notes
    meeting_link = models.URLField(blank=True, null=True, help_text="Zoom, Google Meet, Teams link")
    agenda = models.TextField(blank=True, help_text="Meeting agenda and topics to discuss")
    notes = models.TextField(blank=True, help_text="Meeting notes and outcomes")
    action_items = models.TextField(blank=True, help_text="Action items and follow-ups")
    
    # ML Prediction Context
    prediction_id = models.CharField(max_length=100, blank=True, null=True)
    ml_probability = models.DecimalField(
        max_digits=5, decimal_places=4, blank=True, null=True,
        validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('1.0'))]
    )
    ml_risk_level = models.CharField(max_length=10, blank=True, null=True)
    
    # Status & Tracking
    status = models.CharField(max_length=20, choices=MEETING_STATUS, default='scheduled')
    reminder_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_date']
        db_table = 'hr_meetings'
    
    def __str__(self):
        return f"{self.title} - {self.employee.get_full_name()} ({self.scheduled_date.strftime('%Y-%m-%d %H:%M')})"
    
    @property
    def is_high_priority(self):
        """Check if meeting is high priority based on ML risk"""
        if self.ml_probability:
            return float(self.ml_probability) >= 0.7
        return False


class HRPerformanceReview(models.Model):
    """HR Performance Review Model with star ratings and detailed feedback"""
    
    RATING_CHOICES = [
        (1, '1 Star - Poor'),
        (2, '2 Stars - Below Average'),
        (3, '3 Stars - Average'),
        (4, '4 Stars - Good'),
        (5, '5 Stars - Excellent')
    ]
    
    REVIEW_PERIOD = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annual', 'Semi-Annual'),
        ('annual', 'Annual'),
        ('adhoc', 'Ad-hoc'),
        ('probation', 'Probation Review')
    ]
    
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hr_performance_reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hr_conducted_reviews')
    
    # Review Details
    review_period = models.CharField(max_length=20, choices=REVIEW_PERIOD)
    review_date = models.DateField()
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Star Ratings (1-5 stars)
    overall_rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    technical_skills = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    communication = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    teamwork = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    leadership = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    initiative = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    problem_solving = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3
    )
    
    # Detailed Feedback
    strengths = models.TextField(help_text="Employee's key strengths and achievements")
    areas_for_improvement = models.TextField(help_text="Areas where employee can improve")
    goals_for_next_period = models.TextField(help_text="Goals and objectives for next review period")
    additional_notes = models.TextField(blank=True, help_text="Additional comments and observations")
    
    # ML Context (if review triggered by prediction)
    triggered_by_ml = models.BooleanField(default=False)
    ml_prediction_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Review Status
    is_final = models.BooleanField(default=False, help_text="Mark as final when review is complete")
    employee_acknowledged = models.BooleanField(default=False)
    acknowledged_date = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-review_date']
        db_table = 'hr_performance_reviews'
        # Prevent duplicate reviews for same period
        unique_together = ['employee', 'review_date', 'review_period']
    
    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.review_period.title()} Review ({self.review_date})"
    
    @property
    def average_rating(self):
        """Calculate average rating across all categories"""
        ratings = [
            self.overall_rating,
            self.technical_skills,
            self.communication,
            self.teamwork,
            self.leadership,
            self.initiative,
            self.problem_solving
        ]
        return round(sum(ratings) / len(ratings), 2)
    
    @property
    def rating_breakdown(self):
        """Get detailed rating breakdown"""
        return {
            'overall': self.overall_rating,
            'technical_skills': self.technical_skills,
            'communication': self.communication,
            'teamwork': self.teamwork,
            'leadership': self.leadership,
            'initiative': self.initiative,
            'problem_solving': self.problem_solving,
            'average': self.average_rating
        }


class MLPredictionHistory(models.Model):
    """Store ML prediction history for analytics"""
    
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prediction_history')
    
    # Prediction Results
    prediction_id = models.CharField(max_length=100, unique=True)
    probability = models.DecimalField(
        max_digits=5, decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('1.0'))]
    )
    risk_level = models.CharField(max_length=10)  # low, medium, high
    confidence_score = models.DecimalField(
        max_digits=5, decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('1.0'))]
    )
    
    # Risk Factors
    satisfaction_level = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    last_evaluation = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    number_project = models.IntegerField(blank=True, null=True)
    average_monthly_hours = models.IntegerField(blank=True, null=True)
    time_spend_company = models.IntegerField(blank=True, null=True)
    work_accident = models.BooleanField(default=False)
    promotion_last_5years = models.BooleanField(default=False)
    
    # Model Info
    model_used = models.CharField(max_length=100)
    overall_risk_score = models.DecimalField(max_digits=5, decimal_places=4)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'ml_prediction_history'
    
    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.risk_level} risk ({self.created_at.strftime('%Y-%m-%d')})"


# Add these to your existing models.py or create a new file
