from django.http import HttpResponseServerError
from django.db.models import Count, Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework import serializers, status
from homeplaceapi.models import Property, Swapper, Area, Reservation, PaymentType
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
        address = request.query_params.get('address', None)
        has_yard = request.query_params.get('has_yard', None)
        has_pool = request.query_params.get('has_pool', None)
        area_id = request.query_params.get('area', None)
        min_sq_feet = request.query_params.get('min_sq_feet', None)
        filters={}
        if owner_id is not None:
            filters['owner']= owner_id
        if address is not None:
            filters['address__icontains'] = address
        if has_yard is not None:
            filters['yard'] = True
        if has_pool is not None:
            filters['pool'] = True
        if min_sq_feet is not None:
           filters['square_footage__gte'] =min_sq_feet
        if area_id is not None:
            filters['area']=area_id
        for property_ in properties:
            try:
                swapper = Swapper.objects.get(user=request.auth.user)
                property_.user_favorited =  property_ in swapper.favorites.all()
            except Swapper.DoesNotExist:
                properties = Property.objects.all()
        try: 
            properties = Property.objects.filter(Q(**filters))
            serializer = PropertySerializer(properties, many=True)
            return Response(serializer.data)
        except Property.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

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

    def update(self, request, pk):
            """
            updates the property object
            """
            try:
                owner = Swapper.objects.get(user=request.auth.user)
                area = Area.objects.get(pk=request.data['area'])
                property_ = Property.objects.get(pk=pk, owner = owner)
                property_.owner= owner
                property_.area= area
                property_.address = request.data['address']
                property_.image=request.data['image']
                property_.yard=request.data['yard']
                property_.square_footage= request.data['square_footage']
                property_.pool=request.data['pool']
                property_.save()

                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Property.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    def destroy(self, request, pk):
        """delete property"""
        owner = Swapper.objects.get(user=request.auth.user)
        try:
            property_ = Property.objects.get(pk=pk, owner=owner)
            property_.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Property.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

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
    @action(methods=['post'], detail=True)    
    def make_reservation(self, request, pk):
        property_ = Property.objects.get(pk=pk)
        swapper = Swapper.objects.get(user=request.auth.user)
        reservation = Reservation.objects.create(
            property=property_,
            swapper=swapper,
       
            start_date= request.data['start_date'],
            end_date= request.data['end_date'],
            status= "Submitted",
            completed= False
        )
        return Response({'message': 'Reservation Submitted'}, status=status.HTTP_201_CREATED)
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