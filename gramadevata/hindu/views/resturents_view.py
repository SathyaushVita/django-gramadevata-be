from rest_framework import status, viewsets
from rest_framework.response import Response
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from ..models import TempleNearbyRestaurant
from ..serializers import TempleNearbyRestaurantSerializer,InactiveRestaurantSerializer
from ..utils import save_image_to_azure

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from django.db.models import Q

from ..serializers import TempleNearbyRestaurantSerializer1

class TempleNearbyRestaurantView(viewsets.ModelViewSet):
    queryset = TempleNearbyRestaurant.objects.all()
    serializer_class = TempleNearbyRestaurantSerializer

    def list(self, request):
        filter_kwargs = {}

        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        filter_kwargs['status'] = 'ACTIVE'

        try:
            queryset = TempleNearbyRestaurant.objects.filter(**filter_kwargs)

            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            serialized_data = self.get_serializer(queryset, many=True)
            return Response(serialized_data.data)

        except TempleNearbyRestaurant.DoesNotExist:
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

            saved_locations = []
            if image_locations and "null" not in image_locations:
                entity_type = "restaurants"

                for image_location in image_locations:
                    if image_location and image_location != "null":
                        saved_location = save_image_to_azure(
                            image_location,
                            serializer.instance._id,
                            serializer.instance.name,
                            entity_type
                        )
                        if saved_location:
                            saved_locations.append(saved_location)

            if saved_locations:
                serializer.instance.image_location = saved_locations
                serializer.instance.save()

            created_at = timezone.now()
            user_id = request.user.id if request.user.is_authenticated else "Anonymous"

            send_mail(
                'New Temple Nearby Restaurant Added',
                f'User ID: {user_id}\n'
                f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Restaurant ID: {serializer.instance._id}\n'
                f'Restaurant Name: {serializer.instance.name}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
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

    def retrieve(self, request, pk=None):
        try:
            instance = TempleNearbyRestaurant.objects.get(_id=pk, status='ACTIVE')
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TempleNearbyRestaurant.DoesNotExist:
            return Response({
                "message": "Restaurant not found",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)



    def update(self, request, pk=None, *args, **kwargs):
        try:
            instance = TempleNearbyRestaurant.objects.get(_id=pk, status='ACTIVE')

            image_locations = request.data.get('image_location', [])

            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            # Keep existing images for serializer validation
            request.data['image_location'] = instance.image_location or "null"

            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=True   # supports PATCH also
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_locations = instance.image_location or []

            if image_locations and "null" not in image_locations:
                entity_type = "restaurants"

                for image_location in image_locations:
                    if image_location and image_location != "null":
                        saved_location = save_image_to_azure(
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

            return Response({
                "message": "Restaurant updated successfully",
                "result": serializer.data
            }, status=status.HTTP_200_OK)

        except TempleNearbyRestaurant.DoesNotExist:
            return Response({
                "message": "Restaurant not found",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










class GetRestaurantsByLocation(APIView):

    def get_queryset_filter(self, input_value, search_query=None):
        country_query = Q(village_id__block__district__state__country__pk=input_value)
        state_query = Q(village_id__block__district__state__pk=input_value)
        district_query = Q(village_id__block__district__pk=input_value)
        block_query = Q(village_id__block__pk=input_value)
        village_query = Q(village_id__pk=input_value)

        combined_query = (
            country_query |
            state_query |
            district_query |
            block_query |
            village_query
        )

        queryset = (
            TempleNearbyRestaurant.objects
            .filter(combined_query, status='ACTIVE')
            .select_related(
                'village_id',
                'village_id__block',
                'village_id__block__district',
                'village_id__block__district__state',
                'village_id__block__district__state__country',
                'temple_id',
                'event_id',
                'tourism_places'
            )
        )

        # 🔍 Search by restaurant name / address
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query)
            )

        # 🔁 Fallback: direct village
        if not queryset.exists():
            queryset = TempleNearbyRestaurant.objects.filter(
                village_id=input_value,
                status='ACTIVE'
            )
            if search_query:
                queryset = queryset.filter(
                    Q(name__icontains=search_query) |
                    Q(address__icontains=search_query)
                )

        return queryset

    def get(self, request):
        input_value = request.query_params.get('input_value')
        if not input_value:
            raise ValidationError("input_value is required")

        search_query = request.query_params.get('search', '').strip()

        restaurants = self.get_queryset_filter(input_value, search_query)

        return Response({
            "nearby_restaurants": TempleNearbyRestaurantSerializer1(restaurants, many=True).data
        })









class InactiveRestaurantAPIView(APIView):
    """
    API to get only INACTIVE Temple Nearby Restaurants
    """

    def get(self, request):
        filter_kwargs = {}
        search_query = request.query_params.get('search', None)

        # Dynamic filtering (except search)
        for key, value in request.query_params.items():
            if key != 'search':
                filter_kwargs[key] = value

        # Filter only INACTIVE records
        queryset = TempleNearbyRestaurant.objects.filter(
            status='INACTIVE',
            **filter_kwargs
        )

        # Search by name or address
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query)
            )

        queryset = queryset.order_by('-created_at')

        if not queryset.exists():
            return Response(
                {"message": "Data not found", "status": 404},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = InactiveRestaurantSerializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "inactive_restaurants": serializer.data
        }, status=status.HTTP_200_OK)
    











class GetInactiveRestaurantsByLocation(APIView):

    def get_queryset_filter(self, input_value, search_query=None):
        country_query = Q(village_id__block__district__state__country__pk=input_value)
        state_query = Q(village_id__block__district__state__pk=input_value)
        district_query = Q(village_id__block__district__pk=input_value)
        block_query = Q(village_id__block__pk=input_value)
        village_query = Q(village_id__pk=input_value)

        combined_query = (
            country_query |
            state_query |
            district_query |
            block_query |
            village_query
        )

        queryset = (
            TempleNearbyRestaurant.objects
            .filter(combined_query, status='INACTIVE')
            .select_related(
                'village_id',
                'village_id__block',
                'village_id__block__district',
                'village_id__block__district__state',
                'village_id__block__district__state__country',
                'temple_id',
                'event_id',
                'tourism_places'
            )
        )

        # 🔍 Search by restaurant name / address
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query)
            )

        # 🔁 Fallback: direct village
        if not queryset.exists():
            queryset = TempleNearbyRestaurant.objects.filter(
                village_id=input_value,
                status='INACTIVE'
            )
            if search_query:
                queryset = queryset.filter(
                    Q(name__icontains=search_query) |
                    Q(address__icontains=search_query)
                )

        return queryset

    def get(self, request):
        input_value = request.query_params.get('input_value')
        if not input_value:
            raise ValidationError("input_value is required")

        search_query = request.query_params.get('search', '').strip()

        restaurants = self.get_queryset_filter(input_value, search_query)

        return Response({
            "nearby_restaurants": InactiveRestaurantSerializer(restaurants, many=True).data
        })




