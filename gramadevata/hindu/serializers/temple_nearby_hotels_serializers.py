from rest_framework import serializers
from ..models import TempleNearbyHotel
from ..utils import image_path_to_binary
from django.utils.timesince import timesince
from django.utils import timezone
class TempleNearbyHotelSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    license_copy=serializers.SerializerMethodField()


    class Meta:
        model = TempleNearbyHotel
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

    def get_license_copy(self, instance):
        filename = instance.license_copy
        
        if isinstance(filename, list):
            image_paths = filename
        elif isinstance(filename, str):
            # Remove square brackets, double quotes, and single quotes, then split by comma
            image_paths = filename.strip('[]').replace('"', '').replace("'", '').split(',')
            image_paths = [path.strip() for path in image_paths]  # Clean up any extra spaces
        else:
            image_paths = []

        return [image_path_to_binary(path) for path in image_paths]
    




class TempleNearbyHotelSerializer1(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    # village_id=serializers.SerializerMethodField()


    class Meta:
        model = TempleNearbyHotel
        fields = ["_id","name","image_location","map_location","address","hotel_rating"]
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
    

    # def get_village_id(self, instance):
    #     village = instance.village_id

    #     if village and village.block and village.block.district and village.block.district.state and village.block.district.state.country:
    #         return {
    #             "_id": str(village._id),
    #             "name": village.name,
    #             "block": {
    #                 "block_id": str(village.block.pk),
    #                 "name": village.block.name,
    #                 "district": {
    #                     "district_id": str(village.block.district.pk),
    #                     "name": village.block.district.name,
    #                     "state": {
    #                         "state_id": str(village.block.district.state.pk),
    #                         "name": village.block.district.state.name,
    #                         "country": {
    #                             "country_id": str(village.block.district.state.country.pk),
    #                             "name": village.block.district.state.country.name
    #                         }
    #                     }
    #                 }
    #             }
    #         }







class InactiveHotelSerializer(serializers.ModelSerializer):
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
        # Return full name if user exists, else None
        if instance.user_id:
            return instance.user_id.full_name  
        return None

    class Meta:
        model = TempleNearbyHotel
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
    