from rest_framework import serializers
from .models import MobilizationRecord, Qualification


class QualificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Qualification
        exclude = ['record']
        # record=MobilzationRecord id. No need to explicitly inputted by user.

class MobilizationSerializer(serializers.ModelSerializer):

    qualifications = QualificationSerializer(many=True)

    class Meta:
        model = MobilizationRecord

        fields = '__all__'

        read_only_fields = (
            'id',
            'date',
            'created_by',
            'added_by_name',
        )
    # Need to make Custom create() & update() as Qualifications is Nested within MobilizationRecords. Default create() & update() can't handle that.
    def create(self, validated_data):
        # Handles nested qualification creation.
        qualifications_data = validated_data.pop('qualifications')

        mobilization_record = MobilizationRecord.objects.create(
            **validated_data
        )

        for qualification_data in qualifications_data:

            Qualification.objects.create(
                record=mobilization_record,
                **qualification_data
            )

        return mobilization_record


    def update(self, instance, validated_data):
        # Deletes old qualifications and recreates them.
        qualifications_data = validated_data.pop(
            'qualifications',
            None
        )

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        if qualifications_data is not None:

            instance.qualifications.all().delete()

            for qualification_data in qualifications_data:

                Qualification.objects.create(
                    record=instance,
                    **qualification_data
                )

        return instance