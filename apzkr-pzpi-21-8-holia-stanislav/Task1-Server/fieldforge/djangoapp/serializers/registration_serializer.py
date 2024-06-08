from rest_framework import serializers # type: ignore
from djangoapp.models import User


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    experience = serializers.CharField(required=False)
    specialization = serializers.CharField(required=False)
    unit = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['uuid','first_name', 'last_name', 'email', 'password', 'token', 'role', 'experience', 'specialization', 'unit']
    def validate(self, data):
        role = data.get('role', None)
        if role == 'INSTRUCTOR':
            if not data.get('experience', None):
                raise serializers.ValidationError({"experience": "This field is required for Instructor role."})
            if not data.get('specialization', None):
                raise serializers.ValidationError({"specialization": "This field is required for Instructor role."})
        elif role == 'SOLDIER':
            if not data.get('unit', None):
                raise serializers.ValidationError({"unit": "This field is required for Soldier role."})
            if not data.get('specialization', None):
                raise serializers.ValidationError({"specialization": "This field is required for Soldier role."})
        return data
    
    def create(self, validated_data):
        role = validated_data.get('role')
        if role == 'INSTRUCTOR':
            experience = validated_data.pop('experience', None)
            specialization = validated_data.pop('specialization', None)
            return User.objects.create_user(experience=experience, specialization=specialization, **validated_data)
        elif role == 'SOLDIER':
            unit = validated_data.pop('unit', None)
            specialization = validated_data.pop('specialization', None)
            return User.objects.create_user(unit=unit, specialization=specialization, **validated_data)
        else:
            return User.objects.create_user(**validated_data)
    