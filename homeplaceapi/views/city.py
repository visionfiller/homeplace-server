from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from homeplaceapi.models import Area, City
from homeplaceapi.serializers import CitySerializer




class CityView(ViewSet):
    """HomePlace City View"""
    def get_permissions(self):
        if self.request.method == 'GET':
            # AllowAny permission for GET requests
            return [AllowAny()]
        else:
            # IsAuthenticated permission for other methods (POST, PUT, DELETE)
            return [IsAuthenticated()]

    def retrieve(self, request, pk):
        """Handle GET requests for single area
        
        Returns:
            Response -- JSON serialized area
        """
        try:
            city = City.objects.get(pk=pk)
            serializer = CitySerializer(city)
            return Response(serializer.data)
        except City.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all cities

        Returns:
            Response -- JSON serialized list of cities
        """
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Create a new product for the current user's store"""
       

        try:
            new_city = City.objects.create(
                name= request.data['name']
                
            )
            serializer = CitySerializer(new_city)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except City.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        