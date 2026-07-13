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
            camel_map = {
                'familyIncome': 'family_income',
                'personalIncome': 'personal_income',
                'dateOfEntry': 'date_of_entry',
                'aadharNo': 'aadhar_no',
                'panNo': 'pan_no',
                'fatherName': 'father_name',
                'wardNo': 'ward_no',
                'counsellingDate': 'counselling_date',
                'counselledByName': 'counselled_by_name',
            }
            for camel, snake in camel_map.items():
                if camel in data and (snake not in data or data[snake] is None or data[snake] == ''):
                    data[snake] = data[camel]

            nullable_fields = [
                'family_income', 'personal_income', 'date_of_entry', 'email',
                'aadhar_no', 'pan_no', 'landmark', 'dob', 'counselling_date',
                'father_name', 'ward_no', 'pin', 'slot', 'domain', 'education'
            ]
            for field in nullable_fields:
                if field in data and (data[field] == '' or data[field] == 'null'):
                    data[field] = None
        return super().to_internal_value(data)