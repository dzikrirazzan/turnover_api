from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Department, Employee, TurnoverPrediction, MLModel

# --- User and Authentication Serializers ---

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user info"""
    groups = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'groups']
        read_only_fields = ['id']

class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
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

# --- Employee and Employee Registration Serializers ---

class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'name', 'email', 'phone_number', 'date_of_birth',
            'gender', 'marital_status', 'education_level', 'address', 'position',
            'department', 'department_name', 'hire_date', 'satisfaction_level',
            'last_evaluation', 'number_project', 'average_monthly_hours',
            'time_spend_company', 'work_accident', 'promotion_last_5years',
            'salary', 'left', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    # Validasi untuk bidang ML (tetap ada karena ini serializer umum)
    def validate_satisfaction_level(self, value):
        if value is not None and not 0 <= value <= 1:
            raise serializers.ValidationError("Satisfaction level must be between 0 and 1.")
        return value
    
    def validate_last_evaluation(self, value):
        if value is not None and not 0 <= value <= 1:
            raise serializers.ValidationError("Last evaluation must be between 0 and 1.")
        return value

class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'name', 'email', 'phone_number', 'date_of_birth',
            'gender', 'marital_status', 'education_level', 'address', 'position',
            'department', 'hire_date',
            'password', 'password_confirm'
        ]
        extra_kwargs = {
            'employee_id': {'required': True},
            'name': {'required': True},
            'email': {'required': True},
            'department': {'required': True},
            'hire_date': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password': "Passwords don't match"})
        
        # Use email as username for internal Django User model
        if User.objects.filter(username=attrs['email']).exists():
            raise serializers.ValidationError({'email': "Email already exists (used as username)"})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'email': "Email already exists"})
        
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')

        # Create User instance using email as username
        user = User.objects.create_user(
            username=validated_data['email'], # Use email as username
            email=validated_data['email'],
            password=password
        )
        # Assign to Employees group
        employees_group, created = Group.objects.get_or_create(name='Employees')
        user.groups.add(employees_group)

        # Create Employee instance linked to the User
        employee = Employee.objects.create(user=user, **validated_data)
        return employee

class EmployeeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new employees (admin/HR only, no user account creation)"""
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'name', 'email', 'phone_number', 'date_of_birth',
            'gender', 'marital_status', 'education_level', 'address', 'position',
            'department', 'hire_date'
        ]
        extra_kwargs = {
            'employee_id': {'required': True},
            'name': {'required': True},
            'email': {'required': True},
            'department': {'required': True},
            'hire_date': {'required': True},
        }

# --- Other Serializers (unchanged) ---

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

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
