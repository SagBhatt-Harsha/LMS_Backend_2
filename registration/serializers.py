from rest_framework import serializers
from .models import Registration

class RegistrationSearchSerializer(serializers.ModelSerializer):
    # for Custom Search API Endpoint: GET /api/registration/search/?mobile= 
    # Search by mobile (for onboarding lookup)
    is_onboarded = serializers.SerializerMethodField()

    class Meta:
        model = Registration
        fields = (
            'id',
            'registration_id',
            'name',
            'mobile',
            'slot',
            'domain',
            'is_onboarded',
        )

    def get_is_onboarded(self, obj):
        return hasattr(obj, 'trainee')


class RegistrationSerializer(serializers.ModelSerializer):
    # Main Serializer
    registered_by = serializers.CharField(source='registered_by.name', read_only=True)

    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = (
            'id',
            'registration_id',
            'registered_date',
            'registered_by',
            'name',
            'mobile',
            'gender',
            'father_name',
            'dob',
            'ward_no',
            'pin',
            'slot',
            'domain',
            'counselled_by_name',
            'counselling_date',
            'education',
        )

    def to_internal_value(self, data):
        if hasattr(data, 'copy'):
            data = data.copy()
        elif isinstance(data, dict):
            data = dict(data)
        if isinstance(data, dict):
            for field in ['family_income', 'personal_income', 'date_of_entry', 'email', 'aadhar_no', 'pan_no', 'landmark']:
                if field in data and data[field] == '':
                    data[field] = None
        return super().to_internal_value(data)