# Generated manually
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0007_assessment_skills_score_assessment_theory_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='traineeglobalassessment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Ongoing', 'Ongoing'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
    ]
