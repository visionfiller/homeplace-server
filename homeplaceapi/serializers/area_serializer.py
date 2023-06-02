from rest_framework import serializers
from homeplaceapi.models import Area
from .city_serializer import CitySerializer

class AreaSerializer(serializers.ModelSerializer):
    """Serializes the Area model to convert it to useable json"""
    city = CitySerializer()
    class Meta:
        model = Area
        fields = ('id','neighborhood', 'city')
        
class CreateAreaSerializer(serializers.ModelSerializer):
    """Serializes the Area model to convert it to useable json"""
    class Meta:
        model = Area
        fields = ['id', 'neighborhood', 'city']
        