from django.core.management.base import BaseCommand
from django.db import transaction
from predictions.models import Department, Employee
import os


class Command(BaseCommand):
    help = 'Setup production database with departments and admin user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--admin-email',
            type=str,
            default='admin@company.com',
            help='Admin email address'
        )
        parser.add_argument(
            '--admin-password',
            type=str,
            default='AdminPass123!',
            help='Admin password'
        )

    def handle(self, *args, **options):
        admin_email = options['admin_email']
        admin_password = options['admin_password']
        
        self.stdout.write(
            self.style.SUCCESS('🚀 Setting up production database...')
        )

        with transaction.atomic():
            # Create departments
            departments_data = [
                {
                    'name': 'Human Resources',
                    'description': 'Employee management, recruitment, and HR policies'
                },
                {
                    'name': 'Information Technology',
                    'description': 'Software development, infrastructure, and technical support'
                },
                {
                    'name': 'Finance',
                    'description': 'Financial planning, accounting, and budget management'
                },
                {
                    'name': 'Marketing',
                    'description': 'Brand management, advertising, and market research'
                },
                {
                    'name': 'Sales',
                    'description': 'Customer acquisition, relationship management, and revenue generation'
                },
                {
                    'name': 'Operations',
                    'description': 'Daily operations, process optimization, and logistics'
                },
                {
                    'name': 'Customer Service',
                    'description': 'Customer support, satisfaction, and retention'
                },
                {
                    'name': 'Research & Development',
                    'description': 'Innovation, product development, and research initiatives'
                }
            ]

            created_departments = []
            for dept_data in departments_data:
                department, created = Department.objects.get_or_create(
                    name=dept_data['name'],
                    defaults={'description': dept_data['description']}
                )
                if created:
                    created_departments.append(department.name)
                    self.stdout.write(f"✅ Created department: {department.name}")
                else:
                    self.stdout.write(f"📋 Department already exists: {department.name}")

            # Create admin user
            if not Employee.objects.filter(email=admin_email).exists():
                hr_department = Department.objects.get(name='Human Resources')
                
                admin_user = Employee.objects.create_superuser(
                    email=admin_email,
                    password=admin_password,
                    first_name='System',
                    last_name='Administrator',
                    role='admin',
                    department=hr_department,
                    position='System Administrator',
                    is_staff=True,
                    is_superuser=True
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Created admin user: {admin_email}")
                )
                self.stdout.write(
                    self.style.WARNING(f"🔑 Admin password: {admin_password}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"👤 Admin user already exists: {admin_email}")
                )

            # Create HR manager user
            hr_email = 'hr@company.com'
            if not Employee.objects.filter(email=hr_email).exists():
                hr_department = Department.objects.get(name='Human Resources')
                
                hr_user = Employee.objects.create_user(
                    email=hr_email,
                    password='HRPass123!',
                    first_name='HR',
                    last_name='Manager',
                    role='hr',
                    department=hr_department,
                    position='HR Manager',
                    is_staff=True
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Created HR manager: {hr_email}")
                )
                self.stdout.write(
                    self.style.WARNING(f"🔑 HR password: HRPass123!")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"👤 HR user already exists: {hr_email}")
                )

        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS("🎉 Production setup completed!"))
        self.stdout.write("\n📋 Summary:")
        self.stdout.write(f"   • Departments: {Department.objects.count()}")
        self.stdout.write(f"   • Users: {Employee.objects.count()}")
        self.stdout.write(f"   • Admin email: {admin_email}")
        self.stdout.write(f"   • HR email: hr@company.com")
        self.stdout.write("\n🔐 Security Notice:")
        self.stdout.write("   Please change default passwords after first login!")
        self.stdout.write("="*50)
