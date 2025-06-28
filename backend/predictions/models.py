from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Employee(models.Model):
    SALARY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    # Basic Information
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    hire_date = models.DateField()
    
    # Features for ML Model (based on the Medium article)
    satisfaction_level = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Level of satisfaction (0-1)"
    )
    last_evaluation = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Time since last performance evaluation"
    )
    number_project = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of projects completed"
    )
    average_monthly_hours = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Average monthly hours at workplace"
    )
    time_spend_company = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Number of years spent in the company"
    )
    work_accident = models.BooleanField(
        default=False,
        help_text="Whether the employee had a workplace accident"
    )
    promotion_last_5years = models.BooleanField(
        default=False,
        help_text="Whether the employee was promoted in the last five years"
    )
    salary = models.CharField(
        max_length=10,
        choices=SALARY_CHOICES,
        default='medium'
    )
    
    # Target variable
    left = models.BooleanField(
        default=False,
        help_text="Whether the employee left the workplace"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee_id} - {self.name}"

class TurnoverPrediction(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    prediction_probability = models.FloatField(
        help_text="Probability of employee leaving (0-1)"
    )
    prediction_result = models.BooleanField(
        help_text="Predicted result: True if likely to leave"
    )
    model_used = models.CharField(max_length=50, default='RandomForest')
    confidence_score = models.FloatField(null=True, blank=True)
    
    # Input features used for prediction
    features_used = models.JSONField(
        help_text="Features used for this prediction"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Prediction for {self.employee.name} - {self.prediction_probability:.2%}"

class MLModel(models.Model):
    MODEL_TYPES = [
        ('RandomForest', 'Random Forest'),
        ('GradientBoosting', 'Gradient Boosting'),
        ('LogisticRegression', 'Logistic Regression'),
        ('SVM', 'Support Vector Machine'),
        ('KNN', 'K-Nearest Neighbors'),
    ]
    
    name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    model_file_path = models.CharField(max_length=500)
    accuracy = models.FloatField(null=True, blank=True)
    f1_score = models.FloatField(null=True, blank=True)
    auc_score = models.FloatField(null=True, blank=True)
    
    # Model parameters
    hyperparameters = models.JSONField(default=dict)
    feature_importance = models.JSONField(null=True, blank=True)
    
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    trained_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.model_type})"
