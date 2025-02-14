from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pharmacy_app.models import Staff

class Command(BaseCommand):
    help = "Adds 5 staff members to the database"

    def handle(self, *args, **kwargs):

        staff_data = [
            {"username": "admin", "password": "1649", "role": 0, "name":"Admin"},
            {"username": "cashier_john", "password": "password123", "role": 1, "name": "John"},
            {"username": "warehouse_mike", "password": "password123", "role": 2, "name": "Mike"},
            {"username": "cashier_sara", "password": "password123", "role": 1, "name": "Sara"},
            {"username": "warehouse_anna", "password": "password123", "role": 2, "name": "Annd"},
        ]

        for data in staff_data:
            user, created = User.objects.get_or_create(username=data["username"])
            if created:
                user.set_password(data["password"])
                user.save()
                staff = Staff.objects.create(user=user, role=data["role"], name=data["name"])
                self.stdout.write(self.style.SUCCESS(f"Created Staff: {staff.user.username} (Role: {staff.role})"))
            else:
                self.stdout.write(self.style.WARNING(f"User {data['username']} already exists!"))
