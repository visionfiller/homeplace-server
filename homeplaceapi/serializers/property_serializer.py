from rest_framework import serializers
from homeplaceapi.models import Property, Swapper, Rating

class PropertyOwnerSerializer(serializers.ModelSerializer):
    class Meta: 
        model= Swapper
        fields= ['id','full_name']
class PropertyRatingSerializer(serializers.ModelSerializer):
    swapper = PropertyOwnerSerializer()
    class Meta:
        model = Rating
        fields = ('id','swapper', 'property','score', 'review')
        

class PropertySerializer(serializers.ModelSerializer):
    """Serializes the property model to convert it to useable json"""
    owner=PropertyOwnerSerializer()
    ratings = PropertyRatingSerializer(many=True)
    class Meta:
        model = Property
        fields = ('id', 'owner', 'area', 'address', 'image', 'yard', 'pool', 'square_footage', 'user_favorited', 'ratings', 'average_rating','property_type', 'bathrooms', 'bedrooms')
        depth=1
        
        
class CreatePropertySerializer(serializers.ModelSerializer):
    """Serializes the property model to convert it to useable json"""
    class Meta:
        model = Property
        fields = ['id', 'owner', 'area', 'address', 'image', 'yard', 'pool', 'square_footage','property_type', 'bathrooms', 'bedrooms']
        