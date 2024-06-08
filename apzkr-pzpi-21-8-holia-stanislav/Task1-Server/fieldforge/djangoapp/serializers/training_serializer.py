from djangoapp.serializers.map_serializer import MapsMinesInTrainingSerializer, MapsMinesSerializer
from .user_serializer import UserSerializer
from .task_serializer import TaskSerializer
from .results_serializer import ResultsSerializer
from rest_framework import serializers # type: ignore
from ..models import Training

class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = [ 'description', 'instructor', 'start_time', 'end_time', 'type', 'uuid']
        read_only_fields = ['uuid']

class TrainingDetailSerializer(serializers.ModelSerializer):
    instructor = UserSerializer()
    soldiers = UserSerializer(many=True)
    tasks = TaskSerializer(many=True, source='task_set')
    results = ResultsSerializer()
    map = serializers.StringRelatedField(source='map_set')
    mapsmines = MapsMinesInTrainingSerializer(source='map.mapsmines_set', many=True)

    class Meta:
        model = Training
        fields = ['uuid', 'instructor', 'description', 'start_time', 'end_time', 'type', 'soldiers', 'tasks', 'results', 'map', 'mapsmines']