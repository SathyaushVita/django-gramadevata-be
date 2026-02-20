from rest_framework import serializers
from ..models import BloodBank
from ..utils import image_path_to_binary
from django.utils.timesince import timesince
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

class BloodBankSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    license_copy=serializers.SerializerMethodField()

    class Meta:
        model = BloodBank
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









class BloodBankSerializer1(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    village_id=serializers.SerializerMethodField()

    class Meta:
        model = BloodBank
        fields = ["_id","village_id","name","image_location","map_location","address"]


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
        try:
            village = instance.village_id
        except ObjectDoesNotExist:
            return None   # ✅ prevents crash

        if not village:
            return None

        return {
            "_id": str(village._id),
            "name": village.name,
            "block": {
                "block_id": str(village.block.pk) if village.block else None,
                "name": village.block.name if village.block else None,
                "district": {
                    "district_id": str(village.block.district.pk) if village.block.district else None,
                    "name": village.block.district.name if village.block.district else None,
                    "state": {
                        "state_id": str(village.block.district.state.pk) if village.block.district.state else None,
                        "name": village.block.district.state.name if village.block.district.state else None,
                        "country": {
                            "country_id": str(village.block.district.state.country.pk)
                            if village.block.district.state.country else None,
                            "name": village.block.district.state.country.name
                            if village.block.district.state.country else None
                        }
                    }
                }
            }
        }
    









class BloodBankSerializer2(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()

    class Meta:
        model = BloodBank
        fields = ["_id","blood_group","name","image_location","map_location","address"]


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
    






class BloodBankInactiveSerializer(serializers.ModelSerializer):
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
        model = BloodBank
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