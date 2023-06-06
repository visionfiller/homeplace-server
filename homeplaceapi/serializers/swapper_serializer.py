from rest_framework import serializers
from homeplaceapi.models import Swapper
from .property_serializer import PropertySerializer


class SwapperSerializer(serializers.ModelSerializer):
    """Serializes the swapper model to convert it to useable json"""
    properties= PropertySerializer(many=True)
    class Meta:
        model = Swapper
        fields = ('id', 'user', 'area', 'full_name', 'has_listing', 'favorites', 'properties')
        