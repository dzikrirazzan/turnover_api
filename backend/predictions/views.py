from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from .models import Department, Employee, EmployeePerformanceData
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
        return Response({
            'department': department.name,
            'employees': employee_data,
            'total_employees': len(employee_data)
        })

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
            return Response({
                'message': 'Employee created successfully',
                'employee_id': employee.employee_id,
                'email': employee.email,
                'full_name': employee.full_name
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """Update employee data (admin only)"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Use update serializer for field validation
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            employee = serializer.save()
            return Response({
                'message': 'Employee updated successfully',
                'employee_id': employee.employee_id,
                'full_name': employee.full_name
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete employee (set inactive)"""
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({
            'message': f'Employee {instance.full_name} has been deactivated'
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Reactivate employee"""
        employee = self.get_object()
        employee.is_active = True
        employee.save()
        return Response({
            'message': f'Employee {employee.full_name} has been activated'
        })
    
    @action(detail=True, methods=['get'])
    def performance_data(self, request, pk=None):
        """Get employee's performance data"""
        employee = self.get_object()
        try:
            performance_data = employee.performance_data
            serializer = EmployeePerformanceDataSerializer(performance_data)
            return Response(serializer.data)
        except EmployeePerformanceData.DoesNotExist:
            return Response({
                'message': 'No performance data found for this employee'
            }, status=status.HTTP_404_NOT_FOUND)
    
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
        
        return Response({
            'total_employees': total_employees,
            'active_employees': active_employees,
            'inactive_employees': inactive_employees,
            'department_breakdown': dept_stats,
            'role_breakdown': list(role_stats)
        })

# ========================================
# Existing Function-based Views
# ========================================

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """API health check endpoint"""
    return Response({
        'status': 'healthy',
        'message': 'SMART-EN Turnover Prediction API berjalan',
        'version': '2.0.0'
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """Informasi API"""
    return Response({
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
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def list_departments(request):
    """List all departments"""
    departments = Department.objects.all()
    serializer = DepartmentSerializer(departments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_employee(request):
    """
    Register new employee with COMPLETE DATA response
    Includes authentication token
    """
    serializer = EmployeeRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        employee = serializer.save()
        
        # Use response serializer untuk data lengkap dengan token
        response_serializer = EmployeeRegistrationResponseSerializer(employee)
        
        return Response({
            'message': 'Registrasi berhasil',
            'employee': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({
            'message': 'Login berhasil',
            'user': response_serializer.data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_employee(request):
    """Logout current user"""
    logout(request)
    return Response({'message': 'Logout berhasil'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Get current user profile with token"""
    serializer = LoginResponseSerializer(request.user)
    return Response(serializer.data)

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
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Create new performance data
        serializer = EmployeePerformanceDataSerializer(data=request.data)
        if serializer.is_valid():
            performance_data = serializer.save()
            return Response({
                'message': 'Data performance berhasil ditambahkan',
                'employee_name': performance_data.employee.full_name
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    
    return Response({
        'employees': data,
        'total': len(data)
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def data_separation_stats(request):
    """Show statistics about data separation - ADMIN ONLY"""
    employee_count = Employee.objects.count()
    department_count = Department.objects.count()
    performance_data_count = EmployeePerformanceData.objects.count()
    
    return Response({
        'message': 'Data separation berhasil diimplementasikan',
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
    })
