# Generated manually
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0004_remove_trainee_batch_trainee_batches'),
        ('batches', '0002_batch_modules_completed_batch_total_modules'),
        ('trainer', '0005_module_taught_practical_hrs_module_taught_theory_hrs'),
    ]

    operations = [
        migrations.CreateModel(
            name='TraineeGlobalAssessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_score', models.FloatField(default=0)),
                ('written_exam_score', models.FloatField(default=0)),
                ('viva_score', models.FloatField(default=0)),
                ('grand_total', models.FloatField(default=0)),
                ('grade', models.CharField(blank=True, max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='global_assessments', to='batches.batch')),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='global_assessments', to='onboarding.trainee')),
            ],
            options={
                'unique_together': {('trainee', 'batch')},
            },
        ),
    ]
