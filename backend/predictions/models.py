from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Department(models.Model):
    """Department model for organizing employees"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class EmployeeManager(BaseUserManager):
    """Custom user manager for Employee model"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        
        # Set default role for regular users
        extra_fields.setdefault('role', 'employee')
        extra_fields.setdefault('is_active', True)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Employee(AbstractUser):
    """Enhanced Employee model with proper role-based access"""
    
    # Role choices for employee/admin system
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('admin', 'Admin'),
        ('hr', 'HR Manager'),
        ('manager', 'Department Manager'),
    ]
    
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

    SALARY_LEVEL_CHOICES = [
        ('low', 'Low (< 50K)'),
        ('medium', 'Medium (50K - 100K)'),
        ('high', 'High (> 100K)'),
    ]
    
    # Use email as the unique identifier for login
    username = None
    email = models.EmailField(unique=True, db_index=True)

    # Role-based access control
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='employee',
        help_text="User role for access control"
    )

    # Fix for reverse accessor conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='employee_set',
        related_query_name='employee',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='employee_set',
        related_query_name='employee',
    )

    # Employee identification and contact info
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True, db_index=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Work-related information (basic info for admin)
    position = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(
        Department, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='employees'
    )
    hire_date = models.DateField(null=True, blank=True)
    
    # Basic salary information (for admin info, NOT for ML)
    salary = models.CharField(
        max_length=10,
        choices=SALARY_LEVEL_CHOICES,
        default='medium',
        null=True, blank=True,
        help_text="Salary level category (for admin info only)"
    )
    salary_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Annual salary amount (for admin info only)"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
    
    def save(self, *args, **kwargs):
        """Override save to auto-generate employee_id if not provided"""
        if not self.employee_id:
            # Generate employee ID based on creation time and user count
            from django.utils import timezone
            count = Employee.objects.count() + 1
            year = timezone.now().year
            self.employee_id = f"EMP{year}{count:04d}"
        super().save(*args, **kwargs)
    
    @property
    def full_name(self):
        """Return the full name of the employee"""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def is_admin(self):
        """Check if user has admin role"""
        return self.role in ['admin', 'hr'] or self.is_superuser
    
    @property
    def is_manager(self):
        """Check if user has manager role"""
        return self.role in ['admin', 'hr', 'manager'] or self.is_staff
    
    @property
    def is_hr(self):
        """Check if user has HR role"""
        return self.role == 'hr'
    
    @property
    def can_view_predictions(self):
        """Check if user can view turnover predictions"""
        return self.is_manager or self.role == 'hr'
    
    @property
    def can_manage_employees(self):
        """Check if user can manage other employees"""
        return self.is_admin
    
    def __str__(self):
        full_name = self.full_name
        return f"{self.employee_id} - {full_name}" if full_name else f"{self.employee_id or 'No ID'}"

class EmployeePerformanceData(models.Model):
    """Separate model for ML prediction features to keep Employee model clean"""
    
    employee = models.OneToOneField(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='performance_data',
        primary_key=True
    )
    
    # ML Features for turnover prediction
    satisfaction_level = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Level of satisfaction (0-1)",
        null=True, blank=True
    )
    last_evaluation = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Last performance evaluation score (0-1)",
        null=True, blank=True
    )
    number_project = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Number of projects completed",
        null=True, blank=True
    )
    average_monthly_hours = models.IntegerField(
        validators=[MinValueValidator(0)],
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
        help_text="Whether the employee had a workplace accident"
    )
    promotion_last_5years = models.BooleanField(
        default=False,
        help_text="Whether the employee was promoted in the last five years"
    )
    
    # Target variable for ML
    left = models.BooleanField(
        default=False,
        help_text="Whether the employee left the company (for training data)"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Employee Performance Data'
        verbose_name_plural = 'Employee Performance Data'
    
    def __str__(self):
        return f"Performance data for {self.employee.full_name}"

class TurnoverPrediction(models.Model):
    """Model to store turnover predictions for employees"""
    
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE,
        related_name='predictions'
    )
    prediction_probability = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Probability of employee leaving (0-1)"
    )
    prediction_result = models.BooleanField(
        help_text="Predicted result: True if likely to leave"
    )
    model_used = models.CharField(max_length=50, default='RandomForest')
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True, 
        blank=True,
        help_text="Model confidence in prediction (0-1)"
    )
    
    # Input features used for prediction (stored as JSON)
    features_used = models.JSONField(
        help_text="Features and values used for this prediction",
        default=dict
    )
    
    # Risk categorization
    RISK_LEVELS = [
        ('low', 'Low Risk (< 30%)'),
        ('medium', 'Medium Risk (30-70%)'),
        ('high', 'High Risk (> 70%)'),
    ]
    
    risk_level = models.CharField(
        max_length=10,
        choices=RISK_LEVELS,
        null=True,
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Turnover Prediction'
        verbose_name_plural = 'Turnover Predictions'
    
    def save(self, *args, **kwargs):
        """Auto-calculate risk level based on probability"""
        if self.prediction_probability is not None:
            if self.prediction_probability < 0.3:
                self.risk_level = 'low'
            elif self.prediction_probability < 0.7:
                self.risk_level = 'medium'
            else:
                self.risk_level = 'high'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Prediction for {self.employee.full_name} - {self.prediction_probability:.2%} ({self.risk_level})"

class MLModel(models.Model):
    """Model to track different ML models and their performance"""
    
    MODEL_TYPES = [
        ('RandomForest', 'Random Forest'),
        ('GradientBoosting', 'Gradient Boosting'),
        ('LogisticRegression', 'Logistic Regression'),
        ('SVM', 'Support Vector Machine'),
        ('XGBoost', 'XGBoost'),
        ('Neural Network', 'Neural Network'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    model_file_path = models.CharField(max_length=500)
    
    # Performance metrics
    accuracy = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True, blank=True
    )
    precision = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True, blank=True
    )
    recall = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True, blank=True
    )
    f1_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True, blank=True
    )
    auc_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True, blank=True
    )
    
    # Model configuration
    hyperparameters = models.JSONField(default=dict, blank=True)
    feature_importance = models.JSONField(null=True, blank=True)
    training_data_size = models.IntegerField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(
        default=False,
        help_text="Whether this model is currently being used for predictions"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_trained = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'ML Model'
        verbose_name_plural = 'ML Models'
    
    def save(self, *args, **kwargs):
        """Ensure only one model is active at a time"""
        if self.is_active:
            MLModel.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.name} ({self.model_type}) - {status}"
