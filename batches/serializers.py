from rest_framework import serializers
from .models import Batch

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