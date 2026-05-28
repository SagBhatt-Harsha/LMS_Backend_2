from rest_framework import serializers
from .models import Batch
from onboarding.models import Trainee

class BatchSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.name', read_only=True)
    enrolled_count = serializers.SerializerMethodField()

    class Meta:
        model = Batch
        fields = '__all__'
        read_only_fields = ('id', 'name', 'enrolled_count', 'teacher_name')

    def get_enrolled_count(self, obj):
        # Will get from onboarding App.
        return obj.trainees.count()

    def validate(self, attrs):
        start_date = attrs.get('start_date', getattr(self.instance, 'start_date', None))
        end_date = attrs.get('end_date', getattr(self.instance, 'end_date', None))

        start_time = attrs.get('start_time', getattr(self.instance, 'start_time', None))
        end_time = attrs.get('end_time', getattr(self.instance, 'end_time', None))

        capacity = attrs.get('capacity', getattr(self.instance, 'capacity', None))
        teacher = attrs.get('teacher', getattr(self.instance, 'teacher', None))
        domain = attrs.get('domain', getattr(self.instance, 'domain', None))

        if end_date < start_date:
            raise serializers.ValidationError({"end_date": "End date must be after or equal to start date."})

        if end_time <= start_time:
            raise serializers.ValidationError({"end_time": "End time must be after start time."})

        if capacity < 1:
            raise serializers.ValidationError({"capacity": "Capacity must be at least 1."})

        if teacher and teacher.domain != domain:
            raise serializers.ValidationError({"teacher": "Teacher domain must match batch domain."})

        return attrs

class TrainerBatchProgressSerializer(serializers.ModelSerializer):
    """Serializer for GET /api/batches/trainer-progress/ API Endpoint"""
    completion_percentage = serializers.ReadOnlyField()

    total_students = serializers.SerializerMethodField()

    batch_id = serializers.IntegerField(source='id', read_only=True)

    batch_name = serializers.CharField(source='name', read_only=True)

    class Meta:
        model = Batch

        fields = [
            'batch_id',
            'batch_name',
            'completion_percentage',
            'modules_completed',
            'total_modules',
            'total_students'
        ]

    def get_total_students(self, obj):
        return obj.trainees.count()


class BatchModulesCompletedSerializer(serializers.ModelSerializer):
    """Serializer for PUT /api/batches/{id}/modules-completed/ API Endpoint"""
    class Meta:
        model = Batch
        fields = ['modules_completed']

    def validate_modules_completed(self, value):
        batch = self.instance

        if value > batch.total_modules:
            raise serializers.ValidationError("modules_completed cannot exceed total_modules.")

        return value