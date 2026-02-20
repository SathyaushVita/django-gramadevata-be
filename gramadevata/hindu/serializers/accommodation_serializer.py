from rest_framework import serializers
from ..models import Accommodation
from ..utils import image_path_to_binary

class AccommodationSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()


    class Meta:
        model = Accommodation
        fields = ["_id","name","accommodation_rating","temple_id","address","map_location","user_id","village_id","image_location","owner_name","contact_number","tourism_places","event_id"]
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

