from rest_framework import serializers
from .models import ImageUrl


class ImageUrlSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ImageUrl
        fields = ['image_url']
        
    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None
        
        




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