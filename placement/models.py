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
    
    scheduled = models.BooleanField(default=False)
    appeared = models.BooleanField(default=False)

    designation_offered = models.CharField(max_length=200, blank=True, null=True)
    salary_ctc = models.CharField(max_length=100, blank=True, null=True)
    place_of_posting = models.CharField(max_length=200, blank=True, null=True)
    current_household_income = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Syncing status with scheduled and appeared Variables.

        if self.status == 'Scheduled':
            self.scheduled = True
            self.appeared = False

        elif self.status in ['Appeared', 'Selected', 'Rejected']:
            self.scheduled = True
            self.appeared = True

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.trainee.name} - {self.company_name}"


class Retention(models.Model):
    STATUS_CHOICES = (
        ('Retained', 'Retained'),
        ('Dropped', 'Dropped'),
        ('Changed', 'Changed'),
    )

    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name='retentions')

    month_number = models.PositiveIntegerField()
    retention_status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # To prevent Month_number Duplication.
        unique_together = ('trainee', 'month_number')
    
    def __str__(self):
        return (
            f"{self.trainee.name} "
            f"- Month {self.month_number}"
        )