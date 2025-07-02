from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import Department, Employee, EmployeePerformanceData, TurnoverPrediction, MLModel

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'employee_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    
    def employee_count(self, obj):
        return obj.employees.count()
    employee_count.short_description = 'Employees'

class EmployeePerformanceDataInline(admin.StackedInline):
    model = EmployeePerformanceData
    extra = 0
    fields = [
        'satisfaction_level', 'last_evaluation', 'number_project',
        'average_monthly_hours', 'time_spend_company', 'work_accident',
        'promotion_last_5years', 'left'
    ]

@admin.register(Employee)
class EmployeeAdmin(BaseUserAdmin):
    model = Employee
    inlines = [EmployeePerformanceDataInline]
    
    # Customize the user admin for our Employee model
    list_display = [
        'employee_id', 'email', 'full_name', 'role', 'department', 
        'is_active', 'created_at'
    ]
    list_filter = [
        'role', 'department', 'is_active', 'is_staff', 'created_at',
        'hire_date'
    ]
    search_fields = ['employee_id', 'first_name', 'last_name', 'email']
    list_editable = ['role', 'is_active']
    readonly_fields = ['employee_id', 'created_at', 'updated_at', 'last_login']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Information', {
            'fields': (
                'employee_id', 'first_name', 'last_name', 'phone_number',
                'date_of_birth', 'gender', 'marital_status', 'address'
            )
        }),
        ('Work Information', {
            'fields': (
                'role', 'position', 'department', 'hire_date', 
                'education_level', 'salary', 'salary_amount'
            )
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important dates', {
            'fields': ('last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'first_name', 'last_name',
                'role', 'department', 'position'
            ),
        }),
    )

@admin.register(EmployeePerformanceData)
class EmployeePerformanceDataAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'satisfaction_level', 'last_evaluation', 'number_project',
        'time_spend_company', 'left', 'updated_at'
    ]
    list_filter = ['left', 'work_accident', 'promotion_last_5years', 'updated_at']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']
    list_editable = ['satisfaction_level', 'last_evaluation', 'left']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(TurnoverPrediction)
class TurnoverPredictionAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'prediction_probability', 'risk_level', 'prediction_result',
        'model_used', 'confidence_score', 'created_at'
    ]
    list_filter = ['risk_level', 'prediction_result', 'model_used', 'created_at']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']
    readonly_fields = ['risk_level', 'created_at']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['employee', 'prediction_probability', 'prediction_result']
        return self.readonly_fields
    
    def has_add_permission(self, request):
        return False  # Predictions are created programmatically

@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'model_type', 'accuracy', 'f1_score', 'auc_score',
        'is_active', 'last_trained', 'created_at'
    ]
    list_filter = ['model_type', 'is_active', 'created_at']
    search_fields = ['name']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'last_trained']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['name', 'model_type', 'model_file_path']
        return self.readonly_fields
