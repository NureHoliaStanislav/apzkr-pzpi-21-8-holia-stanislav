from rest_framework import serializers # type: ignore
from djangoapp.models import Instructor, Soldier, User 

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor  
        fields = ['experience', 'specialization']  # Specifying the fields to include in the serialized representation of the Instructor model

class SoldierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soldier  
        fields = ['unit', 'specialization']  # Specifying the fields to include in the serialized representation of the Soldier model
        
class UserSerializer(serializers.ModelSerializer):
    # Defining a custom field for the password, which is write-only (not included in the serialized representation)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        # Specifying the fields to include in the serialized representation of the User model
        fields = ('uuid','first_name','last_name','email', 'password', 'token', 'role', 'is_staff','is_active')
        # Specifying the read-only fields (not included in the serialized representation)
        read_only_fields = ('uuid','token', 'role', 'is_staff','is_active')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # If the user's role is 'INSTRUCTOR', include the serialized representation of the associated Instructor model
        if instance.role == 'INSTRUCTOR':
            instructor_data = InstructorSerializer(instance.instructor).data
            for key, value in instructor_data.items():
                representation[key] = value
        # If the user's role is 'SOLDIER', include the serialized representation of the associated Soldier model
        elif instance.role == 'SOLDIER':
            soldier_data = SoldierSerializer(instance.soldier).data
            for key, value in soldier_data.items():
                representation[key] = value
        return representation

    def update(self, instance, validated_data):
        # Update the instance with the validated data
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        # If a new password is provided, set it for the instance
        if password is not None:
            instance.set_password(password)

        # Save the instance
        instance.save()

        return instance
    
class PublicUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        # Exclude the 'token' field from the serialized representation
        fields = tuple([field for field in UserSerializer.Meta.fields if field != 'token'])
