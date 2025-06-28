from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Avg, Count, Q
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
import pandas as pd
import numpy as np
from datetime import datetime
import logging
import base64

from .models import Department, Employee, TurnoverPrediction, MLModel
from .serializers import (
    DepartmentSerializer, EmployeeSerializer, EmployeeCreateSerializer,
    TurnoverPredictionSerializer, MLModelSerializer, PredictionRequestSerializer,
    EmployeeStatsSerializer, PredictionResultSerializer, BulkPredictionSerializer,
    ModelTrainingSerializer, UserRegistrationSerializer, UserSerializer,
    LoginSerializer, ChangePasswordSerializer, UserUpdateSerializer
)
from .ml_utils import TurnoverPredictor, prepare_employee_data_for_ml, get_model_save_path

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """User registration endpoint"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user_data = UserSerializer(user).data
        return Response({
            'message': 'User registered successfully',
            'user': user_data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Get current user profile"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """User login endpoint"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                # Create basic auth token for response
                credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
                user_data = UserSerializer(user).data
                
                return Response({
                    'message': 'Login successful',
                    'user': user_data,
                    'auth_token': credentials,
                    'auth_header': f'Basic {credentials}'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Account is disabled'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'error': 'Invalid username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """User logout endpoint"""
    return Response({
        'message': 'Logout successful',
        'detail': 'You have been logged out. Remove the Authorization header for future requests.'
    }, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Update user profile"""
    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        user_data = UserSerializer(request.user).data
        return Response({
            'message': 'Profile updated successfully',
            'user': user_data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change user password"""
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        
        if not request.user.check_password(old_password):
            return Response({
                'error': 'Old password is incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.set_password(new_password)
        request.user.save()
        
        return Response({
            'message': 'Password changed successfully',
            'detail': 'Please use your new password for future requests.'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_auth(request):
    """Check if user is authenticated and return user info"""
    user_data = UserSerializer(request.user).data
    return Response({
        'authenticated': True,
        'user': user_data,
        'permissions': list(request.user.get_all_permissions()),
        'groups': [group.name for group in request.user.groups.all()]
    }, status=status.HTTP_200_OK)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EmployeeCreateSerializer
        return EmployeeSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get employee statistics"""
        total_employees = Employee.objects.count()
        total_left = Employee.objects.filter(left=True).count()
        turnover_rate = (total_left / total_employees * 100) if total_employees > 0 else 0
        
        # Department statistics
        dept_stats = {}
        for dept in Department.objects.all():
            dept_employees = Employee.objects.filter(department=dept)
            dept_left = dept_employees.filter(left=True).count()
            dept_stats[dept.name] = {
                'total': dept_employees.count(),
                'left': dept_left,
                'turnover_rate': (dept_left / dept_employees.count() * 100) if dept_employees.count() > 0 else 0
            }
        
        # Salary distribution
        salary_dist = {}
        for salary_choice in Employee.SALARY_CHOICES:
            salary_key = salary_choice[0]
            count = Employee.objects.filter(salary=salary_key).count()
            salary_dist[salary_key] = count
        
        stats = {
            'total_employees': total_employees,
            'total_left': total_left,
            'turnover_rate': round(turnover_rate, 2),
            'avg_satisfaction': Employee.objects.aggregate(avg=Avg('satisfaction_level'))['avg'] or 0,
            'avg_monthly_hours': Employee.objects.aggregate(avg=Avg('average_monthly_hours'))['avg'] or 0,
            'department_stats': dept_stats,
            'salary_distribution': salary_dist
        }
        
        serializer = EmployeeStatsSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def predict_turnover(self, request, pk=None):
        """Predict turnover for a specific employee"""
        employee = self.get_object()
        
        try:
            # Load the active model
            active_model = MLModel.objects.filter(is_active=True).first()
            if not active_model:
                return Response(
                    {'error': 'No active ML model found. Please train a model first.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Initialize predictor and load model
            predictor = TurnoverPredictor()
            model_path = get_model_save_path(active_model.name)
            
            if not predictor.load_model(model_path):
                return Response(
                    {'error': 'Could not load the ML model.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Prepare employee data
            employee_data = prepare_employee_data_for_ml(employee)
            
            # Make prediction
            result = predictor.predict_single(employee_data)
            
            # Determine risk level
            risk_level = self._get_risk_level(result['probability'])
            recommendations = self._get_recommendations(employee, result['probability'])
            
            # Save prediction to database
            prediction = TurnoverPrediction.objects.create(
                employee=employee,
                prediction_probability=result['probability'],
                prediction_result=result['prediction'],
                model_used=active_model.name,
                confidence_score=result['confidence'],
                features_used=employee_data,
                created_by=request.user
            )
            
            response_data = {
                'prediction': result['prediction'],
                'probability': result['probability'],
                'confidence': result['confidence'],
                'risk_level': risk_level,
                'recommendations': recommendations
            }
            
            serializer = PredictionResultSerializer(response_data)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error predicting turnover for employee {employee.employee_id}: {str(e)}")
            return Response(
                {'error': 'An error occurred while making the prediction.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _get_risk_level(self, probability):
        """Determine risk level based on probability"""
        if probability < 0.3:
            return 'Low'
        elif probability < 0.7:
            return 'Medium'
        else:
            return 'High'
    
    def _get_recommendations(self, employee, probability):
        """Generate recommendations based on employee data and prediction"""
        recommendations = []
        
        if probability > 0.5:
            if employee.satisfaction_level < 0.5:
                recommendations.append("Consider conducting a satisfaction survey and addressing concerns")
            
            if employee.average_monthly_hours > 250:
                recommendations.append("Employee may be overworked - consider workload redistribution")
            
            if employee.time_spend_company > 5 and not employee.promotion_last_5years:
                recommendations.append("Consider career development opportunities or promotion")
            
            if employee.salary == 'low':
                recommendations.append("Review compensation package")
            
            if employee.last_evaluation < 0.6:
                recommendations.append("Provide additional training and support")
        
        if not recommendations:
            recommendations.append("Employee appears to be in good standing")
        
        return recommendations

class PredictionViewSet(viewsets.ModelViewSet):
    queryset = TurnoverPrediction.objects.all()
    serializer_class = TurnoverPredictionSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def predict(self, request):
        """Make a prediction for custom employee data"""
        serializer = PredictionRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Load the active model
                active_model = MLModel.objects.filter(is_active=True).first()
                if not active_model:
                    return Response(
                        {'error': 'No active ML model found.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Initialize predictor and load model
                predictor = TurnoverPredictor()
                model_path = get_model_save_path(active_model.name)
                
                if not predictor.load_model(model_path):
                    return Response(
                        {'error': 'Could not load the ML model.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                
                # Make prediction
                result = predictor.predict_single(serializer.validated_data)
                
                # Determine risk level
                risk_level = self._get_risk_level(result['probability'])
                
                # Generate recommendations for custom data
                recommendations = self._get_recommendations_for_custom_data(
                    serializer.validated_data, result['probability']
                )
                
                response_data = {
                    'prediction': result['prediction'],
                    'probability': result['probability'],
                    'confidence': result['confidence'],
                    'risk_level': risk_level,
                    'recommendations': recommendations
                }
                
                result_serializer = PredictionResultSerializer(response_data)
                return Response(result_serializer.data)
                
            except Exception as e:
                logger.error(f"Error making prediction: {str(e)}")
                return Response(
                    {'error': 'An error occurred while making the prediction.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _get_recommendations_for_custom_data(self, employee_data, probability):
        """Generate recommendations for custom employee data"""
        recommendations = []
        
        if probability > 0.5:
            # High risk recommendations
            if employee_data.get('satisfaction_level', 1) < 0.5:
                recommendations.append("Consider conducting a satisfaction survey and addressing concerns")
            
            if employee_data.get('average_monthly_hours', 0) > 250:
                recommendations.append("Employee may be overworked - consider workload redistribution")
            
            if (employee_data.get('time_spend_company', 0) > 5 and 
                not employee_data.get('promotion_last_5years', False)):
                recommendations.append("Consider career development opportunities or promotion")
            
            if employee_data.get('salary') == 'low':
                recommendations.append("Review compensation package")
            
            if employee_data.get('last_evaluation', 1) < 0.6:
                recommendations.append("Provide additional training and support")
        
        elif probability > 0.2:
            # Medium risk recommendations
            if employee_data.get('satisfaction_level', 1) < 0.7:
                recommendations.append("Monitor satisfaction levels and provide support")
            
            if employee_data.get('average_monthly_hours', 0) > 200:
                recommendations.append("Monitor workload to prevent burnout")
                
            recommendations.append("Consider regular check-ins to maintain engagement")
        
        else:
            # Low risk - positive reinforcement
            recommendations.append("Employee appears to be in good standing")
            recommendations.append("Continue current management approach")
            
            if employee_data.get('satisfaction_level', 0) > 0.8:
                recommendations.append("High satisfaction - consider as mentor for other employees")
        
        return recommendations
    
    def _get_risk_level(self, probability):
        """Determine risk level based on probability"""
        if probability < 0.3:
            return 'Low'
        elif probability < 0.7:
            return 'Medium'
        else:
            return 'High'
    
    @action(detail=False, methods=['post'])
    def bulk_predict(self, request):
        """Make predictions for multiple employees"""
        serializer = BulkPredictionSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Load the active model
                active_model = MLModel.objects.filter(is_active=True).first()
                if not active_model:
                    return Response(
                        {'error': 'No active ML model found.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Initialize predictor and load model
                predictor = TurnoverPredictor()
                model_path = get_model_save_path(active_model.name)
                
                if not predictor.load_model(model_path):
                    return Response(
                        {'error': 'Could not load the ML model.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                
                results = []
                for employee_data in serializer.validated_data['employees']:
                    result = predictor.predict_single(employee_data)
                    risk_level = self._get_risk_level(result['probability'])
                    
                    results.append({
                        'employee_id': employee_data.get('employee_id', 'N/A'),
                        'prediction': result['prediction'],
                        'probability': result['probability'],
                        'confidence': result['confidence'],
                        'risk_level': risk_level
                    })
                
                return Response({'predictions': results})
                
            except Exception as e:
                logger.error(f"Error making bulk predictions: {str(e)}")
                return Response(
                    {'error': 'An error occurred while making predictions.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _get_risk_level(self, probability):
        """Determine risk level based on probability"""
        if probability < 0.3:
            return 'Low'
        elif probability < 0.7:
            return 'Medium'
        else:
            return 'High'

class MLModelViewSet(viewsets.ModelViewSet):
    queryset = MLModel.objects.all()
    serializer_class = MLModelSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def train(self, request):
        """Train a new ML model"""
        serializer = ModelTrainingSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                model_name = serializer.validated_data['model_name']
                use_existing_data = serializer.validated_data['use_existing_data']
                
                if use_existing_data:
                    # Use existing employee data
                    employees = Employee.objects.all()
                    if employees.count() < 100:
                        return Response(
                            {'error': 'Insufficient data for training. Need at least 100 employee records.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # Prepare data
                    employee_data = [prepare_employee_data_for_ml(emp) for emp in employees]
                else:
                    # Use sample data (for demonstration)
                    employee_data = self._generate_sample_data()
                
                # Initialize and train the predictor
                predictor = TurnoverPredictor()
                X, y = predictor.prepare_data(employee_data)
                
                results, best_model_name = predictor.train_models(X, y)
                
                # Save the model
                model_path = get_model_save_path(model_name)
                predictor.save_model(model_path)
                
                # Get feature importance
                feature_importance = predictor.get_feature_importance()
                
                # Save model info to database
                # Deactivate other models
                MLModel.objects.filter(is_active=True).update(is_active=False)
                
                # Create new model record
                ml_model = MLModel.objects.create(
                    name=model_name,
                    model_type=best_model_name,
                    model_file_path=model_path,
                    accuracy=results[best_model_name]['accuracy'],
                    f1_score=results[best_model_name]['f1_score'],
                    auc_score=results[best_model_name]['auc_score'],
                    hyperparameters=results[best_model_name]['hyperparameters'],
                    feature_importance=feature_importance,
                    is_active=True,
                    trained_by=request.user
                )
                
                return Response({
                    'message': f'Model trained successfully. Best model: {best_model_name}',
                    'model_id': ml_model.id,
                    'results': {
                        name: {
                            'accuracy': round(info['accuracy'], 4),
                            'f1_score': round(info['f1_score'], 4),
                            'auc_score': round(info['auc_score'], 4)
                        } for name, info in results.items()
                    },
                    'feature_importance': feature_importance
                })
                
            except Exception as e:
                logger.error(f"Error training model: {str(e)}")
                return Response(
                    {'error': f'An error occurred while training the model: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _generate_sample_data(self, n_samples=1000):
        """Generate sample data for model training (for demonstration)"""
        np.random.seed(42)
        
        departments = ['IT', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations']
        salaries = ['low', 'medium', 'high']
        
        sample_data = []
        for i in range(n_samples):
            # Generate correlated features based on the Medium article insights
            satisfaction = np.random.beta(2, 2)  # Bimodal distribution
            time_company = np.random.randint(1, 8)
            monthly_hours = np.random.normal(200, 50)
            monthly_hours = max(120, min(300, monthly_hours))  # Clamp values
            
            # Create correlation between features and turnover
            turnover_prob = (
                (1 - satisfaction) * 0.4 +
                (monthly_hours - 200) / 100 * 0.2 +
                (time_company > 5) * 0.2 +
                np.random.normal(0, 0.1)
            )
            turnover_prob = max(0, min(1, turnover_prob))
            
            left = np.random.random() < turnover_prob
            
            sample_data.append({
                'satisfaction_level': round(satisfaction, 2),
                'last_evaluation': round(np.random.beta(2, 2), 2),
                'number_project': np.random.randint(2, 8),
                'average_monthly_hours': int(monthly_hours),
                'time_spend_company': time_company,
                'work_accident': np.random.random() < 0.15,
                'promotion_last_5years': np.random.random() < 0.2,
                'salary': np.random.choice(salaries),
                'department': np.random.choice(departments),
                'left': left
            })
        
        return sample_data
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a specific model"""
        model = self.get_object()
        
        # Deactivate all other models
        MLModel.objects.filter(is_active=True).update(is_active=False)
        
        # Activate this model
        model.is_active = True
        model.save()
        
        return Response({'message': f'Model {model.name} has been activated.'})
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get the currently active model"""
        active_model = MLModel.objects.filter(is_active=True).first()
        
        if active_model:
            serializer = self.get_serializer(active_model)
            return Response(serializer.data)
        else:
            return Response(
                {'message': 'No active model found.'},
                status=status.HTTP_404_NOT_FOUND
            )
