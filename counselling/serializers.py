from rest_framework import serializers
from .models import CounsellingLog

class CounsellingSerializer(serializers.ModelSerializer):
    # For GET, POST, PUT, DELETE, PATCH
    name = serializers.CharField(source='mobilization_record.name', read_only=True)
    mobile = serializers.CharField(source='mobilization_record.mobile', read_only=True)
    gender = serializers.CharField(source='mobilization_record.gender', read_only=True)

    class Meta:
        model = CounsellingLog
        fields = '__all__'

        read_only_fields = (
            'id',
            'date',
            'counselled_by',
            'counselled_by_name',
            'name',
            'mobile',
            'gender',
        )

    def validate(self, attrs):
        # Enforces the Condition that if status is'Interested', then slot and domain can't be null.
        status = attrs.get('status')

        slot = attrs.get('slot')

        domain = attrs.get('domain')

        if status == 'Interested':

            if not slot:
                raise serializers.ValidationError(
                    {
                        "slot":
                        "Slot is required when status is Interested."
                    }
                )

            if not domain:
                raise serializers.ValidationError(
                    {
                        "domain":
                        "Domain is required when status is Interested."
                    }
                )

        return attrs


class CounsellingStatusUpdateSerializer(serializers.ModelSerializer):
    # For Custom PATCH API Endpoint: /api/counselling/{id}/status/
    class Meta:
        model = CounsellingLog

        fields = (
            'id',
            'status',
            'slot',
            'domain',
        )

        read_only_fields = ('id',)

    def validate(self, attrs):
        status = attrs.get('status', self.instance.status)
        slot = attrs.get('slot', self.instance.slot)
        domain = attrs.get('domain', self.instance.domain)

        if status == 'Interested':
            if not slot:
                raise serializers.ValidationError(
                    {
                        "slot":
                        "Slot required for Interested."
                    }
                )

            if not domain:
                raise serializers.ValidationError(
                    {
                        "domain":
                        "Domain required for Interested."
                    }
                )

        return attrs