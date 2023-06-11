from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from homeplaceapi.models import Area, City
from homeplaceapi.serializers import AreaSerializer




class AreaView(ViewSet):
    """HomePlace Area View"""
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
            area = Area.objects.get(pk=pk)
            serializer = AreaSerializer(area)
            return Response(serializer.data)
        except Area.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all areas

        Returns:
            Response -- JSON serialized list of areas
        """
        areas = Area.objects.all()
        city_id = request.query_params.get('city', None)
        if city_id is not None:
            areas = areas.filter(city=city_id)
        serializer = AreaSerializer(areas, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Create a new product for the current user's store"""
        city = City.objects.get(pk=request.data['city'])

        try:
            new_area = Area.objects.create(
                city=city,
                neighborhood = request.data['neighborhood']
                
            )
            serializer = AreaSerializer(new_area)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except City.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        