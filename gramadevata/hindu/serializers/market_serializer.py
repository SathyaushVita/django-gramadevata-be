from rest_framework import serializers
from ..models import VillageMarket
from ..utils import image_path_to_binary  

class VillageMarketSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()

    class Meta:
        model = VillageMarket
        fields = '__all__'

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
    




class VillageMarketSerializer1(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()

    class Meta:
        model = VillageMarket
        fields = ["_id","name","address","map_location","desc","image_location","contact_number","email_id"]

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