from django.db import models
from teachers.models import Teacher

# Create your models here.
class Batch(models.Model):

    SLOT_CHOICES = (
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    )

    DOMAIN_CHOICES = (
        ('Digital Marketing', 'Digital Marketing'),
        ('ITES', 'ITES'),
        ('Sales and Customer Relation', 'Sales and Customer Relation'),
        ('Hospitality and Tourism', 'Hospitality and Tourism'),
        ('Logistics and Warehousing', 'Logistics and Warehousing'),
        ('Industrial Sewing', 'Industrial Sewing'),
    )

    name = models.CharField(max_length=150)

    slot = models.CharField(max_length=20, choices=SLOT_CHOICES)

    domain = models.CharField(max_length=50, choices=DOMAIN_CHOICES)

    start_date = models.DateField()

    end_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    capacity = models.PositiveIntegerField()

    # TRAINER ASSIGNMENT
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='batches')
    # on_delete=models.SET_NULL means if Teacher Deleted, batch remains intact.

    # TRAINING PROGRESS
    total_modules = models.PositiveIntegerField(default=0)

    modules_completed = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.name}:-{self.domain}"
    
    @property
    def completion_percentage(self):

        if self.total_modules == 0:
            return 0

        return round( (self.modules_completed / self.total_modules) * 100, 2)