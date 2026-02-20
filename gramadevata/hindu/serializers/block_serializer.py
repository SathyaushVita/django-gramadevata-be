from ..models import Block
from rest_framework import serializers
from ..utils import image_path_to_binary
from ..serializers import DistrictSerializer
class BlockSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    # district = DistrictSerializer(read_only=True)

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
    
    
    class Meta:
        model = Block
        fields = ["_id","name","image_location","district"]





class BlockSearch(serializers.ModelSerializer):
    
    
    class Meta:
        model = Block
        fields = ["_id","name"]