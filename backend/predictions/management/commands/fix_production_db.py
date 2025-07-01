"""
Management command to fix production database schema issues.
This command will apply migrations and verify the database schema.
"""
from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line
from django.db import connection
import requests
import json


class Command(BaseCommand):
    help = 'Fix production database schema issues for employee registration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-test',
            action='store_true',
            help='Skip testing the registration endpoint',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Starting production database fix...')
        )
        self.stdout.write('=' * 60)

        # Step 1: Check database connection
        self.stdout.write('\n📡 Step 1: Checking database connection...')
        if not self._check_database_connection():
            return

        # Step 2: Check Employee table schema
        self.stdout.write('\n🔍 Step 2: Checking Employee table schema...')
        schema_ok = self._check_employee_table_schema()

        # Step 3: Apply migrations if needed
        if not schema_ok:
            self.stdout.write('\n🔧 Step 3: Applying database migrations...')
            try:
                execute_from_command_line(['manage.py', 'migrate'])
                self.stdout.write(
                    self.style.SUCCESS('✅ Migrations applied successfully!')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Migration failed: {e}')
                )
                return
        else:
            self.stdout.write('\n✅ Step 3: Database schema looks good, skipping migrations')

        # Step 4: Seed department data
        self.stdout.write('\n🌱 Step 4: Seeding department data...')
        try:
            execute_from_command_line(['manage.py', 'seed_data'])
            self.stdout.write(
                self.style.SUCCESS('✅ Department data seeded successfully!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Seeding failed (might already exist): {e}')
            )

        # Step 5: Verify schema again
        self.stdout.write('\n🔍 Step 5: Verifying Employee table schema...')
        self._check_employee_table_schema()

        # Step 6: Test registration endpoint (if not skipped)
        if not options['skip_test']:
            self.stdout.write('\n🧪 Step 6: Testing registration endpoint...')
            self._test_registration_endpoint()

        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(
            self.style.SUCCESS('🎉 Production database fix completed!')
        )
        self.stdout.write('\n📧 You can now test registration at:')
        self.stdout.write('   https://turnover-api-hd7ze.ondigitalocean.app/api/auth/register/')

    def _check_database_connection(self):
        """Check if we can connect to the database."""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write("✅ Database connection successful")
                return True
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Database connection failed: {e}")
            )
            return False

    def _check_employee_table_schema(self):
        """Check if the Employee table has the password field."""
        try:
            with connection.cursor() as cursor:
                cursor.execute("DESCRIBE predictions_employee")
                columns = [row[0] for row in cursor.fetchall()]
                self.stdout.write(f"📋 Employee table columns: {columns}")

                if 'password' in columns:
                    self.stdout.write("✅ Password field exists in Employee table")
                    return True
                else:
                    self.stdout.write("❌ Password field missing from Employee table")
                    return False
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error checking Employee table: {e}")
            )
            return False

    def _test_registration_endpoint(self):
        """Test the registration endpoint."""
        try:
            url = "https://turnover-api-hd7ze.ondigitalocean.app/api/auth/register/"
            test_data = {
                "email": "test_mgmt_cmd@example.com",
                "first_name": "Management",
                "last_name": "Command",
                "employee_id": "EMP_MGMT_001",
                "phone_number": "08123456789",
                "password": "testpassword123",
                "password_confirm": "testpassword123"
            }

            response = requests.post(url, json=test_data)
            self.stdout.write(f"🧪 Registration test status: {response.status_code}")
            
            if response.status_code == 201:
                self.stdout.write("✅ Registration endpoint working!")
                return True
            else:
                self.stdout.write(
                    self.style.ERROR(f"❌ Registration endpoint still broken: {response.text}")
                )
                return False
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error testing registration: {e}")
            )
            return False
