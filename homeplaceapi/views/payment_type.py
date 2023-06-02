from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from homeplaceapi.models import PaymentType, Swapper
from homeplaceapi.serializers import PaymentTypeSerializer


class PaymentTypeView(ViewSet):
    """HomePlace PaymentType View"""

    def retrieve(self, request, pk):
        """Handle GET requests for single PaymentType
        
        Returns:
            Response -- JSON serialized PaymentType
        """
        try:
            swapper = Swapper.objects.get(user=request.auth.user)
            payment_type = PaymentType.objects.get(pk=pk, swapper=swapper)
            serializer = PaymentTypeSerializer(payment_type)
            return Response(serializer.data)
        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all properties

        Returns:
            Response -- JSON serialized list of properties
        """
        swapper = Swapper.objects.get(user=request.auth.user)
        payment_types = PaymentType.objects.filter(swapper=swapper)
        serializer = PaymentTypeSerializer(payment_types, many=True)
        return Response(serializer.data)
       
        