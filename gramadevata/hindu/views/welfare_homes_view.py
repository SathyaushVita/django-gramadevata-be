from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from ..models import WelfareHomes
from..serializers import WelfareHomesSerializer,WelfareHomesSerializer1,WelfareHomesSerializer2
from rest_framework.pagination import PageNumberPagination
from ..utils import CustomPagination
from ..utils import save_image_to_azure



class WelfareHomesViews(viewsets.ModelViewSet):
    queryset = WelfareHomes.objects.filter(status='ACTIVE').order_by('-created_at')
    serializer_class = WelfareHomesSerializer2
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'address']

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = WelfareHomesSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = WelfareHomesSerializer(queryset, many=True)
        return Response(serializer.data)



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
            entity_type = "welfare_homes"

            saved_images = []

            for image in image_locations:
                if image and image != "null":
                    saved_location = save_image_to_azure(
                        image,
                        instance._id,
                        instance.name,
                        entity_type
                    )
                    if saved_location:
                        saved_images.append(saved_location)

            if saved_images:
                instance.image_location = saved_images
                instance.save()

            created_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

            # ==================================
            # ✅ Email to Admin
            # ==================================
            send_mail(
                'New Welfare Home Added',
                f'User ID: {request.user.id}\n'
                f'Created Time: {created_time}\n'
                f'Welfare Home ID: {instance._id}\n'
                f'Welfare Home Name: {instance.name}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            # ==================================
            # ✅ Email to Same User
            # ==================================
            user_email = getattr(request.user, 'email', None)
            user_name = getattr(request.user, 'full_name', 'User')

            if user_email:
                send_mail(
                    'Welfare Home Submission Successful',
                    f'Dear {user_name},\n\n'
                    f'Your welfare home "{instance.name}" has been successfully submitted.\n\n'
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
            return Response(
                {"message": "An error occurred.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )







    # def create(self, request, *args, **kwargs):
    #     try:
    #         image_locations = request.data.get('image_location', [])
    #         if not isinstance(image_locations, list):
    #             image_locations = [image_locations]
    #         request.data['image_location'] = "null"



    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()

    #         saved_images = []
    #         saved_videos = []
    #         entity_type = "welfare_homes"

    #         for image in image_locations:
    #             if image and image != "null":
    #                 saved_location = save_image_to_azure(image, serializer.instance._id, serializer.instance.name, entity_type)
    #                 if saved_location:
    #                     saved_images.append(saved_location)



    #         if saved_images:
    #             serializer.instance.image_location = saved_images
 
    #             serializer.instance.save()

    #         send_mail(
    #             'Welfare Home Updated',
    #             f'User ID: {request.user.id}\n'
    #             # f'Full Name: {request.user.get_full_name()}\n'
    #             f'Created Time: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
    #             f'Welfare Home ID: {serializer.instance._id}\n'
    #             f'Welfare Home Name: {serializer.instance.name}',
    #             settings.EMAIL_HOST_USER,
    #             [settings.EMAIL_HOST_USER],
    #             fail_silently=False,
    #         )

    #         return Response({
    #             "message": "success",
    #             "result": serializer.data
    #         }, status=status.HTTP_201_CREATED)

    #     except Exception as e:
    #         return Response({"message": "An error occurred.", "error": str(e)},
    #                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = WelfareHomesSerializer(instance)
            return Response(serializer.data)
        except WelfareHomes.DoesNotExist:
            return Response({'message': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            instance = self.get_object()
            image_locations = request.data.get('image_location', [])
            if not isinstance(image_locations, list):
                image_locations = [image_locations]
            request.data['image_location'] = "null"

            serializer = WelfareHomesSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()

            saved_locations = []
            entity_type = "welfare_homes"
            for image in image_locations:
                if image and image != "null":
                    saved_location = save_image_to_azure(image, updated_instance._id, updated_instance.name, entity_type)
                    if saved_location:
                        saved_locations.append(saved_location)

            if saved_locations:
                updated_instance.image_location = saved_locations
                updated_instance.save()

            send_mail(
                'Welfare Home Updated',
                f'User ID: {request.user.id}\n'
                # f'Full Name: {request.user.get_full_name()}\n'
                f'Updated Time: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Welfare Home ID: {updated_instance._id}\n'
                f'Welfare Home Name: {updated_instance.name}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return Response({
                "message": "updated successfully",
                "data": WelfareHomesSerializer(updated_instance).data
            })

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from ..models import WelfareHomes
from ..serializers import WelfareHomesSerializer
from ..utils import CustomPagination






@method_decorator(cache_page(300), name='list')  
class GetWelfareHomesByLocation(generics.ListAPIView):
    serializer_class = WelfareHomesSerializer1
    pagination_class = CustomPagination

    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search', '').strip()

        if not input_value and not category and not search:
            raise ValidationError("Input value, category, or search is required")

        # Location level filtering
        country_query = Q(village_id__block__district__state__country__pk=input_value)
        state_query = Q(village_id__block__district__state__pk=input_value)
        district_query = Q(village_id__block__district__pk=input_value)
        block_query = Q(village_id__block__pk=input_value)
        village_query = Q(village_id__pk=input_value)

        combined_query = Q()
        if input_value:
            combined_query |= country_query | state_query | district_query | block_query | village_query

        if category:
            combined_query &= Q(category=category)

        queryset = WelfareHomes.objects.filter(combined_query).select_related(
            'village_id__block__district__state__country',
            'village_id__block__district__state',
            'village_id__block__district',
            'village_id__block',
            'village_id',
        )

        # Fallback to direct village ID match
        if not queryset.exists() and input_value:
            queryset = WelfareHomes.objects.filter(village_id=input_value)
            if category:
                queryset = queryset.filter(category=category)

        # Apply search filter for name and address
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(address__icontains=search)
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(status='ACTIVE')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from ..models import WelfareHomes
from ..serializers import WelfareHomesInactiveSerializer
from ..enums import EntityStatus




class InactiveWelfareHomesAPIView(APIView):
    """
    API to get INACTIVE Welfare Homes
    - search by name, address
    - recent first
    - count included
    """

    def get(self, request):
        queryset = WelfareHomes.objects.filter(
            status=EntityStatus.INACTIVE.value
        ).select_related('user', 'village_id', 'country', 'category')

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
                {
                    "count": 0,
                    "results": [],
                    "message": "Data not found"
                },
                status=status.HTTP_200_OK
            )

        serializer = WelfareHomesInactiveSerializer(queryset, many=True)

        return Response(
            {
                "count": queryset.count(),
                "results": serializer.data
            },
            status=status.HTTP_200_OK
        )









@method_decorator(cache_page(300), name='list')  
class GetInactiveWelfareHomesByLocation(generics.ListAPIView):
    serializer_class = WelfareHomesSerializer1
    pagination_class = CustomPagination

    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search', '').strip()

        if not input_value and not category and not search:
            raise ValidationError("Input value, category, or search is required")

        # Location level filtering
        country_query = Q(village_id__block__district__state__country__pk=input_value)
        state_query = Q(village_id__block__district__state__pk=input_value)
        district_query = Q(village_id__block__district__pk=input_value)
        block_query = Q(village_id__block__pk=input_value)
        village_query = Q(village_id__pk=input_value)

        combined_query = Q()
        if input_value:
            combined_query |= country_query | state_query | district_query | block_query | village_query

        if category:
            combined_query &= Q(category=category)

        queryset = WelfareHomes.objects.filter(combined_query).select_related(
            'village_id__block__district__state__country',
            'village_id__block__district__state',
            'village_id__block__district',
            'village_id__block',
            'village_id',
        )

        # Fallback to direct village ID match
        if not queryset.exists() and input_value:
            queryset = WelfareHomes.objects.filter(village_id=input_value)
            if category:
                queryset = queryset.filter(category=category)

        # Apply search filter for name and address
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(address__icontains=search)
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(status='INACTIVE')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    