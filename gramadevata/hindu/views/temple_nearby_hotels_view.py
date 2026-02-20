from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from ..models import TempleNearbyHotel
from ..serializers import TempleNearbyHotelSerializer,InactiveHotelSerializer, TempleNearbyHotelSerializer1
from ..utils import save_image_to_azure 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from django.db.models import Q

class TempleNearbyHotelView(viewsets.ModelViewSet):
    queryset = TempleNearbyHotel.objects.all()
    serializer_class = TempleNearbyHotelSerializer
    # permission_classes = []  # Uncomment to apply authentication, if needed

    def list(self, request):
        filter_kwargs = {}

        # Add query params to filter
        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        # Always filter by status='ACTIVE' in GET requests
        filter_kwargs['status'] = 'ACTIVE'

        try:
            queryset = TempleNearbyHotel.objects.filter(**filter_kwargs)

            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            serialized_data = TempleNearbyHotelSerializer(queryset, many=True)
            return Response(serialized_data.data)
 
        except TempleNearbyHotel.DoesNotExist:
            return Response({
                'message': 'Objects not found',
                'status': 404
            })




    def create(self, request, *args, **kwargs):
        try:
            # Extract image_location and license_copy from request data
            image_locations = request.data.get('image_location', [])
            license_copies = request.data.get('license_copy', [])

            # Ensure both are lists
            if not isinstance(image_locations, list):
                image_locations = [image_locations]
            if not isinstance(license_copies, list):
                license_copies = [license_copies]

            # Temporarily set them to "null" for serializer
            request.data['image_location'] = "null"
            request.data['license_copy'] = "null"

            # Serialize and save
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_image_locations = []
            saved_license_copies = []

            # Save image locations
            if image_locations and "null" not in image_locations:
                entity_type = "hotels"
                for image in image_locations:
                    if image and image != "null":
                        saved_location = save_image_to_azure(
                            image,
                            serializer.instance._id,
                            serializer.instance.name,
                            entity_type
                        )
                        if saved_location:
                            saved_image_locations.append(saved_location)

            # Save license copies
            if license_copies and "null" not in license_copies:
                entity_type = "hotel_license"
                for license_file in license_copies:
                    if license_file and license_file != "null":
                        saved_location = save_image_to_azure(
                            license_file,
                            serializer.instance._id,
                            serializer.instance.name,
                            entity_type
                        )
                        if saved_location:
                            saved_license_copies.append(saved_location)

            # Save fields to model
            if saved_image_locations:
                serializer.instance.image_location = saved_image_locations
            if saved_license_copies:
                serializer.instance.license_copy = saved_license_copies
            serializer.instance.save()

            # Email notification
            created_at = timezone.now()
            user_id = request.user.id if request.user.is_authenticated else "Anonymous"

            send_mail(
                'New Temple Nearby Hotel Added',
                f'User ID: {user_id}\n'
                f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Hotel ID: {serializer.instance._id}\n'
                f'Hotel Name: {serializer.instance.name}',
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
            instance = TempleNearbyHotel.objects.get(_id=pk, status='ACTIVE')
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TempleNearbyHotel.DoesNotExist:
            return Response({
                "message": "Hotel not found",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)




    def update(self, request, pk=None, *args, **kwargs):
        try:
            instance = TempleNearbyHotel.objects.get(_id=pk, status='ACTIVE')

            image_locations = request.data.get('image_location', [])
            license_copies = request.data.get('license_copy', [])

            # Ensure lists
            if not isinstance(image_locations, list):
                image_locations = [image_locations]
            if not isinstance(license_copies, list):
                license_copies = [license_copies]

            # Keep existing values for serializer validation
            request.data['image_location'] = instance.image_location or "null"
            request.data['license_copy'] = instance.license_copy or "null"

            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=True   # supports PATCH
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_image_locations = instance.image_location or []
            saved_license_copies = instance.license_copy or []

            # Upload new hotel images
            if image_locations and "null" not in image_locations:
                entity_type = "hotels"
                for image in image_locations:
                    if image and image != "null":
                        saved_location = save_image_to_azure(
                            image,
                            instance._id,
                            instance.name,
                            entity_type
                        )
                        if saved_location:
                            saved_image_locations.append(saved_location)

            # Upload new license copies
            if license_copies and "null" not in license_copies:
                entity_type = "hotel_license"
                for license_file in license_copies:
                    if license_file and license_file != "null":
                        saved_location = save_image_to_azure(
                            license_file,
                            instance._id,
                            instance.name,
                            entity_type
                        )
                        if saved_location:
                            saved_license_copies.append(saved_location)

            # Save final fields
            if saved_image_locations:
                instance.image_location = saved_image_locations
            if saved_license_copies:
                instance.license_copy = saved_license_copies

            instance.save()

            return Response({
                "message": "Hotel updated successfully",
                "result": serializer.data
            }, status=status.HTTP_200_OK)

        except TempleNearbyHotel.DoesNotExist:
            return Response({
                "message": "Hotel not found",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class GetHotelsByLocation(APIView):
    # permission_classes = [AllowAny]

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
            TempleNearbyHotel.objects
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

        # 🔍 Search by hotel name / address / rating
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(hotel_rating__icontains=search_query)
            )

        # 🔁 Fallback: direct village
        if not queryset.exists():
            queryset = TempleNearbyHotel.objects.filter(
                village_id=input_value,
                status='ACTIVE'
            )
            if search_query:
                queryset = queryset.filter(
                    Q(name__icontains=search_query) |
                    Q(address__icontains=search_query) |
                    Q(hotel_rating__icontains=search_query)
                )

        return queryset

    def get(self, request):
        input_value = request.query_params.get('input_value')
        if not input_value:
            raise ValidationError("input_value is required")

        search_query = request.query_params.get('search', '').strip()

        hotels = self.get_queryset_filter(input_value, search_query)

        return Response({
            "nearby_hotels": TempleNearbyHotelSerializer1(hotels, many=True).data
        })













class InactiveHotelAPIView(APIView):
    """
    API to get only INACTIVE Temple Nearby Hotels
    """

    def get(self, request):
        filter_kwargs = {}
        search_query = request.query_params.get('search', None)

        # Dynamic filtering (except search)
        for key, value in request.query_params.items():
            if key != 'search':
                filter_kwargs[key] = value

        # Filter only INACTIVE hotels
        queryset = TempleNearbyHotel.objects.filter(
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

        serializer = InactiveHotelSerializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "inactive_hotels": serializer.data
        }, status=status.HTTP_200_OK)









class GetInactiveHotelsByLocation(APIView):
    # permission_classes = [AllowAny]

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
            TempleNearbyHotel.objects
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

        # 🔍 Search by hotel name / address / rating
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(hotel_rating__icontains=search_query)
            )

        # 🔁 Fallback: direct village
        if not queryset.exists():
            queryset = TempleNearbyHotel.objects.filter(
                village_id=input_value,
                status='INACTIVE'
            )
            if search_query:
                queryset = queryset.filter(
                    Q(name__icontains=search_query) |
                    Q(address__icontains=search_query) |
                    Q(hotel_rating__icontains=search_query)
                )

        return queryset

    def get(self, request):
        input_value = request.query_params.get('input_value')
        if not input_value:
            raise ValidationError("input_value is required")

        search_query = request.query_params.get('search', '').strip()

        hotels = self.get_queryset_filter(input_value, search_query)

        return Response({
            "nearby_hotels": InactiveHotelSerializer(hotels, many=True).data
        })




