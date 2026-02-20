from rest_framework import serializers
from ..models import *
import base64
# from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from .tour_operator_serializer import TourOperatorSerializer
from .temple_festival_serializer import TempleFestivalSerializer
from .event_serializer import EventSerializer,EventSerializer1,TownSerializers1
from .goshala_serializer import GoshalaSerializer,GoshalaSerializer1,StateSerializer1
from .media_serializer import MediaSerializer
from .comment_serializer import CommentSerializer,CommentSerializer12
from .temple_priority_serializer import TemplePrioritySerializer
from .connect_serializer import ConnectModelSerializer1
from ..processor.byte_processor import find_specific_folder
import os
from ..utils import image_path_to_binary,video_path_to_binary
from .temple_nearby_hotels_serializers import TempleNearbyHotelSerializer,TempleNearbyHotelSerializer1
from .tourismplace_serializer import TempleNearbyTourismPlaceSerializer,TourismPlaceSerializer,TourismPlaceSerializer1
from .Transport_serializer import TempleTransportSerializer
from .nearby_hospitals_serializer import NearbyHospitalSerializer,NearbyHospitalSerializer1,NearbyHospitalSerializer2
from .SocialActivity_serializer import SocialActivitySerializer
from .temple_facilities_serializer import TempleFacilitiesSerializer
from .prayers_and_benefits_serializer import PrayersAndBenefitsSerializer
from .tour_guide_serializer import TourGuideSerializer
from .pooja_timing_serializer import TemplePoojaTimingSerializer
from .favorite_temples_serializers import FavoriteTempleSerializer
from .resturents_serilizers import TempleNearbyRestaurantSerializer,TempleNearbyRestaurantSerializer1
from .ambulance_facility_serializers import AmbulanceFacilitySerializer,AmbulanceFacilitySerializer1
from .blood_bank_serializer import BloodBankSerializer,BloodBankSerializer1,BloodBankSerializer2
from .fire_station_seriliazer import FireStationSerializer,FireStationSerializer1
from .police_station_serializer import PoliceStationSerializer,PoliceStationSerializer1
from .pooja_stores_serializer import PoojaStoreSerializer,PoojaStoreSerializer1
from .visit_temple_serializer import VisitTempleSerializer




class TempleSerializer(serializers.ModelSerializer):
    class Meta:
        # print("asdfbgnh")
        model = Temple
        fields = "__all__"



# class TempleSerializer1(serializers.ModelSerializer):

#     image_location = serializers.JSONField()
#     temple_video = serializers.JSONField()

#     nearby_hotels = TempleNearbyHotelSerializer1(many=True, read_only=True)
#     tourismplace = TourismPlaceSerializer(many=True, read_only=True)
#     transport = TempleTransportSerializer(many=True, read_only=True)
#     media = MediaSerializer(many=True, read_only=True)
#     touroperator = TourOperatorSerializer(many=True, read_only=True)
#     social_activity = SocialActivitySerializer(many=True, read_only=True)
#     near_by_hospitals = NearbyHospitalSerializer1(many=True, read_only=True)
#     temple_facilities = TempleFacilitiesSerializer(many=True, read_only=True)
#     prayers_and_benefits = PrayersAndBenefitsSerializer(many=True, read_only=True)
#     tour_guide = TourGuideSerializer(many=True, read_only=True)
#     pooja_timing = TemplePoojaTimingSerializer(many=True, read_only=True)
#     resturents = TempleNearbyRestaurantSerializer1(many=True, read_only=True)
#     pooja_stores = PoojaStoreSerializer1(many=True, read_only=True)
#     ambulance_facility = AmbulanceFacilitySerializer1(many=True, read_only=True)
#     blood_bank = BloodBankSerializer1(many=True, read_only=True)
#     fire_station = FireStationSerializer1(many=True, read_only=True)
#     police_station = PoliceStationSerializer1(many=True, read_only=True)

#     favorite = FavoriteTempleSerializer(many=True, read_only=True)
#     visit_temples = VisitTempleSerializer(many=True, read_only=True)
#     Connections = ConnectModelSerializer1(many=True, read_only=True)

#     ismember = serializers.SerializerMethodField()
#     ispujari = serializers.SerializerMethodField()
#     isvolunteer = serializers.SerializerMethodField()
#     istemplemember = serializers.SerializerMethodField()
#     connectionId = serializers.SerializerMethodField()

#     object_id = serializers.SerializerMethodField()

#     # ---------- USER CONNECTION CACHE ----------
#     def _get_user_connection(self, obj):
#         request = self.context.get("request")
#         if not request or not request.user.is_authenticated:
#             return None

#         if not hasattr(self, "_conn_cache"):
#             self._conn_cache = {}

#         key = (obj.id, request.user.id)
#         if key not in self._conn_cache:
#             self._conn_cache[key] = obj.Connections.filter(
#                 user_id=request.user.id
#             ).first()
#         return self._conn_cache[key]

#     def get_connectionId(self, obj):
#         conn = self._get_user_connection(obj)
#         return conn._id if conn else None

#     def get_istemplemember(self, obj):
#         return bool(self._get_user_connection(obj))

#     def get_ismember(self, obj):
#         conn = self._get_user_connection(obj)
#         return conn and conn.connected_as == "MEMBER"

#     def get_ispujari(self, obj):
#         conn = self._get_user_connection(obj)
#         return conn and conn.connected_as == "PUJARI"

#     def get_isvolunteer(self, obj):
#         conn = self._get_user_connection(obj)
#         return conn and conn.connected_as == "VOLUNTARY"

#     # ---------- LOCATION OBJECT ----------
#     def get_object_id(self, instance):
#         v = instance.object_id
#         if not v:
#             return None

#         return {
#             "_id": v._id,
#             "name": v.name,
#             "block": {
#                 "block_id": v.block_id,
#                 "name": v.block.name,
#                 "district": {
#                     "district_id": v.block.district_id,
#                     "name": v.block.district.name,
#                     "state": {
#                         "state_id": v.block.district.state_id,
#                         "name": v.block.district.state.name,
#                         "country": {
#                             "country_id": v.block.district.state.country_id,
#                             "name": v.block.district.state.country.name
#                         }
#                     }
#                 }
#             }
#         }

#     class Meta:
#         model = Temple
#         fields = "__all__"




 
class TempleSerializer1(serializers.ModelSerializer):
    ismember = serializers.SerializerMethodField()
    ispujari = serializers.SerializerMethodField()
    isvolunteer = serializers.SerializerMethodField()
    connectionId = serializers.SerializerMethodField() 
    istemplemember = serializers.SerializerMethodField()
    comments = CommentSerializer12(many=True, read_only=True)
    image_location = serializers.SerializerMethodField()
    temple_video = serializers.SerializerMethodField()

    object_id=serializers.SerializerMethodField()
    Connections = ConnectModelSerializer1(many=True, read_only=True)
    events = serializers.SerializerMethodField()
    nearby_hotels = serializers.SerializerMethodField()
    tourismplace = serializers.SerializerMethodField()
    transport = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()
    touroperator = serializers.SerializerMethodField()
    social_activity = serializers.SerializerMethodField()
    near_by_hospitals = serializers.SerializerMethodField()
    temple_facilities = serializers.SerializerMethodField()
    prayers_and_benefits = serializers.SerializerMethodField()
    tour_guide = serializers.SerializerMethodField()
    pooja_timing = serializers.SerializerMethodField()
    goshalas = serializers.SerializerMethodField()
    favorite=FavoriteTempleSerializer(many=True, read_only=True)
    visit_temples = serializers.SerializerMethodField()
    # resturents=TempleNearbyRestaurantSerializer(many=True, read_only=True)
    resturents=serializers.SerializerMethodField()
    ambulance_facility=serializers.SerializerMethodField()
    blood_bank=serializers.SerializerMethodField()
    fire_station=serializers.SerializerMethodField()
    police_station=serializers.SerializerMethodField()
    pooja_stores=serializers.SerializerMethodField()
    def get_visit_temples(self, obj):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            visits = obj.visit_temples.filter(user_id=request.user)
            return VisitTempleSerializer(visits, many=True).data

        return []

    # ambulance_facility=AmbulanceFacilitySerializer(many=True,read_only=True)
    # blood_bank=BloodBankSerializer(many=True,read_only=True)
    # fire_station=FireStationSerializer(many=True,read_only=True)
    # police_station=PoliceStationSerializer(many=True,read_only=True)
    # pooja_stores=PoojaStoreSerializer(many=True,read_only=True)
    def get_temple_video(self, instance):
        if isinstance(instance.temple_video, list):
            return [video_path_to_binary(path) for path in instance.temple_video if path and path != "null"]
        elif instance.temple_video:
            return [video_path_to_binary(instance.temple_video)]
        return []

    def get_events(self, obj):
        active_events = obj.events.filter(status='ACTIVE')
        return TownSerializers1(active_events, many=True).data

    def get_nearby_hotels(self, obj):
        active = obj.nearby_hotels.filter(status='ACTIVE')
        return TempleNearbyHotelSerializer1(active, many=True).data

    def get_tourismplace(self, obj):
        active = obj.tourismplace.filter(status='ACTIVE')
        return TourismPlaceSerializer1(active, many=True).data

    def get_transport(self, obj):
        active = obj.transport.filter(status='ACTIVE')
        return TempleTransportSerializer(active, many=True).data

    def get_media(self, obj):
        active = obj.media.filter(status='ACTIVE')
        return MediaSerializer(active, many=True).data

    def get_touroperator(self, obj):
        active = obj.touroperator.filter(status='ACTIVE')
        return TourOperatorSerializer(active, many=True).data
    
    def get_ambulance_facility(self, obj):
        active = obj.ambulance_facility.filter(status='ACTIVE')
        return AmbulanceFacilitySerializer1(active, many=True).data
    
    def get_blood_bank(self, obj):
        active = obj.blood_bank.filter(status='ACTIVE')
        return BloodBankSerializer2(active, many=True).data
    
    def get_fire_station(self, obj):
        active = obj.fire_station.filter(status='ACTIVE')
        return FireStationSerializer1(active, many=True).data
    
    def get_police_station(self, obj):
        active = obj.police_station.filter(status='ACTIVE')
        return PoliceStationSerializer1(active, many=True).data

    def get_social_activity(self, obj):
        active = obj.social_activity.filter(status='ACTIVE')
        return SocialActivitySerializer(active, many=True).data

    def get_near_by_hospitals(self, obj):
        active = obj.near_by_hospitals.filter(status='ACTIVE')
        return NearbyHospitalSerializer2(active, many=True).data
    
    def get_resturents(self, obj):
        active = obj.resturents.filter(status='ACTIVE')
        return TempleNearbyRestaurantSerializer1(active, many=True).data
    

    def get_pooja_stores(self, obj):
        active = obj.pooja_stores.filter(status='ACTIVE')
        return PoojaStoreSerializer1(active, many=True).data

    def get_temple_facilities(self, obj):
        active = obj.temple_facilities.filter(status='ACTIVE')
        return TempleFacilitiesSerializer(active, many=True).data

    def get_prayers_and_benefits(self, obj):
        active = obj.prayers_and_benefits.filter(status='ACTIVE')
        return PrayersAndBenefitsSerializer(active, many=True).data

    def get_tour_guide(self, obj):
        active = obj.tour_guide.filter(status='ACTIVE')
        return TourGuideSerializer(active, many=True).data

    def get_pooja_timing(self, obj):
        active = obj.pooja_timing.filter(status='ACTIVE')
        return TemplePoojaTimingSerializer(active, many=True).data

    def get_goshalas(self, obj):
        goshalas = Goshala.objects.filter(temple=obj, status='ACTIVE')
        return StateSerializer1(goshalas, many=True).data





    # def get_connectionId(self, obj):
    #     request = self.context.get('request')
    #     if not request or not request.user.is_authenticated:
    #         return None
    #     user_id = request.user.id
    #     connection = obj.Connections.filter(user__id=user_id).first()  # Fetch the current user's connection
    #     return connection._id if connection else None

    def get_connectionId(self, obj):
        conns = self._user_connections(obj)
        return conns[0]._id if conns else None
    

    # def get_istemplemember(self, obj):
    #     request = self.context.get('request')
    #     if not request or not request.user.is_authenticated:
    #         return False

    #     user_id = request.user.id
    #     return obj.Connections.filter(user__id=user_id).exists()

    def get_istemplemember(self, obj):
        return bool(self._user_connections(obj))


    # def get_ismember(self, obj):
    #     request = self.context.get('request')
    #     print("jhd",request)
    #     if not request or not request.user.is_authenticated:
    #         print("dytjy")
    #         return False
    #     user_id = request.user.id
    #     print("user",user_id)
    #     return obj.Connections.filter(user__id=user_id, connected_as="MEMBER").exists()

    def get_ismember(self, obj):
        return any(c.connected_as == "MEMBER" for c in self._user_connections(obj))


    # def get_ispujari(self, obj):
    #     request = self.context.get('request')
    #     if not request or not request.user.is_authenticated:
    #         return False
    #     user_id = request.user.id
    #     return obj.Connections.filter(user__id=user_id, connected_as="PUJARI").exists()
    def get_ispujari(self, obj):
        return any(c.connected_as == "PUJARI" for c in self._user_connections(obj))

    
    # def get_isvolunteer(self, obj):
    #     request = self.context.get('request')
    #     if not request or not request.user.is_authenticated:
    #         return False
    #     user_id = request.user.id
    #     return obj.Connections.filter(user__id=user_id, connected_as="VOLUNTARY").exists()

    def get_isvolunteer(self, obj):
        return any(c.connected_as == "VOLUNTARY" for c in self._user_connections(obj))

    def _user_connections(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return []

        uid = request.user.id
        # use prefetched Connections (NO DB HIT)
        return [c for c in obj.Connections.all() if c.user_id == uid]


    



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

    class Meta:
        model = Temple
        fields = ["_id","name","diety","object_id","temple_map_location","address","image_location","temple_timings","contact_email","contact_phone","desc","temple_official_website","other_dieties","dress_code","festivals","temple_video","latitude","longitude","connectionId","ispujari","ismember","comments","goshalas","pooja_timing","tour_guide","prayers_and_benefits","temple_facilities","pooja_stores","resturents","near_by_hospitals","social_activity","police_station","fire_station","blood_bank","ambulance_facility","touroperator","media","transport","tourismplace","nearby_hotels","events","isvolunteer","visit_temples","favorite","istemplemember","Connections"]

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

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
        if instance.temple_video:
            if isinstance(instance.temple_video, str):
                video_paths = instance.temple_video.strip('[]').replace('"', '').split(',')
                video_paths = [path.strip() for path in video_paths]
            elif isinstance(instance.temple_video, list):
                video_paths = [path.strip() for path in instance.temple_video if isinstance(path, str)]
            else:
                video_paths = []
            representation['temple_video'] = [f"{settings.FILE_URL}{path}" for path in video_paths if path and path != "null"]
        else:
            representation['temle_video'] = []

        return representation







def save_image_to_folder(image_location, _id):
    
    image_data = base64.b64decode(image_location)
    
    
    folder_name = str(_id)
    img_url = settings.FILE_URL
    
    
    folder_path = os.path.join(img_url,"temple", folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
   
    image_name = "image.jpg"
    image_path = os.path.join(folder_path, image_name)
    with open(image_path, "wb") as image_file:
        image_file.write(image_data)

    return image_path





import re


def extract_lat_long_from_url(url):
    if not url:
        return None, None
    match = re.search(r'[-+]?\d{1,3}\.\d+,\s*[-+]?\d{1,3}\.\d+', url)
    if match:
        lat, long = match.group(0).split(',')
        return float(lat.strip()), float(long.strip())
    return None, None

class TempleDetailSerializer(serializers.ModelSerializer):
    ismember = serializers.SerializerMethodField()
    ispujari = serializers.SerializerMethodField()
    connectionId = serializers.SerializerMethodField()
    comments = CommentSerializer12(many=True, read_only=True)
    image_location = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    nearby_temples = serializers.SerializerMethodField()
    object_id=serializers.SerializerMethodField()
    temple_video = serializers.SerializerMethodField()


    
    def get_temple_video(self, instance):
        filenames = instance.temple_video
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
        filename = instance.image_location
        if isinstance(filename, list):
            image_paths = filename
        elif isinstance(filename, str):
            image_paths = filename.strip('[]').replace('"', '').split(',')
            image_paths = [path.strip() for path in image_paths]
        else:
            image_paths = []
        return [image_path_to_binary(path) for path in image_paths]

    def get_connectionId(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None
        user_id = request.user.id
        connection = obj.Connections.filter(user__id=user_id).first()
        return connection._id if connection else None

    def get_ismember(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        user_id = request.user.id
        return obj.Connections.filter(user__id=user_id, connected_as="MEMBER").exists()

    def get_ispujari(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        user_id = request.user.id
        return obj.Connections.filter(user__id=user_id, connected_as="PUJARI").exists()


    def get_latitude(self, obj):
        lat, _ = extract_lat_long_from_url(obj.temple_map_location)
        return lat

    def get_longitude(self, obj):
        _, long = extract_lat_long_from_url(obj.temple_map_location)
        return long

    def get_nearby_temples(self, obj):
        try:
            district_id = obj.object_id.block.district.pk
            nearby = Temple.objects.filter(object_id__block__district__pk=district_id).exclude(_id=obj._id)[:5]
            return [
                {
                    "id": temple._id,
                    "name": temple.name,
                    "map_location": temple.temple_map_location,
                }
                for temple in nearby
            ]
        except AttributeError:
            return []


    class Meta:
        model = Temple
        fields = ["_id","name","diety","object_id","temple_map_location","address","image_location","temple_timings","contact_email","contact_phone","desc","temple_official_website","other_dieties","dress_code","festivals","temple_video","latitude","longitude","connectionId","ispujari","ismember","comments","nearby_temples","user"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Handle image URLs
        if instance.image_location:
            if isinstance(instance.image_location, str):
                image_locations = instance.image_location.strip('[]').replace('"', '').split(',')
                image_locations = [path.strip() for path in image_locations]
            elif isinstance(instance.image_location, list):
                image_locations = [path.strip() for path in instance.image_location if isinstance(path, str)]
            else:
                image_locations = []
            image_locations = [f"{settings.FILE_URL}{path}" for path in image_locations if path and path != "null"]
            representation['image_location'] = image_locations
        else:
            representation['image_location'] = []

        # Handle event video URLs
        if instance.temple_video:
            if isinstance(instance.temple_video, str):
                temple_videos = instance.temple_video.strip('[]').replace('"', '').split(',')
                temple_videos = [path.strip() for path in temple_videos]
            elif isinstance(instance.temple_video, list):
                temple_videos = [path.strip() for path in instance.temple_video if isinstance(path, str)]
            else:
                temple_videos = []
            temple_videos = [f"{settings.FILE_URL}{path}" for path in temple_videos if path and path != "null"]
            representation['temple_video'] = temple_videos
        else:
            representation['temple_video'] = []

        return representation








class CitySerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    object_id=serializers.SerializerMethodField()
   



    class Meta:
        model = Temple
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







class CitySerializer1(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()



    class Meta:
        model = Temple
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
 



 
class TempleSearch(serializers.ModelSerializer):
    

    class Meta:
        model = Temple
        fields = ["_id","name"]

 




from django.utils.timesince import timesince
from django.utils import timezone
 
class InactiveTempleSerializer(serializers.ModelSerializer):
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
            return instance.user.full_name  # assuming Register model has 'full_name' field
        return None



    class Meta:
        model = Temple
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