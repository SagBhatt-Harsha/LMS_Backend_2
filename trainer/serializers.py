from rest_framework import serializers

from .models import Assessment


class AssessmentSerializer(serializers.ModelSerializer):

    # student_id = serializers.IntegerField(source='trainee.id',read_only=True)

    student_name = serializers.CharField(source='trainee.name', read_only=True)
    batch_name = serializers.CharField(source='batch.name', read_only=True)
    trainer_name = serializers.CharField(source='teacher.name', read_only=True)

    class Meta:
        model = Assessment

        fields = [
            'id',
            'trainee',
            'student_name',
            'batch',
            'batch_name',
            'trainer_name',
            'assessment_name',
            'score',
            'grade',
            'assessment_date',
            'remarks',
            'created_at'
        ]

        read_only_fields = (
            'id',
            'created_at',
            'student_name',
            'batch_name',
            'trainer_name'
        )

    # DOMAIN VALIDATION
    def validate(self, attrs):
        trainee = attrs.get('trainee', getattr(self.instance, 'trainee', None))
        batch = attrs.get('batch', getattr(self.instance, 'batch', None))
        teacher = attrs.get('teacher', getattr(self.instance, 'teacher', None))

        # TRAINEE vs BATCH DOMAIN
        if trainee and batch:
            if trainee.domain != batch.domain:
                raise serializers.ValidationError({
                    "batch": "Trainee domain and batch domain must match."
                })
        
        # TRAINEE MUST BELONG TO SAME BATCH
        if trainee and batch:
            if trainee.batch != batch:
                raise serializers.ValidationError({
                    "batch":"Trainee is not enrolled in this batch."
                })
        
        # TEACHER ASSIGNED TO BATCH
        if teacher and batch:
            if batch.teacher != teacher:
                raise serializers.ValidationError({
                    "batch":"This teacher is not assigned to this batch."
                })

        return attrs