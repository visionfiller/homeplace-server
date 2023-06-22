from rest_framework import serializers
from homeplaceapi.models import Property, Swapper, Rating
from .area_serializer import AreaSerializer


class PropertyOwnerSerializer(serializers.ModelSerializer):
    class Meta: 
        model= Swapper
        fields= ['id','full_name','contact_email']
class PropertyRatingSerializer(serializers.ModelSerializer):
    swapper = PropertyOwnerSerializer()
    class Meta:
        model = Rating
        fields = ('id','swapper', 'property','score', 'review')
        

class PropertySerializer(serializers.ModelSerializer):
    """Serializes the property model to convert it to useable json"""
    owner=PropertyOwnerSerializer()
    ratings = PropertyRatingSerializer(many=True)
    area = AreaSerializer(many=False)
    class Meta:
        model = Property
        fields = ('id', 'owner', 'area', 'address', 'image', 'yard', 'pool', 'square_footage', 'user_favorited', 'ratings', 'average_rating','property_type', 'bathrooms', 'bedrooms', 'description')
        depth=1
        
        
class CreatePropertySerializer(serializers.ModelSerializer):
    """Serializes the property model to convert it to useable json"""
    class Meta:
        model = Property
        fields = ['id', 'owner', 'area', 'address', 'image', 'yard', 'pool', 'square_footage','property_type', 'bathrooms', 'bedrooms', 'description']
        