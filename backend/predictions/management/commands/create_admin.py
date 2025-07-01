from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import os

Employee = get_user_model()

class Command(BaseCommand):
    help = 'Creates an admin user and assigns them to the HR/Admin group.'

    def handle(self, *args, **options):
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.getenv('ADMIN_PASSWORD', 'adminpassword')
        admin_name = os.getenv('ADMIN_NAME', 'Admin User')

        self.stdout.write(f"Attempting to create admin user with email: {admin_email}")

        if not Employee.objects.filter(email=admin_email).exists():
            try:
                admin_user = Employee.objects.create_superuser(
                    email=admin_email,
                    password=admin_password,
                    name=admin_name,
                    employee_id='ADMIN001', # Assign a default employee_id for admin
                    is_staff=True,
                    is_superuser=True
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created admin user: {admin_email}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating admin user: {e}'))
                return
        else:
            admin_user = Employee.objects.get(email=admin_email)
            if not admin_user.is_superuser or not admin_user.is_staff:
                admin_user.is_superuser = True
                admin_user.is_staff = True
                admin_user.save()
                self.stdout.write(self.style.SUCCESS(f'Admin user {admin_email} already exists, ensuring superuser status.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Admin user {admin_email} already exists and is a superuser.'))

        # Ensure HR/Admin group exists and assign admin to it
        hr_admin_group, created = Group.objects.get_or_create(name='HR/Admin')
        if created:
            self.stdout.write(self.style.SUCCESS('Created HR/Admin group.'))
        
        if hr_admin_group not in admin_user.groups.all():
            admin_user.groups.add(hr_admin_group)
            self.stdout.write(self.style.SUCCESS('Assigned admin to HR/Admin group.'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin is already in HR/Admin group.'))

        self.stdout.write(self.style.SUCCESS('Admin user setup complete.'))