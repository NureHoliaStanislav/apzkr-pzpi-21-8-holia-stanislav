from rest_framework import serializers # type: ignore
from ..models import Mine

class MineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mine
        fields = ['uuid', 'type', 'range', 'is_activated', 'is_defused']
        read_only_fields = ['is_activated', 'is_defused']

    def validate(self, data):
        if 'uuid' not in data or not data['uuid']:
            raise serializers.ValidationError("UUID is required")
        return data
      

class MineUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mine
        fields = ['uuid', 'type', 'range', 'is_activated', 'is_defused']
        read_only_fields = ['uuid', 'type', 'range']
      