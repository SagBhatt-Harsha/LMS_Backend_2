from django.db import models
from django.conf import settings

from counselling.models import CounsellingLog

# Create your models here.

class Registration(models.Model):
    OCCUPATION_CHOICES = (
        ('Fresher', 'Fresher'),
        ('Job', 'Job'),
        ('Studying', 'Studying'),
        ('Housewife', 'Housewife'),
        ('Business', 'Business'),
        ('Others', 'Others'),
    )

    CASTE_CHOICES = (
        ('General', 'General'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('OBC', 'OBC'),
    )

    registration_id = models.CharField(max_length=50, unique=True)

    counselling_log = models.OneToOneField(CounsellingLog, on_delete=models.CASCADE, related_name='registration')
    # FK to CounsellingLog Model: 1 to 1 Rel.

    registered_date = models.DateField(auto_now_add=True)

    registered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='registrations')
    # Fk to User Model

    center = models.CharField(max_length=100)

    # Denormalized Mobilization Fields: Denormalization For Faster Performance.
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    father_name = models.CharField(max_length=100)
    dob = models.DateField()
    ward_no = models.CharField(max_length=20)
    pin = models.CharField(max_length=6)

    # Denormalized Counselling Fields
    slot = models.CharField(max_length=20)
    domain = models.CharField(max_length=100)
    counselled_by_name = models.CharField(max_length=100)
    counselling_date = models.DateField()

    # Registration-specific Fields
    caste = models.CharField(max_length=10, choices=CASTE_CHOICES)
    nationality = models.CharField(max_length=50, default='Indian')
    email = models.EmailField(blank=True, null=True)

    address = models.TextField()
    state = models.CharField(max_length=50)
    landmark = models.CharField(max_length=100, blank=True, null=True)

    aadhar_no = models.CharField(max_length=14, blank=True, null=True)
    pan_no = models.CharField(max_length=10, blank=True, null=True)

    occupation = models.CharField(max_length=20, choices=OCCUPATION_CHOICES)

    family_income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    personal_income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    date_of_entry = models.DateField(blank=True, null=True)

    education = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.registration_id