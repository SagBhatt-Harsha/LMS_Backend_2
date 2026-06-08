from rest_framework import serializers
from .models import Module, Assessment, InternalAssessment, PerformanceCriteria, TraineeGlobalAssessment

class ModuleSerializer(serializers.ModelSerializer):
    batch_name = serializers.CharField(source='batch.name', read_only=True)
    teacher_name = serializers.CharField(source='batch.teacher.name', read_only=True)

    class Meta:
        model = Module

        fields = [
            'id',
            'batch',
            'teacher_name',
            'batch_name',
            'name',
            'theory_hrs',
            'practical_hrs',
            'taught_theory_hrs',
            'taught_practical_hrs',
            'ssc_code',
            'attendance_score',
            'remarks',
            'status',
            'assessment_date'
        ]

        read_only_fields = (
            'id',
            'batch_name',
            'teacher_name'
        )

class InternalAssessmentSerializer(serializers.ModelSerializer):
    batch_name = serializers.CharField(source='batch.name', read_only=True)

    class Meta:
        model = InternalAssessment
        fields = '__all__'
        read_only_fields = ('id', 'batch_name')

class PerformanceCriteriaSerializer(serializers.ModelSerializer):
    batch_name = serializers.CharField(source='batch.name', read_only=True)

    class Meta:
        model = PerformanceCriteria
        fields = '__all__'
        read_only_fields = ('id', 'batch_name')

class AssessmentSerializer(serializers.ModelSerializer):
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
            'attendance_score',
            'class_performance_score',
            'assignments_score',
            'written_exam_score',
            'viva_score',
            'theory_score',
            'skills_score',
            'total_score',
            'grade',
            'assessment_date',
            'remarks',
            'status',
            'created_at'
        ]

        read_only_fields = (
            'id',
            'student_name',
            'batch_name',
            'trainer_name',
            'total_score',
            'created_at'
        )


    # VALIDATION
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
            if batch not in trainee.batches.all():
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

class TraineeGlobalAssessmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='trainee.name', read_only=True)
    batch_name = serializers.CharField(source='batch.name', read_only=True)

    class Meta:
        model = TraineeGlobalAssessment
        fields = '__all__'
        read_only_fields = ('id', 'student_name', 'batch_name', 'created_at')