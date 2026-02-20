from rest_framework import serializers
from ..models import *
from ..utils import image_path_to_binary,video_path_to_binary
from ..serializers.comment_serializer import CommentSerializer12
from django.conf import settings
from .nearby_vetarnary_hospital_serializer import VeterinaryHospitalSerializer
import ast

class GoshalaSerializerForVillage(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()

    class Meta:
        model = Goshala
        fields = ['_id', 'name', 'image_location',"status"]

    def get_image_location(self, instance):
        filename = instance.image_location
        
        if isinstance(filename, list):
            image_paths = filename
        elif isinstance(filename, str):
            image_paths = filename.strip('[]').replace('"', '').split(',')
            image_paths = [path.strip() for path in image_paths]  
        else:
            image_paths = []

        return [image_path_to_binary(path) for path in image_paths]
    


class GoshalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goshala
        fields = "__all__"
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Ensure the image_location is returned as a list
        if instance.image_location:
            # Check if image_location is a string; if it's a list, handle it appropriately
            if isinstance(instance.image_location, str):
                # Split the stored path string into a list
                image_locations = instance.image_location.strip('[]').replace('"', '').split(',')
                # Clean up extra spaces or characters
                image_locations = [path.strip() for path in image_locations]
            elif isinstance(instance.image_location, list):
                # If it's already a list, just clean the entries
                image_locations = [path.strip() for path in instance.image_location if isinstance(path, str)]
            else:
                image_locations = []
            # Prepend the base FILE_URL to each image path
            image_locations = [f"{settings.FILE_URL}{path}" for path in image_locations]
            representation['image_location'] = image_locations
        else:
            representation['image_location'] = []
        return representation
    



class GoshalaSerializer1(serializers.ModelSerializer):
    comments = CommentSerializer12(many=True)
    image_location = serializers.SerializerMethodField()
    goshala_video = serializers.SerializerMethodField()
    object_id = serializers.SerializerMethodField()
    vetarnary_hospital = serializers.SerializerMethodField()
    nearby_goshalas = serializers.SerializerMethodField()
   
    
    def get_nearby_goshalas(self, instance):
        village = instance.object_id
        if not village or not village.block:
            return []
        nearby = Goshala.objects.filter(
            object_id__block=village.block,
            status='ACTIVE'  # Filter only ACTIVE goshala
        ).exclude(_id=instance._id)
        
        serializer = GoshalaSerializer(nearby, many=True, context=self.context)
        return serializer.data

    # def get_nearby_goshalas(self, instance):
    #     village = instance.object_id
    #     if not village or not village.block:
    #         return []
    #     nearby = Goshala.objects.filter(object_id__block=village.block).exclude(_id=instance._id)
    #     serializer = GoshalaSerializer(nearby, many=True, context=self.context)
    #     return serializer.data

    def get_vetarnary_hospital(self, obj):
        active = obj.vetarnary_hospital.filter(status='ACTIVE')
        return VeterinaryHospitalSerializer(active, many=True).data
   

    def get_object_id(self, instance):
        village = instance.object_id
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

    def get_image_location(self, instance):
        if isinstance(instance.image_location, list):
            return [image_path_to_binary(path) for path in instance.image_location if path]
        elif instance.image_location:
            return [image_path_to_binary(instance.image_location)]
        return []

    def get_goshala_video(self, instance):
        if isinstance(instance.goshala_video, list):
            return [video_path_to_binary(path) for path in instance.goshala_video if path and path != "null"]
        elif instance.goshala_video:
            return [video_path_to_binary(instance.goshala_video)]
        return []

    class Meta:
        model = Goshala
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Process image paths
        if instance.image_location:
            if isinstance(instance.image_location, str):
                image_paths = instance.image_location.strip('[]').replace('"', '').split(',')
                image_paths = [path.strip() for path in image_paths]
            elif isinstance(instance.image_location, list):
                image_paths = [path.strip() for path in instance.image_location if isinstance(path, str)]
            else:
                image_paths = []
            representation['image_location'] = [f"{settings.FILE_URL}{path}" for path in image_paths]
        else:
            representation['image_location'] = []

        # Process video paths
        if instance.goshala_video:
            if isinstance(instance.goshala_video, str):
                video_paths = instance.goshala_video.strip('[]').replace('"', '').split(',')
                video_paths = [path.strip() for path in video_paths]
            elif isinstance(instance.goshala_video, list):
                video_paths = [path.strip() for path in instance.goshala_video if isinstance(path, str)]
            else:
                video_paths = []
            representation['goshala_video'] = [f"{settings.FILE_URL}{path}" for path in video_paths if path and path != "null"]
        else:
            representation['goshala_video'] = []

        return representation



class GoshalaMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goshala
        fields = "__all__"





class StateSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    object_id=serializers.SerializerMethodField()



    class Meta:
        model = Goshala
        fields = ["_id","name","image_location","object_id"]
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

    def get_object_id(self, instance):
            village = instance.object_id

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











class StateSerializer1(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()



    class Meta:
        model = Goshala
        fields = ["_id","name","image_location"]
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

 




class GoshalaLocationSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    object_id=serializers.SerializerMethodField()



    class Meta:
        model = Goshala
        fields = ["_id","name","image_location","address","object_id"]
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
        


    def get_object_id(self, instance):
        village = instance.object_id

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








class GoshalaSearch(serializers.ModelSerializer):
    

    class Meta:
        model = Goshala
        fields = ["_id","name"]




from django.utils.timesince import timesince
from django.utils import timezone

class GoshalaInactiveSerializer(serializers.ModelSerializer):
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
        if instance.user:
            return instance.user.full_name  
        return None


    class Meta:
        model = Goshala
        fields = "__all__"
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