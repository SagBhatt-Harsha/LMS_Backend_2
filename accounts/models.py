from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('mobilizer', 'Mobilizer'),
        ('counsellor', 'Counsellor'),
        ('teacher', 'Teacher'),
        ('trainer', 'Trainer'),
        ('placement_officer', 'Placement Officer'),
        ('trainee', 'Trainee'),
    )

    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100, blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'role']

    def __str__(self):
        # String Representation.Shows in admin panel.
        return f"{self.first_name or ''} {self.last_name or ''}".strip() + f":{self.role}"

    @property
    def name(self):
        # Virtual Field made using two Inputted Fields.
        return f"{self.first_name or ''} {self.last_name or ''}".strip()