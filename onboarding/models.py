from django.db import models
from django.conf import settings
from registration.models import Registration
from batches.models import Batch

# Create your models here.
class Trainee(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name='trainee')

    registered_date = models.DateField(auto_now_add=True)

    batches = models.ManyToManyField(Batch, related_name='trainees', blank=True)
    # batches can be empty because trainee may onboard before batch assignment.

    registration_code = models.CharField(max_length=50)
    roll_number = models.CharField(max_length=50, blank=True, null=True)
    
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=10)

    slot = models.CharField(max_length=20)
    domain = models.CharField(max_length=100)

    education = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # TRAINING STATUS
    training_completed = models.BooleanField(default=False)
    ssc_certificate_received = models.BooleanField(default=False)

    eligible_for_placement = models.BooleanField(default=False)
    placed = models.BooleanField(default=False)

    registered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='onboarded_trainees')

    def __str__(self):
        return self.name