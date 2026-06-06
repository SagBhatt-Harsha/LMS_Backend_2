from django.db import models
from django.conf import settings
import django.utils.timezone

from mobilization.models import MobilizationRecord

# Create your models here.

class CounsellingLog(models.Model):

    STATUS_CHOICES = (
        ('Interested', 'Interested'),
        ('Not Interested', 'Not Interested'),
        ('Decision Pending', 'Decision Pending'),
    )

    SLOT_CHOICES = (
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    )

    mobilization_record = models.OneToOneField(MobilizationRecord, on_delete=models.CASCADE, related_name='counselling_log')
    # FK to mob Model

    date = models.DateField(default=django.utils.timezone.now)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    slot = models.CharField(max_length=20, choices=SLOT_CHOICES, blank=True, null=True)
    domain = models.CharField(max_length=100, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    enrolled_flag = models.BooleanField(default=False)
    
    counselled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='counselling_logs')
    # Fk to User Model.

    counselled_by_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.mobilization_record.name} - {self.status}"