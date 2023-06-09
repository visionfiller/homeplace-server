from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from homeplaceapi.models import PropertyType, Swapper
from homeplaceapi.serializers import PropertyTypeSerializer


class PropertyTypeView(ViewSet):
    """HomePlace PropertyType View"""

    def retrieve(self, request, pk):
        """Handle GET requests for single PaymentType
        
        Returns:
            Response -- JSON serialized PaymentType
        """
        try:
            
            property_type = PropertyType.objects.get(pk=pk)
            serializer = PropertyTypeSerializer(property_type)
            return Response(serializer.data)
        except PropertyType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all properties

        Returns:
            Response -- JSON serialized list of properties
        """
        property_types = PropertyType.objects.all()
        serializer = PropertyTypeSerializer(property_types, many=True)
        return Response(serializer.data)
       
        