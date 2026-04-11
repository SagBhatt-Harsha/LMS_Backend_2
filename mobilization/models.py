from django.db import models
from django.conf import settings

# Create your models here.

class MobilizationRecord(models.Model):

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )

    CASTE_CHOICES = (
        ('General', 'General'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('OBC', 'OBC'),
    )

    name = models.CharField(max_length=100)

    father_name = models.CharField(max_length=100)

    dob = models.DateField()

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    caste = models.CharField(max_length=10, choices=CASTE_CHOICES)

    mobile = models.CharField(max_length=10, unique=True)

    ward_no = models.CharField(max_length=20)

    pin = models.CharField(max_length=6)

    state = models.CharField(max_length=50)

    date = models.DateField(auto_now_add=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mobilization_records')
    # related_name='mobilization_records' is the best way to define this Relationship: One User can have/create multiple mobilization Records.

    added_by_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}-{self.mobile}"


class Qualification(models.Model):

    record = models.ForeignKey(MobilizationRecord, related_name='qualifications', on_delete=models.CASCADE)

    sl_no = models.PositiveIntegerField()

    exam_name = models.CharField(max_length=100)

    board = models.CharField(max_length=100)

    year_of_passing = models.CharField(max_length=4)

    grade = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.exam_name} - {self.record.name}"