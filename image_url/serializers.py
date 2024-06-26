from rest_framework import serializers
from .models import ImageUrl


class ImageUrlSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ImageUrl
        fields = ['image_url']
        
        




class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUrl
        fields = ['image_url', 'extension', 'size']

    def update(self, instance, validated_data):
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.extension = validated_data.get('extension', instance.extension)
        instance.size = validated_data.get('size', instance.size)
        instance.save()
        return instance