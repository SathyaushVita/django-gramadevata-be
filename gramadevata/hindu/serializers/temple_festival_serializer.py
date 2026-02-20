# serializers.py
from rest_framework import serializers
from ..models import TempleFestival
from django.utils.timesince import timesince
from ..utils import image_path_to_binary

class TempleFestivalSerializer(serializers.ModelSerializer):
    posted_time_ago = serializers.SerializerMethodField()
    image_location = serializers.SerializerMethodField()


    class Meta:
        model = TempleFestival
        fields = "__all__" 
    def get_image_location(self, instance):
        filename = instance.image_location
        
        if isinstance(filename, list):
            image_paths = filename
        elif isinstance(filename, str):
            # Remove square brackets, double quotes, and single quotes, then split by comma
            image_paths = filename.strip('[]').replace('"', '').replace("'", '').split(',')
            image_paths = [path.strip() for path in image_paths]  # Clean up any extra spaces
        else:
            image_paths = []

        return [image_path_to_binary(path) for path in image_paths]

    def get_posted_time_ago(self, obj):
        return f"{timesince(obj.created_at)} ago"
