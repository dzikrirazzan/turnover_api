from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Department, Employee, EmployeePerformanceData, TurnoverPrediction
from .serializers import (
    EmployeeRegistrationSerializer, 
    EmployeeRegistrationResponseSerializer,
    LoginSerializer, 
    LoginResponseSerializer,
    DepartmentSerializer,
    EmployeePerformanceDataSerializer,
    UserProfileSerializer,
    EmployeeUpdateSerializer,
    EmployeeListSerializer
)
from .permissions import IsAdminUser
from .response_utils import StandardResponse, ResponseMessages
from .ml_utils import TurnoverPredictor, TurnoverRiskCalculator
import json

# ========================================
# CRUD ViewSets for Employee & Department
# ========================================

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    Complete CRUD operations for Department
    - List: All users can view
    - Create/Update/Delete: Admin only
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    
    def get_permissions(self):
        """
        Allow read for all authenticated users,
        write operations only for admin
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """Get all employees in this department"""
        department = self.get_object()
        employees = department.employees.all()
        employee_data = []
        for emp in employees:
            employee_data.append({
                'id': emp.id,
                'employee_id': emp.employee_id,
                'full_name': emp.full_name,
                'email': emp.email,
                'position': emp.position,
                'hire_date': emp.hire_date,
                'is_active': emp.is_active
            })
        return StandardResponse.success(
            message=f"Karyawan di departemen {department.name} berhasil diambil",
            data={
                'department': department.name,
                'employees': employee_data,
                'total_employees': len(employee_data)
            }
        )

    def destroy(self, request, *args, **kwargs):
        """
        Hard delete department - remove from database completely
        Safe deletion with proper foreign key handling
        """
        from django.db import transaction
        
        try:
            instance = self.get_object()
            department_name = instance.name
            department_id = instance.id
            
            with transaction.atomic():
                # Count employees before deletion
                employee_count = instance.employees.count()
                
                # Update employees to remove department reference first
                # Set department to NULL for all employees in this department
                if employee_count > 0:
                    instance.employees.update(department=None)
                
                # Safe delete: just use basic model delete without cascading issues
                from django.db import connection
                with connection.cursor() as cursor:
                    # Delete department directly by ID to avoid FK constraint issues
                    cursor.execute("DELETE FROM predictions_department WHERE id = %s", [department_id])
            
            return StandardResponse.success(
                message=f'Departemen "{department_name}" berhasil dihapus dari sistem',
                data={
                    'deleted_department_id': department_id,
                    'department_name': department_name,
                    'affected_employees': employee_count,
                    'action': 'hard_delete'
                }
            )
        except Exception as e:
            error_message = str(e)
            return StandardResponse.error(
                message=f'Gagal menghapus departemen: {error_message}',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Complete CRUD operations for Employee
    - List/Retrieve: Admin only
    - Create: Registration endpoint (separate)
    - Update/Delete: Admin only
    """
    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EmployeeRegistrationSerializer
        elif self.action in ['update', 'partial_update']:
            return EmployeeUpdateSerializer
        elif self.action == 'list':
            return EmployeeListSerializer
        return UserProfileSerializer
    
    def get_queryset(self):
        """Filter employees with optional query parameters"""
        queryset = Employee.objects.all()
        department_id = self.request.query_params.get('department', None)
        role = self.request.query_params.get('role', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        if role:
            queryset = queryset.filter(role=role)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
            
        return queryset.order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        """Create new employee (admin only)"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            return StandardResponse.created(
                message=ResponseMessages.DATA_CREATED,
                data={
                    'employee_id': employee.employee_id,
                    'email': employee.email,
                    'full_name': employee.full_name
                }
            )
        return StandardResponse.validation_error(
            message=ResponseMessages.VALIDATION_ERROR,
            errors=serializer.errors
        )
    
    def update(self, request, *args, **kwargs):
        """Update employee data (admin only)"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Use update serializer for field validation
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            employee = serializer.save()
            return StandardResponse.success(
                message=ResponseMessages.DATA_UPDATED,
                data={
                    'employee_id': employee.employee_id,
                    'full_name': employee.full_name
                }
            )
        return StandardResponse.validation_error(
            message=ResponseMessages.VALIDATION_ERROR,
            errors=serializer.errors
        )
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete employee (deactivate instead of removing from database)"""
        try:
            instance = self.get_object()
            employee_id = instance.employee_id
            full_name = instance.full_name
            
            # Soft delete: set is_active to False instead of deleting
            instance.is_active = False
            instance.save()
            
            return StandardResponse.success(
                message=f'Karyawan {full_name} berhasil dinonaktifkan',
                data={
                    'employee_id': employee_id, 
                    'full_name': full_name,
                    'status': 'deactivated'
                }
            )
        except Exception as e:
            return StandardResponse.error(
                message=f'Gagal menonaktifkan karyawan: {str(e)}',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Reactivate employee"""
        employee = self.get_object()
        employee.is_active = True
        employee.save()
        return StandardResponse.success(
            message=f'Karyawan {employee.full_name} berhasil diaktifkan',
            data={'employee_id': employee.employee_id, 'full_name': employee.full_name}
        )
    
    @action(detail=True, methods=['get'])
    def performance_data(self, request, pk=None):
        """Get employee's performance data"""
        employee = self.get_object()
        try:
            performance_data = employee.performance_data
            serializer = EmployeePerformanceDataSerializer(performance_data)
            return StandardResponse.success(
                message=f"Data performa {employee.full_name} berhasil diambil",
                data=serializer.data
            )
        except EmployeePerformanceData.DoesNotExist:
            return StandardResponse.not_found(
                message=f'Data performa tidak ditemukan untuk {employee.full_name}'
            )
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get employee statistics"""
        total_employees = Employee.objects.count()
        active_employees = Employee.objects.filter(is_active=True).count()
        inactive_employees = total_employees - active_employees
        
        # Count by department
        dept_stats = []
        for dept in Department.objects.all():
            dept_stats.append({
                'department': dept.name,
                'employee_count': dept.employees.count()
            })
        
        # Count by role
        from django.db.models import Count
        role_stats = Employee.objects.values('role').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return StandardResponse.success(
            message="Statistik karyawan berhasil diambil",
            data={
                'total_employees': total_employees,
                'active_employees': active_employees,
                'inactive_employees': inactive_employees,
                'department_breakdown': dept_stats,
                'role_breakdown': list(role_stats)
            }
        )

# ========================================
# Existing Function-based Views
# ========================================

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """API health check endpoint"""
    return StandardResponse.success(
        message="SMART-EN Turnover Prediction API berjalan",
        data={
            'status': 'healthy',
            'version': '2.0.0'
        }
    )

@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """Informasi API"""
    return StandardResponse.success(
        message="Informasi API berhasil diambil",
        data={
            'api_name': 'SMART-EN Turnover Prediction API',
            'version': '2.0.0',
            'description': 'Sistem prediksi turnover karyawan dengan role-based access',
            'features': [
                'Registrasi dan manajemen karyawan',
                'Role-based access control (Employee/Manager/HR/Admin)',
                'Manajemen department',
                'Data performance tracking (hanya admin)',
                'Prediksi turnover berbasis ML (hanya admin)',
                'Kategorisasi risiko dan alert'
            ],
            'data_separation': {
                'registration_data': 'Data basic karyawan untuk admin info',
                'ml_data': 'Data terpisah untuk machine learning (hanya admin)',
                'shared_data': 'Department digunakan di kedua sistem'
            }
        }
    )

@api_view(['GET'])
@permission_classes([AllowAny])
def list_departments(request):
    """List all departments"""
    departments = Department.objects.all()
    serializer = DepartmentSerializer(departments, many=True)
    return StandardResponse.list_response(
        data=serializer.data,
        message=ResponseMessages.DEPARTMENTS_RETRIEVED
    )

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_employee(request):
    """
    Register new employee with COMPLETE DATA response
    Includes authentication token
    """
    import logging
    logging.warning('REGISTER_EMPLOYEE CALLED - CSRF EXEMPT ACTIVE')
    print('REGISTER_EMPLOYEE CALLED - CSRF EXEMPT ACTIVE')
    
    serializer = EmployeeRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        employee = serializer.save()
        
        # Use response serializer untuk data lengkap dengan token
        response_serializer = EmployeeRegistrationResponseSerializer(employee)
        
        return StandardResponse.created(
            message=ResponseMessages.REGISTRATION_SUCCESS,
            data={'employee': response_serializer.data}
        )
    return StandardResponse.validation_error(
        message=ResponseMessages.VALIDATION_ERROR,
        errors=serializer.errors
    )

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_employee(request):
    """Login with email and password - returns complete user data with token"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        
        # Use login response serializer untuk data lengkap dengan token
        response_serializer = LoginResponseSerializer(user)
        return StandardResponse.success(
            message=ResponseMessages.LOGIN_SUCCESS,
            data={'user': response_serializer.data}
        )
    return StandardResponse.validation_error(
        message=ResponseMessages.INVALID_CREDENTIALS,
        errors=serializer.errors
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_employee(request):
    """Logout current user and invalidate token"""
    try:
        # Delete the user's token to invalidate it
        token = Token.objects.get(user=request.user)
        token.delete()
        
        # Also perform Django logout
        logout(request)
        
        return StandardResponse.success(message=ResponseMessages.LOGOUT_SUCCESS)
    except Token.DoesNotExist:
        # Token already deleted or doesn't exist
        logout(request)
        return StandardResponse.success(message=ResponseMessages.LOGOUT_SUCCESS)
    except Exception as e:
        return StandardResponse.error(
            message=f'Gagal logout: {str(e)}',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Get current user profile with token"""
    serializer = LoginResponseSerializer(request.user)
    return StandardResponse.success(
        message="Profil pengguna berhasil diambil",
        data=serializer.data
    )

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Allow employees to update their own profile data"""
    try:
        employee = request.user
        
        # Fields that employees can update themselves
        allowed_fields = [
            'first_name', 'last_name', 'phone_number', 
            'address', 'position'
        ]
        
        # Filter request data to only allowed fields
        filtered_data = {
            key: value for key, value in request.data.items() 
            if key in allowed_fields
        }
        
        if not filtered_data:
            return StandardResponse.error(
                message='Tidak ada field yang diizinkan untuk diupdate',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Update the employee
        for field, value in filtered_data.items():
            if hasattr(employee, field):
                setattr(employee, field, value)
        
        employee.save()
        
        # Return updated profile
        serializer = LoginResponseSerializer(employee)
        return StandardResponse.success(
            message='Profil berhasil diupdate',
            data=serializer.data
        )
        
    except Exception as e:
        return StandardResponse.error(
            message=f'Gagal mengupdate profil: {str(e)}',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def manage_performance_data(request):
    """
    Manage ML performance data - ADMIN ONLY
    Separated from basic employee data
    """
    if request.method == 'GET':
        # List all performance data
        performance_data = EmployeePerformanceData.objects.all()
        serializer = EmployeePerformanceDataSerializer(performance_data, many=True)
        return StandardResponse.list_response(
            data=serializer.data,
            message=ResponseMessages.PERFORMANCE_DATA_RETRIEVED
        )
    
    elif request.method == 'POST':
        # Create new performance data
        serializer = EmployeePerformanceDataSerializer(data=request.data)
        if serializer.is_valid():
            performance_data = serializer.save()
            return StandardResponse.created(
                message=ResponseMessages.DATA_CREATED,
                data={
                    'employee_name': performance_data.employee.full_name,
                    'performance_data': serializer.data
                }
            )
        return StandardResponse.validation_error(
            message=ResponseMessages.VALIDATION_ERROR,
            errors=serializer.errors
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def list_employees(request):
    """List all employees - ADMIN ONLY"""
    employees = Employee.objects.all()
    data = []
    for emp in employees:
        emp_data = {
            'id': emp.id,
            'employee_id': emp.employee_id,
            'full_name': emp.full_name,
            'email': emp.email,
            'role': emp.role,
            'department': emp.department.name if emp.department else None,
            'position': emp.position,
            'hire_date': emp.hire_date,
            'has_performance_data': hasattr(emp, 'performance_data')
        }
        data.append(emp_data)
    
    return StandardResponse.list_response(
        data=data,
        message=ResponseMessages.EMPLOYEES_RETRIEVED
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def data_separation_stats(request):
    """Show statistics about data separation - ADMIN ONLY"""
    employee_count = Employee.objects.count()
    department_count = Department.objects.count()
    performance_data_count = EmployeePerformanceData.objects.count()
    
    return StandardResponse.success(
        message="Statistik data separation berhasil diambil",
        data={
            'statistics': {
                'employees_registered': employee_count,
                'departments_available': department_count,
                'performance_data_records': performance_data_count,
                'employees_with_ml_data': performance_data_count,
                'employees_without_ml_data': employee_count - performance_data_count
            },
            'data_separation_info': {
                'registration_table': 'predictions_employee (basic data only)',
                'ml_table': 'predictions_employeeperformancedata (ML features only)',
                'shared_table': 'predictions_department (used by both systems)'
            }
        }
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def predict_turnover(request):
    """
    Predict employee turnover risk using ML model - ADMIN ONLY
    
    Input: employee_id
    Output: prediction probability, risk level, and recommendations
    """
    try:
        employee_id = request.data.get('employee_id')
        
        if not employee_id:
            return StandardResponse.error(
                message="Employee ID is required",
                status_code=400
            )
        
        # Get employee and their performance data
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return StandardResponse.error(
                message="Employee not found",
                status_code=404
            )
        
        # Check if performance data exists
        try:
            performance_data = EmployeePerformanceData.objects.get(employee=employee)
        except EmployeePerformanceData.DoesNotExist:
            return StandardResponse.error(
                message="Performance data not found for this employee. Please add performance data first.",
                status_code=404
            )
        
        # Prepare data for ML prediction
        features = {
            'satisfaction_level': performance_data.satisfaction_level or 0.5,
            'last_evaluation': performance_data.last_evaluation or 0.5,
            'number_project': performance_data.number_project or 2,
            'average_monthly_hours': performance_data.average_monthly_hours or 160,
            'time_spend_company': performance_data.time_spend_company or 2,
            'work_accident': 1 if performance_data.work_accident else 0,
            'promotion_last_5years': 1 if performance_data.promotion_last_5years else 0
        }
        
        # Initialize ML predictor
        predictor = TurnoverPredictor()
        
        # For now, use a simple prediction logic since we don't have a trained model
        # In production, you would load a pre-trained model
        prediction_probability = 0.0
        
        # Simple risk calculation based on performance metrics
        risk_score = 0.0
        
        # Low satisfaction increases risk
        if features['satisfaction_level'] < 0.4:
            risk_score += 0.3
        elif features['satisfaction_level'] < 0.6:
            risk_score += 0.1
        
        # Low evaluation increases risk
        if features['last_evaluation'] < 0.4:
            risk_score += 0.3
        elif features['last_evaluation'] < 0.6:
            risk_score += 0.1
        
        # High hours can increase risk
        if features['average_monthly_hours'] > 200:
            risk_score += 0.2
        elif features['average_monthly_hours'] > 180:
            risk_score += 0.1
        
        # Long tenure without promotion increases risk
        if features['time_spend_company'] > 4 and features['promotion_last_5years'] == 0:
            risk_score += 0.2
        
        # Work accidents increase risk
        if features['work_accident'] == 1:
            risk_score += 0.1
        
        # Low project count might indicate disengagement
        if features['number_project'] < 2:
            risk_score += 0.1
        elif features['number_project'] > 6:
            risk_score += 0.1
        
        prediction_probability = min(risk_score, 1.0)
        
        # Determine risk level
        if prediction_probability < 0.3:
            risk_level = 'low'
        elif prediction_probability < 0.7:
            risk_level = 'medium'
        else:
            risk_level = 'high'
        
        # Generate recommendations using risk calculator
        risk_calculator = TurnoverRiskCalculator()
        risk_analysis = risk_calculator.calculate_risk_score(performance_data)
        recommendations = risk_calculator.get_risk_recommendations(risk_analysis)
        
        # Save prediction to database
        prediction = TurnoverPrediction.objects.create(
            employee=employee,
            prediction_probability=prediction_probability,
            prediction_result=prediction_probability > 0.5,
            model_used='RuleBasedModel',
            confidence_score=0.85,
            features_used=features,
            risk_level=risk_level
        )
        
        # Prepare response
        response_data = {
            'employee': {
                'id': employee.id,
                'name': employee.full_name,
                'email': employee.email,
                'department': employee.department.name if employee.department else None,
                'position': employee.position
            },
            'prediction': {
                'probability': round(prediction_probability, 3),
                'risk_level': risk_level,
                'will_leave': prediction_probability > 0.5,
                'confidence_score': 0.85,
                'model_used': 'RuleBasedModel'
            },
            'risk_analysis': {
                'overall_risk_score': round(risk_analysis['overall_risk_score'], 3),
                'risk_factors': risk_analysis['risk_details']
            },
            'recommendations': recommendations,
            'features_used': features,
            'prediction_id': prediction.id,
            'created_at': prediction.created_at.isoformat()
        }
        
        return StandardResponse.success(
            message=f"Turnover prediction completed for {employee.full_name}",
            data=response_data
        )
        
    except Exception as e:
        return StandardResponse.error(
            message=f"Error in prediction: {str(e)}",
            status_code=500
        )
