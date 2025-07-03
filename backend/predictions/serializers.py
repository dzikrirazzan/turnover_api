from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import Department, Employee, EmployeePerformanceData

class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer untuk Department - digunakan di registrasi dan ML"""
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'employee_count', 'created_at']
        read_only_fields = ['created_at']
    
    def get_employee_count(self, obj):
        return obj.employees.count()

class EmployeeRegistrationResponseSerializer(serializers.ModelSerializer):
    """
    Serializer untuk response registrasi - data lengkap yang dikembalikan setelah registrasi (KONSISTEN dengan login)
    """
    department_name = serializers.CharField(source='department.name', read_only=True)
    token = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number', 'date_of_birth', 'gender', 'marital_status', 
            'education_level', 'address', 'position', 'department', 'department_name',
            'hire_date', 'role', 'is_admin', 'is_manager', 'is_hr', 'is_active', 'created_at', 'token'
        ]
        read_only_fields = ['id', 'employee_id', 'full_name', 'role', 'is_admin', 'is_manager', 'is_hr', 'is_active', 'created_at']
    
    def get_token(self, obj):
        """Generate authentication token for the new user"""
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer untuk registrasi karyawan - HANYA data basic untuk admin
    TIDAK termasuk variabel ML (satisfaction_level, last_evaluation, dll)
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = Employee
        fields = [
            # Informasi dasar untuk authentication
            'email', 'first_name', 'last_name', 'password', 'password_confirm',
            
            # Informasi personal (untuk admin info)
            'phone_number', 'date_of_birth', 'gender', 'marital_status', 
            'education_level', 'address',
            
            # Informasi kerja (untuk admin info + department digunakan di ML)
            'position', 'department', 'hire_date',
            
            # Informasi gaji (untuk admin info, bukan ML)
            'salary', 'salary_amount'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'department': {'required': True},  # Department diperlukan karena dipakai ML
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Password tidak cocok")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        # Create employee with basic data only
        employee = Employee.objects.create_user(
            password=password,
            **validated_data
        )
        return employee

class LoginSerializer(serializers.Serializer):
    """Serializer untuk login dengan email dan password"""
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Email atau password salah')
            if not user.is_active:
                raise serializers.ValidationError('Akun tidak aktif')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Email dan password diperlukan')
        
        return attrs

class LoginResponseSerializer(serializers.ModelSerializer):
    """
    Serializer untuk response login - data lengkap user dengan token (KONSISTEN dengan registration)
    """
    department_name = serializers.CharField(source='department.name', read_only=True)
    token = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number', 'date_of_birth', 'gender', 'marital_status', 
            'education_level', 'address', 'position', 'department', 'department_name',
            'hire_date', 'role', 'is_admin', 'is_manager', 'is_hr', 'is_active', 'created_at', 'token'
        ]
        read_only_fields = ['employee_id', 'full_name', 'role', 'is_admin', 'is_manager', 'is_hr']
    
    def get_token(self, obj):
        """Get or create authentication token"""
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer untuk profile user - basic info only"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'department_name', 'position', 'hire_date',
            'phone_number', 'is_admin', 'is_manager', 'is_hr', 'is_active'
        ]
        read_only_fields = ['employee_id', 'email', 'role', 'full_name', 'department_name', 'is_admin', 'is_manager', 'is_hr']

class EmployeeUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer untuk update data karyawan - admin only
    Allows updating most fields except critical ones
    """
    class Meta:
        model = Employee
        fields = [
            'first_name', 'last_name', 'phone_number', 'date_of_birth', 
            'gender', 'marital_status', 'education_level', 'address',
            'position', 'department', 'hire_date', 'salary', 'salary_amount',
            'role', 'is_active'
        ]
        extra_kwargs = {
            'department': {'required': False},
        }

class EmployeeListSerializer(serializers.ModelSerializer):
    """
    Serializer untuk list karyawan - admin only
    Shows essential info for employee listing
    """
    department_name = serializers.CharField(source='department.name', read_only=True)
    has_performance_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'department', 'department_name', 'position', 'hire_date',
            'is_active', 'has_performance_data', 'created_at'
        ]
        read_only_fields = ['employee_id', 'full_name', 'created_at']
    
    def get_has_performance_data(self, obj):
        return hasattr(obj, 'performance_data')

class EmployeePerformanceDataSerializer(serializers.ModelSerializer):
    """
    Serializer untuk data ML - TERPISAH dari registrasi
    Hanya admin yang bisa akses data ini
    """
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_email = serializers.CharField(source='employee.email', read_only=True)
    department_name = serializers.CharField(source='employee.department.name', read_only=True)
    
    class Meta:
        model = EmployeePerformanceData
        fields = [
            'employee', 'employee_name', 'employee_email', 'department_name',
            
            # ML Variables - HANYA di model terpisah
            'satisfaction_level', 'last_evaluation', 'number_project',
            'average_monthly_hours', 'time_spend_company', 'work_accident',
            'promotion_last_5years',
            
            # Target variable
            'left',
            
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'employee_name', 'employee_email', 'department_name']
    
    def validate_employee(self, value):
        # Ensure only one performance data per employee
        if self.instance is None and EmployeePerformanceData.objects.filter(employee=value).exists():
            raise serializers.ValidationError("Employee sudah memiliki data performance")
        return value
