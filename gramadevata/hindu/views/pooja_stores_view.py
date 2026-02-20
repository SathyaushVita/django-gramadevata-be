from rest_framework import status, viewsets
from rest_framework.response import Response
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from ..models import PoojaStore
from ..serializers import PoojaStoreSerializer
from ..utils import save_image_to_azure  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q

from ..models import PoojaStore
from ..serializers import PoojaStoreSerializer1,InactivePoojaStoreSerializer

class PoojaStoreView(viewsets.ModelViewSet):
    queryset = PoojaStore.objects.all()
    serializer_class = PoojaStoreSerializer
    # permission_classes = [] 

    def list(self, request):
        filter_kwargs = {}

        # Collect query params into filter kwargs
        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        # Always ensure status='ACTIVE'
        filter_kwargs['status'] = 'ACTIVE'

        try:
            queryset = PoojaStore.objects.filter(**filter_kwargs)

            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            serialized_data = PoojaStoreSerializer(queryset, many=True)
            return Response(serialized_data.data)

        except PoojaStore.DoesNotExist:
            return Response({
                'message': 'Objects not found',
                'status': 404
            })

    def create(self, request, *args, **kwargs):
        try:
            # Extract image_location from request data
            image_locations = request.data.get('image_location', [])

            # If image_location is not a list, convert it to a list
            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            # Temporarily set image_location to "null" for serializer
            request.data['image_location'] = "null"

            # Serialize data and save
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_locations = []  # To store valid saved locations

            # Check if image locations exist and are not null
            if image_locations and "null" not in image_locations:
                entity_type = "pooja_store"

                # Process each image location
                for image_location in image_locations:
                    if image_location and image_location != "null":
                        saved_location = save_image_to_azure(
                            image_location,
                            serializer.instance._id,
                            serializer.instance.name,
                            entity_type
                        )
                        if saved_location:
                            saved_locations.append(saved_location)  # Add to list

            # If there are saved locations, update the instance's image_location field
            if saved_locations:
                serializer.instance.image_location = saved_locations  # Save as a list
                serializer.instance.save()

            created_at = timezone.now()
            user_id = request.user.id if request.user.is_authenticated else "Anonymous"

            # Send email to EMAIL_HOST_USER (you can modify this part as needed)
            send_mail(
                'New pooja store Added',
                f'User ID: {user_id}\n'
                f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Tourism Place ID: {serializer.instance._id}\n'
                f'Tourism Place Name: {serializer.instance.name}',
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
            instance = PoojaStore.objects.get(_id=pk, status='ACTIVE')
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except PoojaStore.DoesNotExist:
            return Response({
                "message": " pooja store not found",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)


    def update(self, request, pk=None, *args, **kwargs):
        try:
            instance = PoojaStore.objects.get(_id=pk, status='ACTIVE')

            # Get image_location from request
            image_locations = request.data.get('image_location', [])

            # Ensure list
            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            # Temporarily set image_location to null for serializer validation
            request.data['image_location'] = "null"

            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=True  # Allows PATCH-style update
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_locations = []

            # Upload new images if provided
            if image_locations and "null" not in image_locations:
                entity_type = "pooja_store"

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

            # If new images uploaded → replace old ones
            if saved_locations:
                serializer.instance.image_location = saved_locations
                serializer.instance.save()

            updated_at = timezone.now()
            user_id = request.user.id if request.user.is_authenticated else "Anonymous"

            # Email notification
            send_mail(
                'Pooja Store Updated',
                f'User ID: {user_id}\n'
                f'Updated Time: {updated_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Pooja Store ID: {serializer.instance._id}\n'
                f'Pooja Store Name: {serializer.instance.name}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return Response({
                "message": "success",
                "result": serializer.data
            }, status=status.HTTP_200_OK)

        except PoojaStore.DoesNotExist:
            return Response({
                "message": "Pooja store not found",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












class GetPoojaStoresByLocation(APIView):

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
            PoojaStore.objects
            .filter(combined_query, status='ACTIVE')
            .select_related(
                'village_id',
                'village_id__block',
                'village_id__block__district',
                'village_id__block__district__state',
                'village_id__block__district__state__country',
            )
        )

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query)
            )

        if not queryset.exists():
            queryset = PoojaStore.objects.filter(
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

        pooja_stores = self.get_queryset_filter(input_value, search_query)

        return Response({
            "pooja_stores": PoojaStoreSerializer1(pooja_stores, many=True).data
        })











class InactivePoojaStoreAPIView(APIView):
    """
    API to get only INACTIVE Pooja Stores
    """

    def get(self, request):
        filter_kwargs = {}
        search_query = request.query_params.get('search', None)

        # Dynamic filtering (except search)
        for key, value in request.query_params.items():
            if key != 'search':
                filter_kwargs[key] = value

        # Filter only INACTIVE records
        queryset = PoojaStore.objects.filter(
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

        serializer = InactivePoojaStoreSerializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "inactive_pooja_stores": serializer.data
        }, status=status.HTTP_200_OK)














class GetInactivePoojaStoresByLocation(APIView):

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
            PoojaStore.objects
            .filter(combined_query, status='INACTIVE')
            .select_related(
                'village_id',
                'village_id__block',
                'village_id__block__district',
                'village_id__block__district__state',
                'village_id__block__district__state__country',
            )
        )

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query)
            )

        if not queryset.exists():
            queryset = PoojaStore.objects.filter(
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

        pooja_stores = self.get_queryset_filter(input_value, search_query)

        return Response({
            "pooja_stores": InactivePoojaStoreSerializer(pooja_stores, many=True).data
        })




