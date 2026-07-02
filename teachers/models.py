from django.db import models

# Create your models here.

class Teacher(models.Model):

    DOMAIN_CHOICES = (
        ('Digital Marketing', 'Digital Marketing'),
        ('Digital Mitra', 'Digital Mitra'),
        ('Retail Sales Associate', 'Retail Sales Associate'),
        ('Hospitality Management', 'Hospitality Management'),
        ('Logistics and Warehousing', 'Logistics and Warehousing'),
        ('Industrial Sewing', 'Industrial Sewing'),
    )

    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=50, choices=DOMAIN_CHOICES)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        unique_together = ('name', 'domain')

    def __str__(self):
        return f"{self.name} ({self.domain})"