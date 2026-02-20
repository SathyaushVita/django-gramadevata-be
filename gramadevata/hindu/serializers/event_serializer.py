



from rest_framework import serializers
from ..models.event import Event
from ..models import Goshala
from ..utils import image_path_to_binary,video_path_to_binary
from ..serializers.comment_serializer import CommentSerializer12
from django.conf import settings
import json
from .nearby_hospitals_serializer import NearbyHospitalSerializer
from .Transport_serializer import TempleTransportSerializer
from .temple_nearby_hotels_serializers import TempleNearbyHotelSerializer
from .resturents_serilizers import TempleNearbyRestaurantSerializer
from .tour_operator_serializer import TourOperatorSerializer
from .tour_guide_serializer import TourGuideSerializer
from .goshala_serializer import GoshalaSerializer
import ast

class EventSerializerForVillage(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['_id', 'name', 'image_location',"status"]

    def get_image_location(self, instance):
        filename = instance.image_location
        
        # Check if filename is a list or a string
        if isinstance(filename, list):
            # If it's already a list, return it as is
            image_paths = filename
        elif isinstance(filename, str):
            # If it's a string, attempt to parse it as a list-like string
            image_paths = filename.strip('[]').replace('"', '').split(',')
            image_paths = [path.strip() for path in image_paths]  # Clean up any extra spaces
        else:
            # If it's neither a list nor a string, return an empty list
            image_paths = []

        # Apply binary conversion (assuming `image_path_to_binary` is defined)
        return [image_path_to_binary(path) for path in image_paths]



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['_id', 'created_at', 'updated_at', 'image_location', 'event_video']





class EventSerializer1(serializers.ModelSerializer):
    comments = CommentSerializer12(many=True)
    image_location = serializers.SerializerMethodField()
    relative_time = serializers.SerializerMethodField()
    object_id = serializers.SerializerMethodField()
    event_video = serializers.SerializerMethodField()
    near_by_hospitals = serializers.SerializerMethodField()
    transport = serializers.SerializerMethodField()
    nearby_hotels = serializers.SerializerMethodField()
    resturents = serializers.SerializerMethodField()
    touroperator = serializers.SerializerMethodField()
    tour_guide = serializers.SerializerMethodField()
    nearby_events = serializers.SerializerMethodField() 
    nearby_goshalas = serializers.SerializerMethodField()
    map_location = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = "__all__"  # All fields including new ones
    def get_nearby_goshalas(self, instance):
        village = instance.object_id
        if not village or not village.block:
            return []
        nearby = Goshala.objects.filter(object_id__block=village.block).exclude(_id=instance._id)
        serializer = GoshalaSerializer(nearby, many=True, context=self.context)
        return serializer.data
    def get_near_by_hospitals(self, obj):
        active = obj.near_by_hospitals.filter(status='ACTIVE')
        return NearbyHospitalSerializer(active, many=True).data

    def get_transport(self, obj):
        active = obj.transport.filter(status='ACTIVE')
        return TempleTransportSerializer(active, many=True).data

    def get_nearby_hotels(self, obj):
        active = obj.nearby_hotels.filter(status='ACTIVE')
        return TempleNearbyHotelSerializer(active, many=True).data

    def get_resturents(self, obj):
        active = obj.resturents.filter(status='ACTIVE')
        return TempleNearbyRestaurantSerializer(active, many=True).data

    def get_touroperator(self, obj):
        active = obj.touroperator.filter(status='ACTIVE')
        return TourOperatorSerializer(active, many=True).data

    def get_tour_guide(self, obj):
        active = obj.tour_guide.filter(status='ACTIVE')
        return TourGuideSerializer(active, many=True).data
    def get_map_location(self, instance):
        raw = instance.map_location
        if not raw:
            return []
        # If already list
        if isinstance(raw, list):
            return [str(x).strip() for x in raw if x]
        # If string like "['url1','url2']"
        if isinstance(raw, str):
            try:
                parsed = ast.literal_eval(raw)
                if isinstance(parsed, list):
                    return [str(x).strip() for x in parsed if x]
            except Exception:
                return []
        return []

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
        return None

    def get_image_location(self, instance):
        filenames = instance.image_location
        if not filenames:
            return []

        if not isinstance(filenames, list):
            filenames = [filenames]

        images = []
        for filename in filenames:
            if filename and filename != "null":
                binary = image_path_to_binary(filename)
                if binary:
                    images.append(binary)
        return images

    def get_event_video(self, instance):
        filenames = instance.event_video
        if not filenames:
            return []

        if not isinstance(filenames, list):
            filenames = [filenames]

        videos = []
        for filename in filenames:
            if filename and filename != "null":
                binary = video_path_to_binary(filename)
                if binary:
                    videos.append(binary)
        return videos

    def get_relative_time(self, obj):
        return obj.relative_time

    # ✅ Get Nearby Events
    def get_nearby_events(self, instance):
        village = instance.object_id
        if not village:
            return []

        same_village_events = Event.objects.filter(object_id=village).exclude(_id=instance._id)
        same_block_events = Event.objects.filter(object_id__block=village.block).exclude(object_id=village).exclude(_id=instance._id)

        combined_events = same_village_events.union(same_block_events)

        return CityEventSerializer(combined_events, many=True).data


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Process image_location
        raw_images = instance.image_location
        image_locations = []

        if raw_images:
            if isinstance(raw_images, str):
                raw_images = [raw_images]
            for item in raw_images:
                if isinstance(item, str):
                    # Split on commas in case of multiple paths in one string
                    paths = item.split(',')
                    for path in paths:
                        clean_path = path.strip().replace("\\", "/")  # Convert Windows-style paths
                        if clean_path and clean_path.lower() != "null":
                            image_locations.append(f"{settings.FILE_URL}{clean_path}")
        representation["image_location"] = image_locations

        # Process event_video similarly if needed
        raw_videos = instance.event_video
        event_videos = []

        if raw_videos:
            if isinstance(raw_videos, str):
                raw_videos = [raw_videos]
            for item in raw_videos:
                if isinstance(item, str):
                    paths = item.split(',')
                    for path in paths:
                        clean_path = path.strip().replace("\\", "/")
                        if clean_path and clean_path.lower() != "null":
                            event_videos.append(f"{settings.FILE_URL}{clean_path}")
        representation["event_video"] = event_videos

        return representation




  

class CityEventSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    def get_image_location(self, instance):
        filenames = instance.image_location
        if filenames:
            # Handle the case where image_location is a list
            if isinstance(filenames, list):
                # Convert each path to binary format
                return [image_path_to_binary(filename) for filename in filenames]
            else:
                # If it's a single string, just convert that one
                return [image_path_to_binary(filenames)]
        return []

    class Meta:
        model = Event
        fields = ["_id","name","image_location"]
 




    
class TownSerializers(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    object_id=serializers.SerializerMethodField()


    class Meta:
        model = Event
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









 
class TownSerializers1(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()


    class Meta:
        model = Event
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





 
class EventLocationSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()


    class Meta:
        model = Event
        fields = ["_id","name","image_location","address","start_date","end_date"]
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
    








class EventSearch(serializers.ModelSerializer):
    
    

    class Meta:
        model = Event
        fields = ["_id","name"]
 



from django.utils.timesince import timesince
from django.utils import timezone




class EventInactiveSerializer(serializers.ModelSerializer):
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
        model = Event
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