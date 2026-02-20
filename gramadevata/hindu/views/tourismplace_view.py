from rest_framework import status, viewsets
from rest_framework.response import Response
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from ..models import TempleNearbyTourismPlace,Temple,Goshala,Event
from ..serializers import TempleNearbyTourismPlaceSerializer,TempleSerializer,GoshalaSerializer,StateSerializer1,CitySerializer1
from ..utils import save_image_to_azure,save_image_to_azure1 

class TempleNearbyTourismPlacesView(viewsets.ModelViewSet):
    queryset = TempleNearbyTourismPlace.objects.all()
    serializer_class = TempleNearbyTourismPlaceSerializer

    def list(self, request):
        filter_kwargs = {}

        # Collect query params into filter kwargs
        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        # Always ensure status='ACTIVE'
        filter_kwargs['status'] = 'ACTIVE'

        try:
            queryset = TempleNearbyTourismPlace.objects.filter(**filter_kwargs)

            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            serialized_data = TempleNearbyTourismPlaceSerializer(queryset, many=True)
            return Response(serialized_data.data)

        except TempleNearbyTourismPlace.DoesNotExist:
            return Response({
                'message': 'Objects not found',
                'status': 404
            })




    def create(self, request, *args, **kwargs):
        try:
            image_locations = request.data.get('image_location', [])

            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            request.data['image_location'] = "null"

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            instance = serializer.instance
            saved_locations = []
            entity_type = "tourism"

            for image_location in image_locations:
                if image_location and image_location != "null":
                    saved_location = save_image_to_azure1(
                        image_location,
                        instance._id,
                        instance.name,
                        entity_type
                    )
                    if saved_location:
                        saved_locations.append(saved_location)

            if saved_locations:
                instance.image_location = saved_locations
                instance.save()

            created_at = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

            user_id = request.user.id if request.user.is_authenticated else "Anonymous"
            user_email = getattr(request.user, 'email', None)
            user_name = getattr(request.user, 'full_name', 'User')

            # ==================================
            # ✅ Email to Admin
            # ==================================
            send_mail(
                'New Temple Nearby Tourism Place Added',
                f'User ID: {user_id}\n'
                f'Created Time: {created_at}\n'
                f'Tourism Place ID: {instance._id}\n'
                f'Tourism Place Name: {instance.name}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            # ==================================
            # ✅ Email to Same User
            # ==================================
            if request.user.is_authenticated and user_email:
                send_mail(
                    'Tourism Place Submission Successful',
                    f'Dear {user_name},\n\n'
                    f'Your tourism place "{instance.name}" has been successfully submitted.\n\n'
                    f"currently under review by our team.\n\n"
                    f"You will be notified once the review process is completed.\n\n"
                    f"Thank you for your valuable contribution.\n\n"
                    f'Regards,\n'
                    f'Gramadevata Admin Team',
                    settings.EMAIL_HOST_USER,
                    [user_email],
                    fail_silently=False,
                )

            return Response({
                "message": "success",
                "result": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    # def create(self, request, *args, **kwargs):
    #     try:
    #         # Extract image_location from request data
    #         image_locations = request.data.get('image_location', [])

    #         # If image_location is not a list, convert it to a list
    #         if not isinstance(image_locations, list):
    #             image_locations = [image_locations]

    #         # Temporarily set image_location to "null" for serializer
    #         request.data['image_location'] = "null"

    #         # Serialize data and save
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()

    #         saved_locations = []  # To store valid saved locations

    #         # Check if image locations exist and are not null
    #         if image_locations and "null" not in image_locations:
    #             entity_type = "tourism"

    #             # Process each image location
    #             for image_location in image_locations:
    #                 if image_location and image_location != "null":
    #                     saved_location = save_image_to_azure1(
    #                         image_location,
    #                         serializer.instance._id,
    #                         serializer.instance.name,
    #                         entity_type
    #                     )
    #                     if saved_location:
    #                         saved_locations.append(saved_location)  # Add to list

    #         # If there are saved locations, update the instance's image_location field
    #         if saved_locations:
    #             serializer.instance.image_location = saved_locations  # Save as a list
    #             serializer.instance.save()

    #         created_at = timezone.now()
    #         user_id = request.user.id if request.user.is_authenticated else "Anonymous"

    #         # Send email to EMAIL_HOST_USER (you can modify this part as needed)
    #         send_mail(
    #             'New Temple Nearby Tourism Place Added',
    #             f'User ID: {user_id}\n'
    #             f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
    #             f'Tourism Place ID: {serializer.instance._id}\n'
    #             f'Tourism Place Name: {serializer.instance.name}',
    #             settings.EMAIL_HOST_USER,
    #             [settings.EMAIL_HOST_USER],
    #             fail_silently=False,
    #         )

    #         return Response({
    #             "message": "success",
    #             "result": serializer.data
    #         }, status=status.HTTP_201_CREATED)

    #     except Exception as e:
    #         return Response({
    #             "message": "An error occurred.",
    #             "error": str(e)
    #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def retrieve(self, request, pk=None):
        try:
            # Get the tourism place
            instance = TempleNearbyTourismPlace.objects.get(_id=pk, status='ACTIVE')

            # Get linked village
            village = instance.village_id
            if not village:
                return Response({
                    "message": "No village linked to this tourism place",
                    "status": 400
                }, status=status.HTTP_400_BAD_REQUEST)

            # Get block
            block = village.block
            if not block:
                return Response({
                    "message": "Village has no block associated",
                    "status": 400
                }, status=status.HTTP_400_BAD_REQUEST)

            # Get related temples and goshalas
            temples = Temple.objects.filter(object_id__block=block, status='ACTIVE')
            goshalas = Goshala.objects.filter(object_id__block=block, status='ACTIVE')
            events = Event.objects.filter(object_id__block=block, status='ACTIVE')
            # Serialize tourism place
            tourism_data = TempleNearbyTourismPlaceSerializer(instance).data

            # Add related data to same JSON
            tourism_data["temple"] = CitySerializer1(temples, many=True).data
            tourism_data["goshala"] = StateSerializer1(goshalas, many=True).data
            tourism_data["event"] = StateSerializer1(events, many=True).data

            return Response(tourism_data, status=status.HTTP_200_OK)

        except TempleNearbyTourismPlace.DoesNotExist:
            return Response({
                "message": "Tourism Place not found",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)





from django.db.models import Q
from rest_framework.exceptions import ValidationError

from rest_framework import viewsets, generics,status
from ..models import TempleNearbyHotel,TempleNearbyRestaurant,TempleTransport,TourOperator,TourGuide,NearbyHospital
from ..serializers import TempleNearbyHotelSerializer,TempleNearbyRestaurantSerializer,TempleTransportSerializer,TourOperatorSerializer,TourGuideSerializer,NearbyHospitalSerializer,TourismPlaceSerializer


from rest_framework .views import APIView







# class GetTourismByLocation(APIView):

#     def get_queryset_filter(self, model, input_value, search_query=None):
#         country_query = Q(village_id__block__district__state__country__pk=input_value)
#         state_query = Q(village_id__block__district__state__pk=input_value)
#         district_query = Q(village_id__block__district__pk=input_value)
#         block_query = Q(village_id__block__pk=input_value)
#         village_query = Q(village_id__pk=input_value)

#         combined_query = country_query | state_query | district_query | block_query | village_query

#         queryset = model.objects.filter(combined_query, status='ACTIVE').select_related(
#             'village_id__block__district__state__country',
#             'village_id__block__district__state',
#             'village_id__block__district',
#             'village_id__block',
#             'village_id',
#         )

#         if search_query:
#             # Search in both name and address
#             queryset = queryset.filter(
#                 Q(name__icontains=search_query) | Q(address__icontains=search_query)
#             )

#         if not queryset.exists():
#             queryset = model.objects.filter(village_id=input_value, status='ACTIVE')
#             if search_query:
#                 queryset = queryset.filter(
#                     Q(name__icontains=search_query) | Q(address__icontains=search_query)
#                 )

#         return queryset

#     def get(self, request):
#         input_value = request.query_params.get('input_value')
#         if not input_value:
#             raise ValidationError("input_value is required.")

#         search_query = request.query_params.get('search', '').strip()  # get search text

#         tourism_places = self.get_queryset_filter(TempleNearbyTourismPlace, input_value, search_query)

#         return Response({
#             "tourism_places": TourismPlaceSerializer(tourism_places, many=True).data,
#         })




from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


@method_decorator(cache_page(60 * 5), name='get')  # 5 minutes cache
class GetTourismByLocation(APIView):

    def get_queryset(self, model, input_value, search_query=None):

        base_filter = Q(status='ACTIVE')

        location_filter = (
            Q(village_id=input_value) |
            Q(village_id__block_id=input_value) |
            Q(village_id__block__district_id=input_value) |
            Q(village_id__block__district__state_id=input_value) |
            Q(village_id__block__district__state__country_id=input_value)
        )

        queryset = model.objects.filter(base_filter & location_filter)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query)
            )

        return queryset.select_related(
            'village_id',
            'village_id__block',
            'village_id__block__district',
            'village_id__block__district__state',
            'village_id__block__district__state__country'
        )

    def get(self, request):
        input_value = request.query_params.get('input_value')
        if not input_value:
            raise ValidationError("input_value is required.")

        search_query = request.query_params.get('search', '').strip()

        tourism_places = self.get_queryset(
            TempleNearbyTourismPlace,
            input_value,
            search_query
        )

        return Response({
            "tourism_places": TourismPlaceSerializer(tourism_places, many=True).data
        })








from ..serializers import TourismPlaceInactiveSerializer
from ..enums import EntityStatus

class InactiveTourismPlaceAPIView(APIView):


    def get(self, request):
        queryset = TempleNearbyTourismPlace.objects.filter(
            status=EntityStatus.INACTIVE.value
        )

        # search param
        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(address__icontains=search)
            )

        # recent first
        queryset = queryset.order_by("-created_at")

        if not queryset.exists():
            return Response(
                {"message": "Data not found", "count": 0, "results": []},
                status=status.HTTP_200_OK
            )

        serializer = TourismPlaceInactiveSerializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "results": serializer.data
        }, status=status.HTTP_200_OK)





















@method_decorator(cache_page(60 * 5), name='get')  # 5 minutes cache
class GetInactiveTourismByLocation(APIView):

    def get_queryset(self, model, input_value, search_query=None):

        base_filter = Q(status='INACTIVE')

        location_filter = (
            Q(village_id=input_value) |
            Q(village_id__block_id=input_value) |
            Q(village_id__block__district_id=input_value) |
            Q(village_id__block__district__state_id=input_value) |
            Q(village_id__block__district__state__country_id=input_value)
        )

        queryset = model.objects.filter(base_filter & location_filter)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query)
            )

        return queryset.select_related(
            'village_id',
            'village_id__block',
            'village_id__block__district',
            'village_id__block__district__state',
            'village_id__block__district__state__country'
        )

    def get(self, request):
        input_value = request.query_params.get('input_value')
        if not input_value:
            raise ValidationError("input_value is required.")

        search_query = request.query_params.get('search', '').strip()

        tourism_places = self.get_queryset(
            TempleNearbyTourismPlace,
            input_value,
            search_query
        )

        return Response({
            "tourism_places": TourismPlaceSerializer(tourism_places, many=True).data
        })


