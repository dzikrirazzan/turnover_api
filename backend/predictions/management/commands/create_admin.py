from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Creates a hardcoded admin user and assigns them to the HR/Admin group.'

    def handle(self, *args, **options):
        admin_username = 'admin'
        admin_email = 'admin@example.com'
        admin_password = 'adminpassword' # CHANGE THIS IN PRODUCTION!

        self.stdout.write(self.style.NOTICE('Attempting to create admin user...'))

        try:
            user, created = User.objects.get_or_create(
                username=admin_username,
                defaults={
                    'email': admin_email,
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            if created:
                user.set_password(admin_password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully created new admin user: {admin_username}'))
            else:
                # If user already exists, ensure they are superuser and staff
                if not user.is_staff or not user.is_superuser:
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()
                    self.stdout.write(self.style.WARNING(f'Admin user {admin_username} already exists, ensuring superuser status.'))
                else:
                    self.stdout.write(self.style.NOTICE(f'Admin user {admin_username} already exists and is a superuser.'))

            # Ensure HR/Admin group exists and assign user to it
            hr_admin_group, group_created = Group.objects.get_or_create(name='HR/Admin')
            if group_created:
                self.stdout.write(self.style.NOTICE('Created HR/Admin group.'))
            
            if hr_admin_group not in user.groups.all():
                user.groups.add(hr_admin_group)
                self.stdout.write(self.style.SUCCESS(f'Assigned {admin_username} to HR/Admin group.'))
            else:
                self.stdout.write(self.style.NOTICE(f'{admin_username} is already in HR/Admin group.'))

            self.stdout.write(self.style.SUCCESS('Admin user setup complete.'))

        except IntegrityError:
            self.stdout.write(self.style.WARNING(f'Admin user {admin_username} already exists (IntegrityError).'))
        except Exception as e:
            raise CommandError(f'Error creating admin user: {e}')
