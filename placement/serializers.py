from django.db.models import Avg
from rest_framework import serializers

from .models import Interview, Retention
from onboarding.models import Trainee
from trainer.models import Assessment

class PlacementCandidateSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(source='id', read_only=True)

    assessment_score = serializers.SerializerMethodField()
    attendance_score = serializers.SerializerMethodField()
    eligibility_status = serializers.SerializerMethodField()

    class Meta:
        model = Trainee

        fields = [
            'student_id',
            'name',
            'domain',
            'gender',

            'assessment_score',
            'attendance_score',
            'eligibility_status'
        ]

    def get_assessment_score(self, obj):
        avg_score = (Assessment.objects.filter( trainee=obj ).aggregate( avg=Avg('total_score') )['avg'])
        return round(avg_score, 2) if avg_score else 0

    def get_attendance_score(self, obj):
        avg_attendance = (Assessment.objects.filter( trainee=obj ).aggregate( avg=Avg('attendance_score') )['avg'])
        return round(avg_attendance, 2) if avg_attendance else 0

    def get_eligibility_status(self, obj):
        avg_score = (Assessment.objects.filter(trainee=obj).aggregate(avg=Avg('total_score'))['avg'])
        avg_attendance = (Assessment.objects.filter(trainee=obj).aggregate(avg=Avg('attendance_score'))['avg'])

        if not avg_score or not avg_attendance:
            return "Assessment Pending"

        if obj.training_completed:
            return "Eligible for Placements. Completed All Assessments."
        return "Not Eligible for Placements. Training Not Complete OR All Assessments have not been completed."


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
            'created_at',
    
            'scheduled',
            'appeared',

            'designation_offered',
            'salary_ctc',
            'current_household_income'
        ]

        read_only_fields = (
            'id',
            'student_name',
            'created_at',
            'scheduled',
            'appeared'
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
        
        month_number = attrs.get('month_number', getattr(self.instance, 'month_number', None))
        if month_number not in [1,2,3,4,5,6]:
            raise serializers.ValidationError({ "month_number" : "Month number must be between 1 and 6." })

        # Must be Selected in Interview for Retention to come into the picture
        selected = Interview.objects.filter(trainee=trainee, status='Selected').exists()

        if not selected:
            raise serializers.ValidationError({ "trainee" : "Retention can only be recorded for selected students."})
        return attrs


class RetentionMonthSerializer(serializers.ModelSerializer):
    # Nested Retention Serializer
    class Meta:
        model = Retention
        fields = (
            'month_number',
            'retention_status',
            'remarks'
        )

class RetentionRecordSerializer(serializers.ModelSerializer):
    # Main Retention Record Serializer 
    student_name = serializers.CharField(source='name', read_only=True)
    registration_id = serializers.CharField(source='registration.registration_id',read_only=True)
    # registration is the FK in Trainee model linking it to Registration Model.

    company_name = serializers.SerializerMethodField()
    designation_offered = serializers.SerializerMethodField()
    salary_ctc = serializers.SerializerMethodField()

    retention_records = serializers.SerializerMethodField()

    class Meta:
        model = Trainee
        fields = [
            'id',
            'student_name',
            'registration_id',
            'domain',

            'company_name',
            'designation_offered',
            'salary_ctc',
            'retention_records'
        ]

    def get_selected_interview(self, obj):
        return obj.interviews.filter(status='Selected').order_by('-interview_date').first()

    def get_company_name(self, obj):
        interview = self.get_selected_interview(obj)
        return (interview.company_name if interview else None)

    def get_designation_offered(self, obj):
        interview = self.get_selected_interview(obj)
        return (interview.designation_offered if interview else None)

    def get_salary_ctc(self, obj):
        interview = self.get_selected_interview(obj)
        return (interview.salary_ctc if interview else None)

    def get_retention_records(self, obj):
        records = obj.retentions.order_by('month_number')
        return RetentionMonthSerializer(records, many=True).data
