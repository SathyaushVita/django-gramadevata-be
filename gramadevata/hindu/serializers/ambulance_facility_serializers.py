from rest_framework import serializers
from ..models import AmbulanceFacility
from ..utils import image_path_to_binary

class AmbulanceFacilitySerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()


    class Meta:
        model = AmbulanceFacility
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






class AmbulanceFacilitySerializer1(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()


    class Meta:
        model = AmbulanceFacility
        fields = ["_id","name","image_location","map_location","address"]
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