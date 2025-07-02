# Generated manually for SMART-EN Turnover Prediction API
# Pemisahan Data: Registrasi vs ML Data

from django.db import migrations, models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        # Department - Digunakan di REGISTRASI dan ML
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        
        # Employee - HANYA data registrasi (basic info untuk admin)
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user account should be considered active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                
                # Authentication fields
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                
                # Role-based access control
                ('role', models.CharField(choices=[('employee', 'Employee'), ('admin', 'Admin'), ('hr', 'HR Manager'), ('manager', 'Department Manager')], default='employee', help_text='User role for access control', max_length=20)),
                
                # Basic personal info (untuk admin info)
                ('employee_id', models.CharField(blank=True, db_index=True, max_length=20, null=True, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True)),
                ('marital_status', models.CharField(blank=True, choices=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed')], max_length=10, null=True)),
                ('education_level', models.CharField(blank=True, choices=[('high_school', 'High School'), ('diploma', 'Diploma'), ('bachelor', "Bachelor's Degree"), ('master', "Master's Degree"), ('phd', 'PhD')], max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                
                # Work info (untuk admin info + department digunakan di ML)
                ('position', models.CharField(blank=True, max_length=100, null=True)),
                ('hire_date', models.DateField(blank=True, null=True)),
                
                # Salary info (untuk admin info, BUKAN ML)
                ('salary', models.CharField(blank=True, choices=[('low', 'Low (< 50K)'), ('medium', 'Medium (50K - 100K)'), ('high', 'High (> 100K)')], default='medium', help_text='Salary level category (for admin info only)', max_length=10, null=True)),
                ('salary_amount', models.DecimalField(blank=True, decimal_places=2, help_text='Annual salary amount (for admin info only)', max_digits=10, null=True)),
                
                # Metadata
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
                'ordering': ['-created_at'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        
        # EmployeePerformanceData - HANYA variabel ML (admin only access)
        migrations.CreateModel(
            name='EmployeePerformanceData',
            fields=[
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='performance_data', serialize=False, to='predictions.employee')),
                
                # ML Features untuk prediksi turnover
                ('satisfaction_level', models.FloatField(blank=True, help_text='Level of satisfaction (0-1)', null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('last_evaluation', models.FloatField(blank=True, help_text='Last performance evaluation score (0-1)', null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('number_project', models.IntegerField(blank=True, help_text='Number of projects completed', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('average_monthly_hours', models.IntegerField(blank=True, help_text='Average monthly hours at workplace', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('time_spend_company', models.IntegerField(blank=True, help_text='Number of years spent in the company', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('work_accident', models.BooleanField(default=False, help_text='Whether the employee had a workplace accident')),
                ('promotion_last_5years', models.BooleanField(default=False, help_text='Whether the employee was promoted in the last five years')),
                
                # Target variable untuk training
                ('left', models.BooleanField(default=False, help_text='Whether the employee left the company (for training data)')),
                
                # Metadata
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Employee Performance Data',
                'verbose_name_plural': 'Employee Performance Data',
                'ordering': ['-updated_at'],
            },
        ),
        
        # TurnoverPrediction - Hasil prediksi ML
        migrations.CreateModel(
            name='TurnoverPrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prediction_probability', models.FloatField(help_text='Probability of employee leaving (0-1)', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('prediction_result', models.BooleanField(help_text='Predicted result: True if likely to leave')),
                ('model_used', models.CharField(default='RandomForest', max_length=50)),
                ('confidence_score', models.FloatField(blank=True, help_text='Model confidence in prediction (0-1)', null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('features_used', models.JSONField(default=dict, help_text='Features and values used for this prediction')),
                ('risk_level', models.CharField(blank=True, choices=[('low', 'Low Risk (< 30%)'), ('medium', 'Medium Risk (30-70%)'), ('high', 'High Risk (> 70%)')], max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictions', to='predictions.employee')),
            ],
            options={
                'verbose_name': 'Turnover Prediction',
                'verbose_name_plural': 'Turnover Predictions',
                'ordering': ['-created_at'],
            },
        ),
        
        # MLModel - Model management
        migrations.CreateModel(
            name='MLModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('model_type', models.CharField(choices=[('RandomForest', 'Random Forest'), ('GradientBoosting', 'Gradient Boosting'), ('LogisticRegression', 'Logistic Regression'), ('SVM', 'Support Vector Machine'), ('XGBoost', 'XGBoost'), ('Neural Network', 'Neural Network')], max_length=20)),
                ('model_file_path', models.CharField(max_length=500)),
                ('accuracy', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('precision', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('recall', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('f1_score', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('auc_score', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('hyperparameters', models.JSONField(blank=True, default=dict)),
                ('feature_importance', models.JSONField(blank=True, null=True)),
                ('training_data_size', models.IntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False, help_text='Whether this model is currently being used for predictions')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_trained', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'ML Model',
                'verbose_name_plural': 'ML Models',
                'ordering': ['-created_at'],
            },
        ),
        
        # Add relationships
        migrations.AddField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='predictions.department'),
        ),
        migrations.AddField(
            model_name='employee',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='employee_set', related_query_name='employee', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='employee_set', related_query_name='employee', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
