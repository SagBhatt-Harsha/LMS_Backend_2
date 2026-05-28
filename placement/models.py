from django.db import models

# Create your models here.
from django.db import models

from onboarding.models import Trainee

class Interview(models.Model):
    STATUS_CHOICES = (
        ('Scheduled', 'Scheduled'),
        ('Appeared', 'Appeared'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    )

    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name='interviews')

    company_name = models.CharField(max_length=200)

    interview_date = models.DateField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trainee.name} - {self.company_name}"


class Retention(models.Model):
    STATUS_CHOICES = (
        ('Retained', 'Retained'),
        ('Left', 'Left'),
    )

    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name='retentions')

    month_number = models.PositiveIntegerField()

    retention_status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.trainee.name} "
            f"- Month {self.month_number}"
        )