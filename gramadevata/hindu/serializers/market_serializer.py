from rest_framework import serializers
from ..models import VillageMarket,Register
from ..utils import image_path_to_binary  
from django.utils.timesince import timesince
from django.utils import timezone

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





class InactiveVillageMarketSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()
    relative_time = serializers.SerializerMethodField()

    def get_relative_time(self, instance):
        if not instance.created_at:
            return None

        now = timezone.now()
        diff = timesince(instance.created_at, now)

        return f"{diff} ago"

    def get_user_full_name(self, instance):
        try:
            if instance.user_id:
                return instance.user_id.full_name
        except Register.DoesNotExist:
            return None
        return None
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
    