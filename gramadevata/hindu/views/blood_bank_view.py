from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from ..models import BloodBank
from ..serializers import BloodBankSerializer
from ..utils import save_image_to_azure  
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from django.db.models import Q
from rest_framework import status
from ..serializers import BloodBankInactiveSerializer


from ..serializers import BloodBankSerializer1
class BloodBankView(viewsets.ModelViewSet):
    queryset = BloodBank.objects.all()
    serializer_class = BloodBankSerializer
    # permission_classes = []  
    def list(self, request):
        filter_kwargs = {}

        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        filter_kwargs['status'] = 'ACTIVE'

        try:
            queryset = BloodBank.objects.filter(**filter_kwargs)

            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            serialized_data = BloodBankSerializer(queryset, many=True)
            return Response(serialized_data.data)
 
        except BloodBank.DoesNotExist:
            return Response({
                'message': 'Objects not found',
                'status': 404
            })

    def create(self, request, *args, **kwargs):
        try:
            image_locations = request.data.get('image_location', [])
            license_copies = request.data.get('license_copy', [])

            if not isinstance(image_locations, list):
                image_locations = [image_locations]
            if not isinstance(license_copies, list):
                license_copies = [license_copies]

            request.data['image_location'] = "null"
            request.data['license_copy'] = "null"

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_image_locations = []
            saved_license_copies = []
            entity_type = "bloodbank"

            for image_location in image_locations:
                if image_location and image_location != "null":
                    saved = save_image_to_azure(
                        image_location,
                        serializer.instance._id,
                        serializer.instance.name,
                        entity_type
                    )
                    if saved:
                        saved_image_locations.append(saved)

            for license_copy in license_copies:
                if license_copy and license_copy != "null":
                    saved = save_image_to_azure(
                        license_copy,
                        serializer.instance._id,
                        serializer.instance.name + "_license",
                        entity_type
                    )
                    if saved:
                        saved_license_copies.append(saved)

            if saved_image_locations:
                serializer.instance.image_location = saved_image_locations
            if saved_license_copies:
                serializer.instance.license_copy = saved_license_copies

            serializer.instance.save()

            created_at = timezone.now()
            user_id = request.user.id if request.user.is_authenticated else "Anonymous"

            send_mail(
                'New Blood Bank Added',
                f'User ID: {user_id}\n'
                f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'BloodBank ID: {serializer.instance._id}\n'
                f'BloodBank Name: {serializer.instance.name}',
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
            instance = BloodBank.objects.get(_id=pk, status='ACTIVE')
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BloodBank.DoesNotExist:
            return Response({
                "message": "BloodBank not found",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)


    def update(self, request, pk=None, *args, **kwargs):
        try:
            instance = BloodBank.objects.get(_id=pk, status='ACTIVE')

            image_locations = request.data.get('image_location', [])
            license_copies = request.data.get('license_copy', [])

            if not isinstance(image_locations, list):
                image_locations = [image_locations]
            if not isinstance(license_copies, list):
                license_copies = [license_copies]

            # Temporarily set to null for serializer validation
            request.data['image_location'] = instance.image_location or "null"
            request.data['license_copy'] = instance.license_copy or "null"

            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=True   # supports PATCH also
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_image_locations = instance.image_location or []
            saved_license_copies = instance.license_copy or []
            entity_type = "bloodbank"

            # Save new images
            for image_location in image_locations:
                if image_location and image_location != "null":
                    saved = save_image_to_azure(
                        image_location,
                        instance._id,
                        instance.name,
                        entity_type
                    )
                    if saved:
                        saved_image_locations.append(saved)

            # Save new license copies
            for license_copy in license_copies:
                if license_copy and license_copy != "null":
                    saved = save_image_to_azure(
                        license_copy,
                        instance._id,
                        instance.name + "_license",
                        entity_type
                    )
                    if saved:
                        saved_license_copies.append(saved)

            if saved_image_locations:
                instance.image_location = saved_image_locations
            if saved_license_copies:
                instance.license_copy = saved_license_copies

            instance.save()

            return Response({
                "message": "BloodBank updated successfully",
                "result": serializer.data
            }, status=status.HTTP_200_OK)

        except BloodBank.DoesNotExist:
            return Response({
                "message": "BloodBank not found",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










class GetBloodBanksByLocation(APIView):

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
            BloodBank.objects
            .filter(combined_query, status='ACTIVE')
            .select_related(
                'village_id',
                'village_id__block',
                'village_id__block__district',
                'village_id__block__district__state',
                'village_id__block__district__state__country',
            )
        )

        # 🔍 Search by blood bank name / address / blood group
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(blood_group__icontains=search_query)
            )

        # 🔁 Fallback: direct village id
        if not queryset.exists():
            queryset = BloodBank.objects.filter(
                village_id=input_value,
                status='ACTIVE'
            )
            if search_query:
                queryset = queryset.filter(
                    Q(name__icontains=search_query) |
                    Q(address__icontains=search_query) |
                    Q(blood_group__icontains=search_query)
                )

        return queryset

    def get(self, request):
        input_value = request.query_params.get('input_value')
        if not input_value:
            raise ValidationError("input_value is required")

        search_query = request.query_params.get('search', '').strip()

        blood_banks = self.get_queryset_filter(input_value, search_query)

        return Response({
            "blood_banks": BloodBankSerializer1(blood_banks, many=True).data
        })










class InactiveBloodBankAPIView(APIView):
    """API to get only INACTIVE Blood Bank records"""

    def get(self, request):
        filter_kwargs = {}
        search_query = request.query_params.get('search', None)

        # Dynamic filters except search
        for key, value in request.query_params.items():
            if key != 'search':
                filter_kwargs[key] = value

        # Filter only INACTIVE blood banks
        queryset = BloodBank.objects.filter(
            status='INACTIVE',
            **filter_kwargs
        )

        # Search by name and address
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

        serializer = BloodBankInactiveSerializer(queryset, many=True)

        return Response({
            'count': queryset.count(),
            'blood_banks': serializer.data
        }, status=status.HTTP_200_OK)











class GetInactiveBloodBanksByLocation(APIView):

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
            BloodBank.objects
            .filter(combined_query, status='INACTIVE')
            .select_related(
                'village_id',
                'village_id__block',
                'village_id__block__district',
                'village_id__block__district__state',
                'village_id__block__district__state__country',
            )
        )

        # 🔍 Search by blood bank name / address / blood group
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(blood_group__icontains=search_query)
            )

        # 🔁 Fallback: direct village id
        if not queryset.exists():
            queryset = BloodBank.objects.filter(
                village_id=input_value,
                status='ACTIVE'
            )
            if search_query:
                queryset = queryset.filter(
                    Q(name__icontains=search_query) |
                    Q(address__icontains=search_query) |
                    Q(blood_group__icontains=search_query)
                )

        return queryset

    def get(self, request):
        input_value = request.query_params.get('input_value')
        if not input_value:
            raise ValidationError("input_value is required")

        search_query = request.query_params.get('search', '').strip()

        blood_banks = self.get_queryset_filter(input_value, search_query)

        return Response({
            "blood_banks": BloodBankInactiveSerializer(blood_banks, many=True).data
        })


