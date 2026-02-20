from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

from ..models import NearbyHospital
from ..serializers import NearbyHospitalSerializer,InactiveHospitalSerializer
from ..utils import save_image_to_azure  
class NearbyHospitalViewSet(viewsets.ModelViewSet):
    queryset = NearbyHospital.objects.all()
    serializer_class = NearbyHospitalSerializer

    def get_queryset(self):
        filter_kwargs = {'status': 'ACTIVE'}
        for key, value in self.request.query_params.items():
            filter_kwargs[key] = value
        return NearbyHospital.objects.filter(**filter_kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'ACTIVE':
            return Response({'message': 'Data not found', 'status': 404})
        return super().retrieve(request, *args, **kwargs)

 



    def create(self, request, *args, **kwargs):
        try:
            image_locations = request.data.get('image_location', [])
            license_copies = request.data.get('license_copy', [])

            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            if not isinstance(license_copies, list):
                license_copies = [license_copies]

            # Temporarily set to null for initial save
            request.data['image_location'] = "null"
            request.data['license_copy'] = "null"

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_image_locations = []
            saved_license_copies = []

            if image_locations and "null" not in image_locations:
                entity_type = "nearby_hospital"
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

            if license_copies and "null" not in license_copies:
                entity_type = "license_copy"
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

            # Save final image and license paths
            if saved_image_locations:
                serializer.instance.image_location = saved_image_locations

            if saved_license_copies:
                serializer.instance.license_copy = saved_license_copies

            serializer.instance.save()

            # Optional: email notification
            created_at = timezone.now()
            if request.user and request.user.is_authenticated:
                send_mail(
                    'New Nearby Hospital Added',
                    f'User ID: {request.user.id}\n'
                    f'Full Name: {request.user.get_full_name()}\n'
                    f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                    f'Hospital ID: {serializer.instance._id}\n'
                    f'Hospital Name: {serializer.instance.name}',
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




    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            if instance.status != 'ACTIVE':
                return Response({'message': 'Data not found', 'status': 404})

            image_locations = request.data.get('image_location', [])
            license_copies = request.data.get('license_copy', [])

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

            # Save new hospital images
            if image_locations and "null" not in image_locations:
                entity_type = "nearby_hospital"
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

            # Save new license copies
            if license_copies and "null" not in license_copies:
                entity_type = "license_copy"
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

            # Update final values
            if saved_image_locations:
                instance.image_location = saved_image_locations

            if saved_license_copies:
                instance.license_copy = saved_license_copies

            instance.save()

            return Response({
                "message": "Nearby Hospital updated successfully",
                "result": serializer.data
            }, status=status.HTTP_200_OK)

        except NearbyHospital.DoesNotExist:
            return Response({
                "message": "Nearby Hospital not found",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.db.models import Q

from ..serializers import NearbyHospitalSerializer1


class GetHospitalsByLocation(APIView):

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
            NearbyHospital.objects
            .filter(combined_query, status='ACTIVE')
            .select_related(
                'village_id',
                'village_id__block',
                'village_id__block__district',
                'village_id__block__district__state',
                'village_id__block__district__state__country',
            )
        )

        # 🔍 Search by hospital name / address
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query)
            )

        # 🔁 Fallback: direct village
        if not queryset.exists():
            queryset = NearbyHospital.objects.filter(
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

        hospitals = self.get_queryset_filter(input_value, search_query)

        return Response({
            "nearby_hospitals": NearbyHospitalSerializer1(hospitals, many=True).data
        })













class InactiveNearbyHospitalAPIView(APIView):
    """
    API to get only INACTIVE Nearby Hospital records
    """

    def get(self, request):
        filter_kwargs = {}
        search_query = request.query_params.get('search', None)

        # Dynamic filtering (except search)
        for key, value in request.query_params.items():
            if key != 'search':
                filter_kwargs[key] = value

        # Filter only INACTIVE hospitals
        queryset = NearbyHospital.objects.filter(
            status='INACTIVE',
            **filter_kwargs
        )

        # Search functionality (name & address)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query)
            )

        queryset = queryset.order_by('-created_at')

        if not queryset.exists():
            return Response(
                {'message': 'Data not found', 'status': 404},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = InactiveHospitalSerializer(queryset, many=True)

        return Response({
            'count': queryset.count(),
            'nearby_hospitals': serializer.data
        }, status=status.HTTP_200_OK)









class GetInactiveHospitalsByLocation(APIView):

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
            NearbyHospital.objects
            .filter(combined_query, status='INACTIVE')
            .select_related(
                'village_id',
                'village_id__block',
                'village_id__block__district',
                'village_id__block__district__state',
                'village_id__block__district__state__country',
            )
        )

        # 🔍 Search by hospital name / address
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query)
            )

        # 🔁 Fallback: direct village
        if not queryset.exists():
            queryset = NearbyHospital.objects.filter(
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

        hospitals = self.get_queryset_filter(input_value, search_query)

        return Response({
            "nearby_hospitals": InactiveHospitalSerializer(hospitals, many=True).data
        })


