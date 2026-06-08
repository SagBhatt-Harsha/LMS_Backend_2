# Generated manually
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0006_traineeglobalassessment'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='skills_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='assessment',
            name='theory_score',
            field=models.FloatField(default=0),
        ),
    ]
