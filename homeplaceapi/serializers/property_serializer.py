from rest_framework import serializers
from homeplaceapi.models import Property, Swapper

class PropertyOwnerSerializer(serializers.ModelSerializer):
    class Meta: 
        model= Swapper
        fields= ['id','full_name']
class PropertySerializer(serializers.ModelSerializer):
    """Serializes the property model to convert it to useable json"""
    owner=PropertyOwnerSerializer()
    class Meta:
        model = Property
        fields = ('id', 'owner', 'area', 'address', 'image', 'yard', 'pool', 'square_footage', 'user_favorited', 'ratings')
        
        
class CreatePropertySerializer(serializers.ModelSerializer):
    """Serializes the property model to convert it to useable json"""
    class Meta:
        model = Property
        fields = ['id', 'owner', 'area', 'address', 'image', 'yard', 'pool', 'square_footage']
        