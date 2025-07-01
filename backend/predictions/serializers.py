from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .models import Department, Employee, TurnoverPrediction, MLModel

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password', 'password_confirm',
            'employee_id', 'department', 'position', 'salary', 'age', 'years_at_company',
            'satisfaction_level', 'last_evaluation', 'number_project', 
            'average_monthly_hours', 'time_spend_company', 'work_accident', 'promotion_last_5years'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Add user to Employees group by default
        employees_group, created = Group.objects.get_or_create(name='Employees')
        user.groups.add(employees_group)
        
        return user

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user info"""
    groups = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'groups', 'employee_id']
        read_only_fields = ['id']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'name', 'email', 'department', 'department_name',
            'hire_date', 'satisfaction_level', 'last_evaluation', 'number_project',
            'average_monthly_hours', 'time_spend_company', 'work_accident',
            'promotion_last_5years', 'salary', 'left', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_satisfaction_level(self, value):
        if not 0 <= value <= 1:
            raise serializers.ValidationError("Satisfaction level must be between 0 and 1.")
        return value
    
    def validate_last_evaluation(self, value):
        if not 0 <= value <= 1:
            raise serializers.ValidationError("Last evaluation must be between 0 and 1.")
        return value

class EmployeeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new employees"""
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'name', 'email', 'department', 'hire_date',
            'satisfaction_level', 'last_evaluation', 'number_project',
            'average_monthly_hours', 'time_spend_company', 'work_accident',
            'promotion_last_5years', 'salary'
        ]

class PredictionRequestSerializer(serializers.Serializer):
    """Serializer for prediction requests"""
    employee_id = serializers.CharField(required=False)
    satisfaction_level = serializers.FloatField(min_value=0, max_value=1)
    last_evaluation = serializers.FloatField(min_value=0, max_value=1)
    number_project = serializers.IntegerField(min_value=1)
    average_monthly_hours = serializers.IntegerField(min_value=1)
    time_spend_company = serializers.IntegerField(min_value=0)
    work_accident = serializers.BooleanField()
    promotion_last_5years = serializers.BooleanField()
    salary = serializers.ChoiceField(choices=['low', 'medium', 'high'])
    department = serializers.CharField()

class TurnoverPredictionSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    
    class Meta:
        model = TurnoverPrediction
        fields = [
            'id', 'employee', 'employee_name', 'employee_id',
            'prediction_probability', 'prediction_result', 'model_used',
            'confidence_score', 'features_used', 'created_at'
        ]
        read_only_fields = ['created_at']

class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = [
            'id', 'name', 'model_type', 'accuracy', 'f1_score', 'auc_score',
            'hyperparameters', 'feature_importance', 'is_active', 'created_at'
        ]
        read_only_fields = ['created_at']

class EmployeeStatsSerializer(serializers.Serializer):
    """Serializer for employee statistics"""
    total_employees = serializers.IntegerField()
    total_left = serializers.IntegerField()
    turnover_rate = serializers.FloatField()
    avg_satisfaction = serializers.FloatField()
    avg_monthly_hours = serializers.FloatField()
    department_stats = serializers.DictField()
    salary_distribution = serializers.DictField()

class PredictionResultSerializer(serializers.Serializer):
    """Serializer for prediction results"""
    prediction = serializers.BooleanField()
    probability = serializers.FloatField()
    confidence = serializers.FloatField()
    risk_level = serializers.CharField()
    recommendations = serializers.ListField(child=serializers.CharField())

class BulkPredictionSerializer(serializers.Serializer):
    """Serializer for bulk predictions"""
    employees = PredictionRequestSerializer(many=True)

class ModelTrainingSerializer(serializers.Serializer):
    """Serializer for model training requests"""
    model_name = serializers.CharField(max_length=100)

class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password"""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("Email already exists")
        return value
