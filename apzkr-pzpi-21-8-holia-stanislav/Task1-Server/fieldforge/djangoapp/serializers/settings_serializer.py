from rest_framework import serializers # type: ignore
from djangoapp.models import Settings


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = [ 'time_zone', 'language', 'measurement_units']
