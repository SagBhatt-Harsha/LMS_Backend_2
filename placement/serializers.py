from rest_framework import serializers
from .models import Interview, Retention
from onboarding.models import Trainee

class PlacementCandidateSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(source='id', read_only=True)
    eligibility_status = serializers.SerializerMethodField()

    class Meta:
        model = Trainee

        fields = [
            'student_id',
            'name',
            'domain',
            'eligibility_status',
            'gender'
        ]

    def get_eligibility_status(self, obj):
        if obj.training_completed:
            return "Training Finished. Completed All Modules"

        return "Training Pending"


class InterviewSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='trainee.name', read_only=True)

    class Meta:
        model = Interview
        fields = [
            'id',
            'trainee',
            
            'student_name',
            'company_name',

            'interview_date',
            'status',
            'created_at'
        ]

        read_only_fields = (
            'id',
            'student_name',
            'created_at'
        )


class RetentionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='trainee.name', read_only = True)

    class Meta:
        model = Retention

        fields = [
            'id',
            'trainee',
            
            'student_name',
            'month_number',

            'retention_status',
            'remarks',
            'created_at'
        ]

        read_only_fields = (
            'id',
            'student_id',
            'student_name',
            'created_at'
        )
    
    # VALIDATIONS
    def validate(self, attrs):
        trainee = attrs.get('trainee', getattr(self.instance, 'trainee', None))

        # MUST BE SELECTED IN INTERVIEW
        selected = Interview.objects.filter(trainee=trainee, status='Selected').exists()

        if not selected:
            raise serializers.ValidationError({"trainee":"Retention can only be recorded for selected students."})
        return attrs