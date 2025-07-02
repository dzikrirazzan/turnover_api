from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import Department, Employee, EmployeePerformanceData
from .serializers import (
    EmployeeRegistrationSerializer, 
    LoginSerializer, 
    DepartmentSerializer,
    EmployeePerformanceDataSerializer,
    UserProfileSerializer
)
from .permissions import IsAdminUser

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
    Register new employee with BASIC DATA only
    ML data will be added separately by admin
    """
    serializer = EmployeeRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        employee = serializer.save()
        return Response({
            'message': 'Registrasi berhasil',
            'employee_id': employee.employee_id,
            'email': employee.email,
            'full_name': employee.full_name
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_employee(request):
    """Login with email and password"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        
        profile_serializer = UserProfileSerializer(user)
        return Response({
            'message': 'Login berhasil',
            'user': profile_serializer.data
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
    """Get current user profile"""
    serializer = UserProfileSerializer(request.user)
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
