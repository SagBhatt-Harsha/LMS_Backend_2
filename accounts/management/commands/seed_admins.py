from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = "Seed default admin users"

    def handle(self, *args, **kwargs):
        admins = [
            {
                "email": "admin1@lms.com",
                "password": "Admin1@123",
                "first_name": "Admin",
                "last_name": "One",
                "role": "admin"
            },
            {
                "email": "admin2@lms.com",
                "password": "Admin2@123",
                "first_name": "Admin",
                "last_name": "Two",
                "role": "admin"
            }
        ]

        for admin in admins:
            if not User.objects.filter(email=admin["email"]).exists():
                User.objects.create_superuser(
                    email=admin["email"],
                    password=admin["password"],
                    first_name=admin["first_name"],
                    last_name=admin["last_name"],
                    role=admin["role"]
                )

                self.stdout.write(
                    self.style.SUCCESS(f'Created admin: {admin["email"]}')
                )

            else:
                self.stdout.write(
                    self.style.WARNING(f'Admin already exists: {admin["email"]}')
                )