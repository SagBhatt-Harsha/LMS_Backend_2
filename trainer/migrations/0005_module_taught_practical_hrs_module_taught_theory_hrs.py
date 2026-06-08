# Generated manually
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0004_assessment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='taught_practical_hrs',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='module',
            name='taught_theory_hrs',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
