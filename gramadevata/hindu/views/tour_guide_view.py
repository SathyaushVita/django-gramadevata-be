# from rest_framework import viewsets
# from ..models import TourGuide
# from ..serializers import TourGuideSerializer
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from rest_framework import viewsets, status
# from rest_framework.response import Response

# class TourGuideViewSet(viewsets.ModelViewSet):
#     queryset = TourGuide.objects.all()
#     serializer_class = TourGuideSerializer

#     def list(self, request):
#             filter_kwargs = {}

#             # Apply query parameter filters (e.g., ?location=xyz)
#             for key, value in request.query_params.items():
#                 filter_kwargs[key] = value

#             # Always filter by ACTIVE status
#             filter_kwargs['status'] = 'ACTIVE'

#             queryset = TourGuide.objects.filter(**filter_kwargs)

#             if not queryset.exists():
#                 return Response({
#                     'message': 'Data not found',
#                     'status': 404
#                 })

#             serializer = self.get_serializer(queryset, many=True)
#             return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         try:
#             instance = TourGuide.objects.get(_id=pk, status='ACTIVE')
#             serializer = self.get_serializer(instance)
#             return Response(serializer.data)
#         except TourGuide.DoesNotExist:
#             return Response({
#                 'message': 'Tour Guide not found',
#                 'status': 404
#             }, status=status.HTTP_404_NOT_FOUND)
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from ..models import TourGuide
from ..serializers import TourGuideSerializer1,InactiveTourGuideSerializer
from datetime import datetime
from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models import TourGuide
from ..serializers import TourGuideSerializer
from ..utils import save_image_to_azure
import uuid
class TourGuideViewSet(viewsets.ModelViewSet):
    queryset = TourGuide.objects.all()
    serializer_class = TourGuideSerializer
    # permission_classes = [IsAuthenticated]  # optional
    # ---------- LIST ----------
    def list(self, request):
        filter_kwargs = {**request.query_params}
        filter_kwargs['status'] = 'ACTIVE'
        queryset = TourGuide.objects.filter(**filter_kwargs)
        if not queryset.exists():
            return Response({'message': 'Data not found', 'status': 404})
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    # ---------- CREATE ----------
    def create(self, request, *args, **kwargs):
        try:
            image_locations = request.data.get('image_location', [])
            if not isinstance(image_locations, list):
                image_locations = [image_locations]
            # Temporarily remove image_location from serializer
            request.data.pop('image_location', None)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            saved_locations = []
            entity_type = "tour_guide"
            for image in image_locations:
                if image and image != "null":
                    # Use mobile or tourguide ID as filename prefix
                    prefix = instance.user_id.username if instance.user_id else str(instance._id)
                    saved_location = save_image_to_azure(
                        image,
                        instance._id,        # folder
                        f"{prefix}_{uuid.uuid4().hex[:8]}",  # filename
                        entity_type
                    )
                    if saved_location:
                        saved_locations.append(saved_location)
            if saved_locations:
                instance.image_location = saved_locations
                instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # ---------- RETRIEVE ----------
    def retrieve(self, request, pk=None):
        try:
            instance = TourGuide.objects.get(_id=pk, status='ACTIVE')
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except TourGuide.DoesNotExist:
            return Response({
                "message": "Tour Guide not found",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)













@method_decorator(cache_page(60 * 5), name='get')  # 5 minutes cache
class TourGuidesByLocation(APIView):

    def get_queryset(self, input_value, search_query=None):

        filters = Q(status='ACTIVE')

        # Location filter (optimized)
        location_filter = (
            Q(village_id=input_value) |
            Q(village_id__block_id=input_value) |
            Q(village_id__block__district_id=input_value) |
            Q(village_id__block__district__state_id=input_value) |
            Q(village_id__block__district__state__country_id=input_value)
        )
        filters &= location_filter

        # Search filter
        if search_query:
            filters &= (
                Q(user_id__username__icontains=search_query) |
                Q(language__icontains=search_query) |
                Q(tourist_spot_covered__icontains=search_query) |
                Q(mobile__icontains=search_query)
            )

        return TourGuide.objects.filter(filters).select_related(
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

        tour_guides = self.get_queryset(input_value, search_query)

        return Response({
            "tour_guides": TourGuideSerializer1(tour_guides, many=True).data
        })






class InactiveTourGuideAPIView(APIView):
    """
    API to get only INACTIVE TourGuides
    """

    def get(self, request):
        filter_kwargs = {}
        search_query = request.query_params.get('search', None)

        # Dynamic filtering (except search)
        for key, value in request.query_params.items():
            if key != 'search':
                filter_kwargs[key] = value

        # Filter only INACTIVE tour guides
        queryset = TourGuide.objects.filter(
            status='INACTIVE',
            **filter_kwargs
        )

        # Search by user name or village name
        if search_query:
            queryset = queryset.filter(
                Q(user_id__full_name__icontains=search_query) |
                Q(village_id__name__icontains=search_query)
            )

        queryset = queryset.order_by('-created_at')

        if not queryset.exists():
            return Response(
                {"message": "Data not found", "status": 404},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = InactiveTourGuideSerializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "inactive_tour_guides": serializer.data
        }, status=status.HTTP_200_OK)
