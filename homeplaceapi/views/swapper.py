from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from homeplaceapi.models import Swapper, Property
from homeplaceapi.serializers import SwapperSerializer


class SwapperView(ViewSet):
    """HomePlace Swapper View"""

    def get_permissions(self):
        if self.request.method == 'GET':
            # AllowAny permission for GET requests
            return [AllowAny()]
        else:
            # IsAuthenticated permission for other methods (POST, PUT, DELETE)
            return [IsAuthenticated()]

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
                swapper.properties.set(owner_properties)

        serializer = SwapperSerializer(swappers, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def my_profile(self, request):
        """Get the current user's properties"""
        try:
            swapper = Swapper.objects.get(user=request.auth.user)
            owner_properties = Property.objects.filter(owner=swapper)
            properties = Property.objects.all()
            for owner_property in owner_properties:
                swapper.has_listing = owner_property in properties
                swapper.properties.set(owner_properties)
            serializer = SwapperSerializer(swapper, many=False)
            return Response(serializer.data)
        except Swapper.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
