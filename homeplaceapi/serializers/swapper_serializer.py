from rest_framework import serializers
from homeplaceapi.models import Swapper


class SwapperSerializer(serializers.ModelSerializer):
    """Serializes the swapper model to convert it to useable json"""
    class Meta:
        model = Swapper
        fields = ('id', 'user', 'area', 'full_name', 'has_listing', 'favorites')
        