from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Department, TurnoverPrediction, MLModel

Employee = get_user_model()

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id', 'email', 'name', 'employee_id', 'phone_number', 'date_of_birth',
            'gender', 'marital_status', 'education_level', 'address', 'position',
            'department', 'hire_date', 'satisfaction_level', 'last_evaluation',
            'number_project', 'average_monthly_hours', 'time_spend_company',
            'work_accident', 'promotion_last_5years', 'salary', 'left',
            'is_staff', 'is_superuser', 'date_joined', 'last_login'
        )
        read_only_fields = ('date_joined', 'last_login')

class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Employee
        fields = (
            'email', 'password', 'password_confirm', 'name', 'employee_id',
            'phone_number', 'date_of_birth', 'gender', 'marital_status',
            'education_level', 'address', 'position', 'department', 'hire_date'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = Employee.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

    def validate(self, data):
        if data['new_password'] == data['old_password']:
            raise serializers.ValidationError("New password must be different from the old password.")
        return data

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class TurnoverPredictionSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    
    class Meta:
        model = TurnoverPrediction
        fields = (
            'id', 'employee', 'employee_name', 'employee_id',
            'prediction_probability', 'prediction_result', 'model_used',
            'confidence_score', 'features_used', 'created_at'
        )
        read_only_fields = ['created_at']

class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = (
            'id', 'name', 'model_type', 'accuracy', 'f1_score', 'auc_score',
            'hyperparameters', 'feature_importance', 'is_active', 'created_at'
        )
        read_only_fields = ['created_at']
