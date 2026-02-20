

from datetime import datetime
from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models import TourOperator
from ..serializers import TourOperatorSerializer
from ..utils import save_image_to_azure
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from ..models import TourOperator
from ..serializers import TourOperatorSerializer1,TourOperatorInactiveSerializer

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

class TourOperatorViewSet(viewsets.ModelViewSet):
    queryset = TourOperator.objects.all()
    serializer_class = TourOperatorSerializer


    # ---------- LIST ----------
    def list(self, request):
        filter_kwargs = {**request.query_params}
        filter_kwargs['status'] = 'ACTIVE'

        queryset = TourOperator.objects.filter(**filter_kwargs)

        if not queryset.exists():
            return Response(
                {'message': 'No Tour Operators found', 'status': 404},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    # ---------- CREATE ----------
    def create(self, request, *args, **kwargs):
        try:
            image_locations = request.data.get('image_location', [])

            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            # Temporarily set null for serializer
            request.data['image_location'] = "null"

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_locations = []

            if image_locations and "null" not in image_locations:
                entity_type = "tour_operator"

                for image_location in image_locations:
                    if image_location and image_location != "null":
                        saved_location = save_image_to_azure(
                            image_location,
                            serializer.instance._id,
                            serializer.instance.tour_operator_name,
                            entity_type
                        )
                        if saved_location:
                            saved_locations.append(saved_location)

            if saved_locations:
                serializer.instance.image_location = saved_locations
                serializer.instance.save()

            # ✅ OLD RESPONSE FORMAT
            return Response(
                self.get_serializer(serializer.instance).data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    # ---------- RETRIEVE ----------
    def retrieve(self, request, pk=None):
        try:
            instance = TourOperator.objects.get(_id=pk, status='ACTIVE')
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        except TourOperator.DoesNotExist:
            return Response(
                {"message": "Tour Operator not found", "status": 404},
                status=status.HTTP_404_NOT_FOUND
            )


    # ---------- UPDATE ----------
    def update(self, request, pk=None, *args, **kwargs):
        try:
            instance = TourOperator.objects.get(_id=pk, status='ACTIVE')

            image_locations = request.data.get('image_location', [])

            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            # Keep existing images temporarily
            request.data['image_location'] = instance.image_location

            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

            saved_locations = instance.image_location or []

            if image_locations and "null" not in image_locations:
                entity_type = "tour_operator"

                for image_location in image_locations:
                    if image_location and image_location != "null":
                        saved_location = save_image_to_azure(
                            image_location,
                            instance._id,
                            instance.tour_operator_name,
                            entity_type
                        )
                        if saved_location:
                            saved_locations.append(saved_location)

            if saved_locations:
                instance.image_location = saved_locations
                instance.save()

            # ✅ OLD RESPONSE FORMAT
            return Response(
                self.get_serializer(instance).data,
                status=status.HTTP_200_OK
            )

        except TourOperator.DoesNotExist:
            return Response(
                {"message": "Tour Operator not found", "status": 404},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )






@method_decorator(cache_page(60 * 5), name='get')  
class TourOperatorsByLocation(APIView):

    def get_queryset(self, input_value, search_query=None):

        filters = Q(status='ACTIVE')

        location_filter = (
            Q(village_id=input_value) |
            Q(village_id__block_id=input_value) |
            Q(village_id__block__district_id=input_value) |
            Q(village_id__block__district__state_id=input_value) |
            Q(village_id__block__district__state__country_id=input_value)
        )

        filters &= location_filter

        if search_query:
            filters &= (
                Q(tour_operator_name__icontains=search_query) |
                Q(contact_address__icontains=search_query) |
                Q(mobile_number__icontains=search_query)
            )

        return TourOperator.objects.filter(filters).select_related(
            'village_id',
            'village_id__block',
            'village_id__block__district',
            'village_id__block__district__state',
            'village_id__block__district__state__country',
            'temple_id',
            'event_id',
            'user_id'
        )

    def get(self, request):
        input_value = request.query_params.get('input_value')
        if not input_value:
            raise ValidationError("input_value is required")

        search_query = request.query_params.get('search', '').strip()

        tour_operators = self.get_queryset(input_value, search_query)

        return Response({
            "tour_operators": TourOperatorSerializer1(tour_operators, many=True).data
        })














class InactiveTourOperatorAPIView(APIView):
    """API to get only INACTIVE Tour Operator records"""

    def get(self, request):
        filter_kwargs = {}
        search_query = request.query_params.get('search', None)

        # Dynamic filtering (except search)
        for key, value in request.query_params.items():
            if key != 'search':
                filter_kwargs[key] = value

        # Filter only INACTIVE
        queryset = TourOperator.objects.filter(
            status='INACTIVE',
            **filter_kwargs
        )

        # Search functionality
        if search_query:
            queryset = queryset.filter(
                Q(tour_operator_name__icontains=search_query) |
                Q(contact_address__icontains=search_query) 
            )

        queryset = queryset.order_by('-created_at')

        if not queryset.exists():
            return Response(
                {'message': 'Data not found', 'status': 404},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TourOperatorInactiveSerializer(queryset, many=True)

        return Response({
            'count': queryset.count(),
            'tour_operators': serializer.data
        }, status=status.HTTP_200_OK)









@method_decorator(cache_page(60 * 5), name='get')  # 5 minutes cache
class InactiveTourOperatorsByLocation(APIView):

    def get_queryset(self, input_value, search_query=None):

        filters = Q(status='INACTIVE')

        location_filter = (
            Q(village_id=input_value) |
            Q(village_id__block_id=input_value) |
            Q(village_id__block__district_id=input_value) |
            Q(village_id__block__district__state_id=input_value) |
            Q(village_id__block__district__state__country_id=input_value)
        )

        filters &= location_filter

        if search_query:
            filters &= (
                Q(tour_operator_name__icontains=search_query) |
                Q(contact_address__icontains=search_query) |
                Q(mobile_number__icontains=search_query)
            )

        return TourOperator.objects.filter(filters).select_related(
            'village_id',
            'village_id__block',
            'village_id__block__district',
            'village_id__block__district__state',
            'village_id__block__district__state__country',
            'temple_id',
            'event_id',
            'user_id'
        )

    def get(self, request):
        input_value = request.query_params.get('input_value')
        if not input_value:
            raise ValidationError("input_value is required")

        search_query = request.query_params.get('search', '').strip()

        tour_operators = self.get_queryset(input_value, search_query)

        return Response({
            "tour_operators": TourOperatorInactiveSerializer(tour_operators, many=True).data
        })


