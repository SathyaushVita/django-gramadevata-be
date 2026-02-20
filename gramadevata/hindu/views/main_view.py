from rest_framework.views import APIView, status
from ..models .temple_categeory import TempleCategory
from ..models .temple import Temple
from ..models .goshala import Goshala
from ..models .goshala_category import GoshalaCategory
from rest_framework.response import Response
from ..serializers import *
from ..models .village import Village
from ..models.event import Event
from ..models.event_category import EventCategory1





class TempleMain(APIView):
    def get(self, request, *args, **kwargs):
        try:
            categories_id = [
            "742ecf7b-d0b5-11ee-84bd-0242ac110002",
            "742f645c-d0b5-11ee-84bd-0242ac110002",
            "74353e76-d0b5-11ee-84bd-0242ac110002",
            "74344055-d0b5-11ee-84bd-0242ac110002"
        ]

            temple_categories_data = []
            for _id in categories_id:
                temple_categories = TempleCategory.objects.filter(_id=_id)
                temples = TempleCategeorySerializer(temple_categories, many=True)
                temple_categories_data.extend(temples.data)
            # india = country_query_set.filter(name__iexact='India').first()
            indian_location = Village.objects.all()

            temple_query_set = Temple.objects.all()
            indian_temples = temple_query_set.filter(object_id__in=indian_location)[:4]
            # print(indian_temples,"22222222222222222222")
            
            # Filter out global temples based on geo_site condition
            # global_temples = [temple for temple in temple_query_set.exclude(object_id__in=indian_location)[:5] if temple.geo_site not in ['S', 'D', 'B', 'V']]
            global_temples = temple_query_set.exclude(object_id__in=indian_location).exclude(geo_site__in=['S', 'D', 'B', 'V'])[:4]
            # print(global_temples,"333333333333333333333333")

            categorySerializer = categories_id
            # print(categorySerializer,"44444444444444444")
            indianTempleSerializer = TempleDetailSerializer(indian_temples, many=True)
            # print(indianTempleSerializer,"5555555555555555555")
            globalTempleSerializer = TempleDetailSerializer(global_temples, many=True)
            # print(globalTempleSerializer,"66666666666666666666")
            return Response({'categories': temple_categories_data, 'indianTemples': indianTempleSerializer.data, 'globalTemples': globalTempleSerializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error':'Something went Wrong'},status=status.HTTP_400_BAD_REQUEST)




class GoshalaMain(APIView):
    def get(self, request):
        goshala_category = GoshalaCategory.objects.all()[:4]
        goshala_query_set = Goshala.objects.all()
        india_location = Village.objects.all()
        indian_goshalas = goshala_query_set.filter(object_id__in=india_location)[:4]
        global_goshalas = goshala_query_set.exclude(object_id__in=india_location).exclude(geo_site__in=[ 'D', 'B', 'V'])[:4]

        goshalacategory = GoshalaCategorySerializer(goshala_category, many=True)
        indiangoshalas = GoshalaSerializer1(indian_goshalas, many=True)
        globalgoshalas = GoshalaSerializer1(global_goshalas, many=True)   

        return Response({
            'categories': goshalacategory.data,
            'indiangoshalas': indiangoshalas.data,
            "globalgoshalas": globalgoshalas.data
        })
    

class EventsMain(APIView):
    def get(self, request):
        event_category = EventCategory.objects.all()[:4]
        event_query_set = Event.objects.all()
        india_location = Village.objects.all()
        indian_events = event_query_set.filter(object_id__in=india_location)[:4]
        global_events = event_query_set.exclude(object_id__in=india_location).exclude(geo_site__in=['S', 'D', 'B', 'V'])[:4]

        eventcategory = EventCategorySerializer(event_category, many=True)
        indianevents = EventSerializer1(indian_events, many=True)
        globalevents = EventSerializer1(global_events, many=True)   

        return Response({
            'categories': eventcategory.data,
            'indianevents': indianevents.data,
            "globalevents": globalevents.data
        })