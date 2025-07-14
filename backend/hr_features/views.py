# views.py - Django REST Framework views for HR features

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
import calendar

from .models import Meeting, HRPerformanceReview, MLPredictionHistory
from .serializers import (
    MeetingSerializer, MeetingCreateSerializer,
    PerformanceReviewSerializer, PerformanceReviewCreateSerializer,
    MLPredictionHistorySerializer, AnalyticsSummarySerializer
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin

User = get_user_model()

from .models import Meeting, HRPerformanceReview, MLPredictionHistory
from .serializers import (
    MeetingSerializer, MeetingCreateSerializer,
    PerformanceReviewSerializer, PerformanceReviewCreateSerializer,
    MLPredictionHistorySerializer, AnalyticsSummarySerializer
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin


class MeetingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing 1-on-1 meetings
    
    Admin/HR: Full CRUD access
    Employee: Read-only access to own meetings
    """
    queryset = Meeting.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MeetingCreateSerializer
        return MeetingSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role"""
        user = self.request.user
        
        # Admin can see all meetings
        if user.is_staff or user.is_superuser:
            queryset = Meeting.objects.all()
        else:
            # Employees can only see their own meetings
            queryset = Meeting.objects.filter(employee=user)
        
        # Filter by employee if specified
        employee_id = self.request.query_params.get('employee')
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(
                scheduled_date__date__range=[start_date, end_date]
            )
        
        return queryset.order_by('-scheduled_date')
    
    def create(self, request, *args, **kwargs):
        """Create a new meeting (Admin only)"""
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {"error": "Only admin users can schedule meetings"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            meeting = serializer.save()
            
            return Response({
                "success": True,
                "message": "Meeting scheduled successfully",
                "data": MeetingSerializer(meeting).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "success": False,
            "message": "Validation errors",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """Update meeting (Admin only)"""
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {"error": "Only admin users can update meetings"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            meeting = serializer.save()
            return Response({
                "success": True,
                "message": "Meeting updated successfully",
                "data": MeetingSerializer(meeting).data
            })
        
        return Response({
            "success": False,
            "message": "Validation errors",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming meetings"""
        user = request.user
        now = timezone.now()
        
        if user.is_staff or user.is_superuser:
            meetings = Meeting.objects.filter(
                scheduled_date__gte=now,
                status='scheduled'
            ).order_by('scheduled_date')[:10]
        else:
            meetings = Meeting.objects.filter(
                employee=user,
                scheduled_date__gte=now,
                status='scheduled'
            ).order_by('scheduled_date')[:5]
        
        serializer = MeetingSerializer(meetings, many=True)
        return Response({
            "success": True,
            "message": "Upcoming meetings retrieved successfully",
            "data": serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark meeting as completed and add notes"""
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {"error": "Only admin users can complete meetings"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        meeting = self.get_object()
        notes = request.data.get('notes', '')
        action_items = request.data.get('action_items', '')
        
        meeting.status = 'completed'
        meeting.notes = notes
        meeting.action_items = action_items
        meeting.save()
        
        return Response({
            "success": True,
            "message": "Meeting marked as completed",
            "data": MeetingSerializer(meeting).data
        })


class PerformanceReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing performance reviews
    
    Admin/HR: Full CRUD access
    Employee: Read-only access to own reviews
    """
    queryset = HRPerformanceReview.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PerformanceReviewCreateSerializer
        return PerformanceReviewSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role"""
        user = self.request.user
        
        # Admin can see all reviews
        if user.is_staff or user.is_superuser:
            queryset = HRPerformanceReview.objects.all()
        else:
            # Employees can only see their own reviews
            queryset = HRPerformanceReview.objects.filter(employee=user)
        
        # Filter by employee if specified
        employee_id = self.request.query_params.get('employee')
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
        
        # Filter by review period
        period = self.request.query_params.get('period')
        if period:
            queryset = queryset.filter(review_period=period)
        
        # Filter by year
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(review_date__year=year)
        
        return queryset.order_by('-review_date')
    
    def create(self, request, *args, **kwargs):
        """Create a new performance review (Admin only)"""
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {"error": "Only admin users can create performance reviews"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save()
            
            return Response({
                "success": True,
                "message": "Performance review created successfully",
                "data": PerformanceReviewSerializer(review).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "success": False,
            "message": "Validation errors",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """Update performance review (Admin only)"""
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {"error": "Only admin users can update performance reviews"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            review = serializer.save()
            return Response({
                "success": True,
                "message": "Performance review updated successfully",
                "data": PerformanceReviewSerializer(review).data
            })
        
        return Response({
            "success": False,
            "message": "Validation errors",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Employee acknowledges review"""
        review = self.get_object()
        
        # Only the employee being reviewed can acknowledge
        if request.user != review.employee:
            return Response(
                {"error": "You can only acknowledge your own reviews"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        review.employee_acknowledged = True
        review.acknowledged_date = timezone.now()
        review.save()
        
        return Response({
            "success": True,
            "message": "Performance review acknowledged",
            "data": PerformanceReviewSerializer(review).data
        })
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get performance review summary for employee"""
        user = request.user
        employee_id = request.query_params.get('employee')
        
        if employee_id and (user.is_staff or user.is_superuser):
            target_user = get_object_or_404(User, id=employee_id)
        else:
            target_user = user
        
        reviews = HRPerformanceReview.objects.filter(employee=target_user)
        
        summary = {
            "total_reviews": reviews.count(),
            "average_overall_rating": reviews.aggregate(Avg('overall_rating'))['overall_rating__avg'] or 0,
            "latest_review": None,
            "rating_trend": []
        }
        
        if reviews.exists():
            latest = reviews.first()
            summary["latest_review"] = PerformanceReviewSerializer(latest).data
            
            # Get last 6 reviews for trend
            recent_reviews = reviews[:6]
            summary["rating_trend"] = [
                {
                    "date": review.review_date.strftime("%Y-%m"),
                    "rating": review.overall_rating
                }
                for review in recent_reviews
            ]
        
        return Response({
            "success": True,
            "message": "Performance review summary retrieved",
            "data": summary
        })


class AnalyticsViewSet(viewsets.ViewSet):
    """
    ViewSet for ML prediction analytics and charts
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get complete analytics dashboard data"""
        try:
            # Check user permissions - more lenient check
            user = request.user
            if not user.is_authenticated:
                return Response(
                    {"error": "Authentication required"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Allow admin, manager, or HR users
            has_permission = (
                getattr(user, 'is_staff', False) or 
                getattr(user, 'is_superuser', False) or
                getattr(user, 'is_admin', False) or
                getattr(user, 'is_manager', False) or
                getattr(user, 'is_hr', False)
            )
            
            if not has_permission:
                return Response(
                    {"error": "Admin/Manager access required for analytics"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Get basic stats (with safe defaults)
            try:
                total_predictions = MLPredictionHistory.objects.count()
            except:
                total_predictions = 0
                
            try:
                total_meetings = Meeting.objects.count()
            except:
                total_meetings = 0
                
            try:
                total_reviews = HRPerformanceReview.objects.count()
            except:
                total_reviews = 0
            
            # Simple high risk count with fallback
            try:
                high_risk_employees = MLPredictionHistory.objects.filter(
                    probability__gt=0.7
                ).values('employee').distinct().count()
            except:
                high_risk_employees = 0
            
            # Recent predictions (last 30 days) with fallback
            try:
                thirty_days_ago = timezone.now() - timedelta(days=30)
                recent_predictions = MLPredictionHistory.objects.filter(
                    created_at__gte=thirty_days_ago
                ).count()
            except:
                recent_predictions = 0
            
            # Basic analytics data
            analytics_data = {
                "summary": {
                    "total_predictions": total_predictions,
                    "total_meetings": total_meetings,
                    "total_reviews": total_reviews,
                    "high_risk_employees": high_risk_employees,
                    "recent_predictions": recent_predictions
                },
                "status": "success",
                "message": "Analytics data retrieved successfully"
            }
            
            # Try to add advanced analytics (but don't fail if error)
            try:
                analytics_data["charts"] = self._get_safe_chart_data()
            except Exception as e:
                analytics_data["charts"] = {"error": f"Chart data unavailable: {str(e)}"}
            
            return Response(analytics_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            # Return safe error response
            return Response({
                "error": "Analytics service temporarily unavailable",
                "detail": str(e),
                "status": "error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def charts(self, request):
        """Get chart data for frontend visualization"""
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {"error": "Admin access required for analytics"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        risk_distribution = self._get_risk_distribution()
        department_analysis = self._get_department_analysis()
        trend_analysis = self._get_trend_analysis()
        
        chart_data = self._get_chart_data(risk_distribution, department_analysis, trend_analysis)
        
        return Response({
            "success": True,
            "message": "Chart data retrieved successfully",
            "data": chart_data
        })
    
    def _get_risk_distribution(self):
        """Get risk level distribution"""
        # Get latest prediction for each employee
        latest_predictions = MLPredictionHistory.objects.filter(
            employee__in=MLPredictionHistory.objects.values('employee').distinct()
        ).order_by('employee', '-created_at').distinct('employee')
        
        low_risk = sum(1 for p in latest_predictions if float(p.probability) <= 0.3)
        medium_risk = sum(1 for p in latest_predictions if 0.3 < float(p.probability) <= 0.7)
        high_risk = sum(1 for p in latest_predictions if float(p.probability) > 0.7)
        
        return {
            "low_risk": low_risk,
            "medium_risk": medium_risk,
            "high_risk": high_risk,
            "total_employees": len(latest_predictions)
        }
    
    def _get_department_analysis(self):
        """Get department-wise risk analysis"""
        # This would need to be adjusted based on your user profile model
        # For now, using a placeholder implementation
        departments = ["Engineering", "Marketing", "HR", "Finance", "Sales"]
        
        department_data = []
        for dept in departments:
            # Placeholder implementation - replace with actual department filtering
            predictions = MLPredictionHistory.objects.all()[:10]  # Simplified
            if predictions:
                avg_risk = sum(float(p.probability) for p in predictions) / len(predictions) * 100
                high_risk_count = sum(1 for p in predictions if float(p.probability) > 0.7)
                
                department_data.append({
                    "department": dept,
                    "employee_count": len(predictions),
                    "average_risk": round(avg_risk, 2),
                    "high_risk_count": high_risk_count
                })
        
        return department_data
    
    def _get_trend_analysis(self):
        """Get risk trend over last 6 months"""
        trend_data = []
        
        for i in range(6):
            month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)
            
            month_predictions = MLPredictionHistory.objects.filter(
                created_at__range=[month_start, month_end]
            )
            
            if month_predictions.exists():
                avg_risk = month_predictions.aggregate(Avg('probability'))['probability__avg']
                avg_risk_percent = float(avg_risk or 0) * 100
            else:
                avg_risk_percent = 0
            
            trend_data.append({
                "month": month_start.strftime("%b %Y"),
                "average_risk": round(avg_risk_percent, 2),
                "prediction_count": month_predictions.count()
            })
        
        return list(reversed(trend_data))
    
    def _get_chart_data(self, risk_distribution, department_analysis, trend_analysis):
        """Generate chart.js compatible data"""
        return {
            # Pie chart for risk distribution
            "risk_distribution": {
                "chart_type": "pie",
                "title": "Employee Risk Distribution",
                "data": {
                    "labels": ["Low Risk", "Medium Risk", "High Risk"],
                    "datasets": [{
                        "data": [
                            risk_distribution["low_risk"],
                            risk_distribution["medium_risk"],
                            risk_distribution["high_risk"]
                        ],
                        "backgroundColor": ["#28a745", "#ffc107", "#dc3545"],
                        "borderWidth": 2
                    }]
                }
            },
            
            # Bar chart for department analysis
            "department_analysis": {
                "chart_type": "bar",
                "title": "Risk Analysis by Department",
                "data": {
                    "labels": [dept["department"] for dept in department_analysis],
                    "datasets": [{
                        "label": "Average Risk Score (%)",
                        "data": [dept["average_risk"] for dept in department_analysis],
                        "backgroundColor": "#4F46E5",
                        "borderColor": "#3730A3",
                        "borderWidth": 1
                    }]
                }
            },
            
            # Line chart for trend analysis
            "trend_analysis": {
                "chart_type": "line",
                "title": "Turnover Risk Trend (Last 6 Months)",
                "data": {
                    "labels": [trend["month"] for trend in trend_analysis],
                    "datasets": [{
                        "label": "Average Risk %",
                        "data": [trend["average_risk"] for trend in trend_analysis],
                        "borderColor": "#EF4444",
                        "backgroundColor": "rgba(239, 68, 68, 0.1)",
                        "tension": 0.4,
                        "fill": True
                    }]
                }
            }
        }
    
    def _get_safe_chart_data(self):
        """Get chart data with safe fallbacks"""
        try:
            # Basic chart data that won't cause errors
            chart_data = {
                "meetings_chart": {
                    "chart_type": "bar",
                    "title": "Meetings Overview",
                    "data": {
                        "labels": ["Scheduled", "Completed", "Cancelled"],
                        "datasets": [{
                            "label": "Meetings Count",
                            "data": [
                                Meeting.objects.filter(status='scheduled').count(),
                                Meeting.objects.filter(status='completed').count(),
                                Meeting.objects.filter(status='cancelled').count()
                            ],
                            "backgroundColor": ["#007bff", "#28a745", "#dc3545"]
                        }]
                    }
                },
                "reviews_chart": {
                    "chart_type": "line",
                    "title": "Performance Reviews Trend",
                    "data": {
                        "labels": ["This Month", "Last Month"],
                        "datasets": [{
                            "label": "Reviews Count",
                            "data": [
                                HRPerformanceReview.objects.filter(
                                    created_at__month=timezone.now().month
                                ).count(),
                                HRPerformanceReview.objects.filter(
                                    created_at__month=timezone.now().month - 1
                                ).count() if timezone.now().month > 1 else 0
                            ],
                            "borderColor": "#007bff",
                            "backgroundColor": "rgba(0, 123, 255, 0.1)"
                        }]
                    }
                }
            }
            return chart_data
        except Exception as e:
            return {
                "error": f"Chart data generation failed: {str(e)}",
                "fallback_data": {
                    "message": "Using minimal chart data",
                    "charts_available": False
                }
            }
