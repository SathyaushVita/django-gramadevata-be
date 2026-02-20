from rest_framework.views import APIView
from ..models import TempleCategory,GoshalaCategory,EventCategory, Village,TempleMainCategory,WelfareHomesCategory
from ..serializers import TempleCategeorySerializer,GoshalaCategorySerializer,EventCategorySerializer,VillageSerializer1,TempleMainCategorySerializer,VillageSerializer3,WelfareHomesCategorySerializer
from rest_framework .response import Response
from ..models import TempleNearbyTourismPlace
from ..serializers import TourismPlaceSerializer
class HomeView(APIView):

    def get(self, request):  

        villages_id = [
            "1ce1e51e-c342-474c-a088-ca5d627675b9",
            "823149ee-5416-4727-bd63-ac3854fa0e0b",
            "a1f8be42-e035-4b7b-876c-c41e04bccc59",
            "51c77edf-f74d-4024-9119-9b879dceb07f"
        ]

        villages_data=[]
        for _id in villages_id:
            villages = Village.objects.filter(_id=_id)
            village_gb=VillageSerializer1(villages,many=True)
            villages_data.extend(village_gb.data)

 
        main_categories_id = [
            "e9e8933f-81ee-42bd-9b6d-e923d30d2e5b",
            "64dece57-7b94-4eb1-b31c-884bfa57fcce",
            "ed4b72fd-5dd7-4749-9852-a4483899642b",
            "56ee646b-8370-4129-84f5-22af7ed538e5"
        ]

        temple_categories_data = []
        for _id in main_categories_id:
            temple_categories = TempleMainCategory.objects.filter(_id=_id)
            temples = TempleMainCategorySerializer(temple_categories, many=True)
            temple_categories_data.extend(temples.data)

# Now temple_categories_data contains all the data in one list



        goshala_categories = GoshalaCategory.objects.all()[:4]
        goshala = GoshalaCategorySerializer(goshala_categories, many=True)

        event_id =[
            "1cb6a4e7-0491-4516-b096-4c80b8f3caa7",
            "7426b52b-4046-4fe8-9d04-278a9d3562f8",
            "d8d437e8-1a6c-49ea-8cb6-55398bfd0989",
            "a03301df-2f2b-47de-a23d-98b186ed7aca",
        ]
        event_categories_data =[]
        for _id in event_id:
            event_categories = EventCategory.objects.filter(_id=_id)
            event = EventCategorySerializer(event_categories, many=True)
            event_categories_data.extend(event.data)

        tourism_ids = [
            "72a6dd8b-cda6-4eae-b24c-2daadc0f7ae8",
            "96f00598-4daf-11f0-99f8-07abcecb4bc0",
            "2c8f5aa8-4db1-11f0-99f8-07abcecb4bc0",
            "ce654792-4db2-11f0-99f8-07abcecb4bc0"
        ]
        tourism_places_data = []
        for _id in tourism_ids:
            places = TempleNearbyTourismPlace.objects.filter(_id=_id)
            serializer = TourismPlaceSerializer(places, many=True)
            tourism_places_data.extend(serializer.data)
        welfare_home_ids = [
            "d8cd9184-8648-4f94-92c9-8474c396bc37",
            "1c425c71-eea2-4f8b-ad40-d6d2d1deb71f",
            "0760ac6f-b62a-487a-9204-9f5491a91dce",
            "3f159e97-19cf-418d-a99d-9b696c969257",
        ]

        welfare_homes_data = []
        for _id in welfare_home_ids:
            homes = WelfareHomesCategory.objects.filter(_id=_id)
            serializer = WelfareHomesCategorySerializer(homes, many=True)
            welfare_homes_data.extend(serializer.data)
            
        return Response({
            "villages":villages_data,
            "templeCategories": temple_categories_data,
            "goshalaCategories": goshala.data,
            "eventCategories": event_categories_data,
            "tourismPlaces": tourism_places_data, 
            "welfareHomes": welfare_homes_data


        })


