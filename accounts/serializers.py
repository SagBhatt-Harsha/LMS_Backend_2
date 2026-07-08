from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    # Becz name is a Derived Field dynamically created using fname and lname Inputs.

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'created_at']
        read_only_fields = ['id','created_at']

    def get_name(self, obj):
        # Function Name : get_NameofDerivedField.
        return f"{obj.first_name or ''} {obj.last_name or ''}".strip()


class UserCreateUpdateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    last_name = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'role']
        read_only_fields = ['id']

    def create(self, validated_data):
        # for POST api endpoints
        password = validated_data.pop('password')

        user = User(**validated_data)

        user.set_password(password)

        user.save()

        return user


    def update(self, instance, validated_data):
        # for PUT/PATCH api endpoints
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance