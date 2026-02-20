from rest_framework import serializers
from ..models import Village,Block,Temple
from .connect_serializer import ConnectModelSerializer
from .connect_serializer import ConnectModelSerializer,ConnectModelSerializer1
from .temple_serializers import TempleSerializer1
from .goshala_serializer import GoshalaSerializerForVillage
from .event_serializer import EventSerializerForVillage
from .Transport_serializer import TempleTransportSerializer
from ..utils import image_path_to_binary
from django.db.models import Q
from .temple_nearby_hotels_serializers import TempleNearbyHotelSerializer,TempleNearbyHotelSerializer1
from .tour_guide_serializer import TourGuideSerializer
from .tour_operator_serializer import TourOperatorSerializer
from .media_serializer import MediaSerializer
from .tourismplace_serializer import TempleNearbyTourismPlaceSerializer,TourismPlacelocationSerializer
from .welfare_homes_serializer import WelfareHomeslocationSerializer
from .nearby_hospitals_serializer import NearbyHospitalSerializer,NearbyHospitalSerializer2
from .resturents_serilizers import TempleNearbyRestaurantSerializer,TempleNearbyRestaurantSerializer1,TempleNearbyRestaurantSerializer2
from .ambulance_facility_serializers import AmbulanceFacilitySerializer
from .blood_bank_serializer import BloodBankSerializer2
from .fire_station_seriliazer import FireStationSerializer1
from .police_station_serializer import PoliceStationSerializer1
from .village_geographic_serializer import VillageGeographicSerializer
from .village_famous_personalities_serializer import VillageFamousPersonalitySerializer
import base64
from .pooja_stores_serializer import PoojaStoreSerializer,PoojaStoreSerializer2
from .village_artists_serializer import VillageArtistSerializer
from .village_cultural_profile_serializer import VillageCulturalProfileSerializer
from .village_devlopment_facilities_serializer import VillageDevelopmentFacilitySerializer
from .school_serializers import VillageSchoolSerializer,VillageSchoolSerializer1
from .bank_serializers import VillageBankSerializer,VillageBankSerializer1
from .college_serializers import VillageCollegeSerializer,VillageCollegeSerializer1
from .market_serializer import VillageMarketSerializer,VillageMarketSerializer1
from .postoffice_serializers import VillagePostOfficeSerializer,VillagePostOfficeSerializer1
from .sportsground_serializer import VillageSportsgroundSerializer,VillageSportsgroundSerializer1
from .welfare_homes_serializer import WelfareHomeslocationSerializer
from ..models import WelfareHomes
from django.conf import settings
import ast



class GramadevataTempleSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()

    


    class Meta:
        model = Temple
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


class VillageSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    isvillagemember = serializers.SerializerMethodField()
    ismember = serializers.SerializerMethodField()
    ispujari = serializers.SerializerMethodField()
    isvolunteer = serializers.SerializerMethodField()
    connectionId = serializers.SerializerMethodField()
    Connections = ConnectModelSerializer1(many=True, read_only=True)
    block = serializers.SerializerMethodField()
    iconictemples = serializers.SerializerMethodField()
    famoustemples = serializers.SerializerMethodField()
    gramdeavatatemples = serializers.SerializerMethodField()
    othertemples = serializers.SerializerMethodField()
    goshalas = serializers.SerializerMethodField()
    events = serializers.SerializerMethodField()
    transport = serializers.SerializerMethodField()
    tourismplace = serializers.SerializerMethodField()
    welfare_homes=serializers.SerializerMethodField()
    nearby_hotels = serializers.SerializerMethodField()
    tour_guide = serializers.SerializerMethodField()
    touroperator = serializers.SerializerMethodField()
    image_location = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()
    near_by_hospitals = serializers.SerializerMethodField()
    # resturents=TempleNearbyRestaurantSerializer(many=True, read_only=True)
    # ambulance_facility=AmbulanceFacilitySerializer(many=True,read_only=True)
    # blood_bank=BloodBankSerializer(many=True,read_only=True)
    # fire_station=FireStationSerializer(many=True,read_only=True)
    # police_station=PoliceStationSerializer(many=True,read_only=True)
    # pooja_stores=PoojaStoreSerializer(many=True,read_only=True) 

    resturents=serializers.SerializerMethodField()
    ambulance_facility=serializers.SerializerMethodField()
    blood_bank=serializers.SerializerMethodField()
    fire_station=serializers.SerializerMethodField()
    police_station=serializers.SerializerMethodField()
    pooja_stores=serializers.SerializerMethodField()
    geographic =serializers.SerializerMethodField()
    famous_personalities =serializers.SerializerMethodField()
    village_artists =serializers.SerializerMethodField()
    village_cultural_profile =serializers.SerializerMethodField()
    village_development_facilities =serializers.SerializerMethodField()
    schools=serializers.SerializerMethodField()
    banks=serializers.SerializerMethodField()
    colleges=serializers.SerializerMethodField()
    markets=serializers.SerializerMethodField()
    postoffice=serializers.SerializerMethodField()
    sportsground=serializers.SerializerMethodField()
    welfare_homes=serializers.SerializerMethodField()
    mapUrl = serializers.SerializerMethodField()

    class Meta:
        model = Village
        fields = "__all__"
    def get_goshalas(self, obj):
        goshalas = obj.goshalas.filter(status='ACTIVE')
        return GoshalaSerializerForVillage(goshalas, many=True).data
    def get_events(self, obj):
        active_events = obj.events.filter(status='ACTIVE')
        return EventSerializerForVillage(active_events, many=True).data
    def get_transport(self, obj):
        transport = obj.transport.filter(status='ACTIVE')
        return TempleTransportSerializer(transport, many=True).data
    def get_tourismplace(self, obj):
        tourism = obj.tourismplace.filter(status='ACTIVE')
        return TourismPlacelocationSerializer(tourism, many=True).data
    def get_welfare_homes(self, obj):
        welfare_homes = obj.welfare_homes.filter(status='ACTIVE')
        return WelfareHomeslocationSerializer(welfare_homes, many=True).data
    
    def get_nearby_hotels(self, obj):
        hotels = obj.nearby_hotels.filter(status='ACTIVE')
        return TempleNearbyHotelSerializer1(hotels, many=True).data
    def get_tour_guide(self, obj):
        guides = obj.tour_guide.filter(status='ACTIVE')
        return TourGuideSerializer(guides, many=True).data
    def get_touroperator(self, obj):
        operators = obj.touroperator.filter(status='ACTIVE')
        return TourOperatorSerializer(operators, many=True).data
    def get_media(self, obj):
        media = obj.media.filter(status='ACTIVE')
        return MediaSerializer(media, many=True).data
    def get_near_by_hospitals(self, obj):
        hospitals = obj.near_by_hospitals.filter(status='ACTIVE')
        return NearbyHospitalSerializer2(hospitals, many=True).data
    
    def get_resturents(self, obj):
        active = obj.resturents.filter(status='ACTIVE')
        return TempleNearbyRestaurantSerializer2(active, many=True).data
    

    def get_pooja_stores(self, obj):
        active = obj.pooja_stores.filter(status='ACTIVE')
        return PoojaStoreSerializer2(active, many=True).data


    def get_ambulance_facility(self, obj):
        active = obj.ambulance_facility.filter(status='ACTIVE')
        return AmbulanceFacilitySerializer(active, many=True).data
    
    def get_blood_bank(self, obj):
        active = obj.blood_bank.filter(status='ACTIVE')
        return BloodBankSerializer2(active, many=True).data
    
    def get_fire_station(self, obj):
        active = obj.fire_station.filter(status='ACTIVE')
        return FireStationSerializer1(active, many=True).data
    
    def get_police_station(self, obj):
        active = obj.police_station.filter(status='ACTIVE')
        return PoliceStationSerializer1(active, many=True).data
    
    def get_geographic(self, obj):
        active = obj.geographic.filter(status='ACTIVE')
        return VillageGeographicSerializer(active, many=True).data
    
    def get_famous_personalities(self, obj):
        active = obj.famous_personalities.filter(status='ACTIVE')
        return VillageFamousPersonalitySerializer(active, many=True).data
    
    def get_village_artists(self, obj):
        active = obj.village_artists.filter(status='ACTIVE')
        return VillageArtistSerializer(active, many=True).data
    
    def get_village_cultural_profile(self, obj):
        active = obj.village_cultural_profile.filter(status='ACTIVE')
        return VillageCulturalProfileSerializer(active, many=True).data
    
    def get_village_development_facilities(self, obj):
        active = obj.village_development_facilities.filter(status='ACTIVE')
        return VillageDevelopmentFacilitySerializer(active, many=True).data
    
    def get_schools(self, obj):
        active = obj.schools.filter(status='ACTIVE')
        return VillageSchoolSerializer1(active, many=True).data
    
    def get_banks(self, obj):
        active = obj.banks.filter(status='ACTIVE')
        return VillageBankSerializer1(active, many=True).data
    
    def get_colleges(self, obj):
        active = obj.colleges.filter(status='ACTIVE')
        return VillageCollegeSerializer1(active, many=True).data
    
    def get_markets(self, obj):
        active = obj.markets.filter(status='ACTIVE')
        return VillageMarketSerializer1(active, many=True).data
    
    def get_postoffice(self, obj):
        active = obj.postoffice.filter(status='ACTIVE')
        return VillagePostOfficeSerializer1(active, many=True).data
    
    def get_sportsground(self, obj):
        active = obj.sportsground.filter(status='ACTIVE')
        return VillageSportsgroundSerializer1(active, many=True).data
    
   

    
    def get_user_id(self, obj):
        request = self.context.get('request')
        return request.user.id if request and request.user.is_authenticated else None

    def get_connectionId(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            connection = obj.Connections.filter(user__id=request.user.id).first()
            return connection._id if connection else None
        return None

    def get_isvillagemember(self, obj):
        request = self.context.get('request')
        return obj.Connections.filter(user__id=request.user.id).exists() if request and request.user.is_authenticated else False

    def get_ismember(self, obj):
        request = self.context.get('request')
        return obj.Connections.filter(user__id=request.user.id, connected_as="MEMBER").exists() if request and request.user.is_authenticated else False

    def get_ispujari(self, obj):
        request = self.context.get('request')
        return obj.Connections.filter(user__id=request.user.id, connected_as="PUJARI").exists() if request and request.user.is_authenticated else False
    

    def get_isvolunteer(self, obj):
        request = self.context.get('request')
        return obj.Connections.filter(user__id=request.user.id, connected_as="VOLUNTARY").exists() if request and request.user.is_authenticated else False
    
    def get_mapUrl(self, instance):
        raw = instance.mapUrl
        # Already correct
        if isinstance(raw, list):
            return raw
        # Empty
        if not raw:
            return []
        # Convert "['url']" → ['url']
        if isinstance(raw, str):
            try:
                parsed = ast.literal_eval(raw)
                if isinstance(parsed, list):
                    return parsed
            except:
                pass
            # Fallback single string
            return [raw]
        return []





    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # VILLAGE VIDEO
        if instance.village_video and instance.village_video != "null":
            if isinstance(instance.village_video, str):
                video_paths = instance.village_video.strip('[]').replace('"', '').split(',')
                video_paths = [path.strip() for path in video_paths if path.strip()]
            elif isinstance(instance.village_video, list):
                video_paths = [path.strip() for path in instance.village_video if isinstance(path, str) and path.strip()]
            else:
                video_paths = []
            representation['village_video'] = [f"{settings.FILE_URL}{path}" for path in video_paths]
        else:
            representation['village_video'] = []

        return representation



    def get_image_location(self, instance):
        base_url = "https://sathayushstorage.blob.core.windows.net/sathayush/"
        
        raw_list = instance.image_location

        # Handle if it's a string, list, or other
        if isinstance(raw_list, list):
            image_list = raw_list
        elif isinstance(raw_list, str):
            image_list = raw_list.split(",")
        else:
            image_list = []

        cleaned = []
        for url in image_list:
            url = url.strip()
            if url.startswith('["'):
                url = url[2:]
            if url.endswith('"]'):
                url = url[:-2]
            url = url.replace('\\', '/')  # fix backslashes
            
            # Prepend base URL if not already included
            if not url.startswith("http"):
                url = base_url + url
            
            cleaned.append(url)

        return cleaned

    def get_block(self, instance):
        block = instance.block
        if block:
            return {
                "id": block._id,
                "name": block.name,
                "district": {
                    "districtid": str(block.district.pk),
                    "name": block.district.name,
                    "state": {
                        "stateid": str(block.district.state.pk),
                        "name": block.district.state.name,
                        "country": {
                            "countryid": str(block.district.state.country.pk),
                            "name": block.district.state.country.name
                        }
                    }
                }
            }
        return None

    from django.db.models import Q

    def get_filtered_temples(self, instance):
        temples = instance.temples.filter(status="ACTIVE")  # Apply status filter globally if all should be active
        return {
            "iconic": GramadevataTempleSerializer(
                temples.filter(priority="d7df749f-97e8-4635-a211-371c44b3c31f"), many=True
            ).data,
            "famous": GramadevataTempleSerializer(
                temples.filter(priority="630f3239-f515-47fb-be8d-db727b9f2174"), many=True
            ).data,
            "gramdevata": GramadevataTempleSerializer(
                temples.filter(
                    category="742ccfe6-d0b5-11ee-84bd-0242ac110002"
                ).exclude(
                    priority__in=["d7df749f-97e8-4635-a211-371c44b3c31f", "630f3239-f515-47fb-be8d-db727b9f2174"]
                ),
                many=True
            ).data,
            "others": GramadevataTempleSerializer(
                temples.exclude(
                    Q(category="742ccfe6-d0b5-11ee-84bd-0242ac110002") |
                    Q(priority__in=["d7df749f-97e8-4635-a211-371c44b3c31f", "630f3239-f515-47fb-be8d-db727b9f2174"])
                ),
                many=True
            ).data,
        }



    def get_iconictemples(self, instance):
        return self.get_filtered_temples(instance)["iconic"]

    def get_famoustemples(self, instance):
        return self.get_filtered_temples(instance)["famous"]

    def get_gramdeavatatemples(self, instance):
        return self.get_filtered_temples(instance)["gramdevata"]

    def get_othertemples(self, instance):
        return self.get_filtered_temples(instance)["others"]



# class VillageSerializer1(serializers.ModelSerializer):

#     image_location = serializers.SerializerMethodField()

#     block = serializers.SerializerMethodField()

#     def get_image_location(self, instance):
#         base_url = "https://sathayushstorage.blob.core.windows.net/sathayush/"
        
#         raw_list = instance.image_location

#         # Handle if it's a string, list, or other
#         if isinstance(raw_list, list):
#             image_list = raw_list
#         elif isinstance(raw_list, str):
#             image_list = raw_list.split(",")
#         else:
#             image_list = []

#         cleaned = []
#         for url in image_list:
#             url = url.strip()
#             if url.startswith('["'):
#                 url = url[2:]
#             if url.endswith('"]'):
#                 url = url[:-2]
#             url = url.replace('\\', '/')  # fix backslashes
            
#             # Prepend base URL if not already included
#             if not url.startswith("http"):
#                 url = base_url + url
            
#             cleaned.append(url)

#         return cleaned
#     # def get_image_location(self, instance):

#     #         filename = instance.image_location
#     #         if filename:
#     #             format= image_path_to_binary(filename)
#     #             # print(format,"******************")
#     #             return format
#     #         return None
    
#     def get_block(self, instance):
#         block = instance.block
#         if block:
#             return {
#                 "id": block._id,
#                 "name": block.name,
#                 "district": {
#                     "districtid": str(block.district.pk),
#                     "name": block.district.name,
#                     "state": {
#                         "stateid": str(block.district.state.pk),
#                         "name": block.district.state.name,
#                         "country": {
#                             "countryid": str(block.district.state.country.pk),
#                             "name": block.district.state.country.name
#                         }
#                     }
#                 }
#             }
        
#     class Meta:
#         model = Village
#         fields = "__all__"



from django.utils.timesince import timesince
from django.utils import timezone




class VillageSerializer2(serializers.ModelSerializer):
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
    
    class Meta:
        model = Village
        fields = "__all__"







class VillageSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model  =  Village
        fields = ["_id", "name", "block_id"]





# class VillageSerializer3(serializers.ModelSerializer):
#     image_location = serializers.SerializerMethodField()

#     def get_image_location(self, instance):
#         filename = instance.image_location
        
#         # Check if filename is a list or a string
#         if isinstance(filename, list):
#             # If it's already a list, return it as is
#             image_paths = filename
#         elif isinstance(filename, str):
#             # If it's a string, attempt to parse it as a list-like string
#             image_paths = filename.strip('[]').replace('"', '').split(',')
#             image_paths = [path.strip() for path in image_paths]  # Clean up any extra spaces
#         else:
#             # If it's neither a list nor a string, return an empty list
#             image_paths = []

#         # Apply binary conversion (assuming `image_path_to_binary` is defined)
#         return [image_path_to_binary(path) for path in image_paths]

#     class Meta:
#         model  =  Village
#         fields = ["_id", "name", "image_location"]


class VillageSerializer3(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    location_hierarchy = serializers.SerializerMethodField()

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

    def get_location_hierarchy(self, instance):
        village = instance

        try:
            return {
                "village_id": str(village._id),
                "village_name": village.name,
                "block": {
                    "block_id": str(village.block.pk),
                    "block_name": village.block.name,
                    "district": {
                        "district_id": str(village.block.district.pk),
                        "district_name": village.block.district.name,
                        "state": {
                            "state_id": str(village.block.district.state.pk),
                            "state_name": village.block.district.state.name,
                            "country": {
                                "country_id": str(village.block.district.state.country.pk),
                                "country_name": village.block.district.state.country.name
                            }
                        }
                    }
                }
            }
        except AttributeError:
            return None  # Safely handle missing links

    class Meta:
        model = Village
        fields = ["_id", "name", "image_location", "location_hierarchy"]





class VillageSerializer1(serializers.ModelSerializer):
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
        model = Village
        fields = ["_id", "name", "image_location"]






class VillageSearch(serializers.ModelSerializer):
    
    class Meta:
        model = Village
        fields = ["_id", "name"]
