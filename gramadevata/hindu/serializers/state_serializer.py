from rest_framework import serializers
from ..models import State
from ..utils import image_path_to_binary
from ..serializers import CountrySerializer
class StateSeerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    # country = CountrySerializer1(read_only=True)
    # country_id = serializers.CharField(read_only=True)
    
    class Meta:
        model = State
        fields = ["_id","name","country","image_location","desc"]
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
    



class StateSearch(serializers.ModelSerializer):
   

    
    class Meta:
        model = State
        fields = ["_id","name"]
