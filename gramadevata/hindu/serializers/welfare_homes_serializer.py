from rest_framework import serializers
from ..models import WelfareHomes
from ..utils import image_path_to_binary

class WelfareHomesSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()

    def get_image_location(self, instance):
        filename = instance.image_location

        if not filename:
            return []

        if isinstance(filename, list):
            image_paths = filename
        elif isinstance(filename, str):
            # Fix for stringified list like '["path\\to\\file.jpg"]'
            filename = filename.strip('[]').replace('"', '').replace("'", '')
            image_paths = [path.strip() for path in filename.split(',') if path.strip()]
        else:
            image_paths = []

        return [image_path_to_binary(path) for path in image_paths]

    class Meta:
        model = WelfareHomes
        fields = "__all__"




class WelfareHomesSerializer1(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    village_id=serializers.SerializerMethodField()

    def get_image_location(self, instance):
        filename = instance.image_location

        if not filename:
            return []

        if isinstance(filename, list):
            image_paths = filename
        elif isinstance(filename, str):
            # Fix for stringified list like '["path\\to\\file.jpg"]'
            filename = filename.strip('[]').replace('"', '').replace("'", '')
            image_paths = [path.strip() for path in filename.split(',') if path.strip()]
        else:
            image_paths = []

        return [image_path_to_binary(path) for path in image_paths]

    class Meta:
        model = WelfareHomes
        fields =["_id","name","image_location","village_id"]


    def get_village_id(self, instance):
        village = instance.village_id

        if village and village.block and village.block.district and village.block.district.state and village.block.district.state.country:
            return {
                "_id": str(village._id),
                "name": village.name,
                "block": {
                    "block_id": str(village.block.pk),
                    "name": village.block.name,
                    "district": {
                        "district_id": str(village.block.district.pk),
                        "name": village.block.district.name,
                        "state": {
                            "state_id": str(village.block.district.state.pk),
                            "name": village.block.district.state.name,
                            "country": {
                                "country_id": str(village.block.district.state.country.pk),
                                "name": village.block.district.state.country.name
                            }
                        }
                    }
                }
            }






class WelfareHomesSerializer2(serializers.ModelSerializer):


    class Meta:
        model = WelfareHomes
        fields = "__all__"


class WelfareHomesSearchSerializer(serializers.ModelSerializer):
    


    class Meta:
        model = WelfareHomes
        fields = ["_id","name"]

   


        

class WelfareHomeslocationSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()

    def get_image_location(self, instance):
        filename = instance.image_location

        if not filename:
            return []

        if isinstance(filename, list):
            image_paths = filename
        elif isinstance(filename, str):
            # Fix for stringified list like '["path\\to\\file.jpg"]'
            filename = filename.strip('[]').replace('"', '').replace("'", '')
            image_paths = [path.strip() for path in filename.split(',') if path.strip()]
        else:
            image_paths = []

        return [image_path_to_binary(path) for path in image_paths]


    class Meta:
        model = WelfareHomes
        fields = ["_id","name","image_location"]





from django.utils.timesince import timesince
from django.utils import timezone


class WelfareHomesInactiveSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()
    relative_time = serializers.SerializerMethodField()
    def get_relative_time(self, instance):
        if not instance.created_at:
            return None

        now = timezone.now()
        diff = timesince(instance.created_at, now)

        # cleaner output
        return f"{diff.split(',')[0]} ago"
    def get_user_full_name(self, instance):
        if instance.user:
            return instance.user.full_name
        return None

    def get_image_location(self, instance):
        filename = instance.image_location

        if not filename:
            return []

        if isinstance(filename, list):
            image_paths = filename
        elif isinstance(filename, str):
            filename = filename.strip('[]').replace('"', '').replace("'", '')
            image_paths = [path.strip() for path in filename.split(',') if path.strip()]
        else:
            image_paths = []

        return [image_path_to_binary(path) for path in image_paths]


    class Meta:
        model = WelfareHomes
        fields =  "__all__"