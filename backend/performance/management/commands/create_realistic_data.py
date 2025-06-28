from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta, date
import random
from predictions.models import Employee, Department
from performance.models import (
    Goal, KeyResult, Feedback, PerformanceReview, OneOnOneMeeting,
    Shoutout, ShoutoutLike, LearningModule, LearningProgress, LearningGoal,
    AnalyticsMetric, DashboardActivity
)

class Command(BaseCommand):
    help = 'Create realistic performance management data for Smart-EN system'

    def handle(self, *args, **options):
        self.stdout.write('Creating realistic performance management data...')
        
        # Get existing employees
        employees = list(Employee.objects.all()[:20])  # Use first 20 employees
        
        if not employees:
            self.stdout.write(self.style.ERROR('No employees found. Please run seed_data first.'))
            return
        
        # Create Goals & OKRs (matching frontend data)
        self.create_goals(employees)
        
        # Create Feedback system data
        self.create_feedback(employees)
        
        # Create Performance Reviews
        self.create_performance_reviews(employees)
        
        # Create 1-on-1 Meetings
        self.create_oneonone_meetings(employees)
        
        # Create Shoutouts/Recognition
        self.create_shoutouts(employees)
        
        # Create Learning modules and progress
        self.create_learning_data(employees)
        
        # Create Analytics metrics
        self.create_analytics_metrics(employees)
        
        # Create Dashboard activities
        self.create_dashboard_activities(employees)
        
        self.stdout.write(self.style.SUCCESS('Successfully created realistic performance data!'))

    def create_goals(self, employees):
        """Create Goals & OKRs matching frontend"""
        goals_data = [
            {
                'title': 'Improve Team Collaboration',
                'description': 'Enhance cross-functional team communication and collaboration through better tools and processes.',
                'owner': employees[0],
                'priority': 'high',
                'status': 'in_progress',
                'progress_percentage': 85,
                'due_date': date(2024, 12, 31),
                'key_results': [
                    {'title': 'Implement new project management tool', 'is_completed': True},
                    {'title': 'Conduct team collaboration workshops', 'is_completed': True},
                    {'title': 'Establish weekly cross-team sync meetings', 'is_completed': False}
                ]
            },
            {
                'title': 'Increase Customer Satisfaction',
                'description': 'Improve customer satisfaction scores through enhanced service delivery and support processes.',
                'owner': employees[1],
                'priority': 'high', 
                'status': 'in_progress',
                'progress_percentage': 70,
                'due_date': date(2024, 11, 30),
                'key_results': [
                    {'title': 'Reduce average response time to under 2 hours', 'is_completed': True},
                    {'title': 'Achieve 95% customer satisfaction rating', 'is_completed': False},
                    {'title': 'Launch customer feedback portal', 'is_completed': True}
                ]
            },
            {
                'title': 'Digital Transformation Initiative',
                'description': 'Lead the company\'s digital transformation by modernizing key systems and processes.',
                'owner': employees[0],
                'priority': 'medium',
                'status': 'in_progress', 
                'progress_percentage': 45,
                'due_date': date(2025, 3, 31),
                'key_results': [
                    {'title': 'Migrate legacy systems to cloud', 'is_completed': False},
                    {'title': 'Train staff on new digital tools', 'is_completed': True},
                    {'title': 'Implement automated workflows', 'is_completed': False}
                ]
            },
            {
                'title': 'Talent Development Program',
                'description': 'Create a comprehensive talent development program to enhance employee skills and career growth.',
                'owner': employees[3],
                'priority': 'medium',
                'status': 'completed',
                'progress_percentage': 100,
                'due_date': date(2024, 10, 31),
                'key_results': [
                    {'title': 'Design learning curriculum', 'is_completed': True},
                    {'title': 'Launch mentorship program', 'is_completed': True},
                    {'title': 'Establish career progression framework', 'is_completed': True}
                ]
            },
            {
                'title': 'Revenue Growth Strategy',
                'description': 'Develop and execute strategies to increase revenue by 25% through new market opportunities.',
                'owner': employees[2],
                'priority': 'high',
                'status': 'in_progress',
                'progress_percentage': 60,
                'due_date': date(2024, 12, 31),
                'key_results': [
                    {'title': 'Identify three new market segments', 'is_completed': True},
                    {'title': 'Launch two new product lines', 'is_completed': False},
                    {'title': 'Establish partnerships with key distributors', 'is_completed': True}
                ]
            }
        ]
        
        for goal_data in goals_data:
            key_results_data = goal_data.pop('key_results')
            goal = Goal.objects.create(**goal_data)
            
            for i, kr_data in enumerate(key_results_data):
                KeyResult.objects.create(goal=goal, order=i+1, **kr_data)
        
        # Create additional goals for other employees
        for i, emp in enumerate(employees[4:10]):
            Goal.objects.create(
                title=f'Professional Development Goal {i+1}',
                description=f'Focus on skill enhancement and career growth for {emp.name}',
                owner=emp,
                priority=random.choice(['low', 'medium', 'high']),
                status=random.choice(['not_started', 'in_progress', 'completed']),
                progress_percentage=random.randint(0, 100),
                due_date=date(2024, 12, 31)
            )

    def create_feedback(self, employees):
        """Create 360° feedback system data"""
        feedback_samples = [
            {
                'from_employee': employees[1],
                'to_employee': employees[2],
                'feedback_type': 'peer',
                'project': 'Q4 Product Launch',
                'content': 'Great collaboration on the user interface design. Your attention to detail really made a difference.',
                'rating': 5,
                'created_at': timezone.now() - timedelta(days=13)
            },
            {
                'from_employee': employees[0],
                'to_employee': employees[2],
                'feedback_type': 'manager',
                'project': 'Team Leadership',
                'content': 'Excellent job mentoring new team members. Your leadership skills have grown significantly.',
                'rating': 5,
                'created_at': timezone.now() - timedelta(days=16)
            }
        ]
        
        for feedback_data in feedback_samples:
            Feedback.objects.create(**feedback_data)
        
        # Create additional random feedback
        for i in range(20):
            from_emp = random.choice(employees)
            to_emp = random.choice(employees)
            if from_emp != to_emp:
                Feedback.objects.create(
                    from_employee=from_emp,
                    to_employee=to_emp,
                    feedback_type=random.choice(['peer', 'manager', '360']),
                    project=f'Project {random.choice(["Alpha", "Beta", "Gamma", "Delta"])}',
                    content=f'Great work on the recent project. {to_emp.name} showed excellent skills.',
                    rating=random.randint(3, 5),
                    created_at=timezone.now() - timedelta(days=random.randint(1, 90))
                )

    def create_performance_reviews(self, employees):
        """Create performance review system data"""
        for emp in employees[:6]:
            PerformanceReview.objects.create(
                employee=emp,
                reviewer=employees[0],  # Manager
                review_period_start=date(2024, 1, 1),
                review_period_end=date(2024, 12, 31),
                status='manager_review',
                overall_rating=round(3.5 + random.random() * 1.5, 1),
                self_assessment_progress=85,
                peer_reviews_received=random.randint(3, 5),
                peer_reviews_target=5,
                manager_review_completed=True,
                calibration_completed=False,
                comments='Strong performance this year with notable improvements.'
            )

    def create_oneonone_meetings(self, employees):
        """Create 1-on-1 meeting data"""
        meetings_data = [
            {
                'employee': employees[2],
                'manager': employees[0],
                'meeting_date': timezone.now() + timedelta(days=2, hours=10),
                'topic': 'Career development',
                'agenda': 'Discuss promotion timeline and skill development plan',
                'notes': 'Discuss promotion timeline and skill development plan',
                'status': 'upcoming',
                'duration_minutes': 45
            },
            {
                'employee': employees[1],
                'manager': employees[0],
                'meeting_date': timezone.now() - timedelta(days=1, hours=-14),
                'topic': 'Project collaboration',
                'agenda': 'Review project progress and team dynamics',
                'notes': 'Great insights on cross-team communication',
                'status': 'completed',
                'duration_minutes': 45,
                'satisfaction_rating': 5
            }
        ]
        
        for meeting_data in meetings_data:
            OneOnOneMeeting.objects.create(**meeting_data)
        
        # Create additional meetings
        for i in range(22):  # Total 24 meetings as shown in frontend
            OneOnOneMeeting.objects.create(
                employee=random.choice(employees[1:]),
                manager=employees[0],
                meeting_date=timezone.now() - timedelta(days=random.randint(1, 180)),
                topic=random.choice(['Weekly Check-in', 'Project Review', 'Career Discussion', 'Performance Feedback']),
                agenda=f'Regular sync meeting for week {i+1}',
                notes=f'Productive discussion about current projects and goals.',
                status='completed',
                duration_minutes=random.choice([30, 45, 60]),
                satisfaction_rating=random.randint(4, 5)
            )

    def create_shoutouts(self, employees):
        """Create peer recognition/shoutouts system"""
        shoutouts_data = [
            {
                'from_employee': employees[3],
                'to_employee': employees[2],
                'title': 'Amazing work on the client presentation!',
                'message': 'Your research was thorough and the delivery was flawless.',
                'values': ['Excellence', 'Collaboration'],
                'likes_count': 12,
                'created_at': timezone.now() - timedelta(days=1)
            },
            {
                'from_employee': employees[0],
                'to_employee': None,
                'to_team': Department.objects.first(),
                'title': 'Thank you for the quick turnaround on the bug fixes',
                'message': 'Your dedication kept our customers happy!',
                'values': ['Customer Focus', 'Teamwork'],
                'likes_count': 8,
                'created_at': timezone.now() - timedelta(days=2)
            },
            {
                'from_employee': employees[1],
                'to_employee': employees[4],
                'title': 'The new design system is incredible!',
                'message': 'It will make our development process so much more efficient.',
                'values': ['Innovation', 'Excellence'],
                'likes_count': 15,
                'created_at': timezone.now() - timedelta(days=3)
            }
        ]
        
        for shoutout_data in shoutouts_data:
            Shoutout.objects.create(**shoutout_data)
        
        # Create additional shoutouts for statistics (48 given, 32 received)
        for i in range(45):
            from_emp = random.choice(employees)
            to_emp = random.choice(employees) if random.choice([True, False]) else None
            to_team = random.choice(Department.objects.all()) if to_emp is None else None
            
            Shoutout.objects.create(
                from_employee=from_emp,
                to_employee=to_emp,
                to_team=to_team,
                title=f'Great work on {random.choice(["project delivery", "client meeting", "team collaboration"])}!',
                message=f'Excellent contribution to our team success.',
                values=random.sample(['Excellence', 'Collaboration', 'Innovation', 'Customer Focus', 'Teamwork'], 2),
                likes_count=random.randint(1, 20),
                created_at=timezone.now() - timedelta(days=random.randint(1, 30))
            )

    def create_learning_data(self, employees):
        """Create learning modules and progress"""
        learning_modules = [
            {
                'title': 'Effective Remote Leadership',
                'description': 'Learn key strategies for leading distributed teams effectively in the modern workplace...',
                'content_type': 'micro-learning',
                'category': 'leadership',
                'duration_minutes': 5,
                'helpful_count': 0
            },
            {
                'title': 'Data-Driven Decision Making',
                'description': 'How to use analytics and data insights to improve business outcomes and make informed decisions...',
                'content_type': 'article',
                'category': 'technical',
                'duration_minutes': 8,
                'helpful_count': 5
            },
            {
                'title': 'Advanced Communication Skills',
                'description': 'Master the art of clear, concise, and impactful communication in professional settings...',
                'content_type': 'micro-learning',
                'category': 'communication',
                'duration_minutes': 7,
                'helpful_count': 0
            },
            {
                'title': 'Project Management Fundamentals',
                'description': 'Essential project management principles and methodologies for successful project delivery...',
                'content_type': 'course',
                'category': 'project_management',
                'duration_minutes': 15,
                'helpful_count': 8
            }
        ]
        
        modules = []
        for module_data in learning_modules:
            module = LearningModule.objects.create(**module_data)
            modules.append(module)
        
        # Create additional modules for categories
        categories = ['leadership', 'technical', 'communication', 'project_management']
        category_counts = [12, 18, 8, 15]  # From frontend
        
        for category, count in zip(categories, category_counts):
            for i in range(count - 1):  # -1 because we already created one
                LearningModule.objects.create(
                    title=f'{category.title()} Module {i+2}',
                    description=f'Advanced {category} training module',
                    content_type=random.choice(['micro-learning', 'article', 'course', 'video']),
                    category=category,
                    duration_minutes=random.randint(5, 30),
                    helpful_count=random.randint(0, 15)
                )
        
        # Create learning progress for employees
        all_modules = LearningModule.objects.all()
        for emp in employees:
            # Learning goals for current week
            LearningGoal.objects.create(
                employee=emp,
                title='Complete 5 micro-learning modules',
                target_value=5,
                current_value=4,
                unit='modules',
                week_start=timezone.now().date() - timedelta(days=timezone.now().weekday())
            )
            
            LearningGoal.objects.create(
                employee=emp,
                title='Spend 30 minutes on skill development',
                target_value=30,
                current_value=23,
                unit='minutes',
                week_start=timezone.now().date() - timedelta(days=timezone.now().weekday())
            )
            
            LearningGoal.objects.create(
                employee=emp,
                title='Share feedback on 3 learning items',
                target_value=3,
                current_value=2,
                unit='items',
                week_start=timezone.now().date() - timedelta(days=timezone.now().weekday())
            )
            
            # Create learning progress
            completed_modules = random.sample(list(all_modules), random.randint(5, 15))
            for module in completed_modules:
                LearningProgress.objects.create(
                    employee=emp,
                    module=module,
                    is_completed=True,
                    completion_date=timezone.now() - timedelta(days=random.randint(1, 90)),
                    time_spent_minutes=module.duration_minutes + random.randint(-2, 5),
                    rating=random.randint(3, 5),
                    is_helpful=random.choice([True, False]),
                    feedback='Great learning module!' if random.choice([True, False]) else ''
                )

    def create_analytics_metrics(self, employees):
        """Create analytics data for charts and metrics"""
        # Create 30 days of engagement and risk trend data
        for i in range(30):
            date_point = timezone.now().date() - timedelta(days=29-i)
            
            # Team engagement metrics
            AnalyticsMetric.objects.create(
                department=Department.objects.first(),
                metric_type='team_engagement',
                value=8.0 + (i % 10) * 0.1 + random.uniform(-0.2, 0.2),
                date=date_point
            )
            
            # Stress level metrics
            AnalyticsMetric.objects.create(
                department=Department.objects.first(),
                metric_type='stress_level',
                value=3.0 + (i % 8) * 0.2 + random.uniform(-0.1, 0.1),
                date=date_point
            )
        
        # Individual performance metrics for matrix
        performance_data = [
            {'name': 'Bravely Dirgayuska', 'performance': 9.2, 'engagement': 8.8, 'goal_completion': 9.1, 'risk': 'LOW'},
            {'name': 'Dzikri Razzan Athallah', 'performance': 7.5, 'engagement': 6.2, 'goal_completion': 7.8, 'risk': 'MEDIUM'},
            {'name': 'Tasya Salsabila', 'performance': 8.9, 'engagement': 9.1, 'goal_completion': 8.7, 'risk': 'LOW'},
            {'name': 'Annisa', 'performance': 6.8, 'engagement': 5.9, 'goal_completion': 6.5, 'risk': 'HIGH'},
            {'name': 'Putri Aulia', 'performance': 8.1, 'engagement': 8.3, 'goal_completion': 8.0, 'risk': 'LOW'},
            {'name': 'Zenith', 'performance': 7.2, 'engagement': 6.8, 'goal_completion': 7.1, 'risk': 'MEDIUM'}
        ]
        
        for i, data in enumerate(performance_data):
            if i < len(employees):
                emp = employees[i]
                today = timezone.now().date()
                
                AnalyticsMetric.objects.create(
                    employee=emp,
                    metric_type='performance_score',
                    value=data['performance'],
                    date=today
                )
                
                AnalyticsMetric.objects.create(
                    employee=emp,
                    metric_type='team_engagement',
                    value=data['engagement'],
                    date=today
                )
                
                AnalyticsMetric.objects.create(
                    employee=emp,
                    metric_type='goal_completion',
                    value=data['goal_completion'],
                    date=today
                )

    def create_dashboard_activities(self, employees):
        """Create recent activity feed for dashboard"""
        activities = [
            {
                'employee': employees[2],
                'activity_type': 'goal_completed',
                'title': 'Completed goal: Improve team collaboration',
                'description': 'Successfully finished team collaboration improvement initiative',
                'created_at': timezone.now() - timedelta(hours=2)
            },
            {
                'employee': employees[2],
                'activity_type': 'feedback_received',
                'title': 'Received feedback from Bravely Dirgayuska',
                'description': 'New feedback on team leadership project',
                'created_at': timezone.now() - timedelta(days=1)
            },
            {
                'employee': employees[2],
                'activity_type': 'learning_started',
                'title': 'Started learning module: Leadership Skills',
                'description': 'Began advanced leadership training course',
                'created_at': timezone.now() - timedelta(days=3)
            },
            {
                'employee': employees[2],
                'activity_type': 'meeting_attended',
                'title': 'Attended 1-on-1 meeting with manager',
                'description': 'Weekly sync meeting with direct manager',
                'created_at': timezone.now() - timedelta(weeks=1)
            }
        ]
        
        for activity in activities:
            DashboardActivity.objects.create(**activity)
