from django.db import models

from onboarding.models import Trainee
from batches.models import Batch
from teachers.models import Teacher

class Module(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Going On', 'Going On'),
        ('Completed', 'Completed'),
    )

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='modules')

    name = models.CharField(max_length=200)

    theory_hrs = models.PositiveIntegerField()
    practical_hrs = models.PositiveIntegerField()

    ssc_code = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    assessment_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.batch.name} - {self.name}"

class Assessment(models.Model):
    GRADE_CHOICES = (
        ('A+', 'A+'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('Fail', 'Fail'),
    )

    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name='assessments')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='assessments')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='assessments' )

    assessment_name = models.CharField(max_length=200)

    attendance_score = models.PositiveIntegerField(default=0)
    class_performance_score = models.PositiveIntegerField(default=0)
    assignments_score = models.PositiveIntegerField(default=0)
    written_exam_score = models.PositiveIntegerField(default=0)
    viva_score = models.PositiveIntegerField(default=0)

    total_score = models.PositiveIntegerField(default=0)

    grade = models.CharField(max_length=10, choices=GRADE_CHOICES, blank=True, null=True)

    assessment_date = models.DateField()

    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # this auto-computes the total_score value in the backend.Does not wait for frontend input.
        self.total_score = (self.attendance_score + self.class_performance_score + self.assignments_score + 
                            self.written_exam_score + self.viva_score
                        )

        super().save(*args, **kwargs)

    def __str__(self):
        return (f"{self.trainee.name} - {self.assessment_name}")