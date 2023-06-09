from rest_framework import serializers
from homeplaceapi.models import PropertyType


class PropertyTypeSerializer(serializers.ModelSerializer):
    """Serializes the propertyType model to convert it to useable json"""
    class Meta:
        model = PropertyType
        fields = ('id', 'name')
        