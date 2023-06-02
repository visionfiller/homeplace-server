from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from homeplaceapi.models import Area
from homeplaceapi.serializers import AreaSerializer


class AreaView(ViewSet):
    """HomePlace Area View"""

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
       
        