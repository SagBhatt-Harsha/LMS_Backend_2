from rest_framework import serializers

class DashboardSerializer(serializers.Serializer):
    total_mobilized = serializers.IntegerField(required=False)
    total_counselled = serializers.IntegerField(required=False)
    total_interested = serializers.IntegerField(required=False)
    total_registered = serializers.IntegerField(required=False)
    total_onboarded = serializers.IntegerField(required=False)

    gender_distribution = serializers.DictField(required=False)
    caste_distribution = serializers.DictField(required=False)

    counselling_status_breakdown = serializers.DictField(required=False)
    domain_distribution = serializers.DictField(required=False)

    top_states = serializers.ListField(required=False)
    pipeline_funnel = serializers.DictField(required=False)

    active_batches = serializers.IntegerField(required=False)
    closed_batches = serializers.IntegerField(required=False)

    batch_utilization = serializers.ListField(required=False)

    recent_mobilizations = serializers.ListField(required=False)