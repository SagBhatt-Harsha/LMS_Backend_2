from rest_framework import serializers
from .models import Trainee


class BatchNestedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class BatchAssignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trainee
        fields = ('id', 'batch') # 'roll_number' is included here later.
        read_only_fields = ('id',)

    def validate_batch(self, value):
        trainee = self.instance

        if value is None:
            return value

        if trainee.slot != value.slot or trainee.domain != value.domain:
            raise serializers.ValidationError("Trainee slot/domain does not match batch.")

        if value != trainee.batch and value.trainees.count() >= value.capacity:
            raise serializers.ValidationError("Batch is already full.")

        return value


class BatchAssignResponseSerializer(serializers.ModelSerializer):
    registration_id = serializers.CharField(source='registration_code')
    batch = serializers.SerializerMethodField()

    class Meta:
        model = Trainee
        fields = ('id', 'name', 'registration_id', 'roll_number', 'batch')
        # Later make roll_number come after batch.

    def get_batch(self, obj):

        if not obj.batch:
            return None

        return {
            "id": obj.batch.id,
            "name": obj.batch.name
        }


class TraineeSerializer(serializers.ModelSerializer):

    batch_name = serializers.CharField(source='batch.name', read_only=True)

    class Meta:
        model = Trainee
        fields = '__all__'
        read_only_fields = ('id', 'registered_date', 'registration_code', 'name', 'gender', 'contact', 'slot', 'domain', 
        'education', 'address', 'registered_by', 'batch_name', 'roll_number')