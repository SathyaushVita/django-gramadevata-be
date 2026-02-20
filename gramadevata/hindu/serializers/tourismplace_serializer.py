from rest_framework import serializers
from ..models import TempleNearbyTourismPlace,Goshala,Temple
from ..utils import image_path_to_binary
from .resturents_serilizers import TempleNearbyRestaurantSerializer
from .temple_nearby_hotels_serializers import TempleNearbyHotelSerializer
from .Transport_serializer import TempleTransportSerializer
from .nearby_hospitals_serializer import NearbyHospitalSerializer
from .accommodation_serializer import AccommodationSerializer
from .police_station_serializer import PoliceStationSerializer




class TempleNearbyTourismPlaceSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    transport = serializers.SerializerMethodField()
    near_by_hospitals = serializers.SerializerMethodField()
    resturents=serializers.SerializerMethodField()
    nearby_hotels = serializers.SerializerMethodField()
    accommodation= serializers.SerializerMethodField()
    police_station=serializers.SerializerMethodField()
    # temples = serializers.SerializerMethodField()
    # goshalas = serializers.SerializerMethodField()

    def get_near_by_hospitals(self, obj):
        active = obj.near_by_hospitals.filter(status='ACTIVE')
        return NearbyHospitalSerializer(active, many=True).data
    
    def get_resturents(self, obj):
        active = obj.resturents.filter(status='ACTIVE')
        return TempleNearbyRestaurantSerializer(active, many=True).data
    
    def get_accommodation(self, obj):
        active = obj.accommodation.filter(status='ACTIVE')
        return AccommodationSerializer(active, many=True).data

    def get_nearby_hotels(self, obj):
        active = obj.nearby_hotels.filter(status='ACTIVE')
        return TempleNearbyHotelSerializer(active, many=True).data
    
    def get_police_station(self, obj):
        active = obj.police_station.filter(status='ACTIVE')
        return PoliceStationSerializer(active, many=True).data
    def get_temples(self, instance):
        from .temple_serializers import CitySerializer1
        if instance.village_id:
            temples = Temple.objects.filter(object_id=instance.village_id, status='ACTIVE')
            return CitySerializer1(temples, many=True).data
        return []

    def get_goshalas(self, instance):
        from .goshala_serializer import StateSerializer1
        if instance.village_id:
            goshalas = Goshala.objects.filter(object_id=instance.village_id, status='ACTIVE')
            return StateSerializer1(goshalas, many=True).data
        return []


    def get_transport(self, obj):
        active = obj.transport.filter(status='ACTIVE')
        return TempleTransportSerializer(active, many=True).data
    
    class Meta:
        model = TempleNearbyTourismPlace
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





# def get_image_location(self, instance):
#     filename = instance.image_location

#     if isinstance(filename, list):
#         image_paths = filename

#     elif isinstance(filename, str):
#         try:
#             image_paths = json.loads(filename)  # JSON string case
#             if not isinstance(image_paths, list):
#                 image_paths = []
#         except json.JSONDecodeError:
#             # fallback if it's not valid JSON
#             image_paths = filename.strip('[]').replace('"', '').replace("'", '').split(',')
#             image_paths = [p.strip() for p in image_paths if p.strip()]
#     else:
#         image_paths = []

#     return [image_path_to_binary(path) for path in image_paths]








class TourismPlaceSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    village_id=serializers.SerializerMethodField()

    class Meta:
        model = TempleNearbyTourismPlace
        fields = ["_id","name","image_location","village_id"]
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


class TourismPlaceSearchSerializer(serializers.ModelSerializer):
    
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
    
    class Meta:
        model = TempleNearbyTourismPlace
        fields = ["_id","name","image_location"]





class TourismPlaceSerializer1(serializers.ModelSerializer):
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
    
    class Meta:
        model = TempleNearbyTourismPlace
        fields = ["_id","name","image_location","address","map_location"]



class TourismPlacelocationSerializer(serializers.ModelSerializer):
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
    
    class Meta:
        model = TempleNearbyTourismPlace
        fields = ["_id","name","image_location"]





from django.utils.timesince import timesince
from django.utils import timezone


class TourismPlaceInactiveSerializer(serializers.ModelSerializer):
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
        if instance.user_id:
            return instance.user_id.full_name
        return None


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
    
    class Meta:
        model = TempleNearbyTourismPlace
        fields = "__all__"