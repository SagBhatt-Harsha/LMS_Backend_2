from rest_framework import serializers
from .models import Trainee


class BatchNestedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class BatchAssignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trainee
        fields = ('id', 'batches') # 'roll_number' is included here later.
        read_only_fields = ('id',)

    def validate_batches(self, value):
        trainee = self.instance

        if not value:
            return value

        for batch in value:
            if (batch.domain or '').strip().lower() != (trainee.domain or '').strip().lower():
                raise serializers.ValidationError(f"Batch domain ({batch.domain}) does not match Trainee domain ({trainee.domain}).")
            if batch not in trainee.batches.all() and batch.trainees.count() >= batch.capacity:
                raise serializers.ValidationError(f"Batch {batch.name} is already full.")

        return value


class BatchAssignResponseSerializer(serializers.ModelSerializer):
    registration_id = serializers.CharField(source='registration_code')
    batches = serializers.SerializerMethodField()

    class Meta:
        model = Trainee
        fields = ('id', 'name', 'registration_id', 'roll_number', 'batches')
        # Later make roll_number come after batches.

    def get_batches(self, obj):
        return [{"id": batch.id, "name": batch.name} for batch in obj.batches.all()]


class TraineeSerializer(serializers.ModelSerializer):

    batch_name = serializers.SerializerMethodField()

    class Meta:
        model = Trainee
        fields = '__all__'
        read_only_fields = ('id', 'registered_date', 'registration_code', 'name', 'gender', 'contact', 'slot', 'domain', 
        'education', 'address', 'registered_by', 'batch_name', 'roll_number')

    def get_batch_name(self, obj):
        return ", ".join([b.name for b in obj.batches.all()])