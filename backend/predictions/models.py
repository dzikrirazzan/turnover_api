from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class EmployeeManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Employee(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    EDUCATION_LEVEL_CHOICES = [
        ('high_school', 'High School'),
        ('diploma', 'Diploma'),
        ('bachelor', "Bachelor's Degree"),
        ('master', "Master's Degree"),
        ('phd', 'PhD'),
    ]

    SALARY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    # Fields from AbstractUser we want to use: username, first_name, last_name, email, is_staff, is_active, date_joined
    # We will use email as the unique identifier for login
    username = None # We don't need a username, we'll use email
    email = models.EmailField(unique=True)

    # Custom fields
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    
    # Features for ML Model
    satisfaction_level = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Level of satisfaction (0-1)",
        null=True, blank=True
    )
    last_evaluation = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Time since last performance evaluation",
        null=True, blank=True
    )
    number_project = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of projects completed",
        null=True, blank=True
    )
    average_monthly_hours = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Average monthly hours at workplace",
        null=True, blank=True
    )
    time_spend_company = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Number of years spent in the company",
        null=True, blank=True
    )
    work_accident = models.BooleanField(
        default=False,
        help_text="Whether the employee had a workplace accident",
        null=True, blank=True
    )
    promotion_last_5years = models.BooleanField(
        default=False,
        help_text="Whether the employee was promoted in the last five years",
        null=True, blank=True
    )
    salary = models.CharField(
        max_length=10,
        choices=SALARY_CHOICES,
        default='medium',
        null=True, blank=True
    )
    
    # Target variable
    left = models.BooleanField(
        default=False,
        help_text="Whether the employee left the workplace"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

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
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.model_type})"
