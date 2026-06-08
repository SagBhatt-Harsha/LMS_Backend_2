from django.db import models

from onboarding.models import Trainee
from batches.models import Batch
from teachers.models import Teacher

class Module(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    )

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='modules')

    name = models.CharField(max_length=200)

    theory_hrs = models.PositiveIntegerField()
    practical_hrs = models.PositiveIntegerField()
    taught_theory_hrs = models.PositiveIntegerField(default=0)
    taught_practical_hrs = models.PositiveIntegerField(default=0)

    ssc_code = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    attendance_score = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

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

    attendance_score = models.FloatField(default=0)
    class_performance_score = models.FloatField(default=0)
    assignments_score = models.FloatField(default=0)
    written_exam_score = models.FloatField(default=0)
    viva_score = models.FloatField(default=0)

    theory_score = models.FloatField(default=0)
    skills_score = models.FloatField(default=0)

    total_score = models.FloatField(default=0)

    grade = models.CharField(max_length=10, choices=GRADE_CHOICES, blank=True, null=True)

    assessment_date = models.DateField()

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    )

    remarks = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # this auto-computes the total_score value in the backend.Does not wait for frontend input.
        self.total_score = (self.attendance_score + self.class_performance_score + self.assignments_score + 
                            self.written_exam_score + self.viva_score + self.theory_score + self.skills_score
                        )

        super().save(*args, **kwargs)

    def __str__(self):
        return (f"{self.trainee.name} - {self.assessment_name}")

class InternalAssessment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    )

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='internal_assessments')
    name = models.CharField(max_length=200)
    theory_marks = models.PositiveIntegerField(default=0)
    practical_marks = models.PositiveIntegerField(default=0)
    project_marks = models.PositiveIntegerField(default=0)
    viva_marks = models.PositiveIntegerField(default=0)
    weightage_percent = models.PositiveIntegerField(default=0)
    
    assessment_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.batch.name} - {self.name}"

class PerformanceCriteria(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    )

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='performance_criteria')
    criteria_id = models.CharField(max_length=50)
    description = models.TextField()
    
    total_marks = models.FloatField(default=0)
    theory_marks = models.FloatField(default=0)
    skills_marks = models.FloatField(default=0)

    assessment_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.batch.name} - {self.criteria_id}"