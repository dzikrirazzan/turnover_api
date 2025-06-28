from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from predictions.models import Department, Employee, TurnoverPrediction, MLModel
import random

class Command(BaseCommand):
    help = 'Seed the database with admin users and basic groups'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete all existing users before creating new ones',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting Admin User Seeder...'))
        
        # Reset users if requested
        if options['reset']:
            self.stdout.write('🗑️  Deleting all existing users...')
            User.objects.all().delete()
            Group.objects.all().delete()
            self.stdout.write(self.style.WARNING('All users and groups deleted!'))
        
        # Create basic groups for future use
        self.create_basic_groups()
        
        # Create Admin Users only
        self.create_admin_users()
        
        self.display_summary()

    def create_basic_groups(self):
        """Create basic user groups for future use (will be assigned via admin)"""
        self.stdout.write('\n👥 Creating basic user groups...')
        
        # Get content types for our models
        employee_ct = ContentType.objects.get_for_model(Employee)
        prediction_ct = ContentType.objects.get_for_model(TurnoverPrediction)
        model_ct = ContentType.objects.get_for_model(MLModel)
        department_ct = ContentType.objects.get_for_model(Department)
        
        # Super Admins - Full access (for admin users)
        super_admin_group, created = Group.objects.get_or_create(name='Super Admins')
        if created:
            # Give all permissions
            all_permissions = Permission.objects.all()
            super_admin_group.permissions.set(all_permissions)
            self.stdout.write('  ✅ Created Super Admins group with full permissions')
        
        # HR Staff - Employee and prediction management
        hr_group, created = Group.objects.get_or_create(name='HR Staff')
        if created:
            hr_permissions = Permission.objects.filter(
                content_type__in=[employee_ct, prediction_ct, department_ct]
            )
            hr_group.permissions.set(hr_permissions)
            self.stdout.write('  ✅ Created HR Staff group')
        
        # Employees - Limited access (view only for their data)
        employee_group, created = Group.objects.get_or_create(name='Employees')
        if created:
            employee_permissions = Permission.objects.filter(
                content_type__in=[employee_ct, department_ct],
                codename__startswith='view_'
            )
            employee_group.permissions.set(employee_permissions)
            self.stdout.write('  ✅ Created Employees group')

    def create_admin_users(self):
        """Create admin users only"""
        self.stdout.write('\n👑 Creating admin users...')
        
        admin_users_data = [
            {
                'username': 'admin',
                'email': 'admin@company.com',
                'first_name': 'System',
                'last_name': 'Administrator',
                'password': 'admin123',
                'is_superuser': True,
                'is_staff': True,
                'group': 'Super Admins'
            },
            {
                'username': 'hr_admin',
                'email': 'hr.admin@company.com',
                'first_name': 'HR',
                'last_name': 'Administrator',
                'password': 'hradmin123',
                'is_superuser': True,
                'is_staff': True,
                'group': 'Super Admins'
            }
        ]
        
        for user_data in admin_users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_superuser': user_data['is_superuser'],
                    'is_staff': user_data['is_staff'],
                    'is_active': True
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                
                # Add to group
                group = Group.objects.get(name=user_data['group'])
                user.groups.add(group)
                
                self.stdout.write(f'  ✅ Created admin user: {user.username} ({user.email})')
            else:
                self.stdout.write(f'  ⚠️  Admin user {user.username} already exists')

    def display_summary(self):
        """Display summary of created users"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('📊 ADMIN USER SEEDER SUMMARY'))
        self.stdout.write('='*60)
        
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        staff_users = User.objects.filter(is_staff=True).count()
        superusers = User.objects.filter(is_superuser=True).count()
        
        self.stdout.write(f'📈 Total Users: {total_users}')
        self.stdout.write(f'✅ Active Users: {active_users}')
        self.stdout.write(f'👔 Staff Users: {staff_users}')
        self.stdout.write(f'👑 Superusers: {superusers}')
        
        self.stdout.write('\n👥 GROUPS CREATED:')
        for group in Group.objects.all():
            members = group.user_set.count()
            permissions = group.permissions.count()
            self.stdout.write(f'  {group.name}: {members} members, {permissions} permissions')
        
        self.stdout.write('\n🔐 ADMIN CREDENTIALS:')
        self.stdout.write('  Main Admin:')
        self.stdout.write('    Username: admin')
        self.stdout.write('    Password: admin123')
        self.stdout.write('    Email: admin@company.com')
        self.stdout.write('')
        self.stdout.write('  HR Admin:')
        self.stdout.write('    Username: hr_admin')
        self.stdout.write('    Password: hradmin123')
        self.stdout.write('    Email: hr.admin@company.com')
        
        self.stdout.write('\n📝 USER MANAGEMENT:')
        self.stdout.write('  • Other users can register via API or be created from admin panel')
        self.stdout.write('  • HR staff can be created by admin and assigned to "HR Staff" group')
        self.stdout.write('  • Employees can register and will be assigned to "Employees" group')
        self.stdout.write('  • Admin has full control over user management and permissions')
        
        self.stdout.write('\n🎯 NEXT STEPS:')
        self.stdout.write('  1. Login to admin panel: http://127.0.0.1:8000/admin/')
        self.stdout.write('  2. Create HR staff users and assign to HR Staff group')
        self.stdout.write('  3. Configure user registration settings if needed')
        self.stdout.write('  4. Update passwords for production use')
        
        self.stdout.write('\n✅ Admin user seeding completed successfully!')
