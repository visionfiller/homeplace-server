from django.http import HttpResponseServerError
from django.db.models import Count, Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from homeplaceapi.models import Property, Swapper, Area, Reservation, PaymentType, PropertyType, Rating
from homeplaceapi.serializers import PropertySerializer




class PropertyView(ViewSet):
    """HomePlace Property View"""
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
            NOT WORKING BC IT IS NEEDING AN AUTH USER
        """
        try:
            user = request.user if request.user.is_authenticated else None
            property_ = Property.objects.get(pk=pk)
            if user is not None:
                try:
                    swapper = Swapper.objects.get(user=request.auth.user)
                    print(swapper)
                    property_.user_favorited = property_ in swapper.favorites.all()
                except Swapper.DoesNotExist:
                    property_.user_favorited = False
            serializer = PropertySerializer(property_)
            return Response(serializer.data)
        except Property.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all properties

        Returns:
            Response -- JSON serialized list of properties
        """
        user = request.user if request.user.is_authenticated else None
        properties = Property.objects.all()
      
        owner_id = request.query_params.get('owner', None)
        address = request.query_params.get('address', None)
        has_yard = request.query_params.get('has_yard', None)
        has_pool = request.query_params.get('has_pool', None)
        area_id = request.query_params.get('area', None)
        min_sq_feet = request.query_params.get('min_sq_feet', None)
        property_type_id = request.query_params.get('property_type', None)
        min_bathrooms = request.query_params.get('bathrooms', None)
        min_bedrooms = request.query_params.get('bedrooms', None)
        description = request.query_params.get('description', None)

        filters={}
        if owner_id is not None:
            filters['owner']= owner_id
        if address is not None:
            filters['address__icontains'] = address
        if description is not None:
            filters['description__icontains'] = description
        if has_yard is not None:
            filters['yard'] = True
        if has_pool is not None:
            filters['pool'] = True
        if min_sq_feet is not None:
           filters['square_footage__gte'] =min_sq_feet
        if min_bathrooms is not None:
           filters['bathrooms__gte'] =min_bathrooms
        if min_bedrooms is not None:
           filters['bedrooms__gte'] =min_bedrooms
        if area_id is not None:
            filters['area']=area_id
        if property_type_id is not None:
            filters['property_type']=property_type_id
        if user is not None:
            for property_ in properties:
                try:
                    swapper = Swapper.objects.get(user=user)
                   
                    property_.user_favorited = property_ in swapper.favorites.all()
                except Swapper.DoesNotExist:
                    property_.user_favorited = False
        try: 
            properties = Property.objects.filter(Q(**filters))
            serializer = PropertySerializer(properties, many=True)
            return Response(serializer.data)
        except Property.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=False, url_path="my_property")
    def my_property(self, request):
        """Get the current user's properties"""
        try:
            swapper = Swapper.objects.get(user=request.auth.user)
            properties = Property.objects.get(owner=swapper)
            serializer = PropertySerializer(properties, many=False)
            return Response(serializer.data)
        except Swapper.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
       
        
       

    def create(self, request):
        """Create a new product for the current user's store"""
        owner = Swapper.objects.get(user=request.auth.user)
        area = Area.objects.get(pk=request.data['area'])
        property_type = PropertyType.objects.get(pk=request.data['property_type'])

        try:
            new_property = Property.objects.create(
                owner = owner,
                area= area,
                property_type = property_type,
                address = request.data['address'],
                image=request.data['image'],
                description= request.data['description'],
                bedrooms = request.data['bedrooms'],
                bathrooms= request.data['bathrooms'],
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
                property_type = PropertyType.objects.get(pk=request.data['property_type'])
                property_ = Property.objects.get(pk=pk, owner = owner)
                property_.owner= owner
                property_.area= area
                property_.property_type = property_type
                property_.bedrooms = request.data['bedrooms']
                property_.bathrooms= request.data['bathrooms']
                property_.description= request.data['description']
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
            property_ = Property.objects.get(pk=pk)
            
            # Check if the owner of the property matches the authorized user
            if property_.owner != owner:
                raise PermissionDenied()
            
            property_.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        except Property.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except PermissionDenied:
            return Response({'message': 'You are not authorized to delete this property.'}, status=status.HTTP_403_FORBIDDEN)
    @action(methods=['post'], detail=True)    
    def favorite(self, request, pk):
        property_ = Property.objects.get(pk=pk)
        swapper = Swapper.objects.get(user=request.auth.user)
        swapper.favorites.add(property_)
        return Response({'message': 'Favorited Added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def unfavorite(self, request, pk):
        """Post request for a user to sign up for an event"""
        property_ = Property.objects.get(pk=pk)
        swapper = Swapper.objects.get(user=request.auth.user)
        swapper.favorites.remove(property_)
        return Response({'message': 'Unfavorited'}, status=status.HTTP_204_NO_CONTENT) 

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
    @action(methods=['delete'], detail=True)    
    def cancel_reservation(self, request, pk):
        """cancel a reservation"""
        property_ = Property.objects.get(pk=pk)
        swapper = Swapper.objects.get(user=request.auth.user)
        reservation = Reservation.objects.filter(property=property_, swapper=swapper).first()
    
        if not reservation:
            return Response({'message': 'Reservation not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if reservation.swapper != swapper:
            raise PermissionDenied()
        
        reservation.delete()
        return Response({'message': 'Reservation cancelled.'}, status=status.HTTP_204_NO_CONTENT)
    @action(methods=['post'], detail=True)
    def rate_property(self, request, pk):
        """Rate a property"""
        property_ = Property.objects.get(pk=pk)
        swapper = Swapper.objects.get(user=request.auth.user)

        try:
            rating = Rating.objects.get(
                swapper=swapper, property=property_)
            rating.score = request.data['score']
            rating.review = request.data['review']
            rating.save()
        except Rating.DoesNotExist:
            rating = Rating.objects.create(
                swapper = swapper,
                property=property_,
                score=request.data['score'],
                review=request.data['review']
            )

        return Response({'message': 'Rating added'}, status=status.HTTP_201_CREATED)