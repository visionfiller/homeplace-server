from rest_framework import serializers
from homeplaceapi.models import City


class CitySerializer(serializers.ModelSerializer):
    """Serializes the Area model to convert it to useable json"""
    class Meta:
        model = City
        fields = ('id','name')