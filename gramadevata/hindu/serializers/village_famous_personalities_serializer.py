# serializers.py
from rest_framework import serializers
from ..models import VillageFamousPersonality
from ..utils import image_path_to_binary

class VillageFamousPersonalitySerializer(serializers.ModelSerializer):
    person_image=serializers.SerializerMethodField()
    def get_person_image(self, instance):
        filename = instance.person_image
        
        # Check if filename is a list or a string
        if isinstance(filename, list):
            # If it's already a list, return it as is
            image_paths = filename
        elif isinstance(filename, str):
            # If it's a string, attempt to parse it as a list-like string
            image_paths = filename.strip('[]').replace('"', '').split(',')
            image_paths = [path.strip() for path in image_paths]  # Clean up any extra spaces
        else:
            # If it's neither a list nor a string, return an empty list
            image_paths = []

        # Apply binary conversion (assuming `image_path_to_binary` is defined)
        return [image_path_to_binary(path) for path in image_paths]

    class Meta:
        model = VillageFamousPersonality
        fields = '__all__'
        extra_kwargs = {'person_image': {'required': False, 'default': list}}
