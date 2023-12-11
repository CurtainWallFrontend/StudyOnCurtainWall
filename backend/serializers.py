from rest_framework import serializers
from backend.models import Image,Building

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
