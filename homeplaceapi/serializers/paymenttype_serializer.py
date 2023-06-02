from rest_framework import serializers
from homeplaceapi.models import PaymentType


class PaymentTypeSerializer(serializers.ModelSerializer):
    """Serializes the paymenttype model to convert it to useable json"""
    class Meta:
        model = PaymentType
        fields = ('id', 'swapper','acct_number','merchant_name')
        