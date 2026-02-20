# from rest_framework import serializers
# from ..models import TourGuide

# class TourGuideSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TourGuide
#         fields = '__all__'
from rest_framework import serializers
from ..models import TourOperator,Register
from ..utils import image_path_to_binary


from django.utils.timesince import timesince
from django.utils import timezone


class TourOperatorSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    class Meta:
        model = TourOperator
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


from rest_framework import serializers
from ..models import TourGuide
from ..utils import image_path_to_binary
class TourGuideSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    class Meta:
        model = TourGuide
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



class TourGuideSerializer1(serializers.ModelSerializer):
    village_id=serializers.SerializerMethodField()
    image_location = serializers.SerializerMethodField()
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

    class Meta:
        model = TourGuide
        fields = '__all__'





class InactiveTourGuideSerializer(serializers.ModelSerializer):
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
        model = TourGuide
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
