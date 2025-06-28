from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from performance.models import (
    Goal, KeyResult, Feedback, PerformanceReview, OneOnOneMeeting,
    Shoutout, ShoutoutLike, LearningModule, LearningProgress, LearningGoal,
    AnalyticsMetric, DashboardActivity
)
from predictions.models import Employee, Department
import random

class Command(BaseCommand):
    help = 'Seed performance management data to match frontend requirements'

    def handle(self, *args, **options):
        self.stdout.write('Starting to seed performance data...')
        
        # Get existing employees
        employees = list(Employee.objects.all()[:6])  # Use first 6 employees
        departments = list(Department.objects.all())
        
        if not employees:
            self.stdout.write(self.style.ERROR('No employees found. Please run seed_data first.'))
            return
        
        # Clear existing performance data
        self.stdout.write('Clearing existing performance data...')
        Goal.objects.all().delete()
        Feedback.objects.all().delete()
        PerformanceReview.objects.all().delete()
        OneOnOneMeeting.objects.all().delete()
        Shoutout.objects.all().delete()
        LearningModule.objects.all().delete()
        LearningProgress.objects.all().delete()
        LearningGoal.objects.all().delete()
        AnalyticsMetric.objects.all().delete()
        DashboardActivity.objects.all().delete()
        
        # Create Goals & OKRs
        self.stdout.write('Creating goals and OKRs...')
        goals_data = [
            {
                'title': 'Improve Team Collaboration',
                'description': 'Enhance cross-functional team communication and collaboration through better tools and processes.',
                'priority': 'high',
                'status': 'in_progress',
                'progress_percentage': 85,
                'due_date': datetime(2024, 12, 31).date(),
                'key_results': [
                    {'title': 'Implement new project management tool', 'is_completed': True},
                    {'title': 'Conduct team collaboration workshops', 'is_completed': True},
                    {'title': 'Establish weekly cross-team sync meetings', 'is_completed': False},
                ]
            },
            {
                'title': 'Increase Customer Satisfaction',
                'description': 'Improve customer satisfaction scores through enhanced service delivery and support processes.',
                'priority': 'high',
                'status': 'in_progress',
                'progress_percentage': 70,
                'due_date': datetime(2024, 11, 30).date(),
                'key_results': [
                    {'title': 'Reduce average response time to under 2 hours', 'is_completed': True},
                    {'title': 'Achieve 95% customer satisfaction rating', 'is_completed': False},
                    {'title': 'Launch customer feedback portal', 'is_completed': True},
                ]
            },
            {
                'title': 'Digital Transformation Initiative',
                'description': 'Lead the company\'s digital transformation by modernizing key systems and processes.',
                'priority': 'medium',
                'status': 'in_progress',
                'progress_percentage': 45,
                'due_date': datetime(2025, 3, 31).date(),
                'key_results': [
                    {'title': 'Migrate legacy systems to cloud', 'is_completed': False},
                    {'title': 'Train staff on new digital tools', 'is_completed': True},
                    {'title': 'Implement automated workflows', 'is_completed': False},
                ]
            },
            {
                'title': 'Talent Development Program',
                'description': 'Create a comprehensive talent development program to enhance employee skills and career growth.',
                'priority': 'medium',
                'status': 'completed',
                'progress_percentage': 100,
                'due_date': datetime(2024, 10, 31).date(),
                'key_results': [
                    {'title': 'Design learning curriculum', 'is_completed': True},
                    {'title': 'Launch mentorship program', 'is_completed': True},
                    {'title': 'Establish career progression framework', 'is_completed': True},
                ]
            },
            {
                'title': 'Revenue Growth Strategy',
                'description': 'Develop and execute strategies to increase revenue by 25% through new market opportunities.',
                'priority': 'high',
                'status': 'in_progress',
                'progress_percentage': 60,
                'due_date': datetime(2024, 12, 31).date(),
                'key_results': [
                    {'title': 'Identify three new market segments', 'is_completed': True},
                    {'title': 'Launch two new product lines', 'is_completed': False},
                    {'title': 'Establish partnerships with key distributors', 'is_completed': True},
                ]
            }
        ]
        
        for i, goal_data in enumerate(goals_data):
            key_results = goal_data.pop('key_results')
            goal = Goal.objects.create(
                owner=employees[i % len(employees)],
                **goal_data
            )
            
            for j, kr_data in enumerate(key_results):
                KeyResult.objects.create(
                    goal=goal,
                    order=j,
                    **kr_data
                )
        
        # Create Feedback
        self.stdout.write('Creating feedback entries...')
        feedback_data = [
            {
                'from_employee': employees[1],  # Dzikri
                'to_employee': employees[2],    # Tasya
                'feedback_type': 'peer',
                'project': 'Q4 Product Launch',
                'content': 'Great collaboration on the user interface design. Your attention to detail really made a difference.',
                'rating': 5,
                'is_helpful': True
            },
            {
                'from_employee': employees[0],  # Bravely
                'to_employee': employees[2],    # Tasya
                'feedback_type': 'manager',
                'project': 'Team Leadership',
                'content': 'Excellent job mentoring new team members. Your leadership skills have grown significantly.',
                'rating': 5,
                'is_helpful': True
            }
        ]
        
        for feedback in feedback_data:
            Feedback.objects.create(**feedback)
        
        # Create Performance Reviews
        self.stdout.write('Creating performance reviews...')
        current_year = timezone.now().year
        for emp in employees:
            PerformanceReview.objects.create(
                employee=emp,
                reviewer=employees[0],  # Bravely as manager
                review_period_start=datetime(current_year, 1, 1).date(),
                review_period_end=datetime(current_year, 12, 31).date(),
                status='manager_review',
                overall_rating=round(random.uniform(3.5, 5.0), 1),
                self_assessment_progress=85,
                peer_reviews_received=3,
                peer_reviews_target=5,
                manager_review_completed=False,
                calibration_completed=False
            )
        
        # Create 1-on-1 Meetings
        self.stdout.write('Creating 1-on-1 meetings...')
        meetings_data = [
            {
                'employee': employees[2],  # Tasya
                'manager': employees[0],   # Bravely
                'meeting_date': timezone.now() + timedelta(days=2),
                'topic': 'Career development',
                'agenda': 'Discuss promotion timeline and skill development plan',
                'status': 'upcoming',
                'duration_minutes': 45
            },
            {
                'employee': employees[1],  # Dzikri
                'manager': employees[0],   # Bravely
                'meeting_date': timezone.now() - timedelta(days=2),
                'topic': 'Project collaboration',
                'notes': 'Great insights on cross-team communication',
                'status': 'completed',
                'duration_minutes': 45,
                'satisfaction_rating': 5
            }
        ]
        
        for meeting in meetings_data:
            OneOnOneMeeting.objects.create(**meeting)
        
        # Create Shoutouts
        self.stdout.write('Creating shoutouts...')
        shoutouts_data = [
            {
                'from_employee': employees[4],  # Putri
                'to_employee': employees[2],    # Tasya
                'title': '🌟 Amazing work on the client presentation!',
                'message': 'Your research was thorough and the delivery was flawless.',
                'values': ['excellence', 'collaboration'],
                'likes_count': 12,
                'is_public': True
            },
            {
                'from_employee': employees[0],  # Bravely
                'to_team': departments[0] if departments else None,
                'title': '🚀 Thank you for the quick turnaround on the bug fixes',
                'message': 'Your dedication kept our customers happy!',
                'values': ['customer_focus', 'teamwork'],
                'likes_count': 8,
                'is_public': True
            },
            {
                'from_employee': employees[1],  # Dzikri
                'to_employee': employees[3] if len(employees) > 3 else employees[0],
                'title': '🎨 The new design system is incredible!',
                'message': 'It will make our development process so much more efficient.',
                'values': ['innovation', 'excellence'],
                'likes_count': 15,
                'is_public': True
            }
        ]
        
        for shoutout in shoutouts_data:
            Shoutout.objects.create(**shoutout)
        
        # Create Learning Modules
        self.stdout.write('Creating learning modules...')
        learning_modules = [
            {
                'title': 'Effective Remote Leadership',
                'description': 'Learn key strategies for leading distributed teams effectively in the modern workplace...',
                'content_type': 'micro-learning',
                'category': 'leadership',
                'duration_minutes': 5,
                'helpful_count': 8
            },
            {
                'title': 'Data-Driven Decision Making',
                'description': 'How to use analytics and data insights to improve business outcomes and make informed decisions...',
                'content_type': 'article',
                'category': 'technical',
                'duration_minutes': 8,
                'helpful_count': 12
            },
            {
                'title': 'Advanced Communication Skills',
                'description': 'Master the art of clear, concise, and impactful communication in professional settings...',
                'content_type': 'micro-learning',
                'category': 'communication',
                'duration_minutes': 7,
                'helpful_count': 15
            },
            {
                'title': 'Project Management Fundamentals',
                'description': 'Essential project management principles and methodologies for successful project delivery...',
                'content_type': 'course',
                'category': 'project_management',
                'duration_minutes': 15,
                'helpful_count': 20
            }
        ]
        
        for module_data in learning_modules:
            LearningModule.objects.create(**module_data)
        
        # Create Learning Progress
        self.stdout.write('Creating learning progress...')
        modules = LearningModule.objects.all()
        for emp in employees:
            # Each employee completes some modules
            completed_modules = random.sample(list(modules), k=random.randint(1, 3))
            for module in completed_modules:
                LearningProgress.objects.create(
                    employee=emp,
                    module=module,
                    is_completed=True,
                    completion_date=timezone.now() - timedelta(days=random.randint(1, 30)),
                    time_spent_minutes=module.duration_minutes + random.randint(-2, 5),
                    rating=random.randint(4, 5),
                    is_helpful=True
                )
        
        # Create Learning Goals
        self.stdout.write('Creating learning goals...')
        week_start = timezone.now().date() - timedelta(days=timezone.now().weekday())
        learning_goals = [
            {
                'title': 'Complete 5 micro-learning modules',
                'target_value': 5,
                'current_value': 4,
                'unit': 'modules'
            },
            {
                'title': 'Spend 30 minutes on skill development',
                'target_value': 30,
                'current_value': 23,
                'unit': 'minutes'
            },
            {
                'title': 'Share feedback on 3 learning items',
                'target_value': 3,
                'current_value': 2,
                'unit': 'items'
            }
        ]
        
        for emp in employees[:3]:  # First 3 employees
            for goal_data in learning_goals:
                LearningGoal.objects.create(
                    employee=emp,
                    week_start=week_start,
                    **goal_data
                )
        
        # Create Dashboard Activities
        self.stdout.write('Creating dashboard activities...')
        activities = [
            {
                'employee': employees[2],  # Tasya
                'activity_type': 'goal_completed',
                'title': 'Completed goal: Improve team collaboration',
                'description': '',
                'related_object_type': 'goal',
                'created_at': timezone.now() - timedelta(hours=2)
            },
            {
                'employee': employees[2],
                'activity_type': 'feedback_received',
                'title': 'Received feedback from Bravely Dirgayuska',
                'description': '',
                'related_object_type': 'feedback',
                'created_at': timezone.now() - timedelta(days=1)
            },
            {
                'employee': employees[2],
                'activity_type': 'learning_started',
                'title': 'Started learning module: Leadership Skills',
                'description': '',
                'related_object_type': 'learning',
                'created_at': timezone.now() - timedelta(days=3)
            },
            {
                'employee': employees[2],
                'activity_type': 'meeting_attended',
                'title': 'Attended 1-on-1 meeting with manager',
                'description': '',
                'related_object_type': 'meeting',
                'created_at': timezone.now() - timedelta(weeks=1)
            }
        ]
        
        for activity in activities:
            DashboardActivity.objects.create(**activity)
        
        # Create Analytics Metrics
        self.stdout.write('Creating analytics metrics...')
        base_date = timezone.now().date()
        
        for i in range(30):  # Last 30 days
            date = base_date - timedelta(days=29-i)
            
            # Team metrics
            AnalyticsMetric.objects.create(
                department=departments[0] if departments else None,
                metric_type='team_engagement',
                value=round(8.0 + (i % 10) * 0.05, 1),
                date=date
            )
            
            # Individual metrics for each employee
            for emp in employees:
                AnalyticsMetric.objects.create(
                    employee=emp,
                    metric_type='performance_score',
                    value=round(6.0 + (emp.id % 4) * 0.8 + random.uniform(-0.2, 0.2), 1),
                    date=date
                )
                
                AnalyticsMetric.objects.create(
                    employee=emp,
                    metric_type='risk_score',
                    value=round(random.uniform(0.1, 0.9), 2),
                    date=date
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created performance data:\n'
                f'- {Goal.objects.count()} goals with {KeyResult.objects.count()} key results\n'
                f'- {Feedback.objects.count()} feedback entries\n'
                f'- {PerformanceReview.objects.count()} performance reviews\n'
                f'- {OneOnOneMeeting.objects.count()} 1-on-1 meetings\n'
                f'- {Shoutout.objects.count()} shoutouts\n'
                f'- {LearningModule.objects.count()} learning modules\n'
                f'- {LearningProgress.objects.count()} learning progress entries\n'
                f'- {LearningGoal.objects.count()} learning goals\n'
                f'- {DashboardActivity.objects.count()} dashboard activities\n'
                f'- {AnalyticsMetric.objects.count()} analytics metrics'
            )
        )
