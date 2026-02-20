from rest_framework import serializers
from ..models import District
from ..utils import image_path_to_binary
from ..serializers import StateSeerializer

class DistrictSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    # state = StateSeerializer(read_only=True)

    class Meta:
        model = District
        fields = ["_id","name","state","image_location","desc"]
    def get_image_location(self, instance):
        filename = instance.image_location
        
        if isinstance(filename, list):
            image_paths = filename
        elif isinstance(filename, str):
            image_paths = filename.strip('[]').replace('"', '').split(',')
            image_paths = [path.strip() for path in image_paths]  # Clean up any extra spaces
        else:
            image_paths = []

        return [image_path_to_binary(path) for path in image_paths]
    


class DistrictSearchSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = District
        fields = ["_id","name"]
