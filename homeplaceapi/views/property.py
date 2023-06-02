from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework import serializers, status
from homeplaceapi.models import Property, Swapper, Area
from homeplaceapi.serializers import PropertySerializer


class PropertyView(ViewSet):
    """HomePlace Property View"""

    def retrieve(self, request, pk):
        """Handle GET requests for single property
        
        Returns:
            Response -- JSON serialized property
        """
        try:
            property_ = Property.objects.get(pk=pk)
            try:
                swapper = Swapper.objects.get(user=request.auth.user)
                property_.user_favorited =  property_ in swapper.favorites.all()
            except Swapper.DoesNotExist:
                property_ = Property.objects.get(pk=pk)
            serializer = PropertySerializer(property_)
            return Response(serializer.data)
        except Property.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all properties

        Returns:
            Response -- JSON serialized list of properties
        """
        properties = Property.objects.all()
        owner_id = request.query_params.get('owner', None)
        has_yard = request.query_params.get('has_yard', None)
        has_pool = request.query_params.get('has_pool', None)
        min_sq_feet = request.query_params.get('min_sq_feet', None)
        if owner_id is not None:
            properties = properties.filter(owner=owner_id)
        if has_yard is not None:
            properties = properties.filter(yard=True)
        if has_pool is not None:
            properties = properties.filter(pool=True)
        if min_sq_feet is not None:
            properties = properties.filter(square_footage__gte=min_sq_feet)
        for property_ in properties:
            try:
                swapper = Swapper.objects.get(user=request.auth.user)
                property_.user_favorited =  property_ in swapper.favorites.all()
            except Swapper.DoesNotExist:
                properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)
    @action(methods=['GET'], detail=False, url_path="my_properties")
    def my_properties(self, request):
        """Get the current user's properties"""
        try:
            swapper = Swapper.objects.get(user=request.auth.user)
            properties = Property.objects.filter(owner=swapper)
            serializer = PropertySerializer(properties, many=True)
            return Response(serializer.data)
        except Swapper.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
       
        
       

    def create(self, request):
        """Create a new product for the current user's store"""
        owner = Swapper.objects.get(user=request.auth.user)
        area = Area.objects.get(pk=request.data['area'])

        try:
            new_property = Property.objects.create(
                owner = owner,
                area= area,
                address = request.data['address'],
                image=request.data['image'],
                yard=request.data['yard'],
                square_footage= request.data['square_footage'],
                pool=request.data['pool'],
            )
            serializer = PropertySerializer(new_property)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

#     def update(self, request, pk):
#             """Handle PUT requests for a game

#             Returns:
#                 Response -- Empty body with 204 status code
#             """
#             varietal_region = VarietalRegion.objects.get(pk=pk)
#             acidity = Acidity.objects.get(pk=request.data['acidity'])
#             dryness = Dryness.objects.get(pk=request.data['dryness'])
#             body = Body.objects.get(pk=request.data['body'])
#             varietal_region.acidity = acidity
#             varietal_region.dryness = dryness
#             varietal_region.body = body
#             varietal_region.save()

#             return Response(None, status=status.HTTP_204_NO_CONTENT)
#     def destroy(self, request, pk):
#         """delete varietal region"""
#         varietal_region = VarietalRegion.objects.get(pk=pk)
#         varietal_region.delete()
#         return Response(None, status=status.HTTP_204_NO_CONTENT) 

    @action(methods=['post'], detail=True)    
    def favorite(self, request, pk):
        property_ = Property.objects.get(pk=pk)
        swapper = Swapper.objects.get(user=request.auth.user)
        swapper.favorites.add(property_)
        return Response({'message': 'Favorited Added'}, status=status.HTTP_201_CREATED)
#     @action(methods=['delete'], detail=True)
#     def unfavorite(self, request, pk):
#             """Post request for a user to sign up for an event"""
            
#             customer = Customer.objects.get(user=request.auth.user)
#             varietal_region = VarietalRegion.objects.get(pk=pk)
#             customer.favorites.remove(varietal_region)
#             return Response({'message': 'Unfavorited'}, status=status.HTTP_204_NO_CONTENT)        

#     # @action(methods=['delete'], detail=True)
#     # def unsubscribe(self, request, pk):
#     #     subscription = Subscription.objects.get(author=pk, follower=request.auth.user.id)
#     #     subscription.delete()
#     #     return Response({'message': 'Unsubscribed'}, status=status.HTTP_204_NO_CONTENT) 
# class CreateVarietalRegionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VarietalRegion
#         fields = ['id', 'varietal', 'region', 'body', 'dryness', 'acidity']
# class VarietalRegionSerializer(serializers.ModelSerializer):
#     """JSON serializer for game types
#     """
#     class Meta:
#         model = VarietalRegion
#         fields = ('id', 'varietal', 'region', 'body', 'dryness', 'acidity', 'is_favorite')
#         depth =1