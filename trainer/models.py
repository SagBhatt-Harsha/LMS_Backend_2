from django.db import models
from onboarding.models import Trainee
from batches.models import Batch
from teachers.models import Teacher

# Create your models here.
class Assessment(models.Model):

    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name='assessments')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='assessments')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='assessments')

    assessment_name = models.CharField(max_length=200)
    score = models.PositiveIntegerField()
    grade = models.CharField(max_length=10, blank=True, null=True)

    assessment_date = models.DateField()
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trainee.name} - {self.assessment_name}"