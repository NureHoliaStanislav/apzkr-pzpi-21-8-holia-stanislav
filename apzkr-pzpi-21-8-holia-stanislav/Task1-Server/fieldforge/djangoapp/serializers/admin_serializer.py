from rest_framework import serializers # type: ignore
from djangoapp.models import User


class AdminCreationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['uuid','first_name', 'last_name', 'email', 'password', 'token','is_staff']
        read_only_fields = ['is_staff']
    
    def create(self, validated_data):
        return User.objects.create_admin(**validated_data)
