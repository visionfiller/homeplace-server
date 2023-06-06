from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from homeplaceapi.models import Swapper, Property
from homeplaceapi.serializers import SwapperSerializer


class SwapperView(ViewSet):
    """HomePlace Swapper View"""

    def retrieve(self, request, pk):
        """Handle GET requests for single property
        
        Returns:
            Response -- JSON serialized property
        """
        try:
            swapper = Swapper.objects.get(pk=pk)
            owner_properties = Property.objects.filter(owner=swapper)
            properties = Property.objects.all()
            for owner_property in owner_properties:
                swapper.has_listing = owner_property in properties
                swapper.properties.set(owner_properties)
            
            serializer = SwapperSerializer(swapper)
            return Response(serializer.data)
        except Swapper.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all properties

        Returns:
            Response -- JSON serialized list of properties
        """
        swappers = Swapper.objects.all()
        for swapper in swappers:
            owner_properties = Property.objects.filter(owner=swapper)
            properties = Property.objects.all()
            for owner_property in owner_properties:
                swapper.has_listing = owner_property in properties

        serializer = SwapperSerializer(swappers, many=True)
        return Response(serializer.data)
       
        