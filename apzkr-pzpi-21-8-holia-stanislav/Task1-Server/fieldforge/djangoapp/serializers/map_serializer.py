from djangoapp.serializers.mine_serializer import MineSerializer
from rest_framework import serializers # type: ignore
from ..models import Map,MapsMines
from rest_framework_gis.fields import GeometryField # type: ignore


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ['uuid', 'description', 'start_point', 'end_point', 'training']
        read_only_fields = ['uuid', 'training']

      


class MapsMinesSerializer(serializers.ModelSerializer):
    location = GeometryField()
    class Meta:
        model = MapsMines
        fields = ['location', 'mine']


class MapsMinesInTrainingSerializer(serializers.ModelSerializer):
    location = GeometryField()
    mine = MineSerializer()
    class Meta:
        model = MapsMines
        fields = ['location', 'mine']


