from rest_framework import serializers
from homeplaceapi.models import Reservation
from .swapper_serializer import SwapperSerializer, PropertySerializer

class ReservationSerializer(serializers.ModelSerializer):
    """Serializes the reservation model to convert it to useable json"""
    swapper = SwapperSerializer()
    property= PropertySerializer()
    class Meta:
        model = Reservation
        fields = ('id', 'swapper','property', 'start_date', 'end_date','status', 'completed')
        depth=1
        