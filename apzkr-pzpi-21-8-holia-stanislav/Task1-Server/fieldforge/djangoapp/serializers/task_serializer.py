from rest_framework import serializers # type: ignore
from ..models import Task, Training

class TaskSerializer(serializers.ModelSerializer):
    training = serializers.PrimaryKeyRelatedField(queryset=Training.objects.all())
    class Meta:
        model = Task
        fields = ['uuid', 'training', 'type', 'description', 'is_completed']
        read_only_fields = ['uuid']

    def validate(self, data):
        training = data['training']
        request = self.context.get('request')
        if request.user.uuid != training.instructor.uuid:
            raise serializers.ValidationError("You are not the instructor of this training.")
        return data