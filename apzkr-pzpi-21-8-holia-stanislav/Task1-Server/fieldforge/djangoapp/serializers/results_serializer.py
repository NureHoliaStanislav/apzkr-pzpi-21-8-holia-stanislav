from rest_framework import serializers # type: ignore
from djangoapp.models import Results

class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = '__all__'
        read_only_fields = ['uuid']