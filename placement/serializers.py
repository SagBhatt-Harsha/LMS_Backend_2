from django.db.models import Avg
from rest_framework import serializers

from .models import Interview, Retention
from registration.models import Registration
from onboarding.models import Trainee

class PlacementCandidateSerializer(serializers.ModelSerializer):
    registration = serializers.CharField(source='registration_id', read_only=True)
    id = serializers.SerializerMethodField()
    
    assessment_score = serializers.SerializerMethodField()
    attendance_score = serializers.SerializerMethodField()
    eligibility_status = serializers.SerializerMethodField()
    training_completed = serializers.SerializerMethodField()

    class Meta:
        model = Registration
        fields = [
            'id', 
            'registration',
            'mobile',
            'name',
            'domain',
            'gender',
            'training_completed',
            'eligibility_status'
        ]

    def get_id(self, obj):
        try:
            return obj.trainee.id
        except Exception:
            return obj.id

    def get_training_completed(self, obj):
        try:
            return obj.trainee.training_completed
        except Exception:
            return False

    def get_eligibility_status(self, obj):
        try:
            if not hasattr(obj, 'trainee'):
                return "Pending"
                
            trainee = obj.trainee
            all_batches = trainee.batches.all()
            
            if not all_batches.exists():
                return "Pending"
                
            has_ongoing_or_completed = False
            is_eligible = False
            
            for batch in all_batches:
                modules = batch.modules.all()
                if not modules.exists():
                    continue
                    
                batch_has_ongoing = any(m.status in ['Ongoing', 'Completed'] for m in modules)
                if batch_has_ongoing:
                    has_ongoing_or_completed = True
                    
                batch_all_completed = all(m.status == 'Completed' for m in modules)
                
                if batch_all_completed:
                    global_assessment = trainee.global_assessments.filter(batch=batch).first()
                    if global_assessment and (global_assessment.grand_total > 0 or global_assessment.grade):
                        is_eligible = True
                        break
            
            if is_eligible:
                return "Eligible"
            if has_ongoing_or_completed:
                return "In Training"
                
            return "Pending"
        except Exception:
            return "Pending"


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
            'place_of_posting',
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
    place_of_posting = serializers.SerializerMethodField()
    placement_date = serializers.SerializerMethodField()
    batch = serializers.SerializerMethodField()
    assessment_score = serializers.SerializerMethodField()

    def get_batch(self, obj):
        return ", ".join([b.name for b in obj.batches.all()])

    retention_records = serializers.SerializerMethodField()

    class Meta:
        model = Trainee
        fields = [
            'id',
            'student_name',
            'registration_id',
            'domain',
            'batch',
            'assessment_score',

            'company_name',
            'designation_offered',
            'place_of_posting',
            'salary_ctc',
            'placement_date',
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

    def get_place_of_posting(self, obj):
        interview = self.get_selected_interview(obj)
        return (interview.place_of_posting if interview else None)

    def get_placement_date(self, obj):
        interview = self.get_selected_interview(obj)
        return (interview.interview_date if interview else None)

    def get_assessment_score(self, obj):
        avg_score = (Assessment.objects.filter( trainee=obj ).aggregate( avg=Avg('total_score') )['avg'])
        return round(avg_score, 2) if avg_score else 0

    def get_retention_records(self, obj):
        records = obj.retentions.order_by('month_number')
        return RetentionMonthSerializer(records, many=True).data
