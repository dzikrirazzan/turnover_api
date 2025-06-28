from django.contrib import admin
from .models import Department, Employee, TurnoverPrediction, MLModel

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'employee_id', 'name', 'department', 'satisfaction_level',
        'time_spend_company', 'salary', 'left', 'created_at'
    ]
    list_filter = [
        'department', 'salary', 'left', 'work_accident', 
        'promotion_last_5years', 'created_at'
    ]
    search_fields = ['employee_id', 'name', 'email']
    list_editable = ['satisfaction_level', 'left']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('employee_id', 'name', 'email', 'department', 'hire_date')
        }),
        ('ML Features', {
            'fields': (
                'satisfaction_level', 'last_evaluation', 'number_project',
                'average_monthly_hours', 'time_spend_company', 'work_accident',
                'promotion_last_5years', 'salary'
            )
        }),
        ('Target Variable', {
            'fields': ('left',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TurnoverPrediction)
class TurnoverPredictionAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'prediction_probability', 'prediction_result',
        'model_used', 'confidence_score', 'created_at'
    ]
    list_filter = ['prediction_result', 'model_used', 'created_at']
    search_fields = ['employee__name', 'employee__employee_id']
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        return False  # Predictions are created programmatically

@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'model_type', 'accuracy', 'f1_score', 
        'auc_score', 'is_active', 'created_at'
    ]
    list_filter = ['model_type', 'is_active', 'created_at']
    search_fields = ['name']
    list_editable = ['is_active']
    readonly_fields = ['created_at']
