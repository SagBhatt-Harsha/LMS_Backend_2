import os
from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = "Seed default admin users from environment variables"

    def handle(self, *args, **kwargs):
        admins = [
            {
                "email": os.environ.get("DEFAULT_ADMIN_1_EMAIL"),
                "password": os.environ.get("DEFAULT_ADMIN_1_PASSWORD"),
                "first_name": "Admin",
                "last_name": "One",
                "role": "admin"
            },
            {
                "email": os.environ.get("DEFAULT_ADMIN_2_EMAIL"),
                "password": os.environ.get("DEFAULT_ADMIN_2_PASSWORD"),
                "first_name": "Admin",
                "last_name": "Two",
                "role": "admin"
            }
        ]

        for admin in admins:
            if not admin["email"] or not admin["password"]:
                self.stdout.write(
                    self.style.WARNING("Admin ENV variables not set, skipping...")
                )
                continue

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